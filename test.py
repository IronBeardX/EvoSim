from typing import Callable
from ctypes.wintypes import BOOL
from src.evo_entity import *
from src.evo_sim import *
from src.evo_world import *
from src.genetics import *
from src.utils import *


# WORLD TESTING


def main():
    # INITIALIZING GENES:
    # PHYSICAL
    health = Health()
    hunger = Hunger()
    legs = Legs()
    eye = Eye()
    arms = Arms()
    horns = Horns()
    smell = Smell()
    fins = Fins()
    nose = Nose()

    # PERCEPTION
    vision_lin = VisionLinear()
    vision_rad = VisionRadial()
    smelling = Smelling()

    # ACTION
    move = Move()
    eat = Eat()
    rep = Reproduce()
    dup = Duplicate()
    attack = Attack()
    defend = Defend()
    pick = Pick()
    swimming = Swimming()

    # TESTING IN ORGANISMS

    only_phy = [health.get_copy, hunger.get_copy, legs.get_copy, eye.get_copy,
                arms.get_copy, horns.get_copy, smell.get_copy, fins.get_copy, nose.get_copy]

    only_per = [health, hunger, smell, eye, vision_lin, vision_rad, smelling]

    only_act = [health, hunger, legs, eye, arms, horns, smell, fins,
                nose, move, eat, rep, dup, attack, defend, pick, swimming]

    org1 = Organism(only_phy)

    org2 = Organism(only_per)

    org3 = Organism(only_act)

    return


if __name__ == "__main__":
    main()
