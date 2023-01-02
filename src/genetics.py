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
        self.action = action
        self.mod_list = mod_list
        self.action_decision = action_decision

    # TODO: some actions make decisions in the moment of execution

    def instantiate_gene(self, mod_param_select: list):
        specific_mod_list = []
        for i in range(len(mod_param_select)):
            if len(self.mod_list) != 0:
                specific_mod_list.append(
                    self.mod_list[i](*mod_param_select[i]))
        gene_instance = {"name": self.name, "action": self.action,
                         "mod_list": specific_mod_list, "action_des": self.action_decision}
        return (gene_instance, self.get_cost(gene_instance))


class PerceptionGene(Gene):
    # TODO: how should i do gene modifiers
    def __init__(self, name, perception_action: str, mod_list: list[Callable], cost_fn: Callable):
        super().__init__(name, cost_fn, "perception")
        self.perception_action: str = perception_action
        self.mod_list: list = mod_list

    def instantiate_gene(self, mod_param_select: list):
        specific_mod_list = []
        for i in range(len(mod_param_select)):
            if len(self.mod_list) != 0:
                specific_mod_list.append(
                    self.mod_list[i](*mod_param_select[i]))
        gene_instance = {"name": self.name, "perception_action":
                         self.perception_action, "mod_list": specific_mod_list}
        return (gene_instance, self.get_cost(gene_instance))


class PhysicalGene(Gene):
    def __init__(self, name, mod_list: tuple | None, cost_fn):
        super().__init__(name, cost_fn, "physical")
        self.mod_list = mod_list

    def instantiate_gene(self, mod_param_select: list):
        specific_mod_list = []
        for i in range(len(mod_param_select)):
            if len(self.mod_list) != 0:
                specific_mod_list.append(
                    self.mod_list[i](*mod_param_select[i]))
        gene_instance = {"name": self.name, "mod_list": specific_mod_list}
        return (gene_instance, self.get_cost(gene_instance))

# TODO: When creating a gene, parameters should be checked for correct formatting
