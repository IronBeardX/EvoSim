from logger import *
from entity import *
from world import *

class Simulation:
    '''
    This class is responsible for controlling the flow of the simulation, determining when entities and world states should be updated, when events must be triggered, logging, defining and checking simulation goals, etc
    '''

    def __init__(self) -> None:
        '''
        This method initializes the simulation.
        '''
        pass

    def run(self) -> None:
        '''
        This method runs the simulation.
        '''
        pass

    def update(self) -> None:
        '''
        This method updates the simulation.
        '''
        pass

    def update_entities(self) -> None:
        '''
        This method updates the entities.
        '''
        pass

    def update_world(self) -> None:
        '''
        This method updates the world.
        '''
        pass

    def check_simulation_goal(self) -> bool:
        '''
        This method checks if the simulation goal has been reached.
        '''
        pass

    def check_episode_goal(self) -> bool:
        '''
        This method checks if the episode goal has been reached.
        '''
        pass

    def check_event(self, event_id: str) -> bool:
        '''
        This method checks if an event has occurred.
        '''
        pass

    def log(self, message: str) -> None:
        '''
        This method logs a message.
        '''
        pass

    def log_episode(self, episode: int, reward: float) -> None:
        '''
        This method logs an episode.
        '''
        pass

    def log_results(self, results: list[float]) -> None:
        '''
        This method logs the results of the simulation.
        '''
        pass

    def trigger_event(self, event_id: str) -> None:
        '''
        This method triggers an event.
        '''
        pass

    def modify_world(self, influences: list[str]) -> None:
        '''
        This method modifies the world.
        '''
        pass

    def change_world(self, world: World) -> None:
        '''
        This method changes the world.
        '''
        pass

    def modify_entity(self, entity_id: str, influences: list[str]) -> None:
        '''
        This method modifies an entity.
        '''
        pass

    def change_entity(self, entity_id: str, entity: Entity | None) -> None:
        '''
        This method changes or removes an entity.
        '''
        pass

    def add_entity(self, entity: Entity, position: any) -> None:
        '''
        This method adds an entity. to an already existing world.
        '''
        pass

# TODO: More functions will probably be added to this class as the project progresses. 
