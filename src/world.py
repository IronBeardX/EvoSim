from entity import *

class World:
    '''
    Basic class of the world, it contains information about the terrain and the entities that inhabit it. It's responsible for updating its state according to the actions of entities and events  that occur in the world. 
    '''

    def __init__(self) -> None:
        '''
        Here basic information about the world is settled, such as the available terrain types, and the world map itself. Information about basic laws of the world should also be settled with this method, such as if the world map is an array, a Cartesian plane, or if it is finite or infinite. Updating entities should be relegated to the simulation class.
        '''
        pass

    def trigger_event(self, event_id:str):
        '''
        This method is responsible for triggering events that occur in the world. The event_id is a string that represents the event that will be triggered. The event_id should be unique for each event. Events must be defined beforehand in the world class.
        '''
        pass

    def get_state(self) -> list[str]:
        '''
        This method returns the current state of the world. The state is a list of logical propositions that represent the current state of the world.
        '''
        pass

    def execute_action(self, action: str) -> None:
        '''
        This method executes the action that an entity has decided to take. The action is a string that represents the action that the entity will take. The action must be defined beforehand in the world class?
        '''
        pass

    def execute_interaction(self, interaction: list[str], emitter_entity_id: str, receiver_entity_id: str) -> None:
        '''
        This method executes the interaction that an entity has decided to have with another entity. The interaction is a string that represents the interaction that the entity will have.
        '''
        pass

    def update_state(self, influences: list[str]) -> None:
        '''
        This method updates the state of the world.
        '''
        pass

    #TODO: Think if entities states should be modeled by a dictionary or a list of propositions
    def get_entity_state(self, entity_id: str) -> list[str]:
        '''
        This method returns the state of an entity. The state is a list of logical propositions that represent the current state of the entity.
        '''
        pass

    def update_entity_state(self, entity_id: str, influences: list[str]) -> None:
        '''
        This method updates the state of an entity.
        '''
        pass

    def get_entity_position(self, entity_id: str) -> list[int]:
        '''
        This method returns the position of an entity. The position is a list of integers that represent the coordinates of the entity in the world.
        '''
        pass

    def update_entity_position(self, entity_id: str, position: list[int]) -> None:
        '''
        This method updates the position of an entity.
        '''
        pass

    def get_entity_orientation(self, entity_id: str) -> list[int]:
        '''
        This method returns the orientation of an entity. The orientation is a list of integers that represent the direction that the entity is facing.
        '''
        pass

    def update_entity_orientation(self, entity_id: str, orientation: list[int]) -> None:
        '''
        This method updates the orientation of an entity.
        '''
        pass

    def get_all_entities(self) -> list[Entity]:
        '''
        This method returns a list of all entities in the world.
        '''
        pass

# TODO: More functions will probably be added to this class as the project progresses.