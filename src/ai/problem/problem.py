from .variable import Variable
from .domain import Domain

class Problem:
    """
    Esta clase define un problema que contiene una serie de variables
    """
    def __init__(self, variables: list[Variable]):
        self._variables: list[Variable] = variables
        self._domains: list[Domain] = [variable.domain for variable in variables]
        self._initial_state = [variable.get_value for variable in variables]

    def get_random_variables(self):
        """
        This function should return a random state of the problem
        """
        return [domain.sample() for domain in self._domains]

    def fitness(self, state: list) -> float:
        """
        This function should return the fitness of 'state', where 'state' is a list of variables in the search space
        of this specific problem.\n
        'Fitness' should be a function that give greater outputs for better states.\n
        'state' es una lista de valores posibles para las variables del problema
        """
        pass

    def get_variables(self):
        return self._variables

    def is_valid(self, state):
        """
        This function should return True if 'state' is a valid state
        """
        pass

    def __str__(self):
        """
        This function should return a string representation of the problem
        """
        pass