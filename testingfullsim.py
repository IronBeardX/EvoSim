from src.evo_entity import *
from src.evo_sim import *
from src.evo_world import *
from src.genetics import *
from src.utils import *

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
mouth = Mouth()
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
WORLD_DIST1 = [(x, 25) for x in range(50)] + [(x, 26) for x in range(50)]
ONLY_PHY = [health.get_copy, hunger.get_copy, legs.get_copy, eye.get_copy, arms.get_copy, horns.get_copy, smell.get_copy, fins.get_copy, nose.get_copy]

ONLY_PER = [health, hunger, smell, eye, vision_lin, vision_rad, smelling]

ONLY_ACT = [health, hunger, mouth,legs, eye, arms, horns, smell, fins, nose, move, eat, rep, dup, attack, defend, pick, swimming]



def main():
    initial_dist = {}
    for position in WORLD_DIST1:
        initial_dist[position] = "W"
    sim = EvoSim(50,
                    50, 
                    [("G", "grass"), ("D", "dirt"), ("W", "water")],
                    initial_dist,
                    False,
                    1,
                    10
                    )
    sim.add_entity_gen(entity1_gen)
    sim.add_entity_gen(entity2_gen)
    sim.add_entity_gen(entity3_gen)
    sim.run([(2, (0,0)), (2, (0,1)), (2,(0,2))])
    return
    
def entity1_gen():
    return Organism(ONLY_PHY)    

def entity2_gen():
    return Organism(ONLY_PER)

def entity3_gen():
    return Organism(ONLY_ACT)
    

if __name__ == "__main__":
    print(main())