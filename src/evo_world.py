from .actions_world import *
from typing import Callable
from curses.ascii import isdigit
import numpy as np
import random


class World():
    '''
    Basic class of the world, it contains information about the entities and the world map relevant to the positioning
    and movements of things
    '''

    def __init__(self, world_map, terrain_types, finite=False):
        self.world_map = world_map
        self.finite = finite
        self.terrain_types = terrain_types
        self.event_list = []
        self.entities = {}

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
        This method returns the entities that occupies the given position.
        '''
        entities = []
        for i in self.entities.keys():
            if self.entities[i].position == position:
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
    def __init__(self, height, width, terrain_types, terrain_dist, finite, world_actions = None):

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
        self.world_actions = default_world_actions if world_actions is None else default_world_actions.extend(world_actions)

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
