from src.evo_entity import *
from src.evo_sim import *
from src.evo_world import *
from src.genetics import *
from src.utils import *
from random import randint


HEALTH = Health(min_val=100, max_val=100)
HUNGER = Hunger(min_val=100, max_val=100)
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

dna_chain1 = ['health', 'hunger', 'reproduce', 'legs', 'move']
dna_chain2 = ['health', 'hunger', 'reproduce', 'fins', 'swimming']
dna_chain3 = ['health', 'hunger', 'reproduce',
              'arms', 'pick', 'attack', 'defend']
dna_chain4 = ['health', 'legs', 'hunger', 'reproduce',
              'arms', 'eye', 'vision', 'defend', 'move']

species1 = Species('walker', Organism, dna_chain1, POOL, 8, "Z")
species2 = Species('swimmer', Organism, dna_chain2, POOL, 8, "X")
species3 = Species('fighter', Organism, dna_chain3, POOL, 8, "C")
species4 = Species('hunter', Organism, dna_chain4, POOL, 1000, "V")

food = FoodFactory(
    identifier="food",
    food_class=Food,
    representation = "F"
)
apple = FoodFactory(
    identifier="apple",
    food_class=Food,
    storable=True,
    representation="A",
    nutrition=10,
    food_type="fruit"
)
meat = FoodFactory(
    identifier="meat",
    food_class=Food,
    storable=True,
    representation="M",
    nutrition=20,
    food_type="meat"
)


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
    sim.add_species(species1)
    sim.add_species(species2)
    sim.add_species(species3)
    sim.add_species(species4)
    sim.add_object_type(meat)
    sim.add_object_type(apple)

    # generate entities generation list in random positions
    # positions_ent = gen_random_position_tuple_list(9, 9, 10)
    # positions_food = gen_random_position_tuple_list(9, 9, 5)
    # positions_pick = gen_random_position_tuple_list(9, 9, 5)

    # create the (generator_position, position) list

    # gen_pos_ent = [(random.choice([1, 3]), pos) for pos in positions_ent]
    # gen_pos_ent.extend([(2, pos) for pos in positions_food])
    # gen_pos_ent.extend([(1, pos) for pos in positions_pick])

    # clean terminal
    gen_pos_ent = [
        (species1.id, [
            (5, 0),
            (6, 0)
        ]),
        (species2.id, [
            (0, 5),
            (0, 6)
        ]),
        (species3.id, [
            (9, 5),
            (9, 6)
        ]),
        (species4.id, [
            (5, 9),
            (6, 9)
        ]),
        # (meat.id, [
        #     (0, 0),
        #     (9, 0),
        #     (0, 9),
        #     (9, 9)
        # ]),
        (apple.id, [
            (4, 4),
            (5, 4),
            (6, 4),
            (4, 5),
            (6, 5),
            (4, 6),
            (5, 6),
            (6, 6)
        ])
    ]
    print(chr(27) + "[2J")
    print()
    sim.run(gen_pos_ent)
    print("Simulation Finished")

def testing_NN():
    x_train = np.array([[[0,0]], [[0,1]], [[1,0]], [[1,1]]])
    y_train = np.array([[[0]], [[1]], [[1]], [[0]]])

    # network
    net = Network()
    net.add(FCLayer(2, 3))
    net.add(ActivationLayer(tanh, tanh_prime))
    net.add(FCLayer(3, 1))
    net.add(ActivationLayer(tanh, tanh_prime))

    # train
    net.use(mse, mse_prime)
    net.fit(x_train, y_train, epochs=1000, learning_rate=0.1)

    # test
    out = net.predict(x_train)
    print(out)


if __name__ == "__main__":
    main()
    # testing_NN()
