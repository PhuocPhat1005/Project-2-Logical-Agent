import heapq
from utils.util import Action
from utils.util import GameState
from utils.util import Object


class Search:
    def __init__(self, graph, start, goals, visited_states, current_dir):
        self.start = start
        self.goals = goals
        self.visited_states = visited_states
        self.current_dir = current_dir
        self.graph = graph

    def ucs(self):
        pass
