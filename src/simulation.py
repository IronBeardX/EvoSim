from .world_generator import *

class Simulation:
    """Clase base para todas las simulaciones"""
    def __init__(self, episodes_number:int, steps_per_episode:int, world_generator: WorldGenerator):
        self.episodes_number = max(1, episodes_number)
        self.steps_per_episode = max(1, steps_per_episode)
        self.actual_episode = 0
        self.actual_step = 0
        self.world_generator = world_generator

    def reset(self):
        """This function reset the simulation state"""
        self.actual_episode = 0
        self.actual_step = 0

    def next_step(self, allow_next_episode:bool = False) -> bool:
        """This function compute the next step in the simulation for
        the current episode"""
        pass

    def advance_to(self, episode, step):
        """This function compute the simulation until the given episode
        and step"""
        pass
