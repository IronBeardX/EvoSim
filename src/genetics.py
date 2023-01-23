from uuid import uuid4
from .utils import DirectedGraph as DG
import random


class Gene:
    def __init__(self, name, gen_type, genetic_cost=1):
        self.genetic_cost = genetic_cost
        self.name = name
        self.gen_type = gen_type

    def apply_gen(self):
        raise NotImplementedError()


class PhysicalGene(Gene):
    def __init__(self, name, mutation_chance=0.5, min_val=0, max_val=100, mutation_step=1, genetic_cost=1, value=None):
        '''
        [ ] los genes fisicos reciben un solo valor para facilitar otras implementacion y los efectos de este gen en el organismo se
        deben definir tomando este valor en cuenta.
        '''
        # TODO: hacer las validaciones, tambien hacer que el costo 
        self.mutation_chance = mutation_chance
        self.min = min_val
        self.max = max_val
        self.mutation_step = mutation_step
        self.value = random.randint(min_val, max_val) if not value else value
        super().__init__(name, 'physical', genetic_cost)

    def mutate(self):
        new_val = self.value
        if random.random() < self.mutation_chance:
            new_val += random.choice([-self.mutation_step, self.mutation_step])
            if new_val < self.min:
                new_val = self.min
            if new_val > self.max:
                new_val = self.max
        return self.__class__(self.mutation_chance, self.min, self.max, self.mutation_step, self.genetic_cost, new_val)

    def get_copy(self):
        return self.__class__(self.mutation_chance, self.min, self.max, self.mutation_step, self.genetic_cost, self.value)

#TODO: añadir el costo genetico a las inicializaciones de los genes de accion y percepcion 
class ActionGene(Gene):
    def __init__(self, name, cost=10, genetic_cost = 1):
        super().__init__(name, 'action')
        self.cost = cost
        self.genetic_cost = genetic_cost


class PerceptionGene(Gene):
    def __init__(self, name, genetic_cost = 1):
        super().__init__(name, 'perception')


# [ ] Physical Genes
class Health(PhysicalGene):
    def __init__(self, mutation_chance=0.5, min_val=0, max_val=100, mutation_step=1, genetic_cost=1, value=None):
        super().__init__('health', mutation_chance, min_val, max_val, mutation_step, genetic_cost, value)

    def get_property(self):
        return [{"health": self.value}]


class Hunger(PhysicalGene):
    def __init__(self, mutation_chance=0.5, min_val=0, max_val=100, mutation_step=1, genetic_cost=1, value=None):
        super().__init__('hunger', mutation_chance, min_val, max_val, mutation_step, genetic_cost, value)

    def get_property(self):
        return [{
            "hunger": self.value,
            "max hunger": self.value
        }]


class Legs(PhysicalGene):
    def __init__(self, mutation_chance=0.5, min_val=0, max_val=100, mutation_step=1, genetic_cost=1, value=None):
        super().__init__('legs', mutation_chance, min_val, max_val, mutation_step, genetic_cost, value)

    def get_property(self):
        return [{"legs": self.value}]


class Eye(PhysicalGene):
    def __init__(self, mutation_chance=0.5, min_val=0, max_val=100, mutation_step=1, genetic_cost=1, value=None):
        super().__init__('eye', mutation_chance, min_val, max_val, mutation_step, genetic_cost, value)

    def get_property(self):
        return [{"eye": self.value}]


class Arms(PhysicalGene):
    def __init__(self, mutation_chance=0.5, min_val=0, max_val=100, mutation_step=1, genetic_cost=1, value=None):
        super().__init__('arms', mutation_chance, min_val, max_val, mutation_step, genetic_cost, value)

    def get_property(self):
        return [
            {"arms": self.value},
            {"arms_defense": self.value},
            {"arms_attack": self.value},
            {"storage": []},
            {"defending": False}
        ]


class Horns(PhysicalGene):
    def __init__(self, mutation_chance=0.5, min_val=0, max_val=100, mutation_step=1, genetic_cost=1, value=None):
        super().__init__('horns', mutation_chance, min_val, max_val, mutation_step, genetic_cost, value)

    def get_property(self):
        return [{"horns_attack": self.value}]


class Smell(PhysicalGene):
    def __init__(self, mutation_chance=0.5, min_val=0, max_val=100, mutation_step=1, genetic_cost=1, value=None):
        super().__init__('smell', mutation_chance, min_val, max_val, mutation_step, genetic_cost, value)

    def get_property(self):
        return [{"smell": self.value}]


class Fins(PhysicalGene):
    def __init__(self, mutation_chance=0.5, min_val=0, max_val=100, mutation_step=1, genetic_cost=1, value=None):
        super().__init__('fins', mutation_chance, min_val, max_val, mutation_step, genetic_cost, value)

    def get_property(self):
        return [{"fins": self.value}]


class Nose(PhysicalGene):
    def __init__(self, mutation_chance=0.5, min_val=0, max_val=100, mutation_step=1, genetic_cost=1, value=None):
        super().__init__('nose', mutation_chance, min_val, max_val, mutation_step, genetic_cost, value)

    def get_property(self):
        return [{"nose": self.value}]


class Mouth(PhysicalGene):
    def __init__(self, mutation_chance=0.5, min_val=0, max_val=100, mutation_step=1, genetic_cost=1, value=None):
        super().__init__('mouth', mutation_chance, min_val, max_val, mutation_step, genetic_cost, value)

    def get_property(self):
        return [{"mouth": self.value}]

# [ ]Perception Genes


class Smelling(PerceptionGene):
    def __init__(self):
        super().__init__("smelling")

    def get_property(self):
        return [
            "smelling"
        ]


class VisionRadial(PerceptionGene):
    def __init__(self):
        super().__init__("vision")

    def get_property(self):
        return [
            "vision"
        ]

# [ ]Action Genes


class Move(ActionGene):
    def __init__(self, cost=10):
        super().__init__("move", cost=cost)

    def get_property(self):
        return [
            {"name": "move north", "cost": self.cost},
            {"name": "move south", "cost": self.cost},
            {"name": "move east", "cost": self.cost},
            {"name": "move west", "cost": self.cost}
        ]


class Eat(ActionGene):
    def __init__(self, cost=10):
        super().__init__("eat", cost)

    def get_property(self):
        return [
            {"name": "eat", "cost": self.cost}
        ]


class Reproduce(ActionGene):
    def __init__(self, cost=10):
        super().__init__("reproduce", cost)

    def get_property(self):
        return [
            {"name": "reproduce", "cost": self.cost}
        ]


class Attack(ActionGene):
    def __init__(self, cost=10):
        super().__init__("attack", cost)

    def get_property(self):
        return [
            {"name": "attack", "cost": self.cost}
        ]


class Defend(ActionGene):
    def __init__(self, cost=10):
        super().__init__("defend", cost)

    def get_property(self):
        return [
            {"name": "defend", "cost": self.cost}
        ]


class Pick(ActionGene):
    def __init__(self, cost=10):
        super().__init__("pick", cost)

    def get_property(self):
        return [
            {"name": "pick", "cost": self.cost}
        ]


class Swimming(ActionGene):
    def __init__(self, cost=10):
        super().__init__("swimming", cost)

    def get_property(self):
        return [
            {"name": "swim north", "cost": self.cost},
            {"name": "swim south", "cost": self.cost},
            {"name": "swim east", "cost": self.cost},
            {"name": "swim west", "cost": self.cost}
        ]


'''
Genes dependencies:
    Legs: Move
    Arms: Pick, attack, defend
    Horns: Attack
    Nose: Smell
    Eye: Vision
'''


class GeneticPool:
    def __init__(self):
        self.graph = DG()

    def add_gene(self, gene):
        self.graph.add_node(
            gene.name, {"gene": gene, "genetic_cost": gene.genetic_cost})

    def add_genes(self, gene_list):
        for gene in gene_list:
            self.add_gene(gene)

    def remove_gen(self, gene):
        self.graph.remove_node(gene.name)

    def update_gen(self, gene):
        self.graph.set_node_data(gene.name, gene)

    def get_gene(self, gene_name):
        return self.graph.get_node_data(gene_name)

    def add_dependency(self, dependant_gene, other_gene):
        self.graph.add_edge(dependant_gene, other_gene)

    def get_dependencies(self, gene):
        neighbors = self.graph.get_neighbors(gene.name)
        return [neighbor for neighbor in neighbors]

    def validate_chain(self, dna_chain, genetic_potential):
        current_genetic_cost = 0
        for dna in dna_chain:
            if not self.graph.get_node(dna):
                return False
                
            neighbors = self.graph.get_neighbors(dna)

            dependency = len(neighbors) == 0

            for neighbor in neighbors:
                if neighbor in dna_chain:
                    dependency = True
                    break
            if not dependency:
                return False
            
            current_genetic_cost += self.graph.get_node_data(dna)["genetic_cost"]
        return current_genetic_cost <= genetic_potential

    def __str__(self):
        return str(self.graph)

    def __getitem__(self, item):
        return self.graph.get_node_data(item)
