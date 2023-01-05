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


def main():
    initial_dist = {}
    sim = EvoSim(15,
                 15,
                 {"G": "grass", "D": "dirt", "W": "water"},
                 initial_dist,
                 False,
                 1,
                 10
                 )
    sim.add_entity_gen(smeller_gen)
    sim.add_entity_gen(walker_gen)
    sim.add_entity_gen(random_gen)
    #clean terminal
    print(chr(27) + "[2J")
    sim.run([(0, (0, 0)), (1, (0, 1)), (2, (0, 2))])
    return


def smeller_gen():
    dna = gen_basic_dna_chain()
    dna.extend(smeller_ext(dna))
    dna.extend(walker_ext(dna))
    return Organism(dna)


def walker_gen():
    dna = gen_basic_dna_chain()
    dna.extend(watcher_ext(dna))
    dna.extend(walker_ext(dna))
    return Organism(dna)

def random_gen():
    dna = gen_basic_dna_chain()
    dna.extend(walker_ext(dna))
    dna.extend(swimmer_ext(dna))
    dna.extend(arms_ext(dna))
    return Organism(dna)


if __name__ == "__main__":
    print(main())
