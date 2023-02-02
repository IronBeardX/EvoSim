from ..population_search import PopulationSearch
from ...problem.problem import Problem
from ...problem.variable import Variable
from ..utils import *
import random
from typing import Callable

def random_single_point_crossover(parent1: list, parent2: list) -> list[list]:
    """
    This function will return the children of the parents 'parent1' and 'parent2'
    using the single point crossover
    """
    if len(parent1) != len(parent2):
        raise Exception("The parents must have the same length")
    # get random point
    point = random.randint(0, len(parent1) - 1)
    # create children
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return [child1, child2]

def roulette_selection(problem: Problem, population: list[list], k: int) -> list[list]:
    """
    This function will return the best k values of the list 'values'
    """
    # calculate fitness
    # fitness = [sum(x) for x in population]
    fitness = [problem.fitness(x) for x in population]
    # calculate probability
    probability = [x / sum(fitness) for x in fitness]
    # get best k values
    return random.choices(population, probability, k=k)


class GeneticAlgorithm(PopulationSearch):
    """
    This class implements the Genetic Algorithm
    """

    def __init__(self, problem: Problem,
                maximization=True,
                population_size: int = 20,
                generations: int = 100,
                selection_function: Callable[[Problem, list[list], int], list[list]] = roulette_selection,
                mutation_rate: float = 0.1,
                crossover_function: Callable[[list, list], list[list]] = random_single_point_crossover,
                elite_size: int = 1
                ):
        super().__init__(problem, maximization, population_size, generations)
        self.selection_function = selection_function
        self.mutation_rate = mutation_rate
        self.crossover_function = crossover_function
        self.elite_size = clamp(elite_size, 0, population_size - 1)

    def search(self):
        """
        This function should implement the Genetic Algorithm
        """
        population = self.generate_population()
        for i in range(self.generations):
            # BUG: Fix this because when population_size - elite_size is odd then it will throw an exception
            # select the best individuals
            selected = self.selection_function(self.problem, population, self.population_size - self.elite_size)
            # create the next generation
            population = self.create_next_generation(selected)
            # add the elite
            population = self.add_elite(population, selected)
            # mutate the population
            population = self.mutate_population(population)

    def create_next_generation(self, selected: list[list[Variable]]) -> list[list[Variable]]:
        """
        This function will create the next generation
        """
        next_generation = []
        for i in range(0, len(selected), 2):
            # get parents
            parent1 = selected[i]
            parent2 = selected[i + 1]
            # crossover
            children = self.crossover_function(parent1, parent2)
            # add children to the next generation
            next_generation += children
        return next_generation

    def generate_population(self) -> list[list]:
        """
        This function will generate a random population
        """
        population = []
        for i in range(self.population_size):
            population.append([x.domain.sample() for x in self.problem.variables])
        return population

    def random_mutation(self, chromosome: list[Variable], mutation_rate: float) -> list[Variable]:
        """
        This function will mutate the values of 'values' with the probability 'mutation_rate'
        """
        for i in range(len(chromosome)):
            if random.random() < mutation_rate:
                # chromosome[i].set_value(random.choice(chromosome[i].domain.values))
                chromosome[i].set_value(chromosome[i].domain.sample())
        return chromosome
