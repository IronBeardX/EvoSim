class WorldActions:

    def _move_to(self, entity_id, direction: tuple[int,int], allow_water: bool = False):
        entity_pos = self.entities[entity_id].position
        new_pos = (entity_pos[0] + direction[0], entity_pos[1] + direction[1])

        if self.get_terrain_type(entity_pos) == "water" and not allow_water:
            return False
        # Check if the entity is in a finite world
        if self.finite:
            return self.world_map.valid_position(new_pos)
        else:
            new_pos = (new_pos[0] % self.world_map.shape[0], new_pos[1] % self.world_map.shape[1])
        # Check if the entity can coexist with another entities
        new_entities = self.get_entities_in_position(new_pos)
        new_entities = [entityInfo.entity.coexistence for entityInfo in new_entities]
        if self.entities[entity_id].entity.coexistence == False and any([not x for x in new_entities]):
            return False

        # self.entities[entity_id].position = new_pos
        self.move_entity(entity_id, new_pos)
        return True

    # Moves the entity with id entity_id one position north if its not currently standing on water
    def move_n(self, entity_id):
        # get entity position from its id
        return self._move_to(entity_id, (-1, 0))

    # Moves the entity with id entity_id one position south if its not currently standing on water
    def move_s(self, entity_id):
        # get entity position from its id
        return self._move_to(entity_id, (1, 0))

    # Moves the entity with id entity_id one position east if its not currently standing on water
    def move_e(self, entity_id):
        # get entity position from its id
        return self._move_to(entity_id, (0, 1))

    # Moves the entity with id entity_id one position west if its not currently standing on water
    def move_w(self, entity_id):
        # get entity position from its id
        return self._move_to(entity_id, (0, -1))

    # Moves the entity with id entity_id one position north if its currently standing on water
    def swim_n(self, entity_id):
        # get entity position from its id
        return self._move_to(entity_id, (-1, 0), allow_water=True)

    # Moves the entity with id entity_id one position south if its currently standing on water
    def swim_s(self, entity_id):
        # get entity position from its id
        return self._move_to(entity_id, (1, 0), allow_water=True)

    # Moves the entity with id entity_id one position east if its currently standing on water
    def swim_e(self, entity_id):
        # get entity position from its id
        return self._move_to(entity_id, (0, 1), allow_water=True)

    # Moves the entity with id entity_id one position west if its currently standing on water
    def swim_w(self, entity_id):
        # get entity position from its id
        return self._move_to(entity_id, (0, -1), allow_water=True)

    # Returns a list with the ids of all entities in the radius
    def see_r(self, entity_id, radius):
        # get entity position from its id
        entity_position = self.entities[entity_id].position
        entities_in_radius = []
        valid_pos = self.__get_positions_in_radius(entity_position, radius)
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

    '''
    Returns a portion of the map with shape (2*radius + 1, 2*radius + 1) centered in the entity
    note: if the world is not finite this is not an exact copy of the map:
    _e_
    ___
    ___
    should return:
    ___
    _e_
    ___
    note 2 also check that the map is not repeated:
    with radius 2 the returning portion of the map for the previous case should be the same
    '''
    def terrain_r(self, entity_id, radius):
        entity_position = self.entities[entity_id].position
        positions_in_radius = self.__get_positions_in_radius(
            entity_position, radius)
        terrain_in_radius = {}
        for pos in positions_in_radius:
            worldTile = self.world_map[pos]
            terrain_in_radius[pos] = self.terrain_types[worldTile.get_terrain()]

        # terrain_in_radius = [self.world_map[pos] for pos in terrain_in_radius]
        #  # self.world_map["position"]
        # terrain_in_radius = [self.terrain_types[rep] for rep in terrain_in_radius]
        # # self.terrain_types["rep"]
        return terrain_in_radius

    # Returns the manhattan distance between two entities
    def distance(self, entity_id, other_entity_id):
        # This should return a correct value if the world is not finite
        entity_position = self.entities[entity_id].position
        other_entity_position = self.entities[other_entity_id].position
        if self.finite:
            return abs(entity_position[0] - other_entity_position[0]) + abs(entity_position[1] - other_entity_position[1])
        else:
            # Check if the distance is shorter if we go through the other side of the world
            if abs(entity_position[0] - other_entity_position[0]) > self.world_map.shape[0] / 2:
                if entity_position[0] > other_entity_position[0]:
                    entity_position = (
                        entity_position[0] - self.world_map.shape[0], entity_position[1])
                else:
                    other_entity_position = (
                        other_entity_position[0] - self.world_map.shape[0], other_entity_position[1])
            if abs(entity_position[1] - other_entity_position[1]) > self.world_map.shape[1] / 2:
                if entity_position[1] > other_entity_position[1]:
                    entity_position = (
                        entity_position[0], entity_position[1] - self.world_map.shape[1])
                else:
                    other_entity_position = (
                        other_entity_position[0], other_entity_position[1] - self.world_map.shape[1])
            return abs(entity_position[0] - other_entity_position[0]) + abs(entity_position[1] - other_entity_position[1])
