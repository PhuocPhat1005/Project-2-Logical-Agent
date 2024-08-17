from algorithms.program import Program
from algorithms.a_star import a_star, create_graph
import copy
import heapq


# Agent class definition
class Agent:
    def __init__(self, map_size=10):
        self.x = 0  # chi so cot hien tai cua agent
        self.y = 0  # chi so hang hien tai cua agent
        self.current_hp = 100  # luong mau default
        self.map_size = map_size  # kich thuoc map hien tai
        self.direction = (1, 0)

        self.knowledge_base_pit_percept = []
        self.knowledge_base_wumpus_percept = []
        self.knowledge_base_poison_percept = []
        self.knowledge_base_health_percept = []  # bo cung duoc, k can thiet lam

        self.maybe_wumpus = []
        self.maybe_poison = []
        self.maybe_pit = []
        self.maybe_health = []  # bo cung duoc, k can thiet lam

        self.sure_wumpus = []
        self.sure_poison = []
        self.sure_pit = []
        self.sure_health = []  # bo cung duoc, k can thiet lam

        self.healing_potion = 0  # so luong healing potion dang nam giu hien tai
        self.point = 0  # so diem hien tai cua agent
        self.path = []

        # action
        self.grab_heal = []
        self.grab_gold = []
        self.heal = []
        self.shoot_act = []

    def check_have_wumpus(self, y, x, cell=None):
        # print("Knownledge base wumpus: ", self.knowledge_base_wumpus_percept)
        # print("@@@")
        if (y, x) == (0, 0):
            return False
        if cell is not None:
            if not cell.is_stench or (y, x) in self.path:
                return False
        else:
            if (y, x) in self.path:
                return False

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if 0 <= ny <= self.map_size - 1 and 0 <= nx <= self.map_size - 1:
                if (ny, nx) not in self.knowledge_base_wumpus_percept and (
                    ny,
                    nx,
                ) in self.path:
                    return False
        # print("May Wumpus at: ", y, x)
        self.maybe_wumpus.append((y, x))
        return True

    def check_have_pit(self, y, x, cell):
        if (y, x) == (0, 0):
            return False
        if not cell.is_breeze or (y, x) in self.path:
            return False
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if 0 <= ny <= self.map_size - 1 and 0 <= nx <= self.map_size - 1:
                if (ny, nx) not in self.knowledge_base_pit_percept and (
                    ny,
                    nx,
                ) in self.path:
                    return False
        # print("May Pit at: ", y, x)
        self.maybe_pit.append((y, x))
        return True

    def check_have_poison(self, y, x, cell):
        if (y, x) == (0, 0):
            return False
        if not cell.is_whiff or (y, x) in self.path:
            return False
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if 0 <= ny <= self.map_size - 1 and 0 <= nx <= self.map_size - 1:
                if (ny, nx) not in self.knowledge_base_poison_percept and (
                    ny,
                    nx,
                ) in self.path:
                    return False
        # print("May Poison at: ", y, x)
        self.maybe_poison.append((y, x))
        return True

    def check_have_healing(self, y, x, cell):
        if not cell.is_glow or (y, x) in self.path:
            return False
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            if 0 <= ny <= self.map_size - 1 and 0 <= nx <= self.map_size - 1:
                if (ny, nx) not in self.knowledge_base_health_percept and (
                    ny,
                    nx,
                ) in self.path:
                    return False
        # print("May Healing at: ", y, x)
        self.maybe_health.append((y, x))
        return True

    def check_no_safe(self, y, x, cell):
        return self.check_have_pit(y, x, cell) or self.check_have_wumpus(y, x, cell)

    def dfs(self, program):
        """Perform a DFS to explore the map based on current knowledge."""
        frontier = [(self.y, self.x)]  # Initialize the frontier with the current cell

        directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]

        while frontier:  # While there are cells to explore
            # print(frontier)
            # print("Current hp: ", self.current_hp)

            current_y, current_x = frontier.pop()  # Pop the last cell from the frontier

            if self.check_have_poison(
                current_y, current_x, program.cells[self.y][self.x]
            ):
                if self.current_hp == 25:
                    if self.healing_potion == 0:
                        continue
                    self.heal.append((self.y, self.x))
                    self.healing_potion -= 1
                    self.healing_potion = max(self.healing_potion, 0)
                    self.current_hp += 25

            if program.cells[current_y][current_x].is_visited:
                continue

            self.y, self.x = (
                current_y,
                current_x,
            )  # Update agent's current position, agent move to new position
            program.cells[self.y][self.x].is_visited = True
            self.path.append((self.y, self.x))

            if "P_G" in program.cells[self.y][self.x].element:
                self.sure_poison.append((self.y, self.x))
                self.current_hp -= 25
                if self.current_hp <= 0:
                    return []

            if program.cells[self.y][self.x].is_breeze:
                self.knowledge_base_pit_percept.append((self.y, self.x))
            if program.cells[self.y][self.x].is_stench:
                self.knowledge_base_wumpus_percept.append((self.y, self.x))
            if program.cells[self.y][self.x].is_whiff:
                self.knowledge_base_poison_percept.append((self.y, self.x))
            if program.cells[self.y][self.x].is_glow:
                self.knowledge_base_health_percept.append((self.y, self.x))

            # print("Current position: ", self.y, self.x)

            if "H_P" in program.cells[self.y][self.x].element:
                self.healing_potion += 1
                program.cells[self.y][self.x].element.remove("H_P")
                if program.cells[self.y][self.x].element == []:
                    program.cells[self.y][self.x].element.append("-")
                for dy, dx in directions:
                    ny, nx = self.y + dy, self.x + dx
                    if (
                        0 <= ny <= program.map_size - 1
                        and 0 <= nx <= program.map_size - 1
                    ):
                        program.cells[ny][nx].is_glow = False
                        for dyy, dxx in directions:
                            nyy, nxx = ny + dyy, nx + dxx
                            if (
                                0 <= nyy <= program.map_size - 1
                                and 0 <= nxx <= program.map_size - 1
                            ):
                                if "H_P" in program.cells[nyy][nxx].element:
                                    program.cells[ny][nx].is_glow = True
                                    break

                self.grab_heal.append((self.y, self.x))
                program.MAPS.append(copy.deepcopy(program.cells))

            if "G" in program.cells[self.y][self.x].element:
                self.grab_gold.append((self.y, self.x))
                program.cells[self.y][self.x].element.remove("G")
                if program.cells[self.y][self.x].element == []:
                    program.cells[self.y][self.x].element.append("-")
                program.MAPS.append(copy.deepcopy(program.cells))

            for dy, dx in directions:
                ny, nx = current_y + dy, current_x + dx
                if 0 <= ny <= program.map_size - 1 and 0 <= nx <= program.map_size - 1:
                    if not program.cells[ny][nx].is_visited:
                        if not self.check_no_safe(
                            ny, nx, program.cells[current_y][current_x]
                        ):
                            frontier.append((ny, nx))

        return self.path

    def go_to_shoot(self, i, program):
        tmp_graph = create_graph(self.path, self.map_size)
        tmp_move = []
        direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dy, dx in direction:
            ny, nx = self.sure_wumpus[i][0] + dy, self.sure_wumpus[i][1] + dx
            if 0 <= ny < self.map_size and 0 <= nx < self.map_size:
                tmp_path = a_star(tmp_graph, (self.y, self.x), (ny, nx), self, program)
                if tmp_path != []:
                    if len(tmp_path) < len(tmp_move) or tmp_move == []:
                        tmp_move = tmp_path

        # print("Tmp move: ", tmp_move)
        self.path.extend(tmp_move)
        return tmp_move[-1]

    def shoot(self, ny, nx, program):
        # print("Shoot at ", ny, nx)
        # shoot_correct = False
        # if 'W' in program.cells[ny][nx].element:
        #     shoot_correct = True
        try:
            program.cells[ny][nx].element.remove("W")
            if program.cells[ny][nx].element == []:
                program.cells[ny][nx].element.append("-")
            program.reset_percepts(ny, nx)
            program.add_to_adjacent(ny, nx, "Shoot_wumpus")
        except:
            pass
        self.point -= 100
        # if shoot_correct:
        #     program.add_to_adjacent(ny, nx, "Kill_wumpus")

        # program.display_map_test()
        # print("||||||||")
        return program.cells

    def shoot_process(self, program, graph):
        direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        # non_visit = self.sure_wumpus
        for i, cell in enumerate(self.sure_wumpus):
            # MIN = 10**2 * 10**2 + 1
            # BEST_CELL = (-1, -1)
            # for cell2 in self.sure_wumpus:
            #     l2 = (cell2[0] - self.y) ** 2 + (cell2[1] - self.x) ** 2
            #     if l2 < MIN and cell2 in non_visit:
            #         MIN = l2
            #         BEST_CELL = cell2
            # cell2 = BEST_CELL
            # if cell2 == (-1, -1):
            #     return
            # non_visit.remove(cell2)
            if not self.check_have_wumpus(cell[0], cell[1]) or self.check_have_pit(
                cell[0], cell[1], program.cells[self.y][self.x]
            ):
                continue
            y, x = self.go_to_shoot(i, program)
            flag = True
            while flag:
                self.shoot_act.append(((y, x), cell))
                new_map = self.shoot(cell[0], cell[1], program)
                program.MAPS.append(copy.deepcopy(new_map))

                if not program.cells[y][x].is_scream:
                    flag = False

                program.reset_percepts(cell[0], cell[1])
                for dy, dx in direction:
                    ny, nx = cell[0] + dy, cell[1] + dx
                    if 0 <= ny <= self.map_size - 1 and 0 <= nx <= self.map_size - 1:
                        for dyy, dxx in direction:
                            nyy, nxx = ny + dyy, nx + dxx
                            if (
                                0 <= nyy <= self.map_size - 1
                                and 0 <= nxx <= self.map_size - 1
                            ):
                                if "W" in program.cells[nyy][nxx].element:
                                    program.cells[ny][nx].is_stench = True
                                    break

                program.MAPS.append(copy.deepcopy(program.cells))
                # program.display_map_test()
                # print("/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/")

            # for dy, dx in direction:
            #     ny, nx = cell[0] + dy, cell[1] + dx
            #     if 0 <= ny <= self.map_size - 1 and 0 <= nx <= self.map_size - 1:
            #         try:
            #             if not program.cells[ny][nx].is_stench:
            #                 self.knowledge_base_wumpus_percept.remove((ny, nx))
            #         except:
            #             pass

            self.y = cell[0]
            self.x = cell[1]
            graph[self.y][self.x] = 1
            self.dfs(program)
            for cell in self.path:
                graph[cell[0]][cell[1]] = 1
