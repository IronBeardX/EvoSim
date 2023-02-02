from ...local_search_algorithm import LocalSearchAlgorithm
from ....problem.local_search_problem import LocalProblem
from ...utils import *


class SteepestAscentHillClimbing(LocalSearchAlgorithm):
    """
    This class implements the Steepest Ascent Hill Climbing algorithm
    """

    def __init__(self, problem: LocalProblem,
                 maximization=True):
        super().__init__(problem, maximization)
        self.fitness = lambda x: self.problem.fitness(x) * (1 if self.maximization else -1)

    def search(self):
        """
        This function should implement the Simple Hill Climbing algorithm
        """
        current = self.problem.get_initial_state()
        while True:
            neighbors = self.expand_state(current)
            if not neighbors:
                return current
            best_neighbor = best_values(neighbors, 1, self.fitness) # check this
            # if self._is_better(best_neighbor, current):
            if self.fitness(best_neighbor) > self.fitness(current):
                current = best_neighbor
            else:
                return current

    def expand_state(self, state):
        """
        This function should return the neighbors of 'state'
        """
        actions = self.problem.get_actions(state)
        return [self.problem.result(state, action) for action in actions]
