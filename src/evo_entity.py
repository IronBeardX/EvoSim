from .utils import *
from .genetics import *
from .behaviors import *

# TODO: implement knowledge as a class

class Entity:
    '''
    Basic class of world inhabitants, it encompasses everything that exists in the world excluding the terrain. Entities that don't interact with the world should inherit from this class.
    '''

    def __init__(self, intelligence=False, coexistence=True, representation="E"):
        '''
        Here basic information about the entity is stored, such as its id, type, color, etc.
        '''
        self._id = uuid4()
        self.physical_properties = {}
        self.is_intelligent = intelligence
        self.coexistence = coexistence
        self.rep = representation

    def get_string_representation(self):
        ''' Devuelve la representación en string del objeto.
        '''
        return self.rep

    def get_property_value(self, property):
        return (property, self.physical_properties[property] if property in self.physical_properties else None)

    def get_entity_id(self):
        return str(self._id)

    def pass_time(self):
        pass


class Organism(
    Entity
):
    def __init__(self, dna_chain, representation="O", species="default"):
        '''
        This method initializes the organism with the given initial state. The initial state is a dictionary that contains
        the initial values of the properties of the organism. The id is a string that represents the id of the organism. The
        genetic potential is an integer that represents the maximum length of the dna chain.
        '''
        super().__init__(intelligence=True, coexistence=False, representation=representation)
        self.dna_chain = dna_chain
        self.perceptions = []
        self.actions = []
        self.knowledge = []
        self.species = species
        self.age = 0
        self._parse_dna()

    def _parse_dna(self):
        for gene in self.dna_chain:
            if gene.gen_type == "physical":
                for prop in gene.get_property():
                    self.physical_properties.update(prop)
            elif gene.gen_type == "perception":
                self.perceptions.extend(gene.get_property())
            elif gene.gen_type == "action":
                self.actions.extend(gene.get_property())

    def pass_time(self):
        # TODO: if the organism dies, it must drop its inventory
        self.age += 1
        floor = "grass"
        for info in self.knowledge:
            if "floor" in info.keys():
                floor = info["floor"]
                break
        # Check if the entity can stand in that floor
        match floor:
            case "water":
                if "fins" not in self.physical_properties.keys():
                    self.physical_properties["health"] -= 10
            case _:
                pass
        if 'health' in list(self.physical_properties.keys()):
            self.physical_properties["health"] -= 1
            if self.physical_properties["health"] <= 0:
                return False
        if 'hunger' in list(self.physical_properties.keys()):
            self.physical_properties["hunger"] -= 1
            if self.physical_properties["hunger"] <= 0:
                return False
        if "defending" in list(self.physical_properties.keys()):
            self.physical_properties["defending"] = False
        return True


class Food(Entity):
    def __init__(self, Nutrition=10, intelligence=False, coexistence=True, rep="F"):
        '''
        Here basic information about the entity is stored, such as its id, type, color, etc.
        '''
        super().__init__(representation=rep)
        self.physical_properties = {"edible": Nutrition}


class PackableFood(Entity):
    def __init__(self, Nutrition=5, intelligence=False, coexistence=True, rep="P"):
        '''
        Here basic information about the entity is stored, such as its id, type, color, etc.
        '''
        super().__init__(representation=rep)
        self.physical_properties = {"edible": Nutrition, "storable": True}


class RandomOrg(Organism, RandomBehavior):
    def __init__(self, dna_chain, representation="R", species = "default"):
        super().__init__(dna_chain, representation=representation, species = species)


class OpportunisticOrg(Organism, OpportunisticBehavior):
    def __init__(self, dna_chain, representation="O", species="robber"):
        super().__init__(dna_chain, representation=representation, species=species)


class Species:
    def __init__(self, identifier, organism_class, dna_chain, genetic_pool, genetic_potential, representation="O"):
        self.id = identifier
        self.organism_class = organism_class
        self.genetic_potential = genetic_potential
        self.representation = representation
        self.genetic_pool = genetic_pool
        if not genetic_pool.validate_chain(dna_chain, genetic_potential):
            raise ValueError(
                "The given dna chain is not valid for the given genetic pool")
        self.dna_chain = dna_chain

    def get_organism(self):
        dna_chain = []
        for gene in self.dna_chain:
            aux = self.genetic_pool.get_gene(gene)['gene']
            # FIXME: if an gene is not physical it wont have mutate() method
            if hasattr(aux, 'mutate'):
                dna_chain.append(aux.mutate())
            else:
                dna_chain.append(aux)
        org = self.organism_class
        return org(dna_chain, self.representation, self.id)

    def reproduction(self, organism, other_organism):
        if organism.species != other_organism.species:
            raise ValueError("The organisms must be of the same species")

        new_dna_chain = []
        organism1_dna = organism.dna_chain
        organism2_dna = other_organism.dna_chain
        organism1_age = organism.age
        organism2_age = other_organism.age
        age_sum = organism1_age + organism2_age

        for i in range(len(organism1_dna)):
            gene1 = organism1_dna[i]
            gene2 = organism2_dna[i]
            most_valuable = None
            if random.randint(0, age_sum) < organism1_age:
                most_valuable = gene1
            else:
                most_valuable = gene2
            if hasattr(most_valuable, 'mutate'):
                new_dna_chain.append(most_valuable.mutate())
            else:
                new_dna_chain.append(most_valuable)
        
    
        return self.organism_class(new_dna_chain, self.representation, self.id)

def mix(species, other_species, value, other_value):
    #TODO: AQUI FALTA COMPROBAR SI LAS DEPENDENCIAS DE UN GEN NO ESTAN EN EL ADN CUANDO SE AGREGAN
    #TODO: SI ADEMAS SE LE AGREGA EL VALOR AL GEN SERIA AUN MEJOR
    if other_species.genetic_pool != species.genetic_pool:
        raise ValueError("The species must have the same genetic pool")
    
    genetic_pool = species.genetic_pool
    new_identifier = '[' + species.id + other_species.id + ']'
    new_dna_chain = []
    current_genetic_cost = 0
    self_dna_copy = species.dna_chain.copy()
    other_dna_copy = other_species.dna_chain.copy()
    while current_genetic_cost < species.genetic_potential and (len(self_dna_copy) > 0 or len(other_dna_copy) > 0):
        new_gene = None
        if len(self_dna_copy) == 0:
            new_gene = other_dna_copy.pop(0)
            cost = genetic_pool.get_gene(new_gene)['genetic_cost']

            if current_genetic_cost + cost <= species.genetic_potential:
                new_dna_chain.append(new_gene)
                current_genetic_cost += cost

        elif len(other_dna_copy) == 0:
            new_gene = self_dna_copy.pop(0)
            cost = genetic_pool.get_gene(new_gene)['genetic_cost']

            if current_genetic_cost + cost <= species.genetic_potential:
                new_dna_chain.append(new_gene)
                current_genetic_cost += cost
        
        else:
            if random.randint(0, value + other_value) < value:
                new_gene = self_dna_copy.pop(0)
                cost = genetic_pool.get_gene(new_gene)['genetic_cost']

                if current_genetic_cost + cost < species.genetic_potential:
                    new_dna_chain.append(new_gene)
                    current_genetic_cost += cost
                    if new_gene in other_dna_copy:
                        other_dna_copy.remove(new_gene)
            else:
                new_gene = other_dna_copy.pop(0)
                cost = genetic_pool.get_gene(new_gene)['genetic_cost']

                if current_genetic_cost + cost <= species.genetic_potential:
                    new_dna_chain.append(new_gene)
                    current_genetic_cost += cost
                    if new_gene in self_dna_copy:
                        self_dna_copy.remove(new_gene)
    return Species(new_identifier, species.organism_class, new_dna_chain, species.genetic_pool, species.genetic_potential, species.representation)

def __check_gene_validity(species, dna_chain, gene_name):
    dependencies = species.genetic_pool.get_dependencies(gene_name)
    for gene in dna_chain:
        if gene.name in dependencies:
            return True
    return False

def __gene_in_chain(species, dna_chain, gene):
    for g in dna_chain:
        if g.name == gene.name:
            return True
    return False
        
