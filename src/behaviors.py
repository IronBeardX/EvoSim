import random
import math

class Brain:
    '''
    The knowledge will be a list of bidimensional vectors for each goal. Each of these vectors will have the following format:

    | A | B | C | D | E | A1 | A2 | A3 | A4 |
    | 0 | 0 | 0 | 0 | 0 | 0  | 0  | 0  | 0  |
    | 0 | 0 | 0 | 0 | 0 | 0  | 0  | 0  | 0  |
    | 0 | 0 | 0 | 0 | 0 | 0  | 0  | 0  | 0  |
    | 0 | 0 | 0 | 0 | 0 | 0  | 0  | 0  | 0  |

    The first letters represent different information inferred from the perception, for example:
    A: The entity is alive
    B: There are allied entities nearby
    C: There are enemy entities nearby
    D: There are neutral entities nearby
    E: There is food nearby
    The values are boolean?

    The A's represent the available actions for the entity, for example:
    A1: The entity can move north
    A2: The entity can attack
    A3: The entity can eat
    A4: The entity can reproduce
    If the values are boolean then this would mean that this action have helped the entity to achieve the goal in the past.
    We could also use a number to represent the amount of times that this action has helped the entity to achieve the goal or
    if we could quantify how much has an action helped the entity to achieve the goal this could be represented by this number.

    Actions will be a list of all the available actions for the entity and deductions a dictionary with the name and the function that
    generates the deductions from the perception.
    '''
    def __init__(self, actions = None, deductions = None, knowledge = {}, goals = None):
        self.knowledge = knowledge
        self.goals = goals
        self.deductions = deductions
        self.actions = actions

    def decide_action(self, organism, age = 0, time = 0, perception = 0):
        perceptions_vector = self.vectorized_perceptions()

    def get_perceptions(self, organism):
        print('getting perceptions')
        perceptions = []
        for perception in organism.perceptions:
            match perception:
                case "smelling":
                    perceptions.append({"command": "smell", "parameters": [
                                       organism.physical_properties["nose"]]})
                case "vision":
                    perceptions.append({"command": "see", "parameters": [
                                       organism.physical_properties["eye"]]})
                case _:
                    print(perception + " not found")
        return perceptions

    def update_knowledge(self, organism,  new_knowledge):
        return
        for information in new_knowledge:
            self.update_info(information)

    def vectorized_perceptions(self, organism):
        pass

    def update_info(self, new_info):
        return
        if "entity" in list(new_info.keys()):
            entity_id = new_info["entity"]
            for old_info in self.knowledge:
                if ("entity" in old_info) and entity_id == old_info["entity"]:
                    old_info.update(new_info)
                    return
            self.knowledge.append(new_info)
        if "floor" in list(new_info.keys()):
            for old_info in self.knowledge:
                if ("floor" in old_info):
                    old_info.update(new_info)
                    return
            self.knowledge.append(new_info)
        if "surroundings" in list(new_info.keys()):
            for old_info in self.knowledge:
                if ("surroundings" in old_info):
                    old_info.update(new_info)
                    return
            self.knowledge.append(new_info)

    def receive_influences(self, influences_list):
        print("receiving influences")
        return
        for influence in influences_list:
            match influence["name"]:
                case "damage":
                    defense = 0
                    if "defending" in self.physical_properties.keys() and self.physical_properties["defending"]:
                        # find max defense in body
                        body_part = None
                        for defense_dealer in self.physical_properties.keys():
                            if "defense" in defense_dealer:
                                if defense < self.physical_properties[defense_dealer]:
                                    defense = self.physical_properties[defense_dealer]
                                    body_part = defense_dealer
                    self.physical_properties["health"] -= influence["value"] - defense
                    if self.physical_properties["health"] <= 0:
                        self.physical_properties["health"] = 0
                case "storage":
                    self.physical_properties["storage"].append(
                        influence["value"])
                case "nutrients":
                    if self.physical_properties["hunger"] + influence["value"] > self.physical_properties["max hunger"]:
                        self.physical_properties["hunger"] = self.physical_properties["max hunger"]
                    else:
                        self.physical_properties["hunger"] += influence["value"]
                case _:
                    raise Exception("Influence not found")


class Evaluators:
    def __init__(self, goal):
        self.goal = goal

    def evaluate(self, knowledge, perception):
        raise NotImplementedError()
