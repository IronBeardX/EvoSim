from .utils import *
from .genetics import *
from .behaviors import *


class Entity:
    '''
    Basic class of world inhabitants, it encompasses everything that exists in the world excluding the terrain. Entities that don't interact with the world should inherit from this class.
    '''

    def __init__(self, physical={}, intelligence = False, coexistence = True, representation = "E"):
        '''
        Here basic information about the entity is stored, such as its id, type, color, etc.
        '''
        self._id = uuid4()
        self.physical_properties = physical
        self.is_intelligent = intelligence
        self.coexistence = coexistence
        self.rep = representation

    def get_property_value(self, property):
        return (property, self.physical_properties[property] if property in self.physical_properties else None)

    def get_entity_id(self):
        return str(self._id)


class Organism(
    Entity,
    RandomBehavior
):
    def __init__(self, dna_chain):
        '''
        This method initializes the organism with the given initial state. The initial state is a dictionary that contains
        the initial values of the properties of the organism. The id is a string that represents the id of the organism. The
        genetic potential is an integer that represents the maximum length of the dna chain.
        '''
        super().__init__(intelligence = True, coexistence= False)
        self.dna_chain = dna_chain
        self.perceptions = []
        self.actions = []
        self._parse_dna()

    def _parse_dna(self):
        for gene in self.dna_chain:
            if gene.gen_type == "physical":
                for property in gene.get_property():
                    self.physical_properties.update(property)
            elif gene.gen_type == "perception":
                self.perceptions.extend(gene.get_property())
            elif gene.gen_type == "action":
                self.actions.extend(gene.get_property())
