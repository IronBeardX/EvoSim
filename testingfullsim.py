from src.evo_entity import *
from src.evo_sim import *
from src.evo_world import *
from src.genetics import *
from src.utils import *


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
    sim = EvoSim(150,
                 150,
                 {"G": "grass", "D": "dirt", "W": "water"},
                 initial_dist,
                 False,
                 1,
                 10
                 )
    sim.add_entity_gen(food_gen)
    sim.add_entity_gen(pickable_gen)
    sim.add_entity_gen(eater_gen)
    sim.add_entity_gen(picker_gen)
    sim.add_entity_gen(atacker_gen)
    sim.add_entity_gen(defender_gen)
    # clean terminal
    print(chr(27) + "[2J")
    sim.run([
        (0, (1, 0)),
        (1, (1, 1)),
        (5, (1, 2)),
        (2, (0, 0)),
        (3, (0, 1)),
        (4, (0, 2)),
    ])
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
    # adding all genes:
    dna.extend(smeller_ext(dna))
    dna.extend(watcher_ext(dna))
    dna.extend(walker_ext(dna))
    dna.extend(swimmer_ext(dna))
    dna.extend(arms_ext(dna))
    dna.extend(eater_ext(dna))
    dna.extend(pick_ext(dna))
    return Organism(dna)


def food_gen():
    return Food()


def pickable_gen():
    return PackableFood()


def eater_gen():
    dna = gen_basic_dna_chain()
    dna.extend(watcher_ext(dna))
    return SEOrg(dna)


def picker_gen():
    dna = gen_basic_dna_chain()
    dna.extend(pick_ext(dna))
    dna.extend(watcher_ext(dna))
    return SPOrg(dna)


def atacker_gen():
    dna = gen_basic_dna_chain()
    dna.extend(arms_ext(dna))
    dna.extend(watcher_ext(dna))
    return SAOrg(dna)


def defender_gen():
    dna = gen_basic_dna_chain()
    dna.extend(arms_ext(dna))
    return DOrg(dna)


if __name__ == "__main__":
    print(main())
