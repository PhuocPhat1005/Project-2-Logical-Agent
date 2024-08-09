from algorithms.program import Program


class Node:
    def __init__(self, y, x, map: Program):
        self.name = str(y) + "," + str(x)
        self.y = y  # y is row index
        self.x = x  # x is column index
        adjacents = map.get_adjacent(y, x)
        self.left = ""
        self.right = ""
        self.up = ""
        self.down = ""
        for adjacent in adjacents:
            if adjacent[0] == y - 1:
                self.up = str(adjacent[0]) + "," + str(adjacent[1])
            if adjacent[0] == y + 1:
                self.down = str(adjacent[0]) + "," + str(adjacent[1])
            if adjacent[0] == x - 1:
                self.left = str(adjacent[0]) + "," + str(adjacent[1])
            if adjacent[0] == x + 1:
                self.right = str(adjacent[0]) + "," + str(adjacent[1])
