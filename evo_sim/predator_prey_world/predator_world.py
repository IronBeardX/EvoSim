from ..world import World
from ..entity import Entity
import math
import numpy as np

class PredatorWorld(World):
    def __init__(self, width: int, height: int, max_allowed_species: int) -> None:
        # create a numpy matrix of Entities
        self.width = max(10, width)
        self.height = max(10, height)
        self.max_allowed_species = min(self.width * self.height - 50, max(0, max_allowed_species))
        self.world = np.empty((width, height))

    def add_entity(self, entity):
        raise NotImplementedError()

    def valid_entity(self, entity):
        # TODO: Finish this
        raise NotImplementedError()

    # Para los sensores
    def get_surrounding(self, position, radius):
        """This method returns a list of entities that are within a certain radius of the entity"""
        raise NotImplementedError()
