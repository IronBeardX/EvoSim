class MoveNorth:
    def move_n(self, entity_id):
        # get entity position from its id
        entity_pos = self.entities[entity_id].position
        north_pos = (entity_pos[0] - 1, entity_pos[1])

        # check current position is terrain type water
        if self.get_terrain_type(entity_pos) == "water":
            return False

        # check if the entity is in a finite world
        if north_pos[0] < 0:
            if not self.finite:
                north_pos = (self.world_map.shape[0]-1, entity_pos[1])
            else:
                return False

        # Check if the entity can coexist with another entities
        north_entities = self.get_entity_by_position(north_pos)
        north_entities = [self.entities[x].can_coexist for x in north_entities]
        if self.entities[entity_id].can_coexist == False and any([not x for x in north_entities]):
            return False

        self.entities[entity_id].position = north_pos
        return True


class MoveSouth:
    def move_s(self, entity_id):
        # get entity position from its id
        entity_pos = self.entities[entity_id].position
        south_pos = (entity_pos[0] + 1, entity_pos[1])

        # check current position is terrain type water
        if self.get_terrain_type(entity_pos) == "water":
            return False

        # check if the entity is in a finite world
        if south_pos[0] >= self.world_map.shape[0]:
            if not self.finite:
                south_pos = (0, entity_pos[1])
            else:
                return False

        # Check if the entity can coexist with another entities
        south_entities = self.get_entity_by_position(south_pos)
        south_entities = [self.entities[x].can_coexist for x in south_entities]
        if self.entities[entity_id].can_coexist == False and any([not x for x in south_entities]):
            return False

        self.entities[entity_id].position = south_pos
        return True


class MoveEast:
    def move_e(self, entity_id):
        # get entity position from its id
        entity_pos = self.entities[entity_id].position
        east_pos = (entity_pos[0], entity_pos[1] + 1)

        # check current position is terrain type water
        if self.get_terrain_type(entity_pos) == "water":
            return False

        # check if the entity is in a finite world
        if east_pos[1] >= self.world_map.shape[1]:
            if not self.finite:
                east_pos = (entity_pos[0], 0)
            else:
                return False

        # Check if the entity can coexist with another entities
        east_entities = self.get_entity_by_position(east_pos)
        east_entities = [self.entities[x].can_coexist for x in east_entities]
        if self.entities[entity_id].can_coexist == False and any([not x for x in east_entities]):
            return False

        self.entities[entity_id].position = east_pos
        return True


class MoveWest:
    def move_w(self, entity_id):
        # get entity position from its id
        entity_pos = self.entities[entity_id].position
        west_pos = (entity_pos[0], entity_pos[1] - 1)

        # check current position is terrain type water
        if self.get_terrain_type(entity_pos) == "water":
            return False

        # check if the entity is in a finite world
        if west_pos[1] < 0:
            if not self.finite:
                west_pos = (entity_pos[0], self.world_map.shape[1]-1)
            else:
                return False

        # Check if the entity can coexist with another entities
        west_entities = self.get_entity_by_position(west_pos)
        west_entities = [self.entities[x].can_coexist for x in west_entities]
        if self.entities[entity_id].can_coexist == False and any([not x for x in west_entities]):
            return False

        self.entities[entity_id].position = west_pos
        return True


class SwimNorth:
    def swim_n(self, entity_id):
        # get entity position from its id
        entity_pos = self.entities[entity_id].position
        north_pos = (entity_pos[0] - 1, entity_pos[1])

        # check current position is terrain type water
        if self.get_terrain_type(entity_pos) != "water":
            return False

        # check if the entity is in a finite world
        if north_pos[0] < 0:
            if not self.finite:
                north_pos = (self.world_map.shape[0]-1, entity_pos[1])
            else:
                return False

        # Check if the entity can coexist with another entities
        north_entities = self.get_entity_by_position(north_pos)
        north_entities = [self.entities[x].can_coexist for x in north_entities]
        if self.entities[entity_id].can_coexist == False and any([not x for x in north_entities]):
            return False

        self.entities[entity_id].position = north_pos
        return True


class SwimSouth:
    def swim_s(self, entity_id):
        # get entity position from its id
        entity_pos = self.entities[entity_id].position
        south_pos = (entity_pos[0] + 1, entity_pos[1])

        # check current position is terrain type water
        if self.get_terrain_type(entity_pos) != "water":
            return False

        # check if the entity is in a finite world
        if south_pos[0] >= self.world_map.shape[0]:
            if not self.finite:
                south_pos = (0, entity_pos[1])
            else:
                return False

        # Check if the entity can can_coexist with another entities
        south_entities = self.get_entity_by_position(south_pos)
        south_entities = [self.entities[x].can_coexist for x in south_entities]
        if self.entities[entity_id].can_coexist == False and any([not x for x in south_entities]):
            return False

        self.entities[entity_id].position = south_pos
        return True


class SwimEast:
    def swim_e(self, entity_id):
        # get entity position from its id
        entity_pos = self.entities[entity_id].position
        east_pos = (entity_pos[0], entity_pos[1] + 1)

        # check current position is terrain type water
        if self.get_terrain_type(entity_pos) != "water":
            return False

        # check if the entity is in a finite world
        if east_pos[0] >= self.world_map.shape[1]:
            if not self.finite:
                east_pos = (0, entity_pos[1])
            else:
                return False

        # Check if the entity can can_coexist with another entities
        east_entities = self.get_entity_by_position(east_pos)
        east_entities = [self.entities[x].can_coexist for x in east_entities]
        if self.entities[entity_id].can_coexist == False and any([not x for x in east_entities]):
            return False

        self.entities[entity_id].position = east_pos
        return True


class SwimWest:
    def swim_w(self, entity_id):
        # get entity position from its id
        entity_pos = self.entities[entity_id].position
        west_pos = (entity_pos[0], entity_pos[1] - 1)

        # check current position is terrain type water
        if self.get_terrain_type(entity_pos) != "water":
            return False

        # check if the entity is in a finite world
        if west_pos[0] < 0:
            if not self.finite:
                west_pos = (entity_pos[0], self.world_map.shape[1])
            else:
                return False

        # Check if the entity can can_coexist with another entities
        west_entities = self.get_entity_by_position(west_pos)
        west_entities = [self.entities[x].can_coexist for x in west_entities]
        if self.entities[entity_id].can_coexist == False and any([not x for x in west_entities]):
            return False

        self.entities[entity_id].position = west_pos
        return True


class SeeRadius:

    def see_r(self, entity_id, radius):
        # get entity position from its id
        entity_position = self.entities[entity_id].position
        entities_in_radius = []
        valid_pos = self.__get_positions_in_radius(entity_position, radius)
        for entity in self.entities:
            if entity != entity_id:
                if self.entities[entity].position in valid_pos:
                    entities_in_radius.append(
                        (entity, self.entities[entity].position))

        return entities_in_radius

    # Also see what happens if the world is finite
    def __get_positions_in_radius(self, entity_position, radius):
        positions = []
        for i in range(entity_position[0] - radius, entity_position[0] + radius + 1):
            for j in range(entity_position[1] - radius, entity_position[1] + radius + 1):
                if i >= 0 and j >= 0 and i < self.world_map.shape[0] and j < self.world_map.shape[1]:
                    positions.append((i, j))
                if not self.finite:
                    if i < 0:
                        i = self.world_map.shape[0] - 1
                    if j < 0:
                        j = self.world_map.shape[1] - 1
                    if i >= self.world_map.shape[0]:
                        i = 0
                    if j >= self.world_map.shape[1]:
                        j = 0
                    positions.append((i, j))
        return positions


class TerrainRadius:
    def terrain_r(self, entity_id, radius):
        entity_position = self.entities[entity_id].position
        positions_in_radius = self.__get_positions_in_radius(entity_position, radius)
        terrain_in_radius = {}
        for pos in positions_in_radius:
            rep = self.world_map[pos]
            terrain_in_radius[pos] = self.terrain_types[rep]
        
        # terrain_in_radius = [self.world_map[pos] for pos in terrain_in_radius]
        #  # self.world_map["position"]
        # terrain_in_radius = [self.terrain_types[rep] for rep in terrain_in_radius]
        # # self.terrain_types["rep"]    
        return terrain_in_radius

    def __get_positions_in_radius(self, entity_position, radius):
        positions = []
        for i in range(entity_position[0] - radius, entity_position[0] + radius + 1):
            for j in range(entity_position[1] - radius, entity_position[1] + radius + 1):
                if i >= 0 and j >= 0 and i < self.world_map.shape[0] and j < self.world_map.shape[1]:
                    positions.append((i, j))
                if not self.finite:
                    if i < 0:
                        i = self.world_map.shape[0] - 1
                    if j < 0:
                        j = self.world_map.shape[1] - 1
                    if i >= self.world_map.shape[0]:
                        i = 0
                    if j >= self.world_map.shape[1]:
                        j = 0
                    positions.append((i, j))
        return positions

class ManhatanDistance:
    def distance(self, entity_id, other_entity_id):
        entity_position = self.entities[entity_id].position
        other_entity_position = self.entities[other_entity_id].position
        return abs(entity_position[0] - other_entity_position[0]) + abs(entity_position[1] - other_entity_position[1])
