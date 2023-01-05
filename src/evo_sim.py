from .evo_world import *
from .evo_entity import *
from .utils import *


class EvoSim:
    def __init__(self,
                 height,
                 width,
                 terrain_types,
                 terrain_dist,
                 finite=False,
                 episodes_total=10,
                 max_rounds_per_episode=1000,
                 stop_condition=None,
                 available_commands=None
                 ):
        self.init_world(height, width, terrain_types, terrain_dist, finite)
        self.entities_gen = []
        self.entities = {}
        self.intelligent_entities = {}
        self.dead_entities = {}
        self.episodes_total = episodes_total
        self.max_rounds = max_rounds_per_episode
        self.stop_condition = stop_condition
        # TODO: this should be imported
        default_commands = {"floor": self.floor,
                            "smell": self.smell, "see": self.see}
        self.available_commands = default_commands if not available_commands else available_commands

    def run(self, gen_world_pos):
        for episode in range(self.episodes_total):
            self.world = self.world_gen()
            for entity_gen_position, world_position in gen_world_pos:
                self.instantiate_entity(entity_gen_position, world_position)

            self.run_episode()
            self.entities = {}
            self.intelligent_entities = {}
            self.dead_entities = {}

    # TODO: Implement statistics
    def run_episode(self):
        for day in range(self.max_rounds):
            # Time comes for us all ...
            # TODO: pass time function tells if an entity is dead
            for entity_id in self.intelligent_entities:
                entity = self.intelligent_entities[entity_id]
                entity.pass_time()
            for entity_id in self.entities:
                entity = self.entities[entity_id]
                entity.pass_time()

            # Checking stop condition if defined
            if self.stop_condition is not None:
                if self.stop_condition(self):
                    return

            # Executing entities actions
            for entity_id in self.intelligent_entities:
                entity = self.intelligent_entities[entity_id]
                #TODO: perceptions should be before pass time in intelligent entities
                # Executing perception actions:
                perception_list = []
                for action in entity.get_perceptions():
                    command = action["command"]
                    parameters = action["parameters"]
                    if "floor" in self.available_commands:
                        position, floor = self.available_commands["floor"](
                            entity_id)
                        perception_list.append(
                            {"floor": floor, "position": position})
                    if command in self.available_commands:
                        new_information = self.available_commands[command](
                            entity_id, day, *parameters)
                        for info in new_information:
                            self.update_perception(info, perception_list)
                self.intelligent_entities[entity_id].update_knowledge(perception_list)

                # The entity executes its action based on its world perception,
                # which returns world and simulation actions to be executed
                actions = entity.decide_action(perception_list, day)
                for action in actions:
                    action["entity"] = entity_id
                    self.execute_action(action)
                    print(action["command"])
                    print("\n")
                    print(self.world)

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

    def floor(self, ent_id):
        position = self.world.entities[ent_id].position
        return (position, self.world.get_pos_terrain(position))


    def smell(self, ent_id, day, r):
        #FIXME: should not be only intelligent
        entities_list = [(self.intelligent_entities[other_id], pos)
                         for other_id, pos in self.world.see_r(ent_id, r)]
        perception_list = []
        for entity, pos in entities_list:
            if "smell" in entity.physical_properties:
                perception_list.append({
                    "entity": entity.get_entity_id(),
                    "smell": entity.physical_properties["smell"],
                    "position": pos,
                    "day": day
                })
        return perception_list

    def see(self, ent_id, day, r):
        entities_list = [(self.intelligent_entities[other_id], pos)
                         for other_id, pos in self.world.see_r(ent_id, r)]
        perception_list = []
        for entity, pos in entities_list:
            #TODO: add edible, color and shape
            entity_info = {"entity": entity.get_entity_id(), "day":day, "position": pos}
            if "legs" in entity.physical_properties:
                entity_info["legs"] = entity.physical_properties["legs"]
            if "arms" in entity.physical_properties:
                entity_info["arms"] = entity.physical_properties["arms"]
            if "horns" in entity.physical_properties:
                entity_info["horns"] = entity.physical_properties["horns"]
            if "fins" in entity.physical_properties:
                entity_info["fins"] = entity.physical_properties["fins"]
            perception_list.append(entity_info)   
        return perception_list

    def execute_action(self, action):
        #FIXME:
        self.world.execute_action(action)

    def init_world(self, height, width, terrain_types, terrain_dist, finite):
        self.world_gen = lambda: EvoWorld(
            height, width, terrain_types, terrain_dist, finite)

    def add_entity_gen(self, entity_instance_gen):
        self.entities_gen.append(entity_instance_gen)

    def instantiate_entity(self, entity_gen_position, world_position):
        entity = self.entities_gen[entity_gen_position]()
        if entity.is_intelligent:
            self.intelligent_entities[entity.get_entity_id()] = entity
        else:
            self.entities[entity.id] = entity
        self.world.place_entity(entity.get_entity_id(), world_position,
                                entity.rep, entity.coexistence)
