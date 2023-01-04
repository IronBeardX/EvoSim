class MoveNorth:
    def move_n(self, entity_id):
        # get entity position from its id
        entity_pos = self.entities[entity_id].position
        north_pos = (entity_pos[0] - 1, entity_pos[1])

        # check current position is terrain type water
        if self.get_terrain_type(entity_pos) == "water":
            # TODO: Raise exception for water tile
            return False


        # check if the entity is in a finite world
        if north_pos[0] < 0:
            if self.finite:
                north_pos = (self.world_map.shape[0]-1, entity_pos[1])
            else:
                # TODO: Raise exception for border tile 
                return False
        
        # Check if the entity can coexist with another entities
        north_entities = self.get_entity_by_position(north_pos)
        north_entities = [self.entities[x].coexist for x in north_entities] 
        if self.entities[entity_id].coexist == False and any ([not x for x in north_entities]):
            # TODO: Raise exception for entity collision
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
            # TODO: Raise exception for water tile
            return False


        # check if the entity is in a finite world
        if south_pos[0] < 0:
            if self.finite:
                south_pos = (0, entity_pos[1])
            else:
                # TODO: Raise exception for border tile 
                return False
        
        # Check if the entity can coexist with another entities
        south_entities = self.get_entity_by_position(south_pos)
        south_entities = [self.entities[x].coexist for x in south_entities] 
        if self.entities[entity_id].coexist == False and any ([not x for x in south_entities]):
            # TODO: Raise exception for entity collision
            return False

        self.entities[entity_id].position = south_pos
        return True
class MoveEast:
    def move_e(self, entity_id):
        # get entity position from its id
        entity_pos = self.entities[entity_id].position
        east_pos = (entity_pos[0] + 1, entity_pos[1])

        # check current position is terrain type water
        if self.get_terrain_type(entity_pos) == "water":
            # TODO: Raise exception for water tile
            return False


        # check if the entity is in a finite world
        if east_pos[0] < 0:
            if self.finite:
                east_pos = (0, entity_pos[1])
            else:
                # TODO: Raise exception for border tile 
                return False
        
        # Check if the entity can coexist with another entities
        east_entities = self.get_entity_by_position(east_pos)
        east_entities = [self.entities[x].coexist for x in east_entities] 
        if self.entities[entity_id].coexist == False and any ([not x for x in east_entities]):
            # TODO: Raise exception for entity collision
            return False

        self.entities[entity_id].position = east_pos
        return True
class MoveWest:
    def move_w(self, entity_id):
        # get entity position from its id
        entity_pos = self.entities[entity_id].position
        west_pos = (entity_pos[0] + 1, entity_pos[1])

        # check current position is terrain type water
        if self.get_terrain_type(entity_pos) == "water":
            # TODO: Raise exception for water tile
            return False


        # check if the entity is in a finite world
        if west_pos[0] < 0:
            if self.finite:
                west_pos = (0, entity_pos[1])
            else:
                # TODO: Raise exception for border tile 
                return False
        
        # Check if the entity can coexist with another entities
        west_entities = self.get_entity_by_position(west_pos)
        west_entities = [self.entities[x].coexist for x in west_entities] 
        if self.entities[entity_id].coexist == False and any ([not x for x in west_entities]):
            # TODO: Raise exception for entity collision
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
            # TODO: Raise exception for water tile
            return False


        # check if the entity is in a finite world
        if north_pos[0] < 0:
            if self.finite:
                north_pos = (self.world_map.shape[0]-1, entity_pos[1])
            else:
                # TODO: Raise exception for border tile 
                return False
        
        # Check if the entity can coexist with another entities
        north_entities = self.get_entity_by_position(north_pos)
        north_entities = [self.entities[x].coexist for x in north_entities] 
        if self.entities[entity_id].coexist == False and any ([not x for x in north_entities]):
            # TODO: Raise exception for entity collision
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
            # TODO: Raise exception for water tile
            return False


        # check if the entity is in a finite world
        if south_pos[0] < 0:
            if self.finite:
                south_pos = (0, entity_pos[1])
            else:
                # TODO: Raise exception for border tile 
                return False
        
        # Check if the entity can coexist with another entities
        south_entities = self.get_entity_by_position(south_pos)
        south_entities = [self.entities[x].coexist for x in south_entities] 
        if self.entities[entity_id].coexist == False and any ([not x for x in south_entities]):
            # TODO: Raise exception for entity collision
            return False

        self.entities[entity_id].position = south_pos
        return True



class SwimEast:
    def swim_e(self, entity_id):
        # get entity position from its id
        entity_pos = self.entities[entity_id].position
        east_pos = (entity_pos[0] + 1, entity_pos[1])

        # check current position is terrain type water
        if self.get_terrain_type(entity_pos) != "water":
            # TODO: Raise exception for water tile
            return False


        # check if the entity is in a finite world
        if east_pos[0] < 0:
            if self.finite:
                east_pos = (0, entity_pos[1])
            else:
                # TODO: Raise exception for border tile 
                return False
        
        # Check if the entity can coexist with another entities
        east_entities = self.get_entity_by_position(east_pos)
        east_entities = [self.entities[x].coexist for x in east_entities] 
        if self.entities[entity_id].coexist == False and any ([not x for x in east_entities]):
            # TODO: Raise exception for entity collision
            return False

        self.entities[entity_id].position = east_pos
        return True
        
    

class SwimWest:
    def swim_w(self, entity_id):
        # get entity position from its id
        entity_pos = self.entities[entity_id].position
        west_pos = (entity_pos[0] + 1, entity_pos[1])

        # check current position is terrain type water
        if self.get_terrain_type(entity_pos) != "water":
            # TODO: Raise exception for water tile
            return False


        # check if the entity is in a finite world
        if west_pos[0] < 0:
            if self.finite:
                west_pos = (0, entity_pos[1])
            else:
                # TODO: Raise exception for border tile 
                return False
        
        # Check if the entity can coexist with another entities
        west_entities = self.get_entity_by_position(west_pos)
        west_entities = [self.entities[x].coexist for x in west_entities] 
        if self.entities[entity_id].coexist == False and any ([not x for x in west_entities]):
            # TODO: Raise exception for entity collision
            return False

        self.entities[entity_id].position = west_pos
        return True


# TODO: Finite worlds exists

# TODO: Check if copilot hit the bullseye
class SeeRadius:
    def see_r(self, entity_id):
        return lambda radius: self.__see_r(entity_id, radius)

    def __see_r(self, entity_id, radius):
        # get entity position from its id
        entity_position = self.entities[entity_id].position
        entities_in_radius = []
        for entity in self.entities:
            if entity != entity_id:
                if self.entities[entity].position in self.__get_positions_in_radius(entity_position, radius):
                    entities_in_radius.append((entity, self.entities[entity].position))

        return entities_in_radius

    # the radius is a square because the world is a np.array
    def __get_positions_in_radius(self, entity_position, radius):
        positions = []
        for i in range(entity_position[0] - radius, entity_position[0] + radius + 1):
            for j in range(entity_position[1] - radius, entity_position[1] + radius + 1):
                if i >= 0 and j >= 0 and i < self.world_map.shape[0] and j < self.world_map.shape[1]:
                    positions.append((i, j))
        return positions
