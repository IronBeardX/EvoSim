from .evo_world import *
from .evo_entity import *
from .actions_sim import *
from .utils import *
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
import time


class SimActions:
    # TODO: Update this
    def attack(self, ent_id, other_id, value):
        # Check if the ids are correct:
        if (ent_id not in self.intelligent_entities) or (other_id not in self.intelligent_entities):
            return
        # Check if the entities are adjacent:
        if self.world.distance(ent_id, other_id) > 1:
            return

        other_entity = self.intelligent_entities[other_id]
        # influencing other entity
        other_entity.receive_influences([{"name": "damage", "value": value}])

    def pick(self, ent_id, item_id):
        # check if the ids are correct
        if item_id not in self.entities:
            return
        if ent_id not in self.intelligent_entities:
            return
        item = self.entities[item_id]
        entity = self.intelligent_entities[ent_id]
        # check if the entity is adjacent to the item:
        if self.world.distance(ent_id, item_id) > 1:
            return
        # check if the item is storable:
        if "storable" not in item.physical_properties:
            return
        # check if the entity has space to store the item:
        if ("storage" not in entity.physical_properties) or (len(entity.physical_properties["storage"]) > 0):
            return

        # store the item and remove it from the world:
        entity.receive_influences([{"name": "storage", "value": item_id}])
        self.banished_entities[item_id] = self.entities.pop(item_id)
        self.world.remove_entity(item_id)

    def eat(self, ent_id, food_id):
        # Check if the entity and the food exixts:
        if ent_id not in self.intelligent_entities:
            return
        if food_id not in self.entities:
            return
        entity = self.intelligent_entities[ent_id]
        food = self.entities[food_id]

        # Check if the food is edible:
        if "edible" not in food.physical_properties:
            return

        # Check if the entity has the food in its storage:
        if ("storage" in entity.physical_properties) and (food_id in entity.physical_properties["storage"]):
            # Remove the food from the storage:
            entity.physical_properties["storage"].remove(food_id)
        # Check if the entity is adjacent to the food:
        elif self.world.distance(ent_id, food_id) > 1:
            return

        entity.receive_influences(
            [{"name": "nutrients", "value": food.physical_properties["edible"]}])

        self.banished_entities[food_id] = self.entities.pop(food_id)
        self.world.remove_entity(food_id)

    def reproduce(self, ent_id, other_id):
        actor_entity = self.intelligent_entities[ent_id]
        try:
            other_entity = self.intelligent_entities[other_id]
        except:
            return

        # Check if the entities are adjacent:
        if self.world.distance(ent_id, other_id) > 1:
            return

        # Check if the entities are of the same species:
        if actor_entity.species != other_entity.species:
            return

        # getting the new position for the new entity
        new_pos = self.new_empty_pos(ent_id, other_id)

        if new_pos is None:
            return

        if len(self.intelligent_entities) >= 10:
            return
        # creating the new entity
        # getting the dna's and age
        actor_dna = actor_entity.dna_chain
        other_dna = other_entity.dna_chain
        actor_age = actor_entity.age
        other_age = other_entity.age
        species = actor_entity.species

        def generator():
            # selecting the value for each gene from the parents using fuzzy logic and the age of the parents
            # creating a normalized vector with the ages
            ages = np.array([actor_age, other_age])
            ages = ages / np.linalg.norm(ages)
            # creating the fuzzy logic system
            selection_space = [(ages[0], "actor"),
                               (ages[1] + ages[0], "other")]

            new_dna_chain = []
            for i in range(len(actor_dna)):
                new_dna_chain.append(
                    actor_dna[i] if random.random() < ages[0] else other_dna[i])
            return species(new_dna_chain, species=species)

        self.instantiate_entity(-1, new_pos, generator)

    def floor(self, ent_id):
        position = self.world.entities[ent_id].position
        return (position, self.world.get_terrain_type(position))

    def smell(self, ent_id, day, r):
        entities_list = self.entities_in_radius(ent_id, r)
        ent = self.intelligent_entities[ent_id]
        species = ent.species
        perception_list = []
        for entity, pos, distance in entities_list:
            other_species = "None"
            if entity.get_entity_id() in self.intelligent_entities:
                other_ent = entity
                other_species = other_ent.species
            if "smell" in entity.physical_properties:
                perception_list.append({
                    "entity": entity.get_entity_id(),
                    "smell": entity.physical_properties["smell"],
                    "position": pos,
                    "day": day,
                    "distance": distance,
                    "reproductive": species == other_species
                })
        return perception_list

    def see(self, ent_id, day, r):
        entities_list = self.entities_in_radius(ent_id, r)
        ent = self.intelligent_entities[ent_id]
        species = ent.species
        perception_list = []
        for entity, pos, distance in entities_list:
            other_species = "None"
            if entity.get_entity_id() in self.intelligent_entities:
                other_ent = entity
                other_species = other_ent.species
            entity_info = {
                "entity": entity.get_entity_id(),
                "day": day,
                "position": pos,
                "distance": distance,
                "reproductive": species == other_species
            }
            if "legs" in entity.physical_properties:
                entity_info["legs"] = entity.physical_properties["legs"]
            if "arms" in entity.physical_properties:
                entity_info["arms"] = entity.physical_properties["arms"]
            if "horns" in entity.physical_properties:
                entity_info["horns"] = entity.physical_properties["horns"]
            if "fins" in entity.physical_properties:
                entity_info["fins"] = entity.physical_properties["fins"]
            if "edible" in entity.physical_properties:
                entity_info["edible"] = entity.physical_properties["edible"]
            if "storage" in entity.physical_properties:
                entity_info["storage"] = len(
                    entity.physical_properties["storage"])
            if "storable" in entity.physical_properties:
                entity_info["storable"] = entity.physical_properties["storable"]
            perception_list.append(entity_info)
        perception_list.append(
            {"surroundings": self.world.terrain_r(ent_id, r)})
        return perception_list
