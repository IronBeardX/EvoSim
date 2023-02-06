from ...gens import *

class EyesGene(PhysicalTrait):
    def __init__(self, range):
        super().__init__('Eyes')
        self.range = range

    def get_new_physical_properties(self):
        return {"vision_range": self.range}


    