from src.entity import *


class World:
    '''
    Basic class of the world, it contains information about the terrain and the entities that inhabit it. It's responsible
    for updating its state according to the actions of entities and events  that occur in the world. 
    '''
    # What type should this be ?

    def __init__(self, world_map: any, terrain_types: list[tuple[any, str]], map_type: str, finite: bool = True) -> None:
        '''
        Here basic information about the world is settled, such as the available terrain types, and the world map itself.
        Information about basic laws of the world should also be settled with this method, such as if the world map is an 
        array, a Cartesian plane, or if it is finite or infinite. Updating entities should be relegated to the simulation 
        class.
        '''
        self.world_map = world_map
        self.finite = finite
        self.terrain_types = terrain_types
        self.map_type = map_type
        self.event_list = []
        # TODO: Representation must be here
        self.entities: dict[str, MapEntityInfo] = {}
        '''
        The entities dictionary contains information about the entities relevant to the world. The key is the entity id and
        the value is a MapEntityInfo object that contains information about the entity.
        '''

    def is_valid_position(self, position: tuple) -> bool:
        '''
        This method checks if a position is valid in the world.
        '''
        pass

    # [ ]
    def add_event(self, event_id: str, event: any) -> None:
        '''
        This method adds an event to the world.
        '''
        self.event_list.append((event_id, event))

    # [ ]
    def get_terrain_type_in_position(self, position: tuple) -> str:
        '''
        This method returns the terrain type of a position in the world.
        '''
        pass

    # [ ]
    def trigger_event(self, event_id: str):
        '''
        This method is responsible for triggering events that occur in the world. The event_id is a string that represents 
        the event that will be triggered. The event_id should be unique for each event. Events must be defined beforehand in 
        the world class.
        '''
        pass

    # [ ]
    def get_state(self) -> list[str]:
        '''
        This method returns the current state of the world. The state is a list of logical propositions that represent the 
        current state of the world.
        '''
        pass

    # [ ]
    def execute_action(self, action: str) -> None:
        '''
        This method executes the action that an entity has decided to take. The action is a string that represents the action 
        that the entity will take. The action must be defined beforehand in the world class?
        '''
        pass

    # [ ]
    def execute_interaction(self, interaction: list[str], emitter_entity_id: str, receiver_entity_id: str) -> None:
        '''
        This method executes the interaction that an entity has decided to have with another entity. The interaction is a string 
        that represents the interaction that the entity will have.
        '''
        pass

    # [ ]
    def update_state(self, influences: list[str]) -> None:
        '''
        This method updates the state of the world.
        '''
        pass

    # [ ]
    # TODO: Think if entities states should be modeled by a dictionary or a list of propositions
    def get_entity_state(self, entity_id: str) -> list[str]:
        '''
        This method returns the state of an entity. The state is a list of logical propositions that represent the current state 
        of the entity.
        '''
        pass

    # [ ]
    def update_entity_state(self, entity_id: str, influences: list[str]) -> None:
        '''
        This method updates the state of an entity.
        '''
        pass

    # [ ]
    def get_entity_position(self, entity_id: str) -> list[int]:
        '''
        This method returns the position of an entity. The position is a list of integers that represent the coordinates of the 
        entity in the world.
        '''
        pass

    # [ ]
    def update_entity_position(self, entity_id: str, new_position: tuple) -> None:
        '''
        This method updates the position of an entity.
        '''
        self.entities[entity_id].position = new_position

    # [ ]
    def get_entity_orientation(self, entity_id: str) -> list[int]:
        '''
        This method returns the orientation of an entity. The orientation is a list of integers that represent the direction 
        that the entity is facing.
        '''
        pass

    # [ ]
    def update_entity_orientation(self, entity_id: str, orientation: tuple) -> None:
        '''
        This method updates the orientation of an entity.
        '''
        self.entities[entity_id].orientation = orientation

    # [ ]
    def get_all_entities(self) -> list[Entity]:
        '''
        This method returns a list of all entities in the world.
        '''
        pass


class MapEntityInfo:
    '''
    This is an utility class for containerizing entities properties needed for world functions 
    '''

    def __init__(self, position: tuple, orientation: tuple, representation_priority: int, can_coexist: bool, positioning_rules, string_rep: str) -> None:
        '''
        This method initializes the entity properties.

        @param position: The position of the entity in the world
        @param orientation: The orientation of the entity in the world
        @param representation_priority: The priority of the entity representation in the world
        @param can_coexist: If the entity can coexist with other entities
        @param positioning_rules: The positioning rules of the entity in the world. Describes, for example, in which terrains the entity
        can be positioned.
        '''
        
        self.position = position
        self.orientation = orientation
        self.representation_priority = representation_priority
        self.can_coexist = can_coexist
        self.representation = string_rep
