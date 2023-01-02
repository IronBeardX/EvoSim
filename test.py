from typing import Callable
from ctypes.wintypes import BOOL
from evo_entity import *
from evo_sim import *
from evo_world import *
from genetics import *
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

    '''
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
    # physical_genes_defs["0"] = {
    #     "gen_type": "physical",
    #     "gen_name": "color",
    #     "gen_posible_values": ("red", "blue", "green", "yellow", "black", "white")
    # }

    color_gene = PhysicalGene("color", ("red", "blue", "green", "yellow", "black", "white"))

    physical_genes_defs[color_gene.id] = color_gene

    # physical_genes_defs["1"] = {
    #     "gen_type": "physical",
    #     "gen_name": "size",
    #     "gen_posible_values": (1, 2, 3, 4, 5)
    # }

    size_gene = PhysicalGene("size", (1, 2, 3, 4, 5))

    physical_genes_defs[size_gene.id] = size_gene

    # physical_genes_defs["2"] = {
    #     "gen_type": "physical",
    #     "gen_name": "shape",
    #     "gen_posible_values": ("circle", "square", "triangle")
    # }

    shape_gene = PhysicalGene("shape", ("circle", "square", "triangle"))

    physical_genes_defs[shape_gene.id] = shape_gene

    # physical_genes_defs["3"] = {
    #     "gen_type": "physical",
    #     "gen_name": "legs"
    # }

    legs_gene = PhysicalGene("legs", None)

    physical_genes_defs[legs_gene.id] = legs_gene

    # physical_genes_defs["4"] = {
    #     "gen_type": "physical",
    #     "gen_name": "eyes"
    # }

    eyes_gene = PhysicalGene("eyes", None)

    physical_genes_defs[eyes_gene.id] = eyes_gene

    # creating perception genes
    # perception_genes_defs["5"] = {
    #     "gen_type": "perception",
    #     "gen_name": "vision_color",
    #     "perception_action": "see color ",
    #     "mod_1": (1, 2, 3, 4)
    # }

    vision_color_gene = PerceptionGene("vision_color", "see color ", (1, 2, 3, 4))

    perception_genes_defs[vision_color_gene.id] = vision_color_gene

    # perception_genes_defs["6"] = {
    #     "gen_type": "perception",
    #     "gen_name": "vision_shape",
    #     "perception_action": "see shape ",
    #     "mod_1": (1, 2, 3, 4)
    # }

    vision_shape_gene = PerceptionGene("vision_shape", "see shape ", (1, 2, 3, 4))

    perception_genes_defs[vision_shape_gene.id] = vision_shape_gene

    # creating action genes
    # action_genes_defs["7"] = {
    #     "gen_type": "action",
    #     "gen_name": "walk",
    #     "action": " walk ",
    #     "pre_mod_1": (1, 2, 3, 4)
    # }

    walk_gene = ActionGene("walk", " walk ", (1, 2, 3, 4))

    action_genes_defs[walk_gene.id] = walk_gene

    # action_genes_defs["8"] = {
    #     "gen_type": "action",
    #     "gen_name": "turn",
    #     "action": "turn ",
    #     "mod_1": ("N ", "S ", "E ", "W ")
    # }

    turn_gene = ActionGene("turn", "turn ", ("N ", "S ", "E ", "W "))

    action_genes_defs[turn_gene.id] = turn_gene

    # generating pool
    for gene_id in physical_genes_defs:
        gene_pool.add_node(gene_id, physical_genes_defs[gene_id])

    for gene_id in perception_genes_defs:
        gene_pool.add_node(gene_id, perception_genes_defs[gene_id])

    for gene_id in action_genes_defs:
        gene_pool.add_node(gene_id, action_genes_defs[gene_id])

    edges_list = [
        (legs_gene.id, walk_gene.id),
        (legs_gene.id, turn_gene.id),
        (eyes_gene.id, vision_color_gene.id),
        (eyes_gene.id, vision_shape_gene.id)
    ]

    for edge in edges_list:
        gene_pool.add_edge(edge[0], edge[1])


    list1 = gene_pool.get_available_nodes([])
    list2 = gene_pool.get_available_nodes([legs_gene.id])
    list3 = gene_pool.get_available_nodes([legs_gene.id, eyes_gene.id])
    pass

    '''

    gene_pool = DirectedGraph()

    physical_genes_defs = {}
    perception_genes_defs = {}
    action_genes_defs = {}

    # physical_genes
    color_gene = PhysicalGene(
        "color",
        [select_from_options(
            ("red", "blue", "green", "yellow", "black", "white"))],
        lambda x: 1
    )
    physical_genes_defs[color_gene.id] = color_gene

    size_gene = PhysicalGene(
        "size",
        [select_from_options((1, 2, 3, 4, 5))],
        lambda x: 1
    )
    physical_genes_defs[size_gene.id] = size_gene

    shape_gene = PhysicalGene(
        "shape",
        [select_from_options(("circle", "square", "triangle"))],
        lambda x: 1
    )
    physical_genes_defs[shape_gene.id] = shape_gene

    legs_gene = PhysicalGene(
        "legs",
        [],
        lambda x: 1
    )
    physical_genes_defs[legs_gene.id] = legs_gene

    eyes_gene = PhysicalGene(
        "eyes",
        [],
        lambda x: 1
    )
    physical_genes_defs[eyes_gene.id] = eyes_gene

    # perception_genes
    vision_color_gene = PerceptionGene(
        "vision_color",
        "see color ",
        [select_from_options((1, 2, 3, 4))],
        lambda x: 1
    )
    perception_genes_defs[vision_color_gene.id] = vision_color_gene

    vision_shape_gene = PerceptionGene(
        "vision_shape",
        "see shape ",
        [select_from_options((1, 2, 3, 4))],
        lambda x: 1
    )
    perception_genes_defs[vision_shape_gene.id] = vision_shape_gene

    # action_genes
    walk_gene = ActionGene(
        "walk",
        " walk ",
        [select_from_options((1, 2, 3, 4))],
        [],
        lambda x: 1
    )
    action_genes_defs[walk_gene.id] = walk_gene

    turn_gene = ActionGene(
        "turn",
        "turn ",
        [],
        [select_from_options(("N ", "S ", "E ", "W "))],
        lambda x: 1
    )
    action_genes_defs[turn_gene.id] = turn_gene

    # adding nodes to the pool
    for gene_id in physical_genes_defs:
        gene_pool.add_node(gene_id, physical_genes_defs[gene_id])

    for gene_id in perception_genes_defs:
        gene_pool.add_node(gene_id, perception_genes_defs[gene_id])

    for gene_id in action_genes_defs:
        gene_pool.add_node(gene_id, action_genes_defs[gene_id])

    # adding edges to the pool
    edges_list = [
        (legs_gene.id, walk_gene.id),
        (legs_gene.id, turn_gene.id),
        (eyes_gene.id, vision_color_gene.id),
        (eyes_gene.id, vision_shape_gene.id)
    ]

    for edge in edges_list:
        gene_pool.add_edge(edge[0], edge[1])

    # Creating organism genome
    # Genomes are a dict with the gene id as key and the value a list
    # with every parameter that a gene uses for instantiation
    genome_green_not_shape = {
        #physical
        color_gene.id:[[2]],
        size_gene.id:[[0]],
        shape_gene.id:[[]],
        legs_gene.id:[[]],
        eyes_gene.id:[[]],
        #perception
        vision_color_gene.id:[[]],
        #action
        walk_gene.id:[[]],
        turn_gene.id:[[]]
    }
    organism1 = Organism(gene_pool, genome_green_not_shape, 10)
    
    genome_not_color = {
        #physical
        color_gene.id:[[]],
        size_gene.id:[[]],
        shape_gene.id:[[]],
        legs_gene.id:[[]],
        eyes_gene.id:[[]],
        #perception
        vision_shape_gene.id:[[]],
        #action
        walk_gene.id:[[]],
        turn_gene.id:[[]]
    }
    organism2 = Organism(gene_pool, genome_not_color, 10)
    
    genome_sea_cucumber = {
        #physical
        color_gene.id:[[]],
        size_gene.id:[[]],
        shape_gene.id:[[]],
        eyes_gene.id:[[]],
        #perception
        vision_color_gene.id:[[]],
        vision_shape_gene.id:[[]]
    }
    sea_cucumber = Organism(gene_pool, genome_sea_cucumber, 10)


# TODO: Think about defining an action class, could be useful
# TODO: Think about defining a gene class, could be useful
if __name__ == "__main__":
    main()
