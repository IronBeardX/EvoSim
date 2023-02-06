from .evo_world import *


class WorldGenerator:
    """Base class for all clases that generate worlds"""

    def generate_world() -> World:
        """This function returns a new world"""
        pass


class EvoWorldGenerator(WorldGenerator):
    """This class generates a world for the evolution simulation"""

    def __init__(self, height, width, terrain_types: list, terrain_dist, finite, world_actions=None, events=None):
        self.height = height
        self.width = width
        self.terrain_types = terrain_types
        self.terrain_dist = terrain_dist
        self.finite = finite
        self.world_actions = world_actions
        self.events = events

    def generate_world(self) -> EvoWorld:
        """This function returns a new evo world"""
        return EvoWorld(self.height,
                        self.width,
                        self.terrain_types,
                        self.terrain_dist,
                        self.finite,
                        self.world_actions,
                        self.events)
