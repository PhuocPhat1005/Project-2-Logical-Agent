from enum import Enum


# Enum cho các Hướng mà agent có thể đối mặt
class Directions(Enum):
    # Định nghĩa các hướng có thể có mà agent có thể đối mặt
    UP = "up"  # Lên
    RIGHT = "right"  # Phải
    DOWN = "down"  # Xuống
    LEFT = "left"  # Trái

    @staticmethod
    def turn_left(current_direction):
        """
        Dựa trên hướng hiện tại, trả về hướng sau khi rẽ trái.

        :param current_direction: Hướng hiện tại của agent.
        :return: Hướng mới sau khi rẽ trái.
        """
        # Định nghĩa bảng ánh xạ từ hướng hiện tại sang hướng mới khi rẽ trái
        turn_left_mapping = {
            Directions.UP: Directions.LEFT,  # Rẽ trái từ UP (Lên) sẽ thành LEFT (Trái)
            Directions.LEFT: Directions.DOWN,  # Rẽ trái từ LEFT (Trái) sẽ thành DOWN (Xuống)
            Directions.DOWN: Directions.RIGHT,  # Rẽ trái từ DOWN (Xuống) sẽ thành RIGHT (Phải)
            Directions.RIGHT: Directions.UP,  # Rẽ trái từ RIGHT (Phải) sẽ thành UP (Lên)
        }
        return turn_left_mapping[current_direction]

    @staticmethod
    def turn_right(current_direction):
        """
        Dựa trên hướng hiện tại, trả về hướng sau khi rẽ phải.

        :param current_direction: Hướng hiện tại của agent.
        :return: Hướng mới sau khi rẽ phải.
        """
        # Định nghĩa bảng ánh xạ từ hướng hiện tại sang hướng mới khi rẽ phải
        turn_right_mapping = {
            Directions.UP: Directions.RIGHT,  # Rẽ phải từ UP (Lên) sẽ thành RIGHT (Phải)
            Directions.RIGHT: Directions.DOWN,  # Rẽ phải từ RIGHT (Phải) sẽ thành DOWN (Xuống)
            Directions.DOWN: Directions.LEFT,  # Rẽ phải từ DOWN (Xuống) sẽ thành LEFT (Trái)
            Directions.LEFT: Directions.UP,  # Rẽ phải từ LEFT (Trái) sẽ thành UP (Lên)
        }
        return turn_right_mapping[current_direction]

    @staticmethod
    def get_movement_vector(current_direction):
        """
        Dựa trên hướng hiện tại, trả về vector di chuyển cho hướng đó.

        :param current_direction: Hướng hiện tại của agent.
        :return: Một tuple đại diện cho vector di chuyển (dx, dy) cho hướng đó.
        """
        # Định nghĩa các vector di chuyển cho mỗi hướng
        movement_vectors = {
            Directions.UP: (-1, 0),  # Di chuyển UP (Lên) giảm giá trị y-coordinate
            Directions.RIGHT: (
                0,
                1,
            ),  # Di chuyển RIGHT (Phải) tăng giá trị x-coordinate
            Directions.DOWN: (1, 0),  # Di chuyển DOWN (Xuống) tăng giá trị y-coordinate
            Directions.LEFT: (0, -1),  # Di chuyển LEFT (Trái) giảm giá trị x-coordinate
        }
        return movement_vectors[current_direction]
