from ...problem.local_search_problem import LocalProblem
from ..local_search_algorithm import LocalSearchAlgorithm
from ..utils import *
import random
import math

class SimulatedAnnealing(LocalSearchAlgorithm):
    def __init__(self, problem: LocalProblem,
                 maximization=True,
                 temperature=100,
                 cooling_rate=0.9,
                 max_iterations=1000,):
        self.problem = problem
        self.maximization = maximization
        self.temperature = temperature
        self.cooling_rate = cooling_rate
        self.max_iterations = max_iterations
        self.fitness = lambda x: self.problem.fitness(x) * (1 if self.maximization else -1)

    def schedule(self, iteration: int):
        # This function has a slow cooling rate
        return self.temperature * self.cooling_rate ** iteration

    def search(self):
        current = self.problem.get_initial_state()
        current_temperature = self.temperature
        for i in range(self.max_iterations):
            current_temperature = self.schedule(i)
            if current_temperature == 0:
                return current
            neighbors = self.expand_state(current)
            if not neighbors:
                return current
            random_neighbor = random.choice(neighbors)
            # if self._is_better(best_neighbor, current):
            if self.fitness(random_neighbor) > self.fitness(current):
                current = random_neighbor
            else:
                if self.get_acceptance_probability(current, random_neighbor, current_temperature) > random.random():
                    current = random_neighbor

    def expand_state(self, state):
        """
        This function should return the neighbors of 'state'
        """
        actions = self.problem.get_actions(state)
        return [self.problem.result(state, action) for action in actions]

    def get_acceptance_probability(self, current, neighbor, temperature):
        return math.exp((self.problem.fitness(neighbor) - self.problem.fitness(current)) / temperature)
