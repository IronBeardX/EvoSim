from typing import Callable
from uuid import uuid4


class Gene:
    def __init__(self, name, cost_fn: Callable, type: str = "default"):
        self.name = name
        self.id = uuid4()
        self.type: str = type
        self.get_cost = cost_fn

    def instantiate_gene(self):
        pass


class ActionGene(Gene):
    def __init__(self, name, action: str, mod_list: list, action_decision: list, cost_fn: Callable):
        super().__init__(name, cost_fn, "action")
        pass


class PerceptionGene(Gene):
    # TODO: how should i do gene modifiers
    def __init__(self, name, perception_action: str, mod_list: list[Callable], cost_fn: Callable):
        super().__init__(name, cost_fn, "perception")
        pass


class PhysicalGene(Gene):
    def __init__(self, name, mod_list: tuple | None, cost_fn):
        super().__init__(name, cost_fn, "physical")
        

# TODO: When creating a gene, parameters should be checked for correct formatting
