import random
import math


class Behavior:
    def decide_action(self, day, time):
        raise NotImplementedError()


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
        if "surroundings" in list(new_info.keys()):
            for old_info in self.knowledge:
                if ("surroundings" in old_info):
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
                            {"command": "pick", "parameters": [random_ent]})
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
        entities_with_food = False
        # If theres entities nearby information like its position, distance, their storage and if they are available for reproduction will be in this variable
        entities_in_sight = []
        for entity in self._non_edible_ent_in_knowledge():
            any_entity = True
            entities_in_sight.append(entity)
            # TODO: check if "reproductive" is the correct key
            if entity["reproductive"] == True:
                reproductive_entity = True
            if "storage" in entity:
                if entity["storage"] > 0:
                    entities_with_food = True

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
        # TODO: remove after finished
        actions.extend(self._simulated_annealing(entities_with_food, current_goal, day, any_food,
                       food_in_sight, any_entity, entities_in_sight, reproductive_entity, time, 10))
        return actions

    def _simulated_annealing(self, entities_with_food, current_goal, day, any_food, food_in_sight, any_entity, entities_in_sight, reproductive_entity, time, max_iterations):
        # This method will return a list of actions to achieve the current goal using simulated annealing
        # The reward of each "state" will be the distance to the food or the reproductive entity
        # The risk of each "state" will be the distance to the other entities in the final position
        # The "state" refereed earlier is a list of actions

        # First we will determine the temperature
        temperature = current_goal["priority"] / 10

        # First we generate an initial state
        initial_state = []
        match current_goal["goal"]:
            case "reproduction":
                if "eye" in self.physical_properties.keys():
                    surroundings = None
                    for info in self.knowledge:
                        if "surroundings" in info.keys():
                            surroundings = info["surroundings"]
                            break
                    actions, value, new_pos = self._get_state_reproduction(
                        time, any_entity, entities_in_sight, reproductive_entity, surroundings)
                    initial_state = (value, new_pos)
                else:
                    actions, value, new_pos = self._get_state_reproduction(
                        time, entities_with_food, any_food, food_in_sight, any_entity, entities_in_sight)
                    initial_state = (value, new_pos)
            case "food":
                if "eye" in self.physical_properties.keys():
                    # getting the surroundings
                    surroundings = None
                    for info in self.knowledge:
                        if "surroundings" in info.keys():
                            surroundings = info["surroundings"]
                            break
                    actions, value, new_pos = self._get_state_food(
                        time, entities_with_food, any_food, food_in_sight, any_entity, entities_in_sight, surroundings)
                    initial_state = (value, new_pos)
                else:
                    actions, value, new_pos = self._get_state_food(
                        time, entities_with_food, any_food, food_in_sight, any_entity, entities_in_sight)
                    initial_state = (value, new_pos)

            # Now we will generate a new state and actions list:
            # If the new state is better than the initial state we will accept it
            # If the new state is worse than the initial state we will accept it with a probability depending on the temperature
            # If the new state is the same as the initial state we will accept it
            # We will repeat this process until we reach the maximum number of iterations or the temperature is 0
            # The temperature will decrease by 1 every iteration
            # The temperature will be the priority of the goal
            # We will return the actions list of the best state

        for i in range(max_iterations):
            if temperature <= 0:
                break
            # Generating a new state
            new_state = initial_state
            match current_goal["goal"]:
                case "reproduction":
                    if "eye" in self.physical_properties.keys():
                        actions, value, new_pos = self._get_state_reproduction(
                            time, any_entity, entities_in_sight, reproductive_entity, surroundings, previous_state=new_state, iteration=i)
                        new_state = (value, new_pos)
                    else:
                        actions, value, new_pos = self._get_state_reproduction(
                            time, entities_with_food, any_food, food_in_sight, any_entity, entities_in_sight, previous_state=new_state, iteration=i)
                        new_state = (value, new_pos)
                case "food":
                    if "eye" in self.physical_properties.keys():
                        actions, value, new_pos = self._get_state_food(
                            time, entities_with_food, any_food, food_in_sight, any_entity, entities_in_sight, surroundings, previous_state=new_state, iteration=i)
                        new_state = (value, new_pos)
                    else:
                        actions, value, new_pos = self._get_state_food(
                            time, entities_with_food, any_food, food_in_sight, any_entity, entities_in_sight, previous_state=new_state, iteration=i)
                        new_state = (value, new_pos)

            # if the new state value is -1 it means that the state is not valid
            if new_state[0] == -1:
                continue
            # If the new state is better than the initial state we will accept it
            if new_state[0] > initial_state[0]:
                initial_state = new_state
            # If the new state is worse than the initial state we will accept it with a probability depending on the temperature
            elif new_state[0] < initial_state[0]:
                if random.random() < math.exp((new_state[0] - initial_state[0]) / temperature):
                    initial_state = new_state
            # If the new state is the same as the initial state we will accept it
            else:
                initial_state = new_state

            # Decreasing the temperature
            temperature -= 1
        return actions

    def _get_state_food(self, time, ent_w_food, any_food, food_in_sight, any_entity, entities_in_sight, surroundings=None, previous_state=None, iteration=0):
        # This method will return a list of actions to get food
        # If there is food in sight it will return a list of actions to get to the food
        # If there is no food in sight it will return a list of actions to explore the surroundings
        # If there is no previous state it will take the food a try to move to another position where the amount of entities is minimal
        # If there is a previous state the new state will be a variation of the previous state
        entities_in_sight_pos = self._curate_entities_positions(
            entities_in_sight)
        # getting position from the knowledge
        current_pos = None
        for info in self.knowledge:
            if "floor" in info.keys():
                current_pos = info["position"]
                break

        if previous_state:
            if any_food and len(self.physical_properties["storage"]) == 0:
                # If there is food in sight we will try to get to it
                # We will get the i-st closest food
                closest_food = self._order_by_proximity(food_in_sight)
                if len(closest_food) <= iteration:
                    closest_food = closest_food[len(closest_food) - 1]
                else:
                    closest_food = closest_food[iteration]
                # Now we will get the actions to get to the food
                action_time, current_pos, actions = self._get_actions_to_position(
                    current_pos, 0, time, closest_food["position"], entities_in_sight_pos, surroundings)

                # Next we will try to pick up the food or eat it
                if action_time < time:
                    if "storable" in closest_food and closest_food["storable"]:
                        actions.append(
                            {"command": "pick", "parameters": [closest_food["entity"]]})
                        action_time += self.physical_properties["arms"]
                    else:
                        actions.append(
                            {"command": "eat", "parameters": [closest_food["entity"]]})
                        action_time += self.physical_properties["mouth"]

                # Now we will try to move to a position where the amount of entities is minimal
                if action_time < time:
                    action_time, current_pos, new_actions = self._get_actions_to_minimal_entities(
                        current_pos, action_time, time, entities_in_sight, entities_in_sight_pos, surroundings)
                    actions.extend(new_actions)

                state_value = self._get_ents_in_pos_radius(
                    entities_in_sight, entities_in_sight_pos, current_pos, self.physical_properties["eye"])
                return actions, state_value, action_time

            if len(self.physical_properties["storage"]) > 0:
                # If we have food we will try to get to a position where the amount of entities is minimal
                actions_time, current_pos, actions = self._get_actions_to_minimal_entities(
                    current_pos, 0, time, entities_in_sight, entities_in_sight_pos, surroundings)

                if actions_time < time:
                    actions.append({"command": "eat", "parameters": [
                                   self.physical_properties["storage"][0]]})
                    actions_time += self.physical_properties["mouth"]
                state_value = self._get_ents_in_pos_radius(
                    entities_in_sight, entities_in_sight_pos, current_pos, self.physical_properties["eye"])
                return actions, state_value, actions_time

            if ent_w_food:
                # If there is an entity with food we will try to get to it
                # We will get the i-st closest entity with food
                closest_ent = self._order_by_proximity(ent_w_food)[iteration]
                # Now we will get the actions to get to the entity
                action_time, current_pos, actions = self._get_actions_to_position(
                    current_pos, 0, time, closest_ent["position"], entities_in_sight_pos, surroundings)

                # Next we will attack this entity
                if action_time < time:
                    # getting the body part with highest attack
                    body_part = "none"
                    current_attack = 0
                    for part in self.physical_properties:
                        if "attack" in part:
                            body_part = part.split("_")[0]
                            if self.physical_properties[part] > current_attack:
                                current_attack = self.physical_properties[part]
                    actions.append(
                        {"command": "attack", "parameters": [closest_ent["entity"], current_attack]})
                    action_time += self.physical_properties[body_part]

                # Now we will try to move to a position where the amount of entities is minimal
                if action_time < time:
                    action_time, current_pos, new_actions = self._get_actions_to_minimal_entities(
                        current_pos, action_time, time, entities_in_sight, entities_in_sight_pos, surroundings)
                    actions.extend(new_actions)

                state_value = self._get_ents_in_pos_radius(
                    entities_in_sight, entities_in_sight_pos, current_pos, self.physical_properties["eye"])
                return actions, state_value, action_time

            else:
                # If there is no food in sight we will try to explore the surroundings
                action_time, current_pos, actions = self._get_actions_to_minimal_entities(
                    current_pos, 0, time, entities_in_sight, entities_in_sight_pos, surroundings)
                state_value = self._get_ents_in_pos_radius(
                    entities_in_sight, entities_in_sight_pos, current_pos, self.physical_properties["eye"])
                return actions, state_value, action_time
        else:
            if any_food and len(self.physical_properties["storage"]) == 0:
                # If there is food in sight we will try to get to it
                # We will get the i-st closest food
                closest_food = self._order_by_proximity(food_in_sight)[
                    iteration]

                # Now we will get the actions to get to the food
                action_time, current_pos, actions = self._get_actions_to_position(
                    current_pos, 0, time, closest_food["position"], entities_in_sight_pos, surroundings)

                # Next we will try to pick up the food or eat it
                if action_time < time:
                    if "storable" in closest_food and closest_food["storable"]:
                        actions.append(
                            {"command": "pick", "parameters": [closest_food["entity"]]})
                        action_time += self.physical_properties["arms"]
                    else:
                        actions.append(
                            {"command": "eat", "parameters": [closest_food["entity"]]})
                        action_time += self.physical_properties["mouth"]

                # Now we will try to move to a position where the amount of entities is minimal
                if action_time < time:
                    action_time, current_pos, new_actions = self._get_actions_to_minimal_entities(
                        current_pos, action_time, time, entities_in_sight, entities_in_sight_pos, surroundings)
                    actions.extend(new_actions)

                state_value = self._get_ents_in_pos_radius(
                    entities_in_sight, entities_in_sight_pos, current_pos, self.physical_properties["eye"])
                return actions, state_value, action_time

            if len(self.physical_properties["storage"]) > 0:
                # If we have food we will try to get to a position where the amount of entities is minimal
                actions_time, current_pos, actions = self._get_actions_to_minimal_entities(
                    current_pos, 0, time, entities_in_sight, entities_in_sight_pos, surroundings)

                if actions_time < time:
                    actions.append({"command": "eat", "parameters": [
                                   self.physical_properties["storage"][0]]})
                    actions_time += self.physical_properties["mouth"]
                state_value = self._get_ents_in_pos_radius(
                    entities_in_sight, entities_in_sight_pos, current_pos, self.physical_properties["eye"])
                return actions, state_value, actions_time

            if ent_w_food:
                # If there is an entity with food we will try to get to it
                # We will get the i-st closest entity with food
                closest_ent = self._order_by_proximity(entities_in_sight)
                if len(closest_ent) <= iteration:
                    closest_ent = closest_ent[-1]
                else:
                    closest_ent = closest_ent[iteration]
                # Now we will get the actions to get to the entity
                action_time, current_pos, actions = self._get_actions_to_position(
                    current_pos, 0, time, closest_ent["position"], entities_in_sight_pos, surroundings)

                # Next we will attack this entity
                if action_time < time:
                    # getting the body part with highest attack
                    body_part = "none"
                    current_attack = 0
                    for part in self.physical_properties:
                        if "attack" in part:
                            body_part = part.split("_")[0]
                            if self.physical_properties[part] > current_attack:
                                current_attack = self.physical_properties[part]
                    actions.append(
                        {"command": "attack", "parameters": [closest_ent["entity"], current_attack]})
                    action_time += self.physical_properties[body_part]

                # Now we will try to move to a position where the amount of entities is minimal
                if action_time < time:
                    action_time, current_pos, new_actions = self._get_actions_to_minimal_entities(
                        current_pos, action_time, time, entities_in_sight, entities_in_sight_pos, surroundings)
                    actions.extend(new_actions)

                state_value = self._get_ents_in_pos_radius(
                    entities_in_sight, entities_in_sight_pos, current_pos, self.physical_properties["eye"])
                return actions, state_value, action_time

            else:
                # If there is no food in sight we will try to explore the surroundings
                action_time, current_pos, actions = self._get_actions_to_minimal_entities(
                    current_pos, 0, time, entities_in_sight, entities_in_sight_pos, surroundings)
                state_value = self._get_ents_in_pos_radius(
                    entities_in_sight, entities_in_sight_pos, current_pos, self.physical_properties["eye"])
                return actions, state_value, action_time

    def _get_state_reproduction(self, time, any_entity, entities_in_sight, reproductive_entity, surroundings=None, previous_state=None, iteration=0):
        entities_in_sight_pos = self._curate_entities_positions(
            entities_in_sight)
        # getting position from the knowledge
        current_pos = None
        for info in self.knowledge:
            if "floor" in info.keys():
                current_pos = info["position"]
                break

        if any_entity and reproductive_entity:
            # If there is an entity in sight we will try to get to it
            # We will get the closest reproductive entity
            ordered_entities = self._order_by_proximity(entities_in_sight)
            i = 0
            closest_ent = None
            for ent in ordered_entities:
                if "reproductive" in ent and ent["reproductive"]:
                    i += 1
                    if i == iteration:
                        closest_ent = ent
                        break
                    # TODO check how we are comparing the values
            if not closest_ent:
                return [], -1, 0
            # Now we will get the actions to get to the entity
            action_time, current_pos, actions = self._get_actions_to_position(
                current_pos, 0, time, closest_ent["position"], entities_in_sight_pos, surroundings)
            # Next we will reproduce with this entity
            if action_time < time:
                # getting the body part with highest attack
                actions.append(
                    {"command": "reproduce", "parameters": [closest_ent["entity"]]})
                for p in self.actions:
                    if p["name"] == "reproduce":
                        action_time += p["cost"]
                        break
            # Now we will try to move to a position where the amount of entities is minimal
            if action_time < time:
                action_time, current_pos, new_actions = self._get_actions_to_minimal_entities(
                    current_pos, action_time, time, entities_in_sight, entities_in_sight_pos, surroundings)
                actions.extend(new_actions)
            state_value = self._get_ents_in_pos_radius(
                entities_in_sight, entities_in_sight_pos, current_pos, self.physical_properties["eye"])
            return actions, state_value, action_time
        else:
            # If there is no entity in sight we will try to explore the surroundings
            action_time, current_pos, actions = self._get_actions_to_minimal_entities(
                current_pos, 0, time, entities_in_sight, entities_in_sight_pos, surroundings)
            state_value = self._get_ents_in_pos_radius(
                entities_in_sight, entities_in_sight_pos, current_pos, self.physical_properties["eye"])
            return actions, state_value, action_time

    def _order_by_proximity(self, entities):
        # We will order the entities by proximity
        ordered_entities = []
        for ent in entities:
            if len(ordered_entities) == 0:
                ordered_entities.append(ent)
            else:
                for i in range(len(ordered_entities)):
                    if ent["distance"] < ordered_entities[i]["distance"]:
                        ordered_entities.insert(i, ent)
                        break
                    if i == len(ordered_entities) - 1:
                        ordered_entities.append(ent)
                        break
        return ordered_entities

    def _get_actions_to_minimal_entities(self, position, action_time, time, entities_in_sight, entities_in_sight_pos, surroundings):
        # This method will return a list of actions to move to a position where the amount of entities is minimal
        # First we will get the position with the minimal amount of entities
        min_entities = math.inf
        min_entities_pos = None
        for pos in surroundings.keys():
            ent_in_pos = sum(1 for entity in entities_in_sight if self._get_distance(
                pos, entity["position"]) < self.physical_properties["eye"])
            if ent_in_pos < min_entities:
                min_entities = ent_in_pos
                min_entities_pos = pos
        # Now we will get the actions to get to that position
        actions_time, current_pos, actions = self._get_actions_to_position(
            position, action_time, time, min_entities_pos, entities_in_sight, surroundings)
        return actions_time, current_pos, actions

    def _get_ents_in_pos_radius(self, entities_in_sight, entities_in_sight_pos, position, radius):
        # This method will return the amount of entities in the radius of a position
        return sum(1 for entity in entities_in_sight if self._get_distance(position, entity["position"]) < radius)

    def _get_actions_to_position(self, position, actions_time, time, g_pos, entities_in_sight_pos, surroundings):
        has_fins = "fins" in self.physical_properties.keys()
        has_legs = "legs" in self.physical_properties.keys()
        floor = self.knowledge[0]["floor"]
        current_pos = position
        actions = []
        while actions_time < time and self._get_distance(current_pos, g_pos) > 1:
            action = None
            # Now we will check decide from moving or swimming if we are in water
            if floor == "water" and has_fins:
                # If we are in water we will swim
                action = {"command": "swim",
                          "cost": self.physical_properties["fins"]}
                actions_time += self.physical_properties["fins"]
            elif has_legs:
                # If we are not in water we will move
                action = {"command": "move",
                          "cost": self.physical_properties["legs"]}
                actions_time += self.physical_properties["legs"]
            else:
                # the entity can't move
                break

            # We will get the distances to the food in the in the available four directions
            distances = []
            for direction in ["north", "south", "west", "east"]:
                if self._get_new_position(position, direction) in surroundings.keys():
                    new_pos = self._get_new_position(position, direction)
                    new_floor = surroundings[new_pos] if surroundings else "unknown"
                    if new_floor == "unknown" and new_pos not in entities_in_sight_pos:
                        distances.append((self._get_distance(
                            new_pos, g_pos), direction))
                    elif new_floor == "water" and has_fins and new_pos not in entities_in_sight_pos:
                        distances.append((self._get_distance(
                            new_pos, g_pos), direction))
                    elif has_legs and new_pos not in entities_in_sight_pos:
                        distances.append((self._get_distance(
                            new_pos, g_pos), direction))
            # Now we will get the direction in which the distance to the food is minimal
            if len(distances) > 0:
                min_distance = distances[0][0]
                min_direction = distances[0][1]
                for i in range(1, len(distances)):
                    if distances[i][0] < min_distance:
                        min_distance = distances[i][0]
                        min_direction = distances[i][1]
                # Now we will move in the direction of the minimal distance
                action["command"] += " " + min_direction
                current_pos = self._get_new_position(
                    current_pos, min_direction)
                actions.append(action)
            else:
                # If we can't move from any direction we wont move
                break
        return actions_time, current_pos, actions

    def _curate_entities_positions(self, entities):
        # This method will return a list of positions of the entities in sight
        positions = []
        for entity in entities:
            positions.append(entity["position"])
        return positions

    def _get_distance(self, pos1, pos2):
        # This method will return the distance between two positions
        return (abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]))

    def _get_new_position(self, pos, dir):
        # This method will return the new position after moving in a direction
        if dir == "north":
            return (pos[0] - 1, pos[1])
        elif dir == "south":
            return (pos[0] + 1, pos[1])
        elif dir == "west":
            return (pos[0], pos[1] - 1)
        elif dir == "east":
            return (pos[0], pos[1] + 1)
        else:
            return pos


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
