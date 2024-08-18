from algorithms.program import Program
from algorithms.agent import Agent
from algorithms.a_star import create_graph, a_star
import copy
from ui import main_ui

def main():
    choose_map_result = main_ui.showMenu() + 1
    file_path = f"input/map{choose_map_result}.txt"
    program = Program(file_path)
    ma = program.return_map_test()
    map = copy.deepcopy(ma)
    # print("_________________________")
    # for i in range(len(map)):
    #     for j in range(len(map[i])):
    #         print(map[i][j], end=" ")
    #     print()
    program.MAPS.append(copy.deepcopy(program.cells))
    agent = Agent(map_size=program.map_size)
    # program.display_map_test()
    agent.dfs(program)
    
    for cell in agent.maybe_wumpus:
        if cell not in agent.path and cell not in agent.sure_wumpus:
            agent.sure_wumpus.append(cell)
            
    for cell in agent.maybe_pit:
        if cell not in agent.path and cell not in agent.sure_pit:
            agent.sure_pit.append(cell)
            
    # for cell in agent.maybe_poison:
    #         agent.sure_poison.append(cell)
            
    # for cell in agent.maybe_health:
    #         agent.sure_health.append(cell)
    # print("Path: ", agent.path)
    # print("With all information, we have: ")
    # print("Sure Wumpus: ", agent.sure_wumpus)
    # print("Sure Pit: ", agent.sure_pit)
    # print("Sure Health: ", agent.sure_health)
    

    
    graph1 = create_graph(agent.path, agent.map_size)
    graph2 = create_graph(agent.path, agent.map_size)
    agent.shoot_process(program, graph1)
    # print(len(agent.path))
    agent.path.append((0, 0)) #quay ve o (0,0)
    # print("Shoot:", agent.shoot_act)
    # print("Sure Wumpus:", agent.sure_wumpus)
    print("Sure poison:", agent.sure_poison)
    print("Heal:", agent.heal)
    agent.current_hp = 100
    tmp_poition = 0
    tmp_hp = 100
    primary_path = []
    main_ui.showWumpusWorld(choose_map_result, map)
    for i in range(len(agent.path) - 1):
        path_with_info = []
        current = agent.path[i]
        nextt = agent.path[i+1]
        tmp_path = a_star(graph2, current, nextt, agent, program)
        if tmp_path == []:
            graph2 = graph1
            tmp_path = a_star(graph2, current, nextt, agent, program)
        # print("current: ", current)
        # print("nextt: ", nextt)
        # print("tmp_path: ", tmp_path)
        # print("current_hp: ", agent.current_hp)
        # print()
        for j in range(len(tmp_path) - 1):
            action = []
            tmp_hp = agent.current_hp
            if tmp_path[j] in agent.grab_gold:
                action.append("Grab Gold")
                agent.grab_gold.remove(tmp_path[j])
            if tmp_path[j] in agent.grab_heal:
                action.append("Grab Heal")
                agent.grab_heal.remove(tmp_path[j])
                tmp_poition += 1
            vect = tmp_path[j+1][0] - tmp_path[j][0], tmp_path[j+1][1] - tmp_path[j][1]
            if (vect[0] * agent.direction[0]) + (vect[1] * agent.direction[1]) == 0:
                if agent.direction == (1, 0):
                    if vect == (0, 1):
                        action.append("Turn Right")
                    else:
                        action.append("Turn Left")
                elif agent.direction == (-1, 0):
                    if vect == (0, 1):
                        action.append("Turn Left")
                    else:
                        action.append("Turn Right")
                elif agent.direction == (0, 1):
                    if vect == (1, 0):
                        action.append("Turn Left")
                    else:
                        action.append("Turn Right")
                else:
                    if vect == (1, 0):
                        action.append("Turn Right")
                    else:
                        action.append("Turn Left")    
                agent.direction = vect  
            else:
                if (vect[0] * agent.direction[0]) + (vect[1] * agent.direction[1]) == -1:
                    action.append("Turn Left")
                    action.append("Turn Left")
                    agent.direction = (-1 * agent.direction[0], -1 * agent.direction[1])
                # else:
                    # action.append([])
                    
            if (tmp_path[j], tmp_path[j + 1]) in agent.shoot_act:
                while (tmp_path[j], tmp_path[j + 1]) in agent.shoot_act:
                    action.append("Shoot")
                    agent.shoot_act.remove((tmp_path[j], tmp_path[j + 1]))
                graph2[tmp_path[j][0]][tmp_path[j][1]] = 1

            if tmp_hp == 25:
                if tmp_path[j] in agent.heal and tmp_poition > 0 and tmp_path[j+1] in agent.sure_poison:
                    action.append("Heal")
                    agent.heal.remove(tmp_path[j])
                    tmp_poition -= 1
                    tmp_hp += 25
                    
            action.append("Move Forward")
            
            path_with_info.append((tmp_path[j], action, tmp_hp, tmp_poition))
        if path_with_info != []:
            primary_path.append((path_with_info))
            
    if primary_path[-1][-1][0] == (0, 1) or primary_path[-1][-1][0] == (1, 0):
        path_with_info = []
        path_with_info.append(((0, 0), ["Climb"], primary_path[-1][-1][2], primary_path[-1][-1][3]))
        primary_path.append((path_with_info))
    

    # print("primary_path for FE: ")
    # print(primary_path)
    # for path in primary_path:
    #     for cell in path:
    #         print(cell)
    agent.point = 10000
    RESULT = []
    map_index = 0
    for path in primary_path:
        for cell in path:
            for act in cell[1]:
                if act == "Climb":
                    agent.point += 10
                elif act == "Shoot":
                    agent.point -= 100
                    map_index += 1
                    RESULT.append((cell[0], act, agent.point, cell[2], cell[3], map_index))
                    map_index += 1
                    RESULT.append((cell[0], act, agent.point, cell[2], cell[3], map_index))
                    continue
                elif act == "Grab Gold":
                    agent.point += 5000
                    map_index += 1
                elif act == "Grab Heal":
                    agent.point -= 10
                    map_index += 1
                else:
                    agent.point -= 10
                RESULT.append((cell[0], act, agent.point, cell[2], cell[3], map_index))
    # RESULT.append(((0, 0), "Climb", agent.current_hp, agent.healing_potion))
    # print("RESULT: ")
    # for cell in RESULT:
    #     print(cell)
    # for all_cells in program.MAPS:
    #     for row_cell in all_cells:
    #         for cell in row_cell:
    #             print(
    #                 "[",
    #                 cell.element,
    #                 "T" if cell.is_stench else "F",
    #                 # "T" if cell.is_breeze else "F",
    #                 # "T" if cell.is_whiff else "F",
    #                 # "T" if cell.is_glow else "F",
    #                 # "T" if cell.is_scream else "F",
    #                 "]",
    #                 end=" ",
    #             )
    #         print()
    #     print("--------------------------------")
    # print(len(program.MAPS))
    # print("Grab heal:", agent.grab_heal)
    # print("Shoot:", agent.shoot_act)
    # print("Heal:", agent.heal)
    # print("Gold:", agent.grab_gold)
    # print("Final HP:", agent.current_hp)
    # print("Healing potion remaining:", agent.healing_potion)
    # for row in graph2:
    #     for cell in row:
    #         print(cell, end=" ")
    #     print()
    # print(len(program.MAPS))
    # print(len(primary_path))
    # print(primary_path[0])
    # print(RESULT[0])
    # print(program.MAPS[0][0][0].element)
    maps = copy.deepcopy(program.MAPS)
    main_ui.showAgentMove(choose_map_result, RESULT, maps, choose_map_result)
if __name__ == "__main__":
    while True:
        main()
