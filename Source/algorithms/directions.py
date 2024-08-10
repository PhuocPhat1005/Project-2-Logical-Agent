from enum import Enum


# Enum for Directions the agent can face
class Directions(Enum):
    UP = "up"
    RIGHT = "right"
    DOWN = "down"
    LEFT = "left"

    @staticmethod
    def turn_left(current_direction):
        turn_left_mapping = {
            Directions.UP: Directions.LEFT,
            Directions.LEFT: Directions.DOWN,
            Directions.DOWN: Directions.RIGHT,
            Directions.RIGHT: Directions.UP,
        }
        return turn_left_mapping[current_direction]

    @staticmethod
    def turn_right(current_direction):
        turn_right_mapping = {
            Directions.UP: Directions.RIGHT,
            Directions.RIGHT: Directions.DOWN,
            Directions.DOWN: Directions.LEFT,
            Directions.LEFT: Directions.UP,
        }
        return turn_right_mapping[current_direction]

    @staticmethod
    def get_movement_vector(current_direction):
        movement_vectors = {
            Directions.UP: (0, -1),
            Directions.RIGHT: (1, 0),
            Directions.DOWN: (0, 1),
            Directions.LEFT: (-1, 0),
        }
        return movement_vectors[current_direction]
