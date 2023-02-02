
class Domain:
    """
    Esta clase define el dominio de valores que puede tener
    alguna variable.

    Ejemplos de dominios:
    - Los reales
    - Los enteros
    - Los strings de longitud 10
    - Los turnos de clase en forma de tuplas (dia, hora, conferencia)
    """

    def belong(self, value):
        """
        This function says if 'value' belongs to this Domain
        """
        pass

    def sample(self):
        """This function should give a random value of this `Domain`"""
        pass
