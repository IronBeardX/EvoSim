from typing import Callable
from ctypes.wintypes import BOOL
from evo_entity import *
from evo_sim import *
from evo_world import *
from src.utils import *

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
    # [ ]Testing World Generation
    # Empty world creation and representation
    '''
    print(chr(27) + "[2J")
    testing_world_generation_and_representation()
    '''

    # [ ]World with entities storage, positioning and representation
    '''
    world = generate_world_with_river(10, 10)
    print(world)
    print(chr(27) + "[2J")
    world.place_entity("2", (4, 4), "E", 1, "E")
    world.place_entity("1", (0, 0), "S", 1, "E")
    print(world)
    print(chr(27) + "[2J")
    world.execute_action("step 1")
    print(world)
    print(chr(27) + "[2J")
    world.execute_action("step 2")
    print(world)
    print(chr(27) + "[2J")
    world.execute_action("turn 1 E")
    print(world)
    print(chr(27) + "[2J")
    world.execute_action("step 1")
    print(world)
    print(chr(27) + "[2J")
    world.execute_action("turn 1 N")
    print(world)
    print(chr(27) + "[2J")
    world.execute_action("step 1")
    print(world)
    print(chr(27) + "[2J")
    world.execute_action("turn 2 N")
    print(world)
    print(chr(27) + "[2J")
    world.execute_action("step 2")
    print(world)
    print(chr(27) + "[2J")
    world.remove_entity("1")
    print(world)
    print(chr(27) + "[2J")
    world.remove_entity("2")
    print(world)
    print(chr(27) + "[2J")
    pass
    '''

    # [ ] Playing with genetics and entities execution flow
    # Creating a genetic pool
    # init gene pool
    gene_pool = DirectedGraph()

    # init nodes:
    physical_genes_defs = {}
    perception_genes_defs = {}
    action_genes_defs = {}

    # FIXME: We should have a way to define the genes in a file?
    # the dict keys should be the gene ids

    # creating physical genes
    physical_genes_defs["0"] = {
        "gen_type": "physical",
        "gen_name": "color",
        "gen_posible_values": ("red", "blue", "green", "yellow", "black", "white")
    }

    physical_genes_defs["1"] = {
        "gen_type": "physical",
        "gen_name": "size",
        "gen_posible_values": (1, 2, 3, 4, 5)
    }

    physical_genes_defs["2"] = {
        "gen_type": "physical",
        "gen_name": "shape",
        "gen_posible_values": ("circle", "square", "triangle")
    }

    physical_genes_defs["3"] = {
        "gen_type": "physical",
        "gen_name": "legs"
    }

    physical_genes_defs["4"] = {
        "gen_type": "physical",
        "gen_name": "eyes"
    }

    # creating perception genes
    perception_genes_defs["5"] = {
        "gen_type": "perception",
        "gen_name": "vision_color",
        "perception_action": "see color ",
        "mod_1": (1, 2, 3, 4)
    }

    perception_genes_defs["6"] = {
        "gen_type": "perception",
        "gen_name": "vision_shape",
        "perception_action": "see shape ",
        "mod_1": (1, 2, 3, 4)
    }

    # creating action genes
    action_genes_defs["7"] = {
        "gen_type": "action",
        "gen_name": "walk",
        "action": " walk ",
        "pre_mod_1": (1, 2, 3, 4)
    }

    action_genes_defs["8"] = {
        "gen_type": "action",
        "gen_name": "turn",
        "action": "turn ",
        "mod_1": ("N ", "S ", "E ", "W ")
    }

    # generating pool
    for gene_id in physical_genes_defs:
        gene_pool.add_node(gene_id, physical_genes_defs[gene_id])

    for gene_id in perception_genes_defs:
        gene_pool.add_node(gene_id, perception_genes_defs[gene_id])

    for gene_id in action_genes_defs:
        gene_pool.add_node(gene_id, action_genes_defs[gene_id])

    edges_list = [
        ("3", "7"),
        ("3", "8"),
        ("4", "5"),
        ("4", "6")
    ]

    for edge in edges_list:
        gene_pool.add_edge(edge[0], edge[1])
    pass

# TODO: Think about defining an action class, could be useful
# TODO: Think about defining a gene class, could be useful
if __name__ == "__main__":
    main()
