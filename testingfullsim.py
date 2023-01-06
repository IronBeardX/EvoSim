from src.evo_entity import *
from src.evo_sim import *
from src.evo_world import *
from src.genetics import *
from src.utils import *
from random import randint


def gen_basic_dna_chain():
    return [Health(), Hunger(), Smell(), Mouth(), Eat()]


def smeller_ext(dna):
    return [Nose(), Smelling()]


def watcher_ext(dna):
    return [Eye(), VisionRadial()]


def walker_ext(dna):
    return [Legs(), Move()]


def swimmer_ext(dna):
    return [Fins(), Swimming()]


def arms_ext(dna):
    return [Arms(), Attack(), Pick()]


def eater_ext(dna):
    return [Mouth(), Eat()]


def pick_ext(dna):
    dna.extend(arms_ext(dna))
    dna.extend(eater_ext(dna))
    return dna


def main():
    initial_dist = {}
    sim = EvoSim(20,
                 20,
                 {"G": "grass", "D": "dirt", "W": "water"},
                 initial_dist,
                 False,
                 1,
                 5,
                 visualization=False
                 )
    sim.add_entity_gen(fully_capable_opportunistic_gen)
    sim.add_entity_gen(pickable_gen)
    sim.add_entity_gen(food_gen)
    #generate entities generation list in random positions
    positions_ent = gen_random_position_tuple_list(19, 19, 10)
    positions_food = gen_random_position_tuple_list(19, 19, 20)
    positions_pick = gen_random_position_tuple_list(19, 19, 20)
    # create the (generator_position, position) list
    gen_pos_ent = [(0, pos) for pos in positions_ent]
    gen_pos_ent.extend([(2, pos) for pos in positions_food])
    gen_pos_ent.extend([(1, pos) for pos in positions_pick])


    # clean terminal
    print(chr(27) + "[2J")
    sim.run(gen_pos_ent)
    return


def smeller_gen():
    dna = gen_basic_dna_chain()
    dna.extend(smeller_ext(dna))
    return Organism(dna)


def walker_gen():
    dna = gen_basic_dna_chain()
    dna.extend(watcher_ext(dna))
    return Organism(dna)


def random_gen():
    dna = gen_basic_dna_chain()
    #extending dna with all genes:
    dna.extend(smeller_ext(dna))
    dna.extend(watcher_ext(dna))
    dna.extend(walker_ext(dna))
    dna.extend(swimmer_ext(dna))
    dna.extend(arms_ext(dna))
    dna.extend(eater_ext(dna))
    dna.extend(pick_ext(dna))
    return RandomOrg(dna)

def fully_capable_opportunistic_gen():
    dna = gen_basic_dna_chain()
    dna.extend(smeller_ext(dna))
    dna.extend(watcher_ext(dna))
    dna.extend(walker_ext(dna))
    dna.extend(swimmer_ext(dna))
    dna.extend(arms_ext(dna))
    dna.extend(eater_ext(dna))
    dna.extend(pick_ext(dna))
    return OpportunisticOrg(dna)


def gen_random_position_tuple_list(x, y, n):
    #positions should be unique
    positions = set()
    while len(positions) < n:
        positions.add((randint(0, x), randint(0, y)))
    return list(positions)


def food_gen():
    return Food()


def pickable_gen():
    return PackableFood()


if __name__ == "__main__":
    print(main())
