import random
import math
import numpy as np
from .utils import *


def search(target_type, current_position, mind_map, organism):
    print("searching " + target_type)
    return [{'command': 'none', 'parameters': [], 'time': 1, 'cost': 0}]


def search_allies(current_position, mind_map, organism):
    return search("allies", current_position, mind_map, organism)


def search_enemies(current_position, mind_map, organism):
    return search("enemies", current_position, mind_map, organism)


def search_food(current_position, mind_map, organism):
    return search("food", current_position, mind_map, organism)


def take_food(current_position, mind_map, organism):
    print("taking food")
    return [{'command': 'none', 'parameters': [], 'time': 1, 'cost': 0}]


def attack_enemies(current_position, mind_map, organism):
    print("attacking")
    return [{'command': 'none', 'parameters': [], 'time': 1, 'cost': 0}]


def reproduce(current_position, mind_map, organism):
    print("reproducing")
    return [{'command': 'none', 'parameters': [], 'time': 1, 'cost': 0}]


def exploring(current_position, mind_map, organism):
    print("exploring")
    return [{'command': 'none', 'parameters': [], 'time': 1, 'cost': 0}]


def fleeing(current_position, mind_map, organism):
    print("fleeing")
    brain = organism.brain
    enemies = brain.last_enemies.values()
    valid_terrains = brain.valid_terrains
    enemies_position = [entity['position'] for entity in enemies]
    current_distance = enemies_dist_med(current_position, enemies_position)
    goal_position = current_position
    if current_distance == 0:
        return [{'command': 'none', 'parameters': [], 'time': 1, 'cost': 0}]

    def condition(x):
        time_since_percieved = organism.age - x.age_when_updated - 1
        terrain_validity = x.terrain in valid_terrains
        return (time_since_percieved == 0) and terrain_validity

    for position in bfs(current_position, mind_map.shape, condition, mind_map):
        distance = enemies_dist_med(position, enemies_position)
        if distance > current_distance:
            goal_position = position
    return get_commands_to_position(current_position, goal_position, mind_map, valid_terrains, organism.physical_properties, organism.actions)


def get_commands_to_position(current_position, goal_position, mind_map, valid_terrains, ph_props, actions_info):
    command_list = []
    if current_position == goal_position:
        return [{'command': 'none', 'parameters': [], 'time': 1, 'cost': 0}]

    class AstarModeling(Problem):
        def __init__(self, initial=current_position, goal=goal_position, mind_map=mind_map, valid_terrains=valid_terrains):
            self.initial, self.goal, self.mind_map, self.valid_terrains = initial, goal, mind_map, valid_terrains
            self.height, self.width = mind_map.shape

        def actions(self, state):
            valid_positions = []
            if state[0] > 0:
                next_pos = (state[0] - 1, state[1])
                if self.mind_map[next_pos].terrain in valid_terrains:
                    valid_positions.append(next_pos)
            if state[0] < self.height - 1:
                next_pos = (state[0] + 1, state[1])
                if self.mind_map[next_pos].terrain in valid_terrains:
                    valid_positions.append(next_pos)
            if state[1] > 0:
                next_pos = (state[0], state[1] - 1)
                if self.mind_map[next_pos].terrain in valid_terrains:
                    valid_positions.append(next_pos)
            if state[1] < self.width - 1:
                next_pos = (state[0], state[1] + 1)
                if self.mind_map[next_pos].terrain in valid_terrains:
                    valid_positions.append(next_pos)
            return tuple(valid_positions)

        def result(self, state, action):
            return action

        def h(self, node):
            return distance(node.state, self.goal)

    modeling = AstarModeling()
    path = path_states(astar_search(modeling))
    aux_pos = path.pop(0)
    command_list = []
    while len(path) > 0:
        directions = {
            (-1, 0): 'north',
            (1, 0): 'south',
            (0, -1): 'west',
            (0, 1): 'east'
        }
        next_pos = path.pop(0)
        command = 'move ' if mind_map[next_pos].terrain != 'water' else 'swim '
        time = ph_props['legs'] if mind_map[next_pos].terrain != 'water' else ph_props['fins']
        command += directions[(next_pos[0] - aux_pos[0],
                               next_pos[1] - aux_pos[1])]
        metabolic_cost = 1
        for info in actions_info:
            if command == info['name']:
                metabolic_cost = info['cost']
        command_list.append(
            {'command': command, 'parameters': [], 'time': time, 'cost': metabolic_cost})
        aux_pos = next_pos
    return command_list


def enemies_dist_med(pos, enemies):
    if len(enemies) == 0:
        return 0
    else:
        return np.median([distance(pos, enemy) for enemy in enemies])


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
    # default map size (10, 10)
    class KnTile:
        def __init__(self):
            self.terrain = 'unknown'
            self.entities = []
            self.allies = []
            self.enemies = []
            self.age_when_updated = 0

    def __init__(self, behaviors=None, map_size=(10, 10)):
        default_bh = {
            'search allies': search_allies,
            'search food': search_food,
            'take food': take_food,
            'reproduce': reproduce,
            'exploring': exploring,
            'fleeing': fleeing,
            'none': lambda x, y, z: [{'command': 'none', 'time': 1, 'parameters': [], 'cost': 0}]
        }
        self.knowledge = {}
        self.memory_map = np.array(
            [[self.KnTile() for _ in range(map_size[0])] for _ in range(map_size[1])])
        self.behaviors = behaviors if behaviors is not None else default_bh
        self.behavior_list = list(self.behaviors.keys())
        self.last_entities = {}
        self.last_allies = {}
        self.last_enemies = {}

    def decide_action(self, organism, time=0):
        raise NotImplementedError

    def get_perceptions(self, organism):
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
        self.last_allies = {}
        self.last_enemies = {}
        self.last_entities = {}
        for information in new_knowledge:
            if 'surroundings' in information.keys():
                terrain_dist = information['surroundings']
                for position in terrain_dist:
                    tile = self.memory_map[position]
                    tile.terrain = terrain_dist[position]
                    tile.age_when_updated = organism.age
                continue

            tile = self.memory_map[information['position']]
            tile = self.KnTile()
            tile.age_when_updated = organism.age
            if 'floor' in information.keys():
                self.last_position = information['position']
                tile.terrain = information['floor']
            elif 'species' in information.keys():
                if organism.species == information['species']:
                    tile.allies.append(information)
                    self.last_allies[information['id']] = information

                else:
                    tile.enemies.append(information)
                    self.last_enemies[information['id']] = information
            elif 'edible' in information.keys():
                tile.entities.append(information)
                self.last_entities[information['id']] = information
        return

    def vectorized_perceptions(self, organism):
        raise NotImplementedError

    def decide_behavior(self, vector):
        raise NotImplementedError

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


class PreyBrain(Brain):
    def __init__(self, behaviors=None, map_size=(10, 10), learning_rate=0.1):
        super().__init__(behaviors, map_size)

    def decide_action(self, organism, time=10):
        vec = self.vectorized_perceptions(organism)
        bh = self.decide_behavior(vec)
        plan = self.behaviors[bh](
            self.last_position, self.memory_map, organism)
        current_time = 0
        actions = []
        while current_time <= time and len(plan) > 0:
            current_action = plan.pop(0)
            current_time += current_action['time']
            organism.physical_properties['hunger'] -= current_action['cost']

            if organism.physical_properties['hunger'] < 0:
                organism.physical_properties['hunger'] = 0

            actions.append({
                'command': current_action['command'],
                'parameters': current_action['parameters']
            })
        return actions if len(actions) > 0 else [{'command': 'none', 'parameters': []}]

    def vectorized_perceptions(self, organism):
        valid_terrains = []
        if 'fins' in organism.physical_properties.keys():
            valid_terrains.append('water')
        if 'legs' in organism.physical_properties.keys():
            valid_terrains.extend(['grass', 'dirt'])
        self.valid_terrains = set(valid_terrains)

        food_in_range = 0
        for entity in self.last_entities.values():
            if entity['food_type'] in organism.physical_properties['diet']:
                food_in_range += 1

        # vector:
        # 0: reachable food
        # 1: reachable allies
        # 2: reachable enemies
        # 3: hunger
        # 4: health

        hunger = (organism.physical_properties['hunger'] *
                  100) / organism.physical_properties['max hunger']
        if hunger < 25:
            hunger = 0
        elif hunger < 50:
            hunger = 1
        elif hunger < 75:
            hunger = 2
        else:
            hunger = 3

        health = (organism.physical_properties['health'] *
                  100) / organism.physical_properties['max health']
        if health < 25:
            health = 0
        elif health < 50:
            health = 1
        elif health < 75:
            health = 2
        else:
            health = 3

        return [food_in_range, len(self.last_allies), len(self.last_enemies), hunger, health]

    def decide_behavior(self, vector):
        bh_vector = [0] * (len(self.behavior_list))
        if not vector in list(self.knowledge.keys()):
            self.knowledge[str(vector)] = bh_vector
            # TODO: this should assign a value to all behaviors
        else:
            bh_vector = self.knowledge[vector]

        max_expected_val = 0
        bh_name = 0
        # TODO: Select_fuzzy for this
        for i in range(len(bh_vector)):
            if bh_vector[i] > max_expected_val:
                max_expected_val = bh_vector[i]
                bh_name = self.behavior_list[i]
        return bh_name if max_expected_val > 0 else random.choice(self.behavior_list)


class PredatorBrain(Brain):
    def vectorized_perceptions(self, organism):
        perceptions = self.get_perceptions(organism)
        vec = np.zeros((10, 10, 9))
        for perception in perceptions:
            match perception["command"]:
                case "smell":
                    for position in perception["parameters"]:
                        tile = self.get_floor(position[0], position[1])
                        if tile.terrain == 'food':
                            vec[position[0]][position[1]][0] = 1
                        if len(tile.allies) > 0:
                            vec[position[0]][position[1]][1] = 1
                        if len(tile.enemies) > 0:
                            vec[position[0]][position[1]][2] = 1
                        if len(tile.entities) > 0:
                            vec[position[0]][position[1]][3] = 1
                case "see":
                    for position in perception["parameters"]:
                        tile = self.get_floor(position[0], position[1])
                        if tile.terrain == 'food':
                            vec[position[0]][position[1]][0] = 1
                        if len(tile.allies) > 0:
                            vec[position[0]][position[1]][1] = 1
                        if len(tile.enemies) > 0:
                            vec[position[0]][position[1]][2] = 1
                        if len(tile.entities) > 0:
                            vec[position[0]][position[1]][3] = 1
        return vec

    def decide_behavior(self, vector):
        if vector[0][0][0] == 1:
            return 'take food'
        if vector[0][0][1] == 1:
            return 'search allies'
        if vector[0][0][2] == 1:
            return 'search enemies'
        if vector[0][0][3] == 1:
            return 'search food'
        return 'none'
