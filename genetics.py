from typing import Callable
from uuid import uuid4

class Gene:
    def __init__(self, name, type:str = "default"):
        self.name = name
        self.id = uuid4()
        self.type:str = type

class ActionGene(Gene):
    def __init__(self, name, action:str, mod_list:list):
        super().__init__(name, "action")
        self.action = action
        self.mod_list = mod_list

class PerceptionGene(Gene):
    #TODO: how should i do gene modifiers
    def __init__(self, name, perception_action:str, mod_list:list):
        super().__init__(name, "perception")
        self.perception_action:str = perception_action
        self.mod_list:list = mod_list

class PhysicalGene(Gene):
    def __init__(self, name, posible_values:tuple|None):
        super().__init__(name, "physical")
        self.posible_values = posible_values
        
#TODO: When creating a gene, parameters should be checked for correct formatting