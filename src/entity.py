from uuid import uuid4
from src.utils import *

class Entity:
    pass

class IntelligentEntity(Entity):
    '''
    This class is for Entities that can actively interact with the world
    '''
    def __init__(self, physical, actions, perceptions) -> None:
        super().__init__(physical)
        self.actions = actions
        self.perceptions = perceptions
        self.knowledge = {}
        

    #region World-Entity interaction

    def percept(self, world_sate: list[str]) -> list[str]:
        '''
        This method filters the world state to only include the information that is relevant to the entity. The world state is a list of logical propositions which defines it's current state.
        '''
        pass

    def decide_action(self, world_state: list[str]) -> str:
        '''
        This method determines the action that the entity will take based on the world state. The world state is a list of logical propositions which defines it's current state. The action is a string that represents the action that the entity will take. The world then is responsible for executing the action.
        '''
        pass

    def update_state(self, influences: list[str]) -> None:
        '''
        This method updates the state of the entity based on the influences that it receives from the world. The influences are a list of logical propositions that represent the changes that the world has made to the entity.
        '''
        pass

    #endregion

    #region Entity-Entity interaction

    def perceive_entity(self, entity_state: list[str]) -> list[str]:
        '''
        This method filters the entity state to only include the information that is relevant to the entity. The entity state is a list of logical propositions which defines it's current state.
        '''
        pass

    def decide_interaction(self, entity_state: list[str]) -> str:
        '''
        This method determines the interaction that the entity will have with another entity based on the entity state. The entity state is a list of logical propositions which defines it's current state. The interaction is a string that represents the interaction that the entity will have. The world then is responsible for executing the interaction.
        '''
        pass

    def update_entity_state(self, influences: list[str]) -> None:
        '''
        This method updates the state of the entity based on the influences that it receives from another entity. The influences are a list of logical propositions that represent the changes that the entity has made to the entity.
        '''
        pass

    #endregion

# TODO: More functions will probably be added to this class as the project progresses.