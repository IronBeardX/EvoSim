class MoveNorth:
    def move_n(self, entity_id):
        # Get entity position from its id
        entity_pos = self.entities[entity_id].position
        north_pos = (entity_pos[0] - 1, entity_pos[1])

        # Check if the current position terrain's type is water
        if self.get_terrain_type(entity_pos) == "water":
            return False

        # Check if the entity is in a finite world
        if north_pos[0] < 0:
            if not self.finite:
                # If the entity is not in a finite world, then it can move to the other side of the world.
                north_pos = (self.world_map.shape[0]-1, entity_pos[1])
            else:
                return False

        # Getting the entities of the new position and checking if they can coexist
        north_entities = self.get_entity_by_position(north_pos)
        north_entities = [self.entities[x].can_coexist for x in north_entities]
        if self.entities[entity_id].can_coexist == False and any([not x for x in north_entities]):
            return False

        # If the entity can move, then we update its position
        self.entities[entity_id].position = north_pos
        return True


class MoveSouth:
    def move_s(self, entity_id):
        # Get entity position from its id
        entity_pos = self.entities[entity_id].position
        south_pos = (entity_pos[0] + 1, entity_pos[1])

        # Check if the current position terrain's type is water
        if self.get_terrain_type(entity_pos) == "water":
            return False

        # Check if the entity is in a finite world
        if south_pos[0] >= self.world_map.shape[0]:
            if not self.finite:
                # If the entity is not in a finite world, then it can move to the other side of the world.
                south_pos = (0, entity_pos[1])
            else:
                return False

        # Getting the entities of the new position and checking if they can coexist
        south_entities = self.get_entity_by_position(south_pos)
        south_entities = [self.entities[x].can_coexist for x in south_entities]
        if self.entities[entity_id].can_coexist == False and any([not x for x in south_entities]):
            return False

        # If the entity can move, then we update its position
        self.entities[entity_id].position = south_pos
        return True


class MoveEast:
    def move_e(self, entity_id):
        # Get entity position from its id
        entity_pos = self.entities[entity_id].position
        east_pos = (entity_pos[0], entity_pos[1] + 1)

        # Check if the current position terrain's type is water
        if self.get_terrain_type(entity_pos) == "water":
            return False

        # Check if the entity is in a finite world
        if east_pos[1] >= self.world_map.shape[1]:
            if not self.finite:
                # If the entity is not in a finite world, then it can move to the other side of the world.
                east_pos = (entity_pos[0], 0)
            else:
                return False

        # Getting the entities of the new position and checking if they can coexist
        east_entities = self.get_entity_by_position(east_pos)
        east_entities = [self.entities[x].can_coexist for x in east_entities]
        if self.entities[entity_id].can_coexist == False and any([not x for x in east_entities]):
            return False

        # If the entity can move, then we update its position
        self.entities[entity_id].position = east_pos
        return True


class MoveWest:
    def move_w(self, entity_id):
        # Get entity position from its id
        entity_pos = self.entities[entity_id].position
        west_pos = (entity_pos[0], entity_pos[1] - 1)

        # Check if the current position terrain's type is water
        if self.get_terrain_type(entity_pos) == "water":
            return False

        # Check if the entity is in a finite world
        if west_pos[1] < 0:
            if not self.finite:
                # If the entity is not in a finite world, then it can move to the other side of the world.
                west_pos = (entity_pos[0], self.world_map.shape[1]-1)
            else:
                return False

        # Getting the entities of the new position and checking if they can coexist
        west_entities = self.get_entity_by_position(west_pos)
        west_entities = [self.entities[x].can_coexist for x in west_entities]
        if self.entities[entity_id].can_coexist == False and any([not x for x in west_entities]):
            return False

        # If the entity can move, then we update its position
        self.entities[entity_id].position = west_pos
        return True


class SwimNorth:
    def swim_n(self, entity_id):
        # Get entity position from its id
        entity_pos = self.entities[entity_id].position
        north_pos = (entity_pos[0] - 1, entity_pos[1])

        # Check if the current position terrain's type is water
        if self.get_terrain_type(entity_pos) != "water":
            return False

        # Check if the entity is in a finite world
        if north_pos[0] < 0:
            if not self.finite:
                # If the entity is not in a finite world, then it can move to the other side of the world.
                north_pos = (self.world_map.shape[0]-1, entity_pos[1])
            else:
                return False

        # Getting the entities of the new position and checking if they can coexist
        north_entities = self.get_entity_by_position(north_pos)
        north_entities = [self.entities[x].can_coexist for x in north_entities]
        if self.entities[entity_id].can_coexist == False and any([not x for x in north_entities]):
            return False

        # If the entity can move, then we update its position
        self.entities[entity_id].position = north_pos
        return True


class SwimSouth:
    def swim_s(self, entity_id):
        # Get entity position from its id
        entity_pos = self.entities[entity_id].position
        south_pos = (entity_pos[0] + 1, entity_pos[1])

        # Check if the current position terrain's type is water
        if self.get_terrain_type(entity_pos) != "water":
            return False

        # Check if the entity is in a finite world
        if south_pos[0] >= self.world_map.shape[0]:
            if not self.finite:
                # If the entity is not in a finite world, then it can move to the other side of the world.
                south_pos = (0, entity_pos[1])
            else:
                return False

        # Getting the entities of the new position and checking if they can coexist
        south_entities = self.get_entity_by_position(south_pos)
        south_entities = [self.entities[x].can_coexist for x in south_entities]
        if self.entities[entity_id].can_coexist == False and any([not x for x in south_entities]):
            return False

        # If the entity can move, then we update its position
        self.entities[entity_id].position = south_pos
        return True


class SwimEast:
    def swim_e(self, entity_id):
        # Get entity position from its id
        entity_pos = self.entities[entity_id].position
        east_pos = (entity_pos[0], entity_pos[1] + 1)

        # Check if the current position terrain's type is water
        if self.get_terrain_type(entity_pos) != "water":
            return False

        # Check if the entity is in a finite world
        if east_pos[1] >= self.world_map.shape[1]:
            if not self.finite:
                # If the entity is not in a finite world, then it can move to the other side of the world.
                east_pos = (0, entity_pos[1])
            else:
                return False

        # Getting the entities of the new position and checking if they can coexist
        east_entities = self.get_entity_by_position(east_pos)
        east_entities = [self.entities[x].can_coexist for x in east_entities]
        if self.entities[entity_id].can_coexist == False and any([not x for x in east_entities]):
            return False

        # If the entity can move, then we update its position
        self.entities[entity_id].position = east_pos
        return True


class SwimWest:
    def swim_w(self, entity_id):
        # Get entity position from its id
        entity_pos = self.entities[entity_id].position
        west_pos = (entity_pos[0], entity_pos[1] - 1)

        # Check if the current position terrain's type is water
        if self.get_terrain_type(entity_pos) != "water":
            return False

        # Check if the entity is in a finite world
        if west_pos[0] < 0:
            if not self.finite:
                # If the entity is not in a finite world, then it can move to the other side of the world.
                west_pos = (entity_pos[0], self.world_map.shape[1] - 1)
            else:
                return False

        # Getting the entities of the new position and checking if they can coexist
        west_entities = self.get_entity_by_position(west_pos)
        west_entities = [self.entities[x].can_coexist for x in west_entities]
        if self.entities[entity_id].can_coexist == False and any([not x for x in west_entities]):
            return False

        # If the entity can move, then we update its position
        self.entities[entity_id].position = west_pos
        return True


class SeeRadius:

    def see_r(self, entity_id, radius):
        # Get entity position from its id.
        entity_position = self.entities[entity_id].position
        entities_in_radius = []

        # Getting all the positions in the radius.
        valid_pos = self.__get_positions_in_radius(entity_position, radius)

        # Getting all the entities in the radius.
        for entity in self.entities:
            if entity != entity_id:
                if self.entities[entity].position in valid_pos:
                    entities_in_radius.append(
                        (entity, self.entities[entity].position, self.distance(entity_id, entity)))

        return entities_in_radius

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
        # Get entity position from its id.
        entity_position = self.entities[entity_id].position

        # Getting all the positions in the radius.
        positions_in_radius = self.__get_positions_in_radius(
            entity_position, radius)
        terrain_in_radius = {}

        # Getting all the terrain in the positions.
        for pos in positions_in_radius:
            rep = self.world_map[pos]
            terrain_in_radius[pos] = self.terrain_types[rep]

        return terrain_in_radius

    def __get_positions_in_radius(self, entity_position, radius):
        positions = []
        for i in range(entity_position[0] - radius, entity_position[0] + radius + 1):
            for j in range(entity_position[1] - radius, entity_position[1] + radius + 1):
                if i >= 0 and j >= 0 and i < self.world_map.shape[0] and j < self.world_map.shape[1]:
                    positions.append((i, j))
                if self.finite:
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
        # Get entity position from its id.
        entity_position = self.entities[entity_id].position

        # Get the position of the target entity.
        other_entity_position = self.entities[other_entity_id].position

        vertical_distance = abs(entity_position[0] - other_entity_position[0])
        horizontal_distance = abs(entity_position[1] - other_entity_position[1])

        # If the world is finite the we calculate the position.
        if not self.finite:
            # In other case we check if the distance is shorter if we go through the other side of the world
            # [ ]: Fix this
            dist_vert_edges = (self.world_map.shape[0] - max(entity_position[0], other_entity_position[0])) + min(entity_position[0], other_entity_position[0])
            dist_hor_edges = (self.world_map.shape[1] - max(entity_position[1], other_entity_position[1])) + min(entity_position[1], other_entity_position[1])
            if vertical_distance > dist_vert_edges:
                vertical_distance = dist_vert_edges
            if horizontal_distance > dist_hor_edges:
                horizontal_distance = dist_hor_edges
        return vertical_distance + horizontal_distance
