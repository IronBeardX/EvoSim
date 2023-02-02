from ..problem.problem import Problem
from ..problem.variable import Variable
from .utils import *
from typing import Callable


class PopulationSearch(object):
    """
    This is the base class for all population search algorithms
    """

    def __init__(self, problem: Problem, maximization=True, population_size: int = 20, generations: int = 100):
        """
        :param problem: The problem to be solved
        :param maximization: True if the problem is a maximization problem, False otherwise
        :param population_size: The size of the population. This will be clamped in the range [2, 10000]
        :param generations: The number of generations to be evaluated
        """
        self.problem = problem
        self.maximization = maximization
        self.fitness = lambda x: self.problem.fitness(x) * (1 if self.maximization else -1)
        self.population_size = clamp(population_size, 2, 10000)
        self.generations = generations

    def search(self):
        """This method should implement be implemented by a specific population search algorithm"""
        pass
