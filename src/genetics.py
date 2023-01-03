from uuid import uuid4
import random


class Gene:
    def __init__(self, name, mutation_chance=0.5, gen_type="default", val_type="int", min_val=0, max_val=100, value=100, mutation_step=1):
        self.name = name
        self.mutation_chance = mutation_chance
        self.gen_type = gen_type
        self.val_type = val_type
        self.value = value
        self.min = min_val
        self.max = max_val
        self.mutation_step = mutation_step

    def get_property(self):
        return {self.name: self.value}


# [ ]Physical Genes
# These genes gives the organism physical properties
class Health(Gene):
    def __init__(self, mutation_chance=0.5, min_val=1, max_val=100, value=100, mutation_step=1):
        super().__init__("health", mutation_chance, "physical", "int", min_val, max_val, value, mutation_step)

    def mutate(self):
        new_val = self.value
        if random.random() < self.mutation_chance:
            value += random.randint(-self.mutation_step, self.mutation_step)
            if value < self.min:
                value = self.min
            if value > self.max:
                value = self.max
        return Health(self.name, self.mutation_chance, self.min, self.max, new_val, self.mutation_step)


class Legs(Gene):
    def __init__(self, mutation_chance=0.5, min_val=1, max_val=5, value=2, mutation_step=1):
        super().__init__("legs", mutation_chance, "physical", "int", min_val, max_val, value, mutation_step)

    def mutate(self):
        new_val = self.value
        if random.random() < self.mutation_chance:
            value += random.randint(-self.mutation_step, self.mutation_step)
            if value < self.min:
                value = self.min
            if value > self.max:
                value = self.max
        return Legs(self.name, self.mutation_chance, self.min, self.max, new_val, self.mutation_step)



class Eye(Gene):
    def __init__(self, mutation_chance=0.5, min_val=1, max_val=5, value=2, mutation_step=1):
        super().__init__("eye", mutation_chance, "physical", "int", min_val, max_val, value, mutation_step)

    def mutate(self):
        new_val = self.value
        if random.random() < self.mutation_chance:
            value += random.randint(-self.mutation_step, self.mutation_step)
            if value < self.min:
                value = self.min
            if value > self.max:
                value = self.max
        return Eye(self.name, self.mutation_chance, self.min, self.max, new_val, self.mutation_step)


class Arms(Gene):
    def __init__(self, mutation_chance=0.5, min_val=1, max_val=5, value=2, mutation_step=1):
        super().__init__("arms", mutation_chance, "physical", "int", min_val, max_val, value, mutation_step)

    def mutate(self):
        new_val = self.value
        if random.random() < self.mutation_chance:
            value += random.randint(-self.mutation_step, self.mutation_step)
            if value < self.min:
                value = self.min
            if value > self.max:
                value = self.max
        return Arms(self.name, self.mutation_chance, self.min, self.max, new_val, self.mutation_step)


class Horns(Gene):
    def __init__(self, mutation_chance=0.5, min_val=1, max_val=50, value=2, mutation_step=1):
        super().__init__("horns", mutation_chance, "physical", "int", min_val, max_val, value, mutation_step)

    def mutate(self):
        new_val = self.value
        if random.random() < self.mutation_chance:
            value += random.randint(-self.mutation_step, self.mutation_step)
            if value < self.min:
                value = self.min
            if value > self.max:
                value = self.max
        return Horns(self.name, self.mutation_chance, self.min, self.max, new_val, self.mutation_step)


class Smell(Gene):
    def __init__(self, mutation_chance=0.5, min_val=1, max_val=5, value=2, mutation_step=1):
        super().__init__("body_smell", mutation_chance, "physical", "int", min_val, max_val, value, mutation_step)

    def mutate(self):
        new_val = self.value
        if random.random() < self.mutation_chance:
            value += random.randint(-self.mutation_step, self.mutation_step)
            if value < self.min:
                value = self.min
            if value > self.max:
                value = self.max
        return Smell(self.name, self.mutation_chance, self.min, self.max, new_val, self.mutation_step)


class Fins(Gene):
    def __init__(self, mutation_chance=0.5, min_val=0, max_val=100, value=100, mutation_step=1):
        super().__init__("fins", mutation_chance, "physical", "int", min_val, max_val, value, mutation_step)

    def mutate(self):
        new_val = self.value
        if random.random() < self.mutation_chance:
            value += random.randint(-self.mutation_step, self.mutation_step)
            if value < self.min:
                value = self.min
            if value > self.max:
                value = self.max
        return Fins(self.name, self.mutation_chance, self.min, self.max, new_val, self.mutation_step)


class Nose(Gene):
    def __init__(self, mutation_chance=0.5, min_val=0, max_val=100, value=100, mutation_step=1):
        pass

# [ ]Perception Genes
# These genes gives the organism perception actions


class Smelling(Gene):
    pass


class Vision(Gene):
    pass

# [ ]Action Genes
# These genes gives the organism action abilities


class Move(Gene):
    pass


class Eat(Gene):
    pass


class Reproduce(Gene):
    pass


class Attack(Gene):
    pass


class Defend(Gene):
    pass


class Pick(Gene):
    pass


class Swimming(Gene):
    pass


'''
Genes dependencies:
    Legs: Move
    Arms: Pick, attack, defend
    Horns: Attack
    Nose: Smell
    Eye: Vision
'''
