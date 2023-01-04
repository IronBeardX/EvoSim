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
                 stop_condition=None
                 ):
        self.init_world(height, width, terrain_types, terrain_dist, finite)
        self.entities_gen = []
        self.entities = {}
        self.intelligent_entities = {}
        self.episodes_total = episodes_total
        self.max_rounds = max_rounds_per_episode
        self.stop_condition = stop_condition

    def run(self, gen_world_pos):
        for episode in range(self.episodes_total):
            self.world = self.world_gen()
            for entity_gen_position, world_position in gen_world_pos:
                self.instantiate_entity(entity_gen_position, world_position)
            self.run_episode()
            self.entities = {}
            self.intelligent_entities = {}

    # Implement statistics
    def run_episode(self):
        for round in range(self.max_rounds):
            # Time comes for us all ...
            for entity_id in self.intelligent_entities:
                entity = self.intelligent_entities[entity_id]
                #FIXME: all entities change at the same time
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

                # Executing perception actions:
                perception_dict = {}
                for action in entity.perceptions:
                    perception_dict[action.id] = self.world.execute_action(
                        action)
                # The entity executes its action based on its world perception,
                # which returns world and simulation actions to be executed
                actions = entity.decide_action(perception_dict)
                for action in actions:
                    self.execute_action(action)

    def execute_action(self, action):
        pass

    def init_world(self, height, width, terrain_types, terrain_dist, finite):
        self.world_gen = lambda: EvoWorld(height, width, terrain_types, terrain_dist, finite)

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
