from uuid import uuid4

class Gene:
    def __init__(self, name, type:str = "default"):
        self.name = name
        self.id = uuid4()
        self.type:str = type

class ActionGene(Gene):
    def __init__(self, name, value):
        super().__init__(self, name, "action")

class PerceptionGene(Gene):
    def __init__(self, name, perception_action:str, mod_list:list):
        super().__init__(self, name, "perception")
        self.perception_action:str = perception_action
        self.mod_list:list = mod_list

class PhysicalGene(Gene):
    def __init__(self, name, posible_values:tuple|None):
        super().__init__(self, name, "physical")
        self.posible_values = posible_values
        
#TODO: When creating a gene, parameters should be checked for correct formatting