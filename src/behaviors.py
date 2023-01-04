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
            match action:
                case "move north":
                    self.physical_properties["hunger"] -= 5
                    action_time += self.physical_properties["legs"]
                    actions.append({"action": "move north"})
                case "move south":
                    self.physical_properties["hunger"] -= 5
                    action_time += self.physical_properties["legs"]
                    actions.append({"action": "move south"})
                case "move east":
                    self.physical_properties["hunger"] -= 5
                    action_time += self.physical_properties["legs"]
                    actions.append({"action": "move east"})
                case "move west":
                    self.physical_properties["hunger"] -= 5
                    action_time += self.physical_properties["legs"]
                    actions.append({"action": "move west"})
                case "eat":
                    self.physical_properties["hunger"] -= 1
                    action_time += self.physical_properties["mouth"]
                    actions.append({"action": "eat"})
                case "reproduce":
                    self.physical_properties["hunger"] -= 10
                    action_time += 5
                    actions.append({"action": "reproduce"})
                case "duplicate":
                    self.physical_properties["hunger"] -= 10
                    action_time += self.physical_properties["reproduction"]
                    actions.append({"action": "duplicate"})
                case "attack":
                    attack = 0
                    body_part = None
                    for damage_dealer in self.physical_properties.keys():
                        if "attack" in damage_dealer:
                            if attack < self.physical_properties[damage_dealer]:
                                attack = self.physical_properties[damage_dealer]
                                body_part = damage_dealer
                    self.physical_properties["hunger"] -= 5
                    action_time += self.physical_properties[body_part]
                    actions.append({"action": "attack", "value": attack})
                case "defend":
                    defense = 0
                    body_part = None
                    for defense_dealer in self.physical_properties.keys():
                        if "defend" in defense_dealer:
                            if defense < self.physical_properties[defense_dealer]:
                                defense = self.physical_properties[defense_dealer]
                                body_part = defense_dealer
                    self.physical_properties["hunger"] -= 5
                    action_time += self.physical_properties[body_part]
                    actions.append({"action": "defend", "value": defense})
                case _:
                    pass
                #TODO: Add swiming actions
        return actions

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
                        self.physical_properties["health"] -= influence["value"] - self.physical_properties["defending"]
