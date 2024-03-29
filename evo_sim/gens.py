class Gene:
    """This is the basic Gene from which all Genes inherit from"""
    
    def __init__(self, name, description = "Empty description"):
        self.name = name
        self.description = description

    def get_dependencies(self):
        """This is the method that gives the dependencies of the gene. For example if this gene
        where the Reproductive Gene, then it would return for example: the 'Sex Gene'"""
        pass

    def mutate(self):
        """This is the method that mutates the gene giving them new internal values"""
        pass

class PhysicalTrait(Gene):
    """All new Genes that inherit from this Gene can add new properties to an organism"""
    
    def get_new_physical_properties(self):
        """This is the method that gives the physical properties that this gene can add to
        a Specie. For example if this gene where the Reproductive Gene, then 3 properties
        could be added, like 'is_pregnant', 'pregnancy time' and 'time_to_give_birth'"""
        pass

    def update(self):
        """Todos los physical traits deben tener un update. En este update
        modifican las variables del organismo. Por ejemplo:
        - El hambre en el update debe modificar la variable hambre (aumentándola) y hacer que mientras esta avance la
        energía del organismo disminuya y que luego de alcanzado el máximo esta le quite toda la salud al organismo para que muera"""
        pass

class Sense(Gene):
    """All the genes that inherit from Sense should be genes that receive a World
    and ask the world for information surrounding the organism and from this information
    it extracts a subset of characteristics and gives them to the organism"""
    
    def give_dictionary_of_possible_perceptions(self):
        """
        This method returns a Dictionary where the key is a string given a
        name for the info returned and the value is an integer representing
        the amount of variables stored in that value. Example of key-value pairs:
        - 'position':2 -> This represents a position in a 2D space (number 2 reflects this)"""
        pass

    def give_percept(self, world):
        """This is the method that gives the organism the information that it needs
        to make a decision"""
        pass

class Action(Gene):
    """
    All the genes that inherit from Action should be genes that receive a World and execute an action
    """

    def is_world_compatible(self, world):
        """This is the method that checks if the world is compatible with the action"""
        pass

    def execute_action(self, world):
        """This is the method that executes the action"""
        pass
