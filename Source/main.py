from algorithms.program import Program
from algorithms.agent import Agent
from algorithms.a_star import create_graph, a_star

def main():
    program = Program(file_path="input/map4.txt")
    agent = Agent(map_size=program.map_size)
    program.display_map_test()
    print(agent.dfs(program))
    
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
    direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    print("Path: ", agent.path)
    print("With all information, we have: ")
    print("Sure Wumpus: ", agent.sure_wumpus)
    print("Sure Pit: ", agent.sure_pit)
    print("Sure Poison: ", agent.sure_poison)
    print("Sure Health: ", agent.sure_health)
    

    
    agent.shoot_process(program)
    # print(len(agent.path))
    agent.path.append((0, 0)) #quay ve o (0,0)

    print('--------------------------------')
    print("Final path: ", agent.path)
    
    print("Moving from cell to cell: ")
    graph = create_graph(agent.path, agent.map_size)
    agent.current_hp = 100
    RESULT = []
    for i in range(len(agent.path) - 1):
        path_with_info = []
        current = agent.path[i]
        nextt = agent.path[i+1]
        tmp_path = a_star(graph, current, nextt, agent, program)
        print(tmp_path)
        for j in range(len(tmp_path) - 1):
            vect = tmp_path[j+1][0] - tmp_path[j][0], tmp_path[j+1][1] - tmp_path[j][1]
            print(agent.direction)
            print(vect)
            if (vect[0] * agent.direction[0]) + (vect[1] * agent.direction[1]) == 0:
                if agent.direction == (1, 0):
                    if vect == (0, 1):
                        action = "Turn Right"
                    else:
                        action = "Turn Left"
                elif agent.direction == (-1, 0):
                    if vect == (0, 1):
                        action = "Turn Left"
                    else:
                        action = "Turn Right"
                elif agent.direction == (0, 1):
                    if vect == (1, 0):
                        action = "Turn Left"
                    else:
                        action = "Turn Right"
                else:
                    if vect == (1, 0):
                        action = "Turn Right"
                    else:
                        action = "Turn Left"    
                agent.direction = vect  
            else:
                if (vect[0] * agent.direction[0]) + (vect[1] * agent.direction[1]) == -1:
                    action = "Turn Left, Turn Left"
                    agent.direction = (-1 * agent.direction[0], -1 * agent.direction[1])
                else:
                    action = ""
            action += ", Move Forward"
            print(action)
            print()
            
            path_with_info.append((tmp_path[j], action))
        RESULT.append(path_with_info)
        RESULT.append((tmp_path[-1], "_"))
        
    print("Result for FE: ")
    print(RESULT)
    
    print("Grab heal:", agent.grab_heal)
    print("Shoot:", agent.shoot_act)
    print("Heal:", agent.heal)
    print("Gold:", agent.grab_gold)
    print("Final HP:", agent.current_hp)
    print("Healing potion remaining:", agent.healing_potion)
    
if __name__ == "__main__":
    main()
