class MoveNorth:
    def move_n(self, entity_id):
        # get entity position from its id
        entity_pos = self.entities[entity_id].position

        if entity_pos[0] == 0:
            if not self.finite:
                self.entities[entity_id] = (
                    self.world_map.shape[0], entity_pos[1])
        else:
            self.entities[entity_id] = (entity_pos[0] - 1, entity_pos[1])


class MoveSouth:
    def move_s(self, entity_id):
        # get entity position from its id
        entity_pos = self.entities[entity_id].position

        if entity_pos[0] == self.world_map.shape[0]:
            if not self.finite:
                self.entities[entity_id] = (0, entity_pos[1])
        else:
            self.entities[entity_id] = (entity_pos[0] + 1, entity_pos[1])


class MoveEast:
    def move_e(self, entity_id):
        # get entity position from its id
        entity_pos = self.entities[entity_id].position

        if entity_pos[1] == self.world_map.shape[1]:
            if not self.finite:
                self.entities[entity_id] = (entity_pos[0], 0)
        else:
            self.entities[entity_id] = (entity_pos[0], entity_pos[1] + 1)


class MoveWest:
    def move_w(self, entity_id):
        # get entity position from its id
        entity_pos = self.entities[entity_id].position

        if entity_pos[1] == 0:
            if not self.finite:
                self.entities[entity_id] = (
                    entity_pos[0], self.world_map.shape[1])
        else:
            self.entities[entity_id] = (entity_pos[0], entity_pos[1] - 1)


# TODO: Finite worlds exists
class SeeNorth:
    def see_n(self, entity_id):
        return lambda max_steps: self.__see_n(entity_id, max_steps)

    def __see_n(self, entity_id, max_steps):
        # get entity position from its id
        entity_pos = self.entities[entity_id].position
        next_pos = (entity_pos[0] - 1, entity_pos[1]) if entity_pos[0] > 0 else (
            self.world_map.shape[0], entity_pos[1])
        return self.see(entity_pos, next_pos, max_steps)

    def see(self, first_pos, current_pos, max_steps, current_step=1):
        # check if current_pos is in the edge of the world
        for entity in self.entities:
            if self.entities[entity].position == current_pos:
                return entity
        if current_step == max_steps:
            return None
        next_pos = (current_pos[0] - 1, current_pos[1]) if current_pos[0] > 0 else (
            self.world_map.shape[0], current_pos[1])
        return self.see(first_pos, next_pos, max_steps, current_step + 1)


class SeeSouth:
    def see_s(self, entity_id):
        return lambda max_steps: self.__see_s(entity_id, max_steps)

    def __see_s(self, entity_id, max_steps):
        # get entity position from its id
        entity_pos = self.entities[entity_id].position
        next_pos = (entity_pos[0] + 1, entity_pos[1]
                    ) if entity_pos[0] < self.world_map.shape[0] else (0, entity_pos[1])
        return self.see(entity_pos, next_pos, max_steps)

    def see(self, first_pos, current_pos, max_steps, current_step=1):
        # check if current_pos is in the edge of the world
        for entity in self.entities:
            if self.entities[entity].position == current_pos:
                return entity
        if current_step == max_steps:
            return None
        next_pos = (current_pos[0] + 1, current_pos[1]
                    ) if current_pos[0] < self.world_map.shape[0] else (0, current_pos[1])
        return self.see(first_pos, next_pos, max_steps, current_step + 1)


class SeeEast:
    def see_e(self, entity_id):
        return lambda max_steps: self.__see_e(entity_id, max_steps)

    def __see_e(self, entity_id, max_steps):
        # get entity position from its id
        entity_pos = self.entities[entity_id].position
        next_pos = (entity_pos[0], entity_pos[1] +
                    1) if entity_pos[1] < self.world_map.shape[1] else (entity_pos[0], 0)
        return self.see(entity_pos, next_pos, max_steps)

    def see(self, first_pos, current_pos, max_steps, current_step=1):
        # check if current_pos is in the edge of the world
        for entity in self.entities:
            if self.entities[entity].position == current_pos:
                return entity
        if current_step == max_steps:
            return None
        next_pos = (current_pos[0], current_pos[1] +
                    1) if current_pos[1] < self.world_map.shape[1] else (current_pos[0], 0)
        return self.see(first_pos, next_pos, max_steps, current_step + 1)


class SeeWest:
    def see_w(self, entity_id):
        return lambda max_steps: self.__see_w(entity_id, max_steps)

    def __see_w(self, entity_id, max_steps):
        # get entity position from its id
        entity_pos = self.entities[entity_id].position
        next_pos = (entity_pos[0], entity_pos[1] - 1) if entity_pos[1] > 0 else (
            entity_pos[0], self.world_map.shape[1])
        return self.see(entity_pos, next_pos, max_steps)

    def see(self, first_pos, current_pos, max_steps, current_step=1):
        # check if current_pos is in the edge of the world
        for entity in self.entities:
            if self.entities[entity].position == current_pos:
                return entity
        if current_step == max_steps:
            return None
        next_pos = (current_pos[0], current_pos[1] - 1) if current_pos[1] > 0 else (
            current_pos[0], self.world_map.shape[1])
        return self.see(first_pos, next_pos, max_steps, current_step + 1)

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
                    entities_in_radius.append(entity)

        return entities_in_radius

    # the radius is a square because the world is a np.array
    def __get_positions_in_radius(self, entity_position, radius):
        positions = []
        for i in range(entity_position[0] - radius, entity_position[0] + radius + 1):
            for j in range(entity_position[1] - radius, entity_position[1] + radius + 1):
                if i >= 0 and j >= 0 and i < self.world_map.shape[0] and j < self.world_map.shape[1]:
                    positions.append((i, j))
        return positions
