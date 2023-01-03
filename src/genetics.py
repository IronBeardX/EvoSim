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

    @property
    def get_copy(self):
        return self.__class__(self.name, self.mutation_chance, self.gen_type, self.val_type, self.min, self.max, self.value, self.mutation_step)


# [ ]Physical Genes
# These genes gives the organism physical properties
class Health(PhysicalGene):
    def __init__(self, mutation_chance=0.5, min_val=1, max_val=100, value=100, mutation_step=1):
        super().__init__("health", mutation_chance, "physical",
                         "int", min_val, max_val, value, mutation_step)

    def mutate(self):
        new_val = self.value
        if random.random() < self.mutation_chance:
            value += random.randint(-self.mutation_step, self.mutation_step)
            if value < self.min:
                value = self.min
            if value > self.max:
                value = self.max
        return Health(self.name, self.mutation_chance, self.min, self.max, new_val, self.mutation_step)


class Hunger(PhysicalGene):
    def __init__(self, mutation_chance=0.5, min_val=1, max_val=100, value=50, mutation_step=1):
        super().__init__("hunger", mutation_chance, "physical",
                         "int", min_val, max_val, value, mutation_step)

    def mutate(self):
        new_val = self.value
        if random.random() < self.mutation_chance:
            value += random.randint(-self.mutation_step, self.mutation_step)
            if value < self.min:
                value = self.min
            if value > self.max:
                value = self.max
        return Hunger(self.name, self.mutation_chance, self.min, self.max, new_val, self.mutation_step)


class Legs(PhysicalGene):
    def __init__(self, mutation_chance=0.5, min_val=1, max_val=5, value=2, mutation_step=1):
        super().__init__("legs", mutation_chance, "physical",
                         "int", min_val, max_val, value, mutation_step)

    def mutate(self):
        new_val = self.value
        if random.random() < self.mutation_chance:
            value += random.randint(-self.mutation_step, self.mutation_step)
            if value < self.min:
                value = self.min
            if value > self.max:
                value = self.max
        return Legs(self.name, self.mutation_chance, self.min, self.max, new_val, self.mutation_step)


class Eye(PhysicalGene):
    def __init__(self, mutation_chance=0.5, min_val=1, max_val=5, value=2, mutation_step=1):
        super().__init__("eye", mutation_chance, "physical",
                         "int", min_val, max_val, value, mutation_step)

    def mutate(self):
        new_val = self.value
        if random.random() < self.mutation_chance:
            value += random.randint(-self.mutation_step, self.mutation_step)
            if value < self.min:
                value = self.min
            if value > self.max:
                value = self.max
        return Eye(self.name, self.mutation_chance, self.min, self.max, new_val, self.mutation_step)


class Arms(PhysicalGene):
    def __init__(self, mutation_chance=0.5, min_val=1, max_val=5, value=2, mutation_step=1):
        super().__init__("arms", mutation_chance, "physical",
                         "int", min_val, max_val, value, mutation_step)

    def mutate(self):
        new_val = self.value
        if random.random() < self.mutation_chance:
            value += random.randint(-self.mutation_step, self.mutation_step)
            if value < self.min:
                value = self.min
            if value > self.max:
                value = self.max
        return Arms(self.name, self.mutation_chance, self.min, self.max, new_val, self.mutation_step)


class Horns(PhysicalGene):
    def __init__(self, mutation_chance=0.5, min_val=1, max_val=50, value=2, mutation_step=1):
        super().__init__("horns", mutation_chance, "physical",
                         "int", min_val, max_val, value, mutation_step)

    def mutate(self):
        new_val = self.value
        if random.random() < self.mutation_chance:
            value += random.randint(-self.mutation_step, self.mutation_step)
            if value < self.min:
                value = self.min
            if value > self.max:
                value = self.max
        return Horns(self.name, self.mutation_chance, self.min, self.max, new_val, self.mutation_step)


class Smell(PhysicalGene):
    def __init__(self, mutation_chance=0.5, min_val=1, max_val=5, value=2, mutation_step=1):
        super().__init__("body_smell", mutation_chance, "physical",
                         "int", min_val, max_val, value, mutation_step)

    def mutate(self):
        new_val = self.value
        if random.random() < self.mutation_chance:
            value += random.randint(-self.mutation_step, self.mutation_step)
            if value < self.min:
                value = self.min
            if value > self.max:
                value = self.max
        return Smell(self.name, self.mutation_chance, self.min, self.max, new_val, self.mutation_step)


class Fins(PhysicalGene):
    def __init__(self, mutation_chance=0.5, min_val=0, max_val=4, value=2, mutation_step=1):
        super().__init__("fins", mutation_chance, "physical",
                         "int", min_val, max_val, value, mutation_step)

    def mutate(self):
        new_val = self.value
        if random.random() < self.mutation_chance:
            value += random.randint(-self.mutation_step, self.mutation_step)
            if value < self.min:
                value = self.min
            if value > self.max:
                value = self.max
        return Fins(self.name, self.mutation_chance, self.min, self.max, new_val, self.mutation_step)


class Nose(PhysicalGene):
    def __init__(self, mutation_chance=0.5, min_val=0, max_val=4, value=2, mutation_step=1):
        super().__init__("nose", mutation_chance, "physical",
                         "int", min_val, max_val, value, mutation_step)

    def mutate(self):
        new_val = self.value
        if random.random() < self.mutation_chance:
            value += random.randint(-self.mutation_step, self.mutation_step)
            if value < self.min:
                value = self.min
            if value > self.max:
                value = self.max
        return Nose(self.name, self.mutation_chance, self.min, self.max, new_val, self.mutation_step)

# [ ]Perception Genes
# These genes gives the organism perception actions
# Perception functions take modifiers from the physical traits of the organism


class PerceptionGene:
    def __init__(self, name, perception_func, gen_type="perception"):
        self.name = name
        self.perception_func = perception_func
        self.gen_type = gen_type

    def perceive(self):
        pass


class Smelling(PerceptionGene):
    def __init__(self):
        super().__init__("smelling")

    def perceive(self):
        pass


class VisionLinear(PerceptionGene):
    def __init__(self):
        super().__init__("vision", "PLACEHOLDER")  # TODO

    def perceive(self):
        pass


class VisionRadial(PerceptionGene):
    def __init__(self):
        super().__init__("vision", "PLACEHOLDER")  # TODO

    def perceive(self):
        pass

# [ ]Action Genes
# These genes gives the organism action abilities


class ActionGene:
    def __init__(self, name, gen_type="action"):
        self.name = name
        self.gen_type = gen_type

    def gen_act(self):
        pass

    def cost_func(self):
        pass


class Move(ActionGene):
    def __init__(self):
        super().__init__("move")  # TODO

    def gen_act(self, value):
        return [
            {"action": "move north"},
            {"action": "move south"},
            {"action": "move east"},
            {"action": "move west"}
        ]


class Eat(ActionGene):
    def __init__(self):
        super().__init__("eat")

    def gen_act(self):
        return [
            {"action": "eat"}
        ]


class Reproduce(ActionGene):
    def __init__(self):
        super().__init__("reproduce")

    def gen_act(self):
        return [
            {"action": "reproduce"}
        ]


class Duplicate(ActionGene):
    def __init__(self):
        super().__init__("duplicate")

    def gen_act(self):
        return [
            {"name": "duplicate"}
        ]


class Attack(ActionGene):
    def __init__(self):
        super().__init__("attack")

    def gen_act(self):
        return [
            {"action": "attack"}
        ]


class Defend(ActionGene):
    def __init__(self):
        super().__init__("defend")

    def gen_act(self):
        return [
            {"action": "defend"}
        ]


class Pick(ActionGene):
    def __init__(self):
        super().__init__("pick")

    def gen_act(self):
        return [
            {"action": "pick"}
        ]


class Swimming(ActionGene):
    def __init__(self):
        super().__init__("swimming")

    def gen_act(self):
        return [
            {"action": "swim north"},
            {"action": "swim south"},
            {"action": "swim east"},
            {"action": "swim west"}
        ]


'''
Genes dependencies:
    Legs: Move
    Arms: Pick, attack, defend
    Horns: Attack
    Nose: Smell
    Eye: Vision
'''
