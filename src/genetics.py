from uuid import uuid4
import random


class PhysicalGene:
    def __init__(self, name, mutation_chance=0.5, gen_type="physical", val_type="int", min_val=0, max_val=100, value=100, mutation_step=1):
        self.name = name
        self.mutation_chance = mutation_chance
        self.gen_type = gen_type
        self.val_type = val_type
        self.value = value
        self.min = min_val
        self.max = max_val
        self.mutation_step = mutation_step

    def get_property(self):
        return (self.name, self.value)

    def mutate(self):
        new_val = self.value
        if random.random() < self.mutation_chance:
            value += random.randint(-self.mutation_step, self.mutation_step)
            if value < self.min:
                value = self.min
            if value > self.max:
                value = self.max
        return __class__(self.name, self.mutation_chance, self.min, self.max, new_val, self.mutation_step)

    @property
    def get_copy(self):
        return self.__class__(self.mutation_chance, self.min, self.max, self.value, self.mutation_step)


# [ ] Physical Genes
# These genes gives the organism physical properties
class Health(PhysicalGene):
    def __init__(self, mutation_chance=0.5, min_val=1, max_val=100, value=100, mutation_step=1):
        super().__init__("health", mutation_chance, "physical",
                         "int", min_val, max_val, value, mutation_step)

    def get_property(self):
        return [{"health": self.value}]


class Hunger(PhysicalGene):
    def __init__(self, mutation_chance=0.5, min_val=1, max_val=100, value=50, mutation_step=1):
        super().__init__("hunger", mutation_chance, "physical",
                         "int", min_val, max_val, value, mutation_step)

    def get_property(self):
        return [{
            "hunger": self.value,
            "max hunger": self.value
            }]


class Legs(PhysicalGene):
    def __init__(self, mutation_chance=0.5, min_val=1, max_val=5, value=2, mutation_step=1):
        super().__init__("legs", mutation_chance, "physical",
                         "int", min_val, max_val, value, mutation_step)

    def get_property(self):
        return [{"legs": self.value}]


class Eye(PhysicalGene):
    def __init__(self, mutation_chance=0.5, min_val=1, max_val=5, value=2, mutation_step=1):
        super().__init__("eye", mutation_chance, "physical",
                         "int", min_val, max_val, value, mutation_step)

    def get_property(self):
        return [{"eye": self.value}]


class Arms(PhysicalGene):
    def __init__(self, mutation_chance=0.5, min_val=1, max_val=50, value=25, mutation_step=1):
        super().__init__("arms", mutation_chance, "physical",
                         "int", min_val, max_val, value, mutation_step)

    def get_property(self):
        return [
            {"arms": self.value},
            {"arms_defense": self.value},
            {"arms_attack": self.value},
            {"storage": []},
            {"defending": False}
        ]


class Horns(PhysicalGene):
    def __init__(self, mutation_chance=0.5, min_val=1, max_val=50, value=20, mutation_step=1):
        super().__init__("horns", mutation_chance, "physical",
                         "int", min_val, max_val, value, mutation_step)

    def get_property(self):
        return [{"horns_attack": self.value}]


class Smell(PhysicalGene):
    def __init__(self, mutation_chance=0.5, min_val=1, max_val=5, value=2, mutation_step=1):
        super().__init__("body_smell", mutation_chance, "physical",
                         "int", min_val, max_val, value, mutation_step)

    def get_property(self):
        return [{"smell": self.value}]


class Fins(PhysicalGene):
    def __init__(self, mutation_chance=0.5, min_val=0, max_val=4, value=2, mutation_step=1):
        super().__init__("fins", mutation_chance, "physical",
                         "int", min_val, max_val, value, mutation_step)

    def get_property(self):
        return [{"fins": self.value}]


class Nose(PhysicalGene):
    def __init__(self, mutation_chance=0.5, min_val=0, max_val=4, value=2, mutation_step=1):
        super().__init__("nose", mutation_chance, "physical",
                         "int", min_val, max_val, value, mutation_step)

    def get_property(self):
        return [{"nose": self.value}]


class Mouth(PhysicalGene):
    def __init__(self, mutation_chance=0.5, min_val=0, max_val=4, value=2, mutation_step=1):
        super().__init__("mouth", mutation_chance, "physical",
                         "int", min_val, max_val, value, mutation_step)

    def get_property(self):
        return [{"mouth": self.value}]

# [ ]Perception Genes
# These genes gives the organism perception actions
# Perception functions take modifiers from the physical traits of the organism


class PerceptionGene:
    def __init__(self, name, gen_type="perception"):
        self.name = name
        self.gen_type = gen_type

    def get_property(self):
        pass


class Smelling(PerceptionGene):
    def __init__(self):
        super().__init__("smelling")

    def get_property(self):
        return [
            "smelling"
        ]


class VisionRadial(PerceptionGene):
    def __init__(self):
        super().__init__("vision")

    def perceive(self):
        pass

    def get_property(self):
        return [
            "vision"
        ]

# [ ]Action Genes
# These genes gives the organism action abilities


class ActionGene:
    def __init__(self, name, gen_type="action"):
        self.name = name
        self.gen_type = gen_type

    def gen_act(self):
        pass

    def get_property(self):
        pass


class Move(ActionGene):
    def __init__(self):
        super().__init__("move")

    def get_property(self):
        return [
            {"name": "move north", "cost": 10},
            {"name": "move south", "cost": 10},
            {"name": "move east", "cost": 10},
            {"name": "move west", "cost": 10}
        ]


class Eat(ActionGene):
    def __init__(self):
        super().__init__("eat")

    def get_property(self):
        return [
            {"name": "eat", "cost": 10}
        ]


class Reproduce(ActionGene):
    def __init__(self):
        super().__init__("reproduce")

    def get_property(self):
        return [
            {"name": "reproduce", "cost": 10}
        ]


class Duplicate(ActionGene):
    def __init__(self):
        super().__init__("duplicate")

    def get_property(self):
        return [
            {"name": "duplicate", "cost": 10}
        ]


class Attack(ActionGene):
    def __init__(self):
        super().__init__("attack")

    def get_property(self):
        return [
            {"name": "attack", "cost": 10}
        ]


class Defend(ActionGene):
    def __init__(self):
        super().__init__("defend")

    def get_property(self):
        return [
            {"name": "defend", "cost": 10}
        ]


class Pick(ActionGene):
    def __init__(self):
        super().__init__("pick")

    def get_property(self):
        return [
            {"name": "pick", "cost": 10}
        ]


class Swimming(ActionGene):
    def __init__(self):
        super().__init__("swimming")

    def get_property(self):
        return [
            {"name": "swim north", "cost": 10},
            {"name": "swim south", "cost": 10},
            {"name": "swim east", "cost": 10},
            {"name": "swim west", "cost": 10}
        ]


'''
Genes dependencies:
    Legs: Move
    Arms: Pick, attack, defend
    Horns: Attack
    Nose: Smell
    Eye: Vision
'''
