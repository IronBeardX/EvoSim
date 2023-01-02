from .utils import *
from .genetics import *


class Entity:
    '''
    Basic class of world inhabitants, it encompasses everything that exists in the world excluding the terrain. Entities that don't interact with the world should inherit from this class.
    '''

    def __init__(self, physical: list = []) -> None:
        '''
        Here basic information about the entity is stored, such as its id, type, color, etc.
        '''
        self.physical_properties = physical
        self._id = uuid4()

    def get_property_value(self, property: str) -> any:
        return self.physical_properties[property] if property in self.physical_properties else None

    def get_entity_id(self) -> str:
        return str(self._id)


class Organism(Entity):
    def __init__(self, gene_pool: DirectedGraph, dna_chain, genetic_potential: int) -> None:
        '''
        This method initializes the organism with the given initial state. The initial state is a dictionary that contains
        the initial values of the properties of the organism. The id is a string that represents the id of the organism. The
        genetic potential is an integer that represents the maximum length of the dna chain.
        '''
        super().__init__()
        self.genetic_potential = genetic_potential
        self.gene_pool = gene_pool
        self.actions = []
        self.perceptions = []
        self.knowledge = {}
        self.dna_chain = dna_chain
        self.gen_state_from_dna(dna_chain)

    def gen_state_from_dna(self, dna_chain):
        '''
        This method generates the initial state of the organism based on the given dna chain. The dna chain is a list of
        tuples that contains the id and the strength of the gene. The initial state is a dictionary that contains the initial
        values of the properties of the organism.
        '''
        initial_state = []
        for gene_id in dna_chain.keys():
            gene = self.gene_pool.get_node_data(gene_id)
            instantiated_gene = gene.instantiate_gene(dna_chain[gene_id])
            if gene.type == "action":
                self.actions.append(instantiated_gene)
            elif gene.type == "perception":
                self.perceptions.append(instantiated_gene)
            elif gene.type == "physical":
                self.physical_properties.append(instantiated_gene)
        pass

    # TODO: what does this method returns? should reproduction be left for the simulation module ?
    def reproduce(self, other_dna, recombination_function) -> list[tuple[str, int]]:
        '''
        Generates an initial state for creating another instance of the Organism
        '''
        pass

    def percept(self, world_sate: list[str]) -> list[str]:
        '''
        This method filters the world state to only include the information that is relevant to the entity. The world 
        state is a list of logical propositions which defines it's current state.
        '''
        pass

    def decide_action(self, world_state: list[str]) -> str:
        '''
        This method determines the action that the entity will take based on the world state. The world state is a list
        of logical propositions which defines it's current state. The action is a string that represents the action that the 
        entity will take. The world then is responsible for executing the action.
        '''
        pass

    def update_state(self, influences: list[str]) -> None:
        '''
        This method updates the state of the entity based on the influences that it receives from the world. The influences 
        are a list of logical propositions that represent the changes that the world has made to the entity.
        '''
        pass

    def update_perception_filter(self) -> None:
        '''
        This method updates the perception filter of the entity based of its dna chain
        '''
        pass

    def update_available_actions(self) -> None:
        '''
        This method updates the available actions of the entity based of its dna chain
        '''
        pass

    def get_property_by_key(self, key: str) -> any:
        '''
        This method returns the value of the property with the given key
        '''
        pass


class TestOrganism(Organism):
    '''
    The difference between this class and the Organism class is that this one will receive a predefined list
    of actions it will execute in sequence rather that deciding which it will execute
    '''

    def __init__(self, gene_pool: DirectedGraph, dna_chain: list[tuple[str, int]], id: str, genetic_potential: int, actions: list[str]) -> None:
        '''
        This method initializes the organism with the given initial state. The initial state is a dictionary that contains
        the initial values of the properties of the organism. The id is a string that represents the id of the organism. The
        genetic potential is an integer that represents the maximum length of the dna chain.
        '''
        self.actions = actions
        self.action_pointer = 0
        super().__init__(gene_pool, dna_chain, id, genetic_potential)

    def decide_action(self, world_state: list[str]) -> str:
        '''
        This method determines the action that the entity will take based on the world state. The world state is a list
        of logical propositions which defines it's current state. The action is a string that represents the action that the 
        entity will take. The world then is responsible for executing the action.
        '''
        action = self.actions[self.action_pointer]
        self.action_pointer += 1
        return action
