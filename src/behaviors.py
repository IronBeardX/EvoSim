import random


class Behavior:
    def decide_action(self, day, time):
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

    def decide_action(self, day, time=10):
        actions = []
        action_time = 0
        while action_time < time:
            action = random.choice(self.actions)
            match action["name"]:
                # TODO: the actions in each case should be in methods for easier usage
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

    def _edible_ent_in_knowledge(self):
        # this method returns all the edible entities in the knowledge
        edible_ents = []
        for info in self.knowledge:
            if "edible" in info.keys():
                edible_ents.append(info)
        return edible_ents

    def _non_edible_ent_in_knowledge(self):
        # this method returns all the non edible entities in the knowledge
        non_edible_ents = []
        for info in self.knowledge:
            if "edible" not in info.keys() and "entity" in info.keys():
                non_edible_ents.append(info)
        return non_edible_ents

    def _fuzzy_goal_selector(self, goal):
        # TODO: return the priority with the new normalized valor
        current_goal = "none"
        normalized_goal_vector = []
        total = 0
        for g in goal:
            total += g["priority"]
        for g in goal:
            normalized_goal_vector.append(g["priority"] / total)

        relative_frequency = []
        for i in range(len(goal)):
            relative_frequency.append(0)
            for j in range(i + 1):
                relative_frequency[i] += normalized_goal_vector[j]

        random_number = random.random()
        for i in range(len(goal)):
            if random_number <= relative_frequency[i]:
                current_goal = goal[i]
                break
        return current_goal


class OpportunisticBehavior(RandomBehavior):
    def decide_action(self, day, time=10):
        # This will be a behavior that will try to take the food, and eat it when far from other entities
        # this will be implemented with an algorithm similar to Simulated annealing(but not exactly) that will try to find the best path to the food
        # and will measure risk reward of each action based on hunger, distance to food and distance to other entities and will fight only if
        # the reward is greater than the risk.

        actions = []

        # First we will determine our current goal from reproduction, food, fighting or exploring

        # Checking how hungry are we
        hungry_level = None
        if self.physical_properties["hunger"] < 10:
            hungry_level = "famished"
        elif self.physical_properties["hunger"] < 25:
            hungry_level = "very hungry"
        elif self.physical_properties["hunger"] < 50:
            hungry_level = "hungry"
        elif self.physical_properties["hunger"] >= 50:
            hungry_level = "not hungry"
        elif self.physical_properties["hunger"] >= 75:
            hungry_level = "satisfied"
        elif self.physical_properties["hunger"] >= 90:
            hungry_level = "full"

        # Getting all the food in the knowledge and if there is any food
        any_food = False
        # If theres food nearby information like its position and distance will be in this variable
        food_in_sight = []
        for food in self._edible_ent_in_knowledge():
            any_food = True
            food_in_sight.append(food)

        # Getting all the non food entities in the knowledge and if there is any entity
        any_entity = False
        reproductive_entity = False
        # If theres entities nearby information like its position, distance, their storage and if they are available for reproduction will be in this variable
        entities_in_sight = []
        for entity in self._non_edible_ent_in_knowledge():
            any_entity = True
            entities_in_sight.append(entity)
            # TODO: chech if "reproductive" is the correct key
            if entity["reproductive"] == True:
                reproductive_entity = True

        # Now we will determine our current goals and how badly we want to achieve them
        goal = []
        # Food goal priority will be lowered if we have food in the storage
        if "storage" in self.physical_properties.keys():
            stored_food = int(len(self.physical_properties["storage"]) > 0)

        # If we are famished we will try to get food as soon as possible
        if hungry_level == "famished":
            goal.append({"goal": "food", "priority": 100})
        # If we are very hungry we will try to get food as soon as possible or eat if we have food in the storage
        elif hungry_level == "very hungry":
            goal.append({"goal": "food", "priority": 80 - stored_food * 20})
        elif hungry_level == "hungry":
            goal.append({"goal": "food", "priority": 60 - stored_food * 20})
        elif hungry_level == "not hungry":
            goal.append({"goal": "food", "priority": 40 - stored_food * 20})
        elif hungry_level == "satisfied":
            goal.append({"goal": "food", "priority": 20 - stored_food * 20})
        elif hungry_level == "full":
            goal.append({"goal": "food", "priority": 1 - stored_food})
        # TODO: think about time between reproductions
        # reproduction urgency will depend on how much time has passed since the simulation started (day)
        # the more time it passes, the more the urgency will increase

        # If we are not hungry we will try to reproduce
        if hungry_level != "famished" and hungry_level != "very hungry":
            goal.append({"goal": "reproduction", "priority": 1 + day})

        # With the goal list we will determine the most urgent goal using fuzzy logic
        current_goal = "none" if len(
            goal) <= 0 else self._fuzzy_goal_selector(goal)
        # Now we will determine the best action to achieve our current goal using simulated annealing with the priority of the goal as the temperature
        # and the reward of each action as the energy
        actions.extend(self._simulated_annealing(current_goal, day, any_food, food_in_sight, any_entity, entities_in_sight, reproductive_entity, time, 10))

    def _simulated_annealing(self, current_goal, day, any_food, food_in_sight, any_entity, entities_in_sight, reproductive_entity, time, max_iterations):
        # This method will return a list of actions to achieve the current goal using simulated annealing
        # The reward of each "state" will be the distance to the food or the reproductive entity
        # The risk of each "state" will be the distance to the other entities in the final position
        # The "state" refereed earlier is a list of actions

        # First we will determine the temperature
        temperature = current_goal["priority"]

        # First we generate an initial state
        match current_goal["goal"]:
            case "reproduction":
                pass
            case "food":
                pass

        # Next we generate variations of this state and change it depending on the temperature and
        # the values of both states




class GluttonyBehavior(Behavior):
    def decide_action(self, perceptions, day, time=10):
        pass


class FighterBehavior(Behavior):
    def decide_action(self, perceptions, day, time=10):
        pass


class LoverBehavior(Behavior):
    def decide_action(self, perceptions, day, time=10):
        pass


class ExplorerBehavior(Behavior):
    def decide_action(self, perceptions, day, time=10):
        pass
