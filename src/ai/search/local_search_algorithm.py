from ..problem.local_search_problem import LocalProblem

class LocalSearchAlgorithm(object):

    def __init__(self, problem: LocalProblem, maximization=True):
        self.problem = problem
        self.maximization = maximization

    def search(self):
        """This method should implement be implemented by a specific local search algorithm"""
        pass

