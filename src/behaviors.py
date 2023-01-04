import random


class Behavior:
    def __init__(self, pass_time):
        pass

    def decide_action(self, organism_state, world_state, action_options):
        pass


class RandomBehavior(Behavior):

    def decide_action(self, action_options):
        actions = []
        speed = 10
        action_time = 0
        while action_time < speed:
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
                    self.physical_properties["hunger"] -= action["cost"]
                    action_time += self.physical_properties["mouth"]
                    actions.append({"command": "eat"})
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
                    actions.append({"command": "attack", "value": attack})
                case "defend":
                    # TODO: Finish this
                    defense = 0
                    body_part = None
                    for defense_dealer in self.physical_properties.keys():
                        if "defense" in defense_dealer:
                            if defense < self.physical_properties[defense_dealer]:
                                defense = self.physical_properties[defense_dealer]
                                body_part = defense_dealer
                    self.physical_properties["hunger"] -= action["cost"]
                    action_time += self.physical_properties[body_part]
                case "pick":
                    self.physical_properties["hunger"] -= action["cost"]
                    action_time += self.physical_properties["arms"]
                    actions.append({"command": "pick"})
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
                    pass
        return actions

    def get_prop_by_name(self, name):
        for action in self.actions:
            if action["name"] == self.name:
                return action

    def pass_time(self):
        self.physical_properties["health"] -= 1
        self.physical_properties["hunger"] -= 1
        if self.physical_properties["health"] <= 0:
            return False
        if self.physical_properties["hunger"] <= 0:
            return False
        return True

    def receive_influences(self, influences_list):
        for influence in influences_list:
            match influence["name"]:
                case "attack":
                    if "defending" in self.physical_properties.keys():
                        self.physical_properties["health"] -= influence["value"] - \
                            self.physical_properties["defending"]
