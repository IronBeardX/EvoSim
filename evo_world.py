from typing import Callable
from curses.ascii import isdigit
from src.world import *
import numpy as np

DIRECTIONS = {"N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1)}


class EvoWorld(World):
    def __init__(self, height, width, terrain_types: list[tuple[str, str]], terrain_dist: dict[tuple[int, int], str],
                 finite: bool = True, step_size: int = 1) -> None:

        # Initialize the world map
        world_map = np.empty((height, width), dtype=str)
        for i in range(height):
            for j in range(width):
                if (i, j) in terrain_dist:
                    world_map[i, j] = terrain_dist[(i, j)]
                else:
                    world_map[i, j] = terrain_types[0][0]

        # Initialize world actions
        self.world_actions = {
            "step": self.step,
            "turn": self.turn
        }

        super().__init__(world_map, terrain_types, "Array", finite)

    # [ ]
    def __str__(self) -> str:
        terrain_copy = self.world_map.copy()
        # TODO: If two entities coexists in the same cell only the one with higher priority will be shown
        for entity in self.entities.keys():
            entity_position = self.entities[entity].position
            terrain_copy[entity_position[0], entity_position[1]
                         ] = self.entities[entity].representation
        return str(terrain_copy)

    # [ ]
    def place_entity(self, id: str, position: tuple[int, int], orientation: str, priority: int, representation: str, coexistence: bool = False) -> None:
        # TODO: check which parameters are needed
        orientation = DIRECTIONS[orientation]
        entity_information = MapEntityInfo(
            position, orientation, priority, coexistence, None, representation)

        self.entities[id] = entity_information

    def remove_entity(self, entity_id: str) -> None:
        self.entities.pop(entity_id)

    def execute_action(self, action: str) -> None:
        repeat = 1
        tokenized_command = action.split(" ")
        if tokenized_command[0].isdigit():
            repeat = int(tokenized_command[0])
            tokenized_command = tokenized_command[1:]
        if tokenized_command[0] not in self.world_actions:
            raise Exception("Invalid action")

        for _ in range(repeat):
            self.world_actions[tokenized_command[0]](*tokenized_command[1:])

    def step(self, entity_id: str) -> None:
        # check if the entity is in the world
        if entity_id not in self.entities:
            raise Exception("Entity not found in the world")

        # get the entity information
        entity = self.entities[entity_id]
        entity_position = entity.position
        entity_orientation = entity.orientation

        # get the new position
        new_position = (entity_position[0] + entity_orientation[0],
                        entity_position[1] + entity_orientation[1])

        # check if the new position is valid
        if not self.is_valid_position(new_position):
            raise Exception("Invalid position")

        # update the entity position
        # TODO: Simple implementation in world class
        self.update_entity_position(entity_id, new_position)

    def is_valid_position(self, position: tuple) -> bool:
        return 0 <= position[0] < self.world_map.shape[0] and 0 <= position[1] < self.world_map.shape[1]

    def turn(self, entity_id: str, new_direction: str) -> None:
        # check if the entity is in the world
        if entity_id not in self.entities:
            raise Exception("Entity not found in the world")

        # get the entity information
        entity = self.entities[entity_id]
        entity_orientation = entity.orientation

        # get the new orientation
        new_orientation = DIRECTIONS[new_direction]

        # update the entity orientation
        self.update_entity_orientation(entity_id, new_orientation)

    def add_action(self, action_descriptor: str, action_execution: Callable[..., any]) -> None:
        self.world_actions[action_descriptor] = action_execution