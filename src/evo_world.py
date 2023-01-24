from .actions_world import *
from typing import Callable
from curses.ascii import isdigit
import numpy as np
import random
from .evo_entity import Entity

class World():
    '''
    Basic class of the world, it contains information about the entities and the world map relevant to the positioning
    and movements of things
    '''

    def __init__(self, world_map, terrain_types, world_actions={}, finite=False, events=None):
        # The map of the world
        self.world_map = world_map
        # If the world is finite
        self.finite = finite
        # The types of terrain existing in the world, this should be a dictionary {<representation>: <name>}
        self.terrain_types = terrain_types
        # A dictionary containing events that can occur in the world
        self.events = {} if not events else events
        # A dictionary containing the entities in the world
        self.entities = {}
        # World actions
        self.world_actions = world_actions

    def execute_action(self, action):
        '''
        This method executes the given action in the world.
        '''
        command = action["command"]
        if command not in list(self.world_actions.keys()):
            raise Exception("Command not recognized")
        if "entity" in action:
            entity_id = action["entity"]
            if entity_id not in self.entities:
                raise Exception("Invalid entity")

        if "parameters" in action:
            parameters = action["parameters"]
            self.world_actions[command](entity_id)(*parameters)
        else:
            self.world_actions[command](entity_id)

    # TODO: From here there will be the declarations of methods that every world should implement
    def get_entity_info(self, entity_id):
        '''
        This method returns the information about the entity with the given id.
        '''
        return self.entities[entity_id]

    def valid_position(self, position):
        '''
        This method returns True if the given position is valid, False otherwise.
        '''
        raise NotImplementedError()

    def get_entities_in_position(self, position):
        '''
        This method returns the entities that occupies the given position.
        '''
        raise NotImplementedError()

    def get_terrain_type(self, position):
        '''
        This method returns the terrain type of the given position.
        '''
        raise NotImplementedError()

    def place_entity(self, entity, position):
        raise NotImplementedError()

    def remove_entity(self, entity_id, entity_representation, position):
        raise NotImplementedError()

    @property
    def world_shape(self):
        '''
        Returns the shape of the world in a tuple
        '''
        raise NotImplementedError()


class MapEntityInfo:
    '''
    This is an utility class for containerizing entities properties needed for world functions 
    '''

    def __init__(self, entity, position):
        self.entity = entity
        self.position = position
        # self.priority = priority

class WorldTile:
    def __init__(self, terrain_rep, terrain_name):
        self.terrain_rep = terrain_rep
        self.terrain_name = terrain_name
        self.entities = []

    def add_entity(self, entity_id):
        self.entities.append(entity_id)

    def remove_entity(self, entity_id):
        return self.entities.pop(entity_id)

    def get_terrain(self):
        return self.terrain_rep


class EvoWorld(
    World,
    WorldActions
):
    def __init__(self, height, width, terrain_types, terrain_dist, finite, world_actions=None, events=None):
        default_world_actions = {
            "move north": self.move_n,
            "move south": self.move_s,
            "move east": self.move_e,
            "move west": self.move_w,
            "swim north": self.swim_n,
            "swim south": self.swim_s,
            "swim east": self.swim_e,
            "swim west": self.swim_w,
            "see radius": self.see_r
        }

        # This dictionary contains the commands that the world can interpret and the corresponding functions
        world_actions = default_world_actions if world_actions is None else default_world_actions.extend(
            world_actions)

        # TODO: Remake this so the world map is made of WorldTiles
        # Initialize the world map
        world_map = np.empty((height, width), dtype=type(WorldTile))
        for i in range(height):
            for j in range(width):
                if (i, j) in terrain_dist:
                    world_map[i, j] = WorldTile(terrain_rep=terrain_dist[(i, j)], terrain_name='None')
                elif "default" in terrain_types:
                    world_map[i, j] = WorldTile(terrain_rep=terrain_types["default"], terrain_name='default')
                else:
                    key = random.choice(list(terrain_types.keys()))
                    world_map[i, j] = WorldTile(terrain_rep=key, terrain_name=terrain_types[key]) # La llave seria algo como G y el valor Grass

        super().__init__(world_map, terrain_types, world_actions, finite, events)

    def get_terrain_type(self, position):
        x, y = position
        return self.world_map[x, y].terrain_name

    def get_entities_in_position(self, position):
        x, y = position
        entities = self.world_map[x,y].entities # world_map is a map of WorldTiles
        # return all MapEntityInfo from this entities
        return [self.entities[entity.get_entity_id()] for entity in entities]
        # return [entity for entity in entities if entity.get_entity_id() in self.entities]

    def valid_position(self, position):
        row_max, col_max = self.world_map.shape
        x, y = position
        return x in range(row_max) and y in range(col_max)

    def place_entity(self, entity: Entity, position):
        if not self.valid_position(position):
            raise Exception('The position is out of range')
        x, y = position
        world_tile = self.world_map[x, y]
        map = self.world_map
        if not entity in world_tile.entities:
            world_tile.entities.append(entity)
        self.entities[entity.get_entity_id()] = MapEntityInfo(entity, position)

    def move_entity(self, entity_id, position):
        entityInfo = self.entities[entity_id]
        if self.valid_position(position):
            self.place_entity(entityInfo.entity, position)
            entityInfo.position = position
            self.remove_entity(entity_id, only_position=True)
        else:
            raise Exception('The position is out of range')

    def remove_entity(self, entity_id, only_position=False):
        entityInfo = self.entities[entity_id]
        entity = entityInfo.entity
        x, y = entityInfo.position
        world_tile = self.world_map[x, y]
        map = self.world_map
        try:
            if not only_position:
                self.entities.pop(entity_id)
            world_tile.entities.remove(entity)
            # print('All alright')
        except:
            print('The entity to remove does not appear in the WorldTile')

    def __str__(self) -> str:
        map = self.world_map
        if len(map.shape) != 2:
            raise Exception('Debe tener 2 dimensiones')
        for i in range(map.shape[0]):
            row = ''
            for j in range(map.shape[1]):
                row += f'{map[i, j]} '
            print(row)
