from src.evo_entity import *
from src.evo_sim import *
from src.evo_world import *
from src.genetics import *
from src.utils import *
from random import randint


def main():
    initial_dist = {}
    sim = EvoSim(10,
                 10,
                 {"G": "grass", "D": "dirt", "W": "water"},
                 initial_dist,
                 False,
                 10,
                 100,
                 visualization=True
                 )
    sim.add_entity_gen(fully_capable_opportunistic_gen)
    sim.add_entity_gen(pickable_gen)
    sim.add_entity_gen(food_gen)
    sim.add_entity_gen(random_gen)
    #generate entities generation list in random positions
    positions_ent = gen_random_position_tuple_list(9, 9, 10)
    positions_food = gen_random_position_tuple_list(9, 9, 5)
    positions_pick = gen_random_position_tuple_list(9, 9, 5)
    # create the (generator_position, position) list
    gen_pos_ent = [(random.choice([1, 3]), pos) for pos in positions_ent]
    gen_pos_ent.extend([(2, pos) for pos in positions_food])
    gen_pos_ent.extend([(1, pos) for pos in positions_pick])


    # clean terminal
    print(chr(27) + "[2J")
    sim.run(gen_pos_ent)
    print("Simulation Finished")


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
    return RandomOrg(dna)

def fully_capable_opportunistic_gen():
    dna = gen_basic_dna_chain()
    dna.extend(smeller_ext(dna))
    dna.extend(watcher_ext(dna))
    dna.extend(walker_ext(dna))
    dna.extend(swimmer_ext(dna))
    dna.extend(arms_ext(dna))
    dna.extend(eater_ext(dna))
    dna.append(Reproduce())
    return OpportunisticOrg(dna, species = OpportunisticOrg)


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
    main()
