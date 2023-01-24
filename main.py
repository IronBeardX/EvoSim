from src.evo_entity import *
from src.evo_sim import *
from src.evo_world import *
from src.genetics import *
from src.utils import *
from random import randint


HEALTH = Health(min_val=0, max_val=4)
HUNGER = Hunger(min_val=0, max_val=4)
LEGS = Legs(min_val=0, max_val=4)
EYE = Eye(min_val=0, max_val=4)
ARMS = Arms(min_val=0, max_val=4)
HORNS = Horns(min_val=0, max_val=4)
SMELL = Smell(min_val=0, max_val=4)
FINS = Fins(min_val=0, max_val=4)
NOSE = Nose(min_val=0, max_val=4)
MOUTH = Mouth(min_val=0, max_val=4)
SMELLING = Smelling()
VISIONRADIAL = VisionRadial()
MOVE = Move()
EAT = Eat()
REPRODUCE = Reproduce()
ATTACK = Attack()
DEFEND = Defend()
PICK = Pick()
SWIMMING = Swimming()

# Initializing Genetic Pool:
POOL = GeneticPool()

# Adding all genes to the genetic pool:
POOL.add_genes([HEALTH, HUNGER, LEGS, EYE, ARMS, HORNS, SMELL, FINS, NOSE, MOUTH,
               SMELLING, VISIONRADIAL, MOVE, EAT, REPRODUCE, ATTACK, DEFEND, PICK, SWIMMING])
# Adding some edges:
POOL.add_dependency("move", "legs")
POOL.add_dependency("pick", "arms")
POOL.add_dependency("attack", "arms")
POOL.add_dependency("defend", "arms")
POOL.add_dependency("attack", "horns")
POOL.add_dependency("smelling", "nose")
POOL.add_dependency("vision", "eye")
POOL.add_dependency("swimming", "fins")




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
    # generate entities generation list in random positions
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


if __name__ == "__main__":
    main()
