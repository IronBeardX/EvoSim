import random


class Behavior:
    def decide_action(self, organism_state, world_state, action_options):
        pass


class RandomBehavior(Behavior):

    def get_perceptions(self):
        perceptions = []
        for perception in self.perceptions:
            match perception:
                case "smelling":
                    perceptions.append({"command": "smell", "parameters": [
                                       self.physical_properties["nose"]]})
                case "vision":
                    perceptions.append({"command": "see", "parameters": [
                                       self.physical_properties["eye"]]})
                case _:
                    print(perception + " not found")
        return perceptions

    def update_knowledge(self, new_knowledge):
        for information in new_knowledge:
            self.update_info(information)

    def update_info(self, new_info):
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

    def decide_action(self, perceptions, day, time=10):
        actions = []
        action_time = 0
        while action_time < time:
            action = random.choice(self.actions)
            match action["name"]:
                case "move north":
                    self.physical_properties["hunger"] -= action["cost"]
                    action_time += self.physical_properties["legs"]
                    actions.append({"command": "move north"})
                case "move south":
                    self.physical_properties["hunger"] -= action["cost"]
                    action_time += self.physical_properties["legs"]
                    actions.append({"command": "move south"})
                case "move east":
                    self.physical_properties["hunger"] -= action["cost"]
                    action_time += self.physical_properties["legs"]
                    actions.append({"command": "move east"})
                case "move west":
                    self.physical_properties["hunger"] -= action["cost"]
                    action_time += self.physical_properties["legs"]
                    actions.append({"command": "move west"})
                case "eat":
                    random_ent = self.rand_ent()
                    if random_ent != "none":
                        self.physical_properties["hunger"] -= action["cost"]
                        action_time += self.physical_properties["mouth"]
                        actions.append(
                            {"command": "eat", "parameters": [random_ent]})
                case "reproduce":
                    self.physical_properties["hunger"] -= action["cost"]
                    action_time += 5
                    actions.append({"command": "reproduce"})
                case "duplicate":
                    self.physical_properties["hunger"] -= action["cost"]
                    action_time += 5
                    actions.append({"command": "duplicate"})
                case "attack":
                    attack = 0
                    body_part = None
                    for damage_dealer in self.physical_properties.keys():
                        if "attack" in damage_dealer:
                            if attack < self.physical_properties[damage_dealer]:
                                attack = self.physical_properties[damage_dealer]
                                body_part = damage_dealer
                    self.physical_properties["hunger"] -= action["cost"]
                    action_time += self.physical_properties[body_part]
                    objective = self.rand_ent()
                    actions.append(
                        {"command": "attack", "parameters": [objective, attack]})
                case "defend":
                    defense = 0
                    body_part = None
                    for defense_dealer in self.physical_properties.keys():
                        if "defense" in defense_dealer:
                            if defense < self.physical_properties[defense_dealer]:
                                defense = self.physical_properties[defense_dealer]
                                body_part = defense_dealer
                    self.physical_properties["hunger"] -= action["cost"]
                    action_time += self.physical_properties[body_part]
                    self.physical_properties["defending"] = True
                case "pick":
                    random_ent = self.rand_ent()
                    if random_ent != "none":
                        self.physical_properties["hunger"] -= action["cost"]
                        action_time += self.physical_properties["arms"]
                        actions.append(
                            {"command": "eat", "parameters": [random_ent]})
                case "swim north":
                    self.physical_properties["hunger"] -= action["cost"]
                    action_time += self.physical_properties["fins"]
                    actions.append({"command": "swim north"})
                case "swim south":
                    self.physical_properties["hunger"] -= action["cost"]
                    action_time += self.physical_properties["fins"]
                    actions.append({"command": "swim south"})
                case "swim east":
                    self.physical_properties["hunger"] -= action["cost"]
                    action_time += self.physical_properties["fins"]
                    actions.append({"command": "swim east"})
                case "swim west":
                    self.physical_properties["hunger"] -= action["cost"]
                    action_time += self.physical_properties["fins"]
                    actions.append({"command": "swim west"})
                case _:
                    raise Exception("Action not found")
        self.knowledge = []
        return actions

    def rand_ent(self):
        entity_list = []
        for info in self.knowledge:
            if "entity" in info.keys():
                entity_list.append(info["entity"])
        return random.choice(entity_list) if len(entity_list) > 0 else "none"

    def pass_time(self, name):
        floor = "grass"
        for info in self.knowledge:
            if "floor" in info.keys():
                floor = info["floor"]
                break
        # Check if the entity can stand in that floor
        match floor:
            case "water":
                if "fins" not in self.physical_properties.keys():
                    self.physical_properties["health"] -= 10
            case _:
                if "legs" not in self.physical_properties.keys():
                    self.physical_properties["health"] -= 10

        self.physical_properties["health"] -= 1
        self.physical_properties["hunger"] -= 1
        if self.physical_properties["health"] <= 0:
            return False
        if self.physical_properties["hunger"] <= 0:
            return False
        if "defending" in list(self.physical_properties.keys()):
            self.physical_properties["defending"] = False
        return True

    def receive_influences(self, influences_list):
        for influence in influences_list:
            match influence["name"]:
                case "damage":
                    if "defending" in self.physical_properties.keys() and self.physical_properties["defending"]:
                        # find max defense in body
                        defense = 0
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


class RobberBehavior(RandomBehavior):
    def decide_action(self, perceptions, day, time=10):
        pass


class GluttonyBehavior(Behavior):
    def decide_action(self, perceptions, day, time=10):
        pass


class FighterBehavior(Behavior):
    def decide_action(self, perceptions, day, time=10):
        pass


class LoverBehavior(Behavior):
    def decide_action(self, perceptions, day, time=10):
        pass
