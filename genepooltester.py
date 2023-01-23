from src.actions_sim import *
from src.actions_world import *
from src.behaviors import *
from src.behaviors import *
from src.evo_entity import *
from src.evo_sim import *
from src.evo_world import *
from src.genetics import *
# from src.meta_heuristics import *
from src.utils import *

# Initializing genes:
HEALTH = Health(min_val= 0, max_val= 4)
HUNGER = Hunger(min_val= 0, max_val= 4)
LEGS = Legs(min_val= 0, max_val= 4)
EYE = Eye(min_val= 0, max_val= 4)
ARMS = Arms(min_val= 0, max_val= 4)
HORNS = Horns(min_val= 0, max_val= 4)
SMELL = Smell(min_val= 0, max_val= 4)
FINS = Fins(min_val= 0, max_val= 4)
NOSE = Nose(min_val= 0, max_val= 4)
MOUTH = Mouth(min_val= 0, max_val= 4)
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
print(POOL)

# Generating two species:
dna_chain1 = ['health', 'hunger', 'reproduce', 'legs', 'smell', 'move']
dna_chain2 = ['health', 'hunger', 'reproduce', 'fins', 'smell', 'swimming']
invalid_chain = ['move']

species1 = Species('walker', RandomOrg, dna_chain1, POOL, 6, "W")
species2 = Species('swimmer', RandomOrg, dna_chain2, POOL, 6, "S")
# invalid_species = Species('invalid', RandomOrg, invalid_chain, POOL, 10, "I")
# Generating some organisms
org1 = species1.get_organism()
org1.pass_time()
org2 = species2.get_organism()

org3 = species1.get_organism()
org3.pass_time()
org3.pass_time()
org4 = species2.get_organism()

#making them reproduce:
org5 = species1.reproduction(org1, org3)
org6 = species2.reproduction(org2, org4)

# errororg = species1.reproduction(org1, org2)

new_species = mix(species1, species2, 10, 20)
print()
pass