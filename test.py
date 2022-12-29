from typing import Callable
from ctypes.wintypes import BOOL
from evo_entity import *
from evo_sim import *
from evo_world import *

# WORLD TESTING


def generate_world_with_river_terrain_dist(width, height):
    terrain_dist = {}
    for i in range(2):
        for j in range(width):
            terrain_dist[(int(height/2) + i, j)] = "W"
    return terrain_dist


def generate_world_with_river(width, height):
    terrain_types = [("D", "Dirt"), ("W", "Water")]
    terrain_dist = generate_world_with_river_terrain_dist(width, height)
    world = EvoWorld(height, width, terrain_types, terrain_dist)
    return world


def testing_world_generation_and_representation():
    world = generate_world_with_river(10, 10)
    print(world)


def testing_entity_generation():
    world = generate_world_with_river(10, 10)

def testing_callable_typing(func: Callable[[int, bool], int]):
    print(func(5, True))
# Entity Testing

# Simulation Testing


def main():
    # ##[ ]Testing World Generation
    # #Empty world creation and representation
    # print(chr(27) + "[2J")
    # testing_world_generation_and_representation()

    # #[ ]World with entities storage, positioning and representation
    # world = generate_world_with_river(10, 10)
    # print(world)
    # print(chr(27) + "[2J")
    # world.place_entity("2", (4, 4), "E", 1, "E")
    # world.place_entity("1", (0, 0), "S", 1, "E")
    # print(world)
    # print(chr(27) + "[2J")
    # world.execute_action("step 1")
    # print(world)
    # print(chr(27) + "[2J")
    # world.execute_action("step 2")
    # print(world)
    # print(chr(27) + "[2J")
    # world.execute_action("turn 1 E")
    # print(world)
    # print(chr(27) + "[2J")
    # world.execute_action("step 1")
    # print(world)
    # print(chr(27) + "[2J")
    # world.execute_action("turn 1 N")
    # print(world)
    # print(chr(27) + "[2J")
    # world.execute_action("step 1")
    # print(world)
    # print(chr(27) + "[2J")
    # world.execute_action("turn 2 N")
    # print(world)
    # print(chr(27) + "[2J")
    # world.execute_action("step 2")
    # print(world)
    # print(chr(27) + "[2J")
    # world.remove_entity("1")
    # print(world)
    # print(chr(27) + "[2J")
    # world.remove_entity("2")
    # print(world)
    # print(chr(27) + "[2J")
    # pass

    ##[ ]Testing ... 

if __name__ == "__main__":
    main()
