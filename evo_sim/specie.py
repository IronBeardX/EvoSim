
class Specie:
    """This class is the base class for all living organism"""
    def __init__(self, dna, max_health: float, max_stamina: float) -> None:
        self.dna = dna
        self.max_health = self.health = max_health
        self.max_stamina = self.stamina = max_stamina

    def get_physical_characteristic(physical_characteristic: str):
        """This function should return the value of a physical
        characteristic like 'health', 'stamina', etc. All this characteristics"""
        pass

    def get_dna(self):
        """This should return the DNA.
        TODO: We should think if this should return a shallow or deep copy
        """
        return self.dna

    def get_actions(self):
        """This will return all the actions that this Specie can do. Looking to his DNA structure"""
        pass

    def get_sensors(self):
        """This will return all the sensors that this specie has. Looking to his DNA structure"""
        pass

    def get_state_cardinality(self) -> int:
        """This function returns an integer expressing the amount of variables of a state"""
        # TODO: Implement because this is common in all the species
        raise NotImplementedError()

    def create_state(self, world):
        """This function will create a state with the same amount that return `get_state_cardinality`"""
        pass
