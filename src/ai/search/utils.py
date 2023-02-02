from ..problem import Variable
# import callable
from typing import Callable

def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)

def best_values(values: list[Variable],
                k:int,
                fitness_function: Callable[[list[Variable]], float],
                ):
    """
    This function will return the best k values of the list 'values'
    """
    return sorted(values, key=fitness_function)[:k]

def set_values(values: list[Variable], new_values: list):
    """
    This function will set the values of 'values' to the values of 'new_values'
    """
    if len(values) != len(new_values):
        return False
    for i in range(len(values)):
        # check if value belongs to domain
        if not values[i].domain.belong(new_values[i]):
            return False
        values[i].set_value(new_values[i].get_value)
    return True