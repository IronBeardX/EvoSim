from .evo_world import *
from .evo_entity import *
from .utils import *
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style


class EvoSim:
    def __init__(self,
                 height,
                 width,
                 terrain_types,
                 terrain_dist,
                 finite=False,
                 episodes_total=1,
                 max_rounds_per_episode=10,
                 stop_condition=None,
                 available_commands={},
                 visualization=False,
                 actions_time=10
                 ):
        self.init_world(height, width, terrain_types, terrain_dist, finite)
        self.actions_time = actions_time
        self.visualization = visualization
        self.entities_gen = []
        self.entities = {}
        self.banished_entities = {}
        self.intelligent_entities = {}
        self.dead_entities = {}
        self.episodes_total = episodes_total
        self.max_rounds = max_rounds_per_episode
        self.stop_condition = stop_condition
        self.day = 0
        # TODO: this should be imported
        default_commands = {"floor": self.floor,
                            "smell": self.smell,
                            "see": self.see,
                            "pick": self.pick,
                            "attack": self.attack,
                            "eat": self.eat,
                            "reproduce": self.reproduce
                            }
        self.available_commands = default_commands if not available_commands else default_commands.update(
            available_commands)

    def run(self, gen_world_pos):
        for episode in range(self.episodes_total):
            self.world = self.world_gen()
            for entity_gen_position, world_position in gen_world_pos:
                self.instantiate_entity(entity_gen_position, world_position)

            self.run_episode()
            self.entities = {}
            self.intelligent_entities = {}
            self.dead_entities = {}

    def run_episode(self):
        for day in range(self.max_rounds):
            self.day = day
            # Checking stop condition if defined
            if self.stop_condition is not None:
                if self.stop_condition(self):
                    return

            # Time comes for us all ...
            for entity_id in self.entities:
                entity = self.entities[entity_id]
                entity.pass_time()

            # Executing entities actions
            for entity_id in list(self.intelligent_entities.keys()):
                entity = self.intelligent_entities[entity_id]
                # TODO: perceptions should be before pass time in intelligent entities
                # Executing perception actions:
                perception_list = []
                if "floor" in self.available_commands:
                    position, floor = self.available_commands["floor"](
                        entity_id)
                    perception_list.append(
                        {"floor": floor, "position": position})
                for action in entity.get_perceptions():
                    command = action["command"]
                    parameters = action["parameters"]
                    new_per = []
                    if command in self.available_commands:
                        new_information = self.available_commands[command](
                            entity_id, day, *parameters)
                        for info in new_information:
                            self.update_perception(info, perception_list)
                self.intelligent_entities[entity_id].update_knowledge(
                    perception_list)

                if not entity.pass_time():
                    self.banished_entities[entity_id] = self.intelligent_entities.pop(
                        entity_id)
                    self.world.remove_entity(entity_id)
                    # print : entity_id, "was banished"
                    if self.visualization:
                        self.visualization_fun(banished=entity_id)
                    continue
                # The entity executes its action based on its world perception,
                # which returns world and simulation actions to be executed
                actions = entity.decide_action(time=self.actions_time)
                for action in actions:
                    action["entity"] = entity_id
                    self.execute_action(action)
                    if self.visualization:
                        self.visualization_fun(action)

    def gol_visualizer(self):
        print("\n")
        for i in range(self.world.world_rep().shape[0]):
            for j in range(self.world.world_rep().shape[1]):
                if self.world.world_rep()[i, j] == "R":
                    print(
                        f"{Fore.YELLOW}{self.world.world_rep()[i,j]}{Style.RESET_ALL}", end=" ")
                elif self.world.world_rep()[i, j] == "W":
                    print(
                        f"{Fore.BLUE}{self.world.world_rep()[i, j]}{Style.RESET_ALL}", end=" ")
                elif self.world.world_rep()[i, j] == "F":
                    print(
                        f"{Fore.RED}{self.world.world_rep()[i,j]}{Style.RESET_ALL}", end=" ")
                elif self.world.world_rep()[i, j] == "P":
                    print(
                        f"{Fore.RED}{self.world.world_rep()[i,j]}{Style.RESET_ALL}", end=" ")
                else:
                    print(self.world.world_rep()[i, j], end=" ")
            print("\n")
        print("\n \n")

    def visualization_fun(self, action=None, banished=None):
        if action:
            print(action["command"])
        if banished:
            print(f"{banished} was banished")
        print("\n")
        for i in range(self.world.world_rep().shape[0]):
            for j in range(self.world.world_rep().shape[1]):
                if self.world.world_rep()[i, j] == "R":
                    print(
                        f"{Fore.YELLOW}{self.world.world_rep()[i,j]}{Style.RESET_ALL}", end=" ")
                elif self.world.world_rep()[i, j] == "W":
                    print(
                        f"{Fore.BLUE}{self.world.world_rep()[i, j]}{Style.RESET_ALL}", end=" ")
                elif self.world.world_rep()[i, j] == "F":
                    print(
                        f"{Fore.RED}{self.world.world_rep()[i,j]}{Style.RESET_ALL}", end=" ")
                elif self.world.world_rep()[i, j] == "P":
                    print(
                        f"{Fore.RED}{self.world.world_rep()[i,j]}{Style.RESET_ALL}", end=" ")
                else:
                    print(self.world.world_rep()[i, j], end=" ")
            print("\n")
        print("\n \n")

    def update_perception(self, new_info, current_info):
        if "entity" in list(new_info.keys()):
            entity_id = new_info["entity"]
            for old_info in current_info:
                if ("entity" in old_info) and entity_id == old_info["entity"]:
                    old_info.update(new_info)
                    return
            current_info.append(new_info)
        if "floor" in list(new_info.keys()):
            for old_info in current_info:
                if ("floor" in old_info):
                    old_info.update(new_info)
                    return
            current_info.append(new_info)
        if "surroundings" in list(new_info.keys()):
            for old_info in current_info:
                if ("surroundings" in old_info):
                    old_info.update(new_info)
                    return
            current_info.append(new_info)

    def floor(self, ent_id):
        position = self.world.entities[ent_id].position
        return (position, self.world.get_pos_terrain(position))

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

    def entities_in_radius(self, ent_id, r):
        entities_id_list = [(other_id, pos, distance)
                            for other_id, pos, distance in self.world.see_r(ent_id, r)]
        entities = []
        for ent_id, pos, distance in entities_id_list:
            if ent_id in self.entities:
                entities.append((self.entities[ent_id], pos, distance))
            elif ent_id in self.intelligent_entities:
                entities.append(
                    (self.intelligent_entities[ent_id], pos, distance))
        return entities

    def entities_in_radius(self, ent_id, r):
        entities_id_list = [(other_id, pos, distance)
                            for other_id, pos, distance in self.world.see_r(ent_id, r)]
        entities = []
        for ent_id, pos, distance in entities_id_list:
            if ent_id in self.entities:
                entities.append((self.entities[ent_id], pos, distance))
            elif ent_id in self.intelligent_entities:
                entities.append(
                    (self.intelligent_entities[ent_id], pos, distance))
        return entities

    def entities_around_position(self, position):
        aux = len(self.world.get_entities_around_position(position))
        return aux

    def entities_in_position(self, position):
        aux = len(self.world.get_entity_by_position(position))
        return aux

    def kill_in_position(self, position):
        entities_id = self.world.get_entity_by_position(position)
        if len(entities_id) > 0:
            self.entities.pop(entities_id[0])
            self.world.remove_entity(entities_id[0])

    def create_in_position(self, position):
        self.instantiate_entity(0, (position[0], position[1]))

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

    def new_empty_pos(self, ent_id, other_id):
        # Generate the a new position adjacent to ent_id or other_id:
        pos = self.world.entities[ent_id].position
        other_pos = self.world.entities[ent_id].position
        posible_options = [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]),
                           (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]
        posible_options += [(other_pos[0] + 1, other_pos[1]), (other_pos[0] - 1, other_pos[1]),
                            (other_pos[0], other_pos[1] + 1), (other_pos[0], other_pos[1] - 1)]
        for option in posible_options:
            if self.world.valid_position(option) and len(self.world.get_entity_by_position(option)):
                return option
        return None

    def execute_action(self, action):
        if action["command"] in list(self.available_commands.keys()):
            self.available_commands[action["command"]](
                action["entity"], *action["parameters"])
        else:
            self.world.execute_action(action)

    def init_world(self, height, width, terrain_types, terrain_dist, finite):
        self.world_gen = lambda: EvoWorld(
            height, width, terrain_types, terrain_dist, finite)

    def add_entity_gen(self, entity_instance_gen):
        self.entities_gen.append(entity_instance_gen)

    def instantiate_entity(self, entity_gen_position, world_position, generator=None):
        if generator != None:
            entity = generator()
            self.intelligent_entities[entity.get_entity_id()] = entity
            self.world.place_entity(entity.get_entity_id(), world_position,
                                    entity.rep, entity.coexistence)
            return

        entity = self.entities_gen[entity_gen_position]()
        if entity.is_intelligent:
            self.intelligent_entities[entity.get_entity_id()] = entity
        else:
            self.entities[entity.get_entity_id()] = entity
        self.world.place_entity(entity.get_entity_id(), world_position,
                                entity.rep, entity.coexistence)

    def dest(self):
        print("hi")
