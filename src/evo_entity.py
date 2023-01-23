from .utils import *
from .genetics import *
from .behaviors import *


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
    def __init__(self, dna_chain, representation="R"):
        super().__init__(dna_chain, representation=representation)


class OpportunisticOrg(Organism, OpportunisticBehavior):
    def __init__(self, dna_chain, representation="O", species="robber"):
        super().__init__(dna_chain, representation=representation, species = species)
