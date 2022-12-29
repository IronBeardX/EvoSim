from src.entity import *
from src.utils import *

class Organism(IntelligentEntity):
    def __init__(self, gene_pool:DirectedGraph, dna_chain:list[tuple[str, int]], id:str, genetic_potential:int) -> None:
        '''
        This method initializes the organism with the given initial state. The initial state is a dictionary that contains
        the initial values of the properties of the organism. The id is a string that represents the id of the organism. The
        genetic potential is an integer that represents the maximum length of the dna chain.
        '''
        self.gene_pool = gene_pool
        initial_state = self.gen_state_dna(dna_chain)
        super().__init__(initial_state["entity_state"], id)
        self.dna_chain = initial_state["dna_chain"]
        self.perception_filter:list[str] #TODO: How should this be implemented
        
    #TODO: what does this method returns? should reproduction be left for the simulation module ?
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

    def get_property_by_key(self, key:str) -> any:
        '''
        This method returns the value of the property with the given key
        '''
        pass        