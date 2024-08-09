from algorithms.program import Program
from algorithms.node import Node


class State:
    def __init__(self, map: Program):
        self.max_row = map.map_size
        self.max_height = map.map_size
        self.state = dict()
        self.visited = []
        self.unvisited_safe = []

    def add_state(self, node: Node):
        if node.left == "":
            node.left == "Wall"
        if node.right == "":
            node.right == "Wall"
        if node.up == "":
            node.up == "Wall"
        if node.down == "":
            node.down == "Wall"
        self.state[node.name] = node
        if node.name not in self.visited:
            self.visited.append(node.name)
