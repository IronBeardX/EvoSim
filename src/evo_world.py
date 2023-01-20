from .actions_world import *
from typing import Callable
from curses.ascii import isdigit
import numpy as np
import random


class World():
    '''
    Basic class of the world, it contains information about the terrain and the entities that inhabit it. It's responsible
    for updating its state according to the actions of entities and events  that occur in the world. 
    '''

    def __init__(self, world_map, terrain_types, finite=False):
        '''
        Here basic information about the world is settled, such as the available terrain types, and the world map itself.
        Information about basic laws of the world should also be settled with this method, such as if the world map is an 
        array, a Cartesian plane, or if it is finite or infinite. Updating entities should be relegated to the simulation 
        class.
        '''
        self.world_map = world_map
        self.finite = finite
        self.terrain_types = terrain_types
        self.event_list = []
        self.entities: dict[str, MapEntityInfo] = {}
        '''
        The entities dictionary contains information about the entities relevant to the world. The key is the entity id and
        the value is a MapEntityInfo object that contains information about the entity.
        '''

    def get_entity_info(self, entity_id):
        '''
        This method returns the information about the entity with the given id.
        '''
        return self.entities[entity_id]

    def valid_position(self, position):
        '''
        This method returns True if the given position is valid, False otherwise.
        '''
        try:
            self.world_map[position[0], position[1]]
            return True
        except:
            return False

    def get_entity_by_position(self, position):
        '''
        This method returns the entity that occupies the given position.
        '''
        entities = []
        for i in self.entities.keys():
            if self.entities[i].position[0] == position[0] and self.entities[i].position[1] == position[1]:
                entities.append(i)
        return entities

    def get_terrain_type(self, position):
        '''
        This method returns the terrain type of the given position.
        '''
        if not self.valid_position(position):
            return "unknown"
        return self.terrain_types[self.world_map[position[0], position[1]]]


class MapEntityInfo:
    '''
    This is an utility class for containerizing entities properties needed for world functions 
    '''

    def __init__(self, position, can_coexist, string_rep):
        '''
        This method initializes the entity properties.

        @param position: The position of the entity in the world
        @param orientation: The orientation of the entity in the world
        @param representation_priority: The priority of the entity representation in the world
        @param can_coexist: If the entity can coexist with other entities
        @param positioning_rules: The positioning rules of the entity in the world. Describes, for example, in which terrains the entity
        can be positioned.
        '''
        self.position = position
        self.can_coexist = can_coexist
        self.representation = string_rep


class EvoWorld(
    World,
    MoveNorth,
    MoveSouth,
    MoveEast,
    MoveWest,
    SwimNorth,
    SwimSouth,
    SwimEast,
    SwimWest,
    SeeRadius,
    ManhatanDistance,
    TerrainRadius
):
    def __init__(self, height, width, terrain_types, terrain_dist, finite):

        # Initialize the world map
        world_map = np.empty((height, width), dtype=str)
        for i in range(height):
            for j in range(width):
                if (i, j) in terrain_dist:
                    world_map[i, j] = terrain_dist[(i, j)]
                elif "default" in terrain_types:
                    world_map[i, j] = terrain_types["default"]
                else:
                    world_map[i, j] = random.choice(list(terrain_types.keys()))

        # Initialize world actions
        self.world_actions = {
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

        super().__init__(world_map, terrain_types, finite)

    def execute_action(self, action):
        '''
        This method executes the given action in the world.
        '''
        command = action["command"]
        if command not in list(self.world_actions.keys()):
            return
            # raise Exception("Invalid command")
        if "entity" in action:
            entity_id = action["entity"]
            if entity_id not in self.entities:
                raise Exception("Invalid entity")
        if "parameters" in action:
            parameters = action["parameters"]
            self.world_actions[command](entity_id)(*parameters)
        else:
            self.world_actions[command](entity_id)

    def __str__(self) -> str:
        # This methods returns a string representation of the world
        terrain_copy = self.world_map.copy()
        for entity in self.entities.keys():
            entity_position = self.entities[entity].position
            terrain_copy[entity_position[0], entity_position[1]
                         ] = self.entities[entity].representation
        string_rep = ""
        for i in range(terrain_copy.shape[0]):
            for j in range(terrain_copy.shape[1]):
                string_rep += terrain_copy[i, j] + " "
            string_rep += "\n"
        return string_rep + "\n \n"

    def world_rep(self):
        terrain_copy = self.world_map.copy()
        for entity in self.entities.keys():
            entity_position = self.entities[entity].position
            terrain_copy[entity_position[0], entity_position[1]
                         ] = self.entities[entity].representation
        return terrain_copy

    def place_entity(self, id, position, representation, coexistence=False):
        entity_information = MapEntityInfo(
            position, coexistence, representation)

        self.entities[id] = entity_information

    def remove_entity(self, entity_id):
        del self.entities[entity_id]

    def get_random_position(self):
        '''
        This method returns a random position in the world.
        '''
        return (np.random.randint(0, self.world_map.shape[0]), np.random.randint(0, self.world_map.shape[1]))

    def get_pos_terrain(self, position):
        return self.terrain_types[self.world_map[position]]
