from problem.variable import Variable
from problem.domain import Domain
from problem.problem import Problem
# from problem.local_search_problem import LocalSearchProblem
from search.population.genetic import GeneticAlgorithm
import numpy as np
import random

def print_board(state: list[Variable], size: int = 8):
    board = np.zeros((size, size))
    for i in range(size):
        board[state[i]][i] = 1
    print(board)

class QueensDomain(Domain):
    def __init__(self, size:int = 8):
        """Size is the size of the board. Default is 8, for the 8 queens problem"""
        self._size = size

    def belong(self, value):
        return value >= 0 and value < self._size

    def sample(self):
        return random.randint(0, self._size - 1)

class QueensProblem(Problem):
    def __init__(self, size:int = 8):
        """Size is the size of the board. Default is 8, for the 8 queens problem"""
        self._size = size
        domain = QueensDomain(size)
        self._variables = [Variable(f"Queen {i}", domain) for i in range(size)]
        self._domains = [variable.domain for variable in self._variables]
        self._initial_state = [variable.get_value for variable in self._variables]

    def fitness(self, state: list) -> float:
        """
        This function should return the fitness of 'state', where 'state' is a list of variables in the search space
        of this specific problem
        """
        # generate a board of size x size
        board = np.zeros((self._size, self._size))
        # place the queens in the board
        # later, verify the number of pair of queens that are attacking each other
        # then return that number
        for i in range(self._size):
            board[state[i]][i] = 1
        # count the number of queens that are attacking each other
        count = 0
        for i in range(self._size):
            for j in range(self._size):
                if board[i][j] == 1:
                    # check if there is another queen in the same row
                    for k in range(j + 1, self._size):
                        if board[i][k] == 1:
                            count += 1
                    # check if there is another queen in the same column
                    for k in range(i + 1, self._size):
                        if board[k][j] == 1:
                            count += 1
                    # check if there is another queen in the diagonal
                    for k in range(1, self._size):
                        if i + k < self._size and j + k < self._size:
                            if board[i + k][j + k] == 1:
                                count += 1
                        if i - k >= 0 and j - k >= 0:
                            if board[i - k][j - k] == 1:
                                count += 1
                        if i + k < self._size and j - k >= 0:
                            if board[i + k][j - k] == 1:
                                count += 1
                        if i - k >= 0 and j + k < self._size:
                            if board[i - k][j + k] == 1:
                                count += 1
        return count

genetic_search = GeneticAlgorithm(QueensProblem(8), population_size=100, generations=1000, mutation_rate=0.1, elite_size=1)
genetic_search.search()
