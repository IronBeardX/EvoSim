# Actions


class Eat:
    def eat(self, entity_id, food_id):
        food = self.entities[food_id]
        nutrition = 0
        if "edible" in food.physical_properties:
            nutrition = food.physical_properties["edible"]
        return ({"command": "delete", "entity_id": food_id}, {"nutrition": nutrition})


class Reproduce:
    def reproduce(self, entity_id, other_id):
        pass


class Duplicate:
    def duplicate(self, entity_id):
        pass


class Attack:
    def attack(self, other_id, damage):
        self.entities[other_id].receive_influence({"damage": damage})


class Pick:
    def pick(self, entity_id, item_id):
        item = self.entities[item_id]
        if "packable" in item.physical_properties:
            return ({"command": "delete", "entity_id": item_id}, {"store": item_id})


# Perceptions

class Smelling:
    def smell(self, entity_id, radius):
        # TODO: Check world implementation of get entities in radius
        # TODO: when done, manhattan distance should be used here
        perception = []
        entities = self.world.see_r(entity_id, radius)
        for entity, position in entities:
            if "smell" in self.entities[entity].physical_properties:
                #entity id, posicion, prop
                #
                #
                #
                perception.append(
                    
                )



class Seeing:
    def see(self, entity_id):
        # TODO: Check world implementation of get entities in radius
        pass
