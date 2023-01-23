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

#Initializing genes:
HEALTH = Health()
HUNGER = Hunger()
LEGS = Legs()
EYE = Eye()
ARMS = Arms()
HORNS = Horns()
SMELL = Smell()
FINS = Fins()
NOSE = Nose()
MOUTH = Mouth()
SMELLING = Smelling()
VISIONRADIAL = VisionRadial()
MOVE = Move()
EAT = Eat()
REPRODUCE = Reproduce()
ATTACK = Attack()
DEFEND = Defend()
PICK = Pick()
SWIMMING = Swimming()

#Initializing Genetic Pool:
POOL = GeneticPool()

#Adding all genes to the genetic pool:
POOL.add_genes([HEALTH, HUNGER, LEGS, EYE, ARMS, HORNS, SMELL, FINS, NOSE, MOUTH, SMELLING, VISIONRADIAL, MOVE, EAT, REPRODUCE, ATTACK, DEFEND, PICK, SWIMMING])
#Adding some edges:
POOL.add_dependency("move", "legs")
POOL.add_dependency("pick", "arms")
POOL.add_dependency("attack", "arms")
POOL.add_dependency("defend", "arms")
POOL.add_dependency("attack", "horns")
POOL.add_dependency("smelling", "nose")
POOL.add_dependency("vision", "eye")
POOL.add_dependency("swimming", "fins")

available = POOL.graph.get_available_nodes(["move", 'attack'])
print(available)
