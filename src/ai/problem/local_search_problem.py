from .problem import Problem
from .variable import Variable
from copy import deepcopy

class LocalProblem(Problem):
    def __init__(self, variables: list[Variable]):
        super().__init__(variables)

    def get_initial_state(self):
        """
        This function should return the initial state of the problem
        """
        return deepcopy(self._initial_state)

    def fitness(self, state: list[Variable]) -> float:
        pass

    def get_actions(self, state):
        """
        This function should return the actions aplicable to the 'state'
        """
        pass

    def result(self, state, action):
        """
        This function should return the state reached by applying 'action'
        in 'state'
        """
        pass

    def get_cost(self, state, action, state2):
        """
        This function should return the cost of doing 'action' in 'state'
        to reach 'state2'
        """
        pass

    def is_goal(self, state) -> bool:
        """
        This function should return True if 'state' is a goal state
        """
        pass