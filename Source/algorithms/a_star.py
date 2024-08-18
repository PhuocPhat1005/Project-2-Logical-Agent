import heapq


def create_graph(list_cell, map_size):
    graph = []
    for i in range(map_size):
        graph.append([])
        for _ in range(map_size):
            graph[i].append(-1)

    for cell in list_cell:
        graph[cell[0]][cell[1]] = 1

    return graph


def a_star(graph, start, goal, agent, program):
    map_size = len(graph[0])
    visited = []
    cost = []
    parent = []

    tmp_heal = []

    for i in range(map_size):
        visited.append([])
        cost.append([])
        parent.append([])
        for _ in range(map_size):
            visited[i].append(False)
            cost[i].append(float("inf"))
            parent[i].append((-1, -1))

    cost[start[0]][start[1]] = 0
    frontier = [
        (
            100 if start in agent.sure_poison else 0,
            start,
            agent.current_hp,
            agent.healing_potion,
        )
    ]

    direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    prev = (-1, -1)
    while frontier:
        _, current, hp, potion = heapq.heappop(frontier)
        if visited[current[0]][current[1]]:
            continue
        visited[current[0]][current[1]] = True
        if current != start:
            if current in agent.sure_poison:
                if hp == 25:
                    if potion > 0:
                        potion -= 1
                        hp += 25
                        tmp_heal.append(current)
                    else:
                        continue

            if "P_G" in program.cells[current[0]][current[1]].element:
                hp -= 25
                if hp <= 0:
                    graph[current[0]][current[1]] = -1
                    continue

        for dy, dx in direction:
            ny, nx = current[0] + dy, current[1] + dx
            if 0 <= ny < map_size and 0 <= nx < map_size:
                if not visited[ny][nx] and graph[ny][nx] != -1:
                    new_cost = cost[current[0]][current[1]] + 1
                    if new_cost < cost[ny][nx]:
                        cost[ny][nx] = new_cost
                        parent[ny][nx] = current
                        new_f = (
                            abs(ny - goal[0])
                            + abs(nx - goal[1])
                            + (100 if (ny, nx) in agent.sure_poison else 0)
                        )  # heuristic -> l2 dis
                        if (prev[0] - current[0]) * (current[0] - ny) + (
                            prev[1] - current[1]
                        ) * (current[1] - nx) == 0:
                            new_f += (
                                10  # update -> huong vuong goc -> day heu -> ko uu tien
                            )
                        heapq.heappush(frontier, (new_f, (ny, nx), hp, potion))

        if visited[goal[0]][goal[1]]:
            agent.current_hp = hp
            agent.healing_potion = potion
            break
        prev = current

    if not visited[goal[0]][goal[1]]:
        return []

    path = []
    while goal != start:
        path.append(goal)
        goal = parent[goal[0]][goal[1]]
    path.append(start)
    path.reverse()

    for cell in tmp_heal:
        if cell in path:
            agent.heal.append(cell)

    return path
