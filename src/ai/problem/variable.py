from problem.domain import Domain

class Variable:
    """
    This class represents a variable in a problem
    """
    def __init__(self, name:str, domain:Domain) -> None:
        """
        This variable will be created with a random value of the domain"""
        self._name = name
        self._domain = domain
        self._value = self._domain.sample()

    @property
    def name(self):
        """Returns the name of the variable"""
        return self._name

    @property
    def domain(self):
        """Returns the Domain of the variable"""
        return self._domain

    def set_value(self, value):
        """This function will try to set the value to this variable.
        However, if the value doesn't belong to the domain it will return false
        and the variable will not be modified"""
        if not self._domain.belong(value):
            return False
        self._value = value
        return True

    @property
    def get_value(self):
        """
        This will return the value of the variable"""
        return self._value
        