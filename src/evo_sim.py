from .evo_world import *
from .evo_entity import *
from .actions_sim import *
from .utils import *
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
import time


class EvoSim(SimActions):
    def __init__(self,
                 height,
                 width,
                 terrain_types,
                 terrain_dist,
                 finite=False,
                 episodes_total=1,
                 max_rounds_per_episode=10,
                 stop_condition=None,
                 available_commands={},
                 visualization=False,
                 actions_time=10
                 ):
        self.init_world(height, width, terrain_types, terrain_dist, finite)
        self.actions_time = actions_time
        self.visualization = visualization
        self.entities_gen = []
        self.entities = {}
        self.banished_entities = {}
        self.intelligent_entities = {}
        self.dead_entities = {}
        self.episodes_total = episodes_total
        self.max_rounds = max_rounds_per_episode
        self.stop_condition = stop_condition
        self.day = 0
        default_commands = {"floor": self.floor,
                            "smell": self.smell,
                            "see": self.see,
                            "pick": self.pick,
                            "attack": self.attack,
                            "eat": self.eat,
                            "reproduce": self.reproduce
                            }
        self.available_commands = default_commands if not available_commands else default_commands.update(
            available_commands)

    def run(self, gen_world_pos):
        for episode in range(self.episodes_total):
            self.world = self.world_gen()
            for entity_gen_position, world_position in gen_world_pos:
                self.instantiate_entity(entity_gen_position, world_position)

            self.run_episode()
            self.entities = {}
            self.intelligent_entities = {}
            self.dead_entities = {}

    def run_episode(self):
        for day in range(self.max_rounds):
            self.day = day
            # Checking stop condition if defined
            if self.stop_condition is not None:
                if self.stop_condition(self):
                    return

            # Time comes for us all ...
            for entity_id in self.entities:
                entity = self.entities[entity_id]
                entity.pass_time()

            # Executing entities actions
            for entity_id in list(self.intelligent_entities.keys()):
                entity = self.intelligent_entities[entity_id]
                # TODO: perceptions should be before pass time in intelligent entities
                # Executing perception actions:
                perception_list = []
                if "floor" in self.available_commands:
                    position, floor = self.available_commands["floor"](
                        entity_id)
                    perception_list.append(
                        {"floor": floor, "position": position})
                for action in entity.get_perceptions():
                    command = action["command"]
                    parameters = action["parameters"]
                    new_per = []
                    if command in self.available_commands:
                        new_information = self.available_commands[command](
                            entity_id, day, *parameters)
                        for info in new_information:
                            self.update_perception(info, perception_list)
                self.intelligent_entities[entity_id].update_knowledge(
                    perception_list)

                if not entity.pass_time():
                    self.banished_entities[entity_id] = self.intelligent_entities.pop(
                        entity_id)
                    self.world.remove_entity(entity_id)
                    # print : entity_id, "was banished"
                    if self.visualization:
                        self.visualization_fun(banished=entity_id)
                    continue
                # The entity executes its action based on its world perception,
                # which returns world and simulation actions to be executed
                actions = entity.decide_action(time=self.actions_time)
                for action in actions:
                    action["entity"] = entity_id
                    self.execute_action(action)
                    if self.visualization:
                        self.visualization_fun(action)

    def update_perception(self, new_info, current_info):
        if "entity" in list(new_info.keys()):
            entity_id = new_info["entity"]
            for old_info in current_info:
                if ("entity" in old_info) and entity_id == old_info["entity"]:
                    old_info.update(new_info)
                    return
            current_info.append(new_info)
        if "floor" in list(new_info.keys()):
            for old_info in current_info:
                if ("floor" in old_info):
                    old_info.update(new_info)
                    return
            current_info.append(new_info)
        if "surroundings" in list(new_info.keys()):
            for old_info in current_info:
                if ("surroundings" in old_info):
                    old_info.update(new_info)
                    return
            current_info.append(new_info)

    def entities_in_radius(self, ent_id, r):
        entities_id_list = [(other_id, pos, distance)
                            for other_id, pos, distance in self.world.see_r(ent_id, r)]
        entities = []
        for ent_id, pos, distance in entities_id_list:
            if ent_id in self.entities:
                entities.append((self.entities[ent_id], pos, distance))
            elif ent_id in self.intelligent_entities:
                entities.append(
                    (self.intelligent_entities[ent_id], pos, distance))
        return entities

    def entities_in_radius(self, ent_id, r):
        entities_id_list = [(other_id, pos, distance)
                            for other_id, pos, distance in self.world.see_r(ent_id, r)]
        entities = []
        for ent_id, pos, distance in entities_id_list:
            if ent_id in self.entities:
                entities.append((self.entities[ent_id], pos, distance))
            elif ent_id in self.intelligent_entities:
                entities.append(
                    (self.intelligent_entities[ent_id], pos, distance))
        return entities

    def entities_around_position(self, position):
        aux = len(self.world.get_entities_around_position(position))
        return aux

    def entities_in_position(self, position):
        aux = len(self.world.get_entities_in_position(position))
        return aux

    def create_in_position(self, position):
        self.instantiate_entity(0, (position[0], position[1]))

    def new_empty_pos(self, ent_id, other_id):
        # Generate the a new position adjacent to ent_id or other_id:
        pos = self.world.entities[ent_id].position
        other_pos = self.world.entities[ent_id].position
        posible_options = [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]),
                           (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]
        posible_options += [(other_pos[0] + 1, other_pos[1]), (other_pos[0] - 1, other_pos[1]),
                            (other_pos[0], other_pos[1] + 1), (other_pos[0], other_pos[1] - 1)]
        for option in posible_options:
            if self.world.valid_position(option) and len(self.world.get_entities_in_position(option)):
                return option
        return None

    def execute_action(self, action):
        if action["command"] in list(self.available_commands.keys()):
            self.available_commands[action["command"]](
                action["entity"], *action["parameters"])
        else:
            self.world.execute_action(action)

    def init_world(self, height, width, terrain_types, terrain_dist, finite):
        self.world_gen = lambda: EvoWorld(
            height, width, terrain_types, terrain_dist, finite)

    def add_entity_gen(self, entity_instance_gen):
        self.entities_gen.append(entity_instance_gen)

    def instantiate_entity(self, entity_gen_position, world_position, generator=None):
        if generator != None:
            entity = generator()
            self.intelligent_entities[entity.get_entity_id()] = entity
            self.world.place_entity(entity, world_position)
            return

        entity = self.entities_gen[entity_gen_position]()
        if entity.is_intelligent:
            self.intelligent_entities[entity.get_entity_id()] = entity
        else:
            self.entities[entity.get_entity_id()] = entity
        self.world.place_entity(entity, world_position)
