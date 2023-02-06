from simulation import Simulation
from world_generator import *
from evo_world import *
from evo_entity import *
from actions_sim import *
from utils import *

class EvoWorldSimulation(Simulation, SimActions):
    def __init__(self,
                episodes_number,
                steps_per_episode,
                world_generator: WorldGenerator,
                available_commands = None,
                actions_time: int = 10,
                visualization: bool = False,
                ):
        super().__init__(episodes_number, steps_per_episode)
        self.world_generator = world_generator
        self.actions_time = actions_time
        self.visualization = visualization
        # Here will be also the food generators
        self.species = {}
        self.object_types = {}
        #TODO: Change entities for objects
        self.entities = {}
        self.intelligent_entities = {}
        self.banished_entities = []
        self.day = 0
        default_commands = {"floor": self.floor,
                            "smell": self.smell,
                            "see": self.see,
                            "pick": self.pick,
                            "attack": self.attack,
                            "eat": self.eat,
                            "reproduce": self.reproduce,
                            "none": lambda x:None
                            }
        self.available_commands = default_commands if not available_commands else default_commands.update(
            available_commands)
    
    def reset(self):
        super().reset()
        self.world = self.world_generator.generate_world()

    def next_step(self, allow_next_episode: bool = False) -> bool:
        if self.actual_step >= self.steps_per_episode:
            if allow_next_episode and self.actual_episode < self.episodes_number:
                self.actual_episode += 1
                self.actual_step = 0
            else:
                return False
        self.actual_step += 1
        day = self.actual_step // self.actions_time
        episode = self.actual_episode

        for entity_id in self.entities:
            entity = self.entities[entity_id]
            entity.pass_time()

        for entity_id in list(self.intelligent_entities.keys()):
            entity = self.intelligent_entities[entity_id]
            perception_list = []
            if "floor" in self.available_commands:
                position, floor = self.available_commands["floor"](
                        entity_id)
            perception_list.append(
                        {"floor": floor, "position": position})
            for action in entity.get_perceptions():
                command = action["command"]
                parameters = action["parameters"]
                if command in self.available_commands:
                    new_information = self.available_commands[command](
                        entity_id, day, *parameters)
                    for info in new_information:
                        self.update_perception(info, perception_list)
            self.intelligent_entities[entity_id].update_knowledge(
                    perception_list)
            time_actions = entity.pass_time()
            if time_actions['dies']:
                self.banished_entities.append((
                    day,
                    episode,
                    self.intelligent_entities.pop(entity_id)
                ))
                position = self.world.get_entity_info(entity_id).position
                self.world.remove_entity(entity_id)
                if 'generates' in time_actions:
                    self.instantiate_entity(time_actions['generates'], position)
                # print : entity_id, "was banished"
                if self.visualization:
                    # self.visualization_fun(banished=entity_id)
                    pass
                continue
            # The entity executes its action based on its world perception,
            # which returns world and simulation actions to be executed
            actions = entity.decide_action()
            for action in actions:
                action["entity"] = entity_id
                self.execute_action(action)
                if self.visualization:
                    self.visualization_fn(action)

    def advance_to(self, episode, step):
        while self.actual_episode < episode or self.actual_step < step:
            self.next_step(allow_next_episode=True)

    # All the following functions are auxiliar

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

    def execute_action(self, action):
        if action["command"] in list(self.available_commands.keys()):
            if action['command'] == 'reproduce':
                # TODO: Fix These actions
                return
            self.available_commands[action["command"]](
                action["entity"], *action["parameters"])
        else:
            self.world.execute_action(action)

    def add_species(self, species):
        # self.entities_gen.append((species.name, species))
        self.species[species.id] = species

    def add_object_type(self, object_type):
        self.object_types[object_type.id] = object_type

    def instantiate_entity(self, entity_type, world_position, generator=None):
        if generator != None:
            entity = generator()
            self.intelligent_entities[entity.get_entity_id()] = entity
            self.world.place_entity(entity, world_position)
            return
        entity = None
        if entity_type in self.species:
            entity = self.species[entity_type].get_entity()
        elif entity_type in self.object_types:
            entity = self.object_types[entity_type].get_entity()
        else:
            raise Exception("Entity type not found")
            
        if entity.is_intelligent:
            self.intelligent_entities[entity.get_entity_id()] = entity
        else:
            self.entities[entity.get_entity_id()] = entity
        self.world.place_entity(entity, world_position)