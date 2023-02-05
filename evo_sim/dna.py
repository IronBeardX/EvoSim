from gens import *
from typing import Set

class DNA:
    """This class represent the DNA of an Organism"""
    
    def __init__(self, genes: list[Gene]):
        """This is the constructor of the DNA class. It takes a list of genes and it decomposes it into
        a set of physical traits, senses and actions genes. Whenever you inherit from this you should call it
        with the super() method"""
        if not self.is_valid(genes):
            raise Exception("The DNA is not valid")
        self.genes = genes
        """This is the list of genes that the organism has"""
        physicals, senses, actions = self.decompose_dna(genes)
        self.physicals = physicals
        """This are all the physical traits that the organism has"""
        self.senses = senses
        """This are all the senses that the organism has"""
        self.actions = actions
        """This are all the actions that the organism can do"""

    def is_valid(self, dna: list[Gene]) -> bool:
        """This method checks if all the genes in the DNA have their dependencies included"""
        pass

    def decompose_dna(self, dna: list[Gene]) -> tuple[Set[PhysicalTrait], Set[Sense], Set[Action]]:
        """
        This method decompose the DNA into a set of physical traits, senses and actions
        """
        physicals = set()
        senses = set()
        actions = set()
        for gene in dna:
            if isinstance(gene, PhysicalTrait):
                physicals.add(gene)
            elif isinstance(gene, Sense):
                senses.add(gene)
            elif isinstance(gene, Action):
                actions.add(gene)
        return physicals, senses, actions

    def is_compatible(self, dna: list[Gene]):
        """This method checks if the DNA is compatible with the DNA of another Organism.\n
        This could be useful for example when mating.\n
        Two DNAs could be compatible not only for having the same genes but also for having a specific
        subset of genes that are compatible with each other. The idea is allowing that a certain organism
        could belong to different sets of species. For example, a human could be a member of the species
        'Human' and also a member of the species 'Mammal'"""
        pass
