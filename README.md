_**University of Science (HCMUS) - Introduction to Artificial Intelligence - CSC14003**_
# PROJECT 2: LOGICAL AGENT
## 1. Wumpus World
The purpose of this project is to design and implement a <font style='color:blue'>***logical agent***</font> that navigates through the Wumpus World, a <font style='color:blue'>***partially-observable***</font> environment.
The Wumpus World presents the following key features:
* The environment is an underground cave with a network of interconnected two-dimensional rooms.
* A room may contain a <font style='color:blue'>*deadly **pit***</font>, signaled by a perceivable <font style='color:blue'>***breeze***</font>, or a <font style='color:blue'>*fatal **Wumpus** monster*</font>, detectable via a discernible <font style='color:blue'>***stench***</font>.
	* The agent will die immediately when entering a room containing one of those harmful factors. No withdrawal is possible.
	* The percepts are available in the <font style='color:blue'>*four-neighborhood of the room*</font> containing one of those harmful factors.
* The agent has <font style='color:blue'>***arrows***</font> to shoot in the direction he is facing.
* There is one <font style='color:blue'>***chest of gold***</font>, located somewhere in the cave.
* Movement options: <font style='color:blue'>*forward, turn left, or right by 90 degrees*</font>.

<font style='color:red'>**The primary objective encompasses locating the gold.**</font> During the journal, the agent may need to kill Wumpus to pursuit success in this environment.
Figure 1 demonstrates an example of the Wumpus world with key entities.

<center>
    <img src = "https://github.com/user-attachments/assets/0cd417d1-5731-435c-8d44-2bee515755fa" width="400" alt="Figure 1: 2D City map."/>
	<div style="text-align: center;"><i><b>Figure 1.</b> An example of the Wumpus world with key entities.</i></div>
</center>


## 2. Project Description
Our Wumpus World for actual implementation slightly differs from the original problem description. The environment’s specification is as follows.
1. <font style='color:blue'>**Grid Layout**</font>
	* The grid size has increased from 4x4 to <font style='color:blue'>**10x10**</font>.
2. <font style='color:blue'>**Elements**</font>
	* **Agent**: The agent moves around the grid trying to achieve its goals.
	* **Wumpus**: A monster that kills the agent if they end up in the same cell.
	* **Gold**: The agent’s goal is to find and retrieve the gold.
	* **Pits**: Dangerous cells that the agent falls into and dies.
	* **Poisonous Gas**: Reduces the agent's health by 25% if entered.
	* **Healing Potions**: Restores the agent's health by 25% when using.
3. <font style='color:blue'>**Percepts**</font>
	* **Breeze**: Indicates an adjacent cell contains a pit.
	* **Stench**: Indicates an adjacent cell contains the Wumpus.
	* **Scream**: Heard if the Wumpus is killed.
	* **Whiff**: Indicates an adjacent cell contains poisonous gas.
	* **Glow**: Indicates an adjacent cell contains a healing potion.
4. <font style='color:blue'>**Agent's Actions**</font>
	* **Move Forward**: Moves to the next cell in the direction the agent is facing.
	* **Turn Left/Right**: Changes the agent's direction.
	* **Grab**: Picks up gold or healing potions if present in the cell.
	* **Shoot**: Fires an arrow in the direction the agent is facing to kill the Wumpus. Arrows can only hit targets in adjacent cells.
	* **Climb**: Exits the cave (used when the agent is in the starting position).
	* **Heal**: Uses a healing potion to restore health.
5. <font style='color:blue'>**Goals**</font>
	* The primary goal remains to find the gold and return to the starting position without dying with the highest score the agent can achieve.
6. <font style='color:blue'>**Other requirements**</font>
	* Recommended libraries for solving logic problems on Python: PySAT, SciPy.
	* There may be any number of pits and chests of gold in the world.
	* There is <font style='color:blue'>**at least**</font> one Wumpus.
	* The agent carries an <font style='color:blue'>**infinite**</font> number of arrows.
	* When the agent <font style='color:blue'>**grabs**</font> the <font style='color:blue'>**healing potion**</font>, the <font style='color:blue'>**glow of that healing potion**</font> will <font style='color:blue'>**disappear**</font>.
	* The <font style='color:blue'>**poison gas**</font> will <font style='color:blue'>**last forever**</font>. The agent can be poisoned **multiple times** in the same cell.
	* When the <font style='color:blue'>**Wumpus dies**</font>. It will <font style='color:blue'>**scream**</font> and you will know this information.
	* After Wumpus dies, the <font style='color:blue'>**stench of that Wumpus**</font> will <font style='color:blue'>**disappear**</font> (you should update the state of map after Wumpus dies)
		* The game will end when one of the following <font style='color:blue'>**two**</font> conditions occurs:
			* The agent dies **(by wumpus, pit or 0% of health)**.
			* The agent climbs out of the cave **(exit the cave)**.

The following activities can give the agent certain amounts of points.
| Activity                                |  Points  |
| --------------------------------------- |:--------:|
| Pick up each chest of gold              |  +5000   |
| Shoot an arrow                          |  − 100   |
| Killed by the Wumpus or Fall into a pit | − 10,000 |
| Climb of the cave                       |   +10    |
| All Agent’s Action                      |   − 10   |

## 3. Tasks
Your group must play two roles:
* **Program**: set up a program to build the map
* **Agent**: explore the Wumpus world and get the highest score possible for that world, using either Propositional Logic or First-Order Logic (or both).

Your implementation should <font style='color:blue'>*output information about the search*</font>, including the <font style='color:blue'>*percepts at every room the agent enters*</font>, the <font style='color:blue'>*updates in the knowledge base after each new percept*</font>, and the <font style='color:blue'>*action decided upon by the agent*</font>. The program should also <font style='color:blue'>*output the score of the agent*</font>.
Having your implementation generate worlds randomly can help you test your agent.
## 4. Specifications
You need to create 2 classes Program and Agent in separate files.
<font style='color:red'>**For class Program**</font>: This class is responsible for building the map, and reporting information about the elements in the cell.
**Input**: the given map is represented by matrix, which is stored in the input file, for example, map1.txt.
The input file format is described as follows:
* The first line contains an integer N, which is the size of map.
* N next lines with each line represents a string. If room empty, it is marked by hyphen character (-). If room has some things or signal such as Wumpus(W), Pit( P ), Breeze(B), Stench(S), Agent(A) or Gold(G). Between two adjacent rooms is separated by a dot (.)
* <font style='color:red'>**Input only includes Wumpus(W), Pit(P), Agent(A) and Gold(G)**</font>, **Poisonous Gas(P_G),Healing Potions(H_P)**. <font style='color:red'>**You need to update information about Stench(S), Breeze(B),**</font> **Whiff(W) and Glow(G_L)** <font style='color:red'>**on the map based on input data**</font>.
* For example:
	```tex
	-.-.W.-.P.-.-.P_G.-.-
	-.-.-.-.-.-.-.-.-.-
	```
	![89dc203e-6400-4830-baf5-2460433359bb](https://github.com/user-attachments/assets/c3267c64-cc85-4a58-aede-501b0447753b)

**Output**: The map with all infomation
<font style='color:red'>**Class Agent**</font>
The agent can **only know the components of the cell where it is standing**. The agent must **go step by step** and call the program to get information about the cell it is standing on **from class program**. From there, it makes percepts to find the direction of movement and infer objects based on the available information.
<font style='color:red'>**NOTE:** The agent does not know the information on the whole map.</font>
**Result**: a result with path for agent, game point will be displayed on screen and written in output text file such as result1.txt.

You can write output in the following format:
![image](https://github.com/user-attachments/assets/73201aef-644f-4748-8f10-605675603e52)

## 5. Requirements
| No. | Specifications                                                                                                                  |  Scores   |
|:---:| ------------------------------------------------------------------------------------------------------------------------------- |:---------:|
|  1  | Finish problem success                                                                                                          |   50 %    |
|  2  | Graphical demonstration of each step of the running process. You can demo in console screen or use any other graphical library. |   20 %    |
|  3  | Generate at least 5 maps with difference structures such as position and number of Pit, Gold and Wumpus.                        |   20 %    |
|  4  | Report your algorithm, experiment with some reflection or comments.                                                             |   20 %    |
|     | **Total**                                                                                                                       | **100 %** |
## 6. Notice
This assignment will be completed in <font style='color:blue' >**groups**</font>, as registered at the beginning of the course. To prepare, you will need to create a folder that contains various subfolders, including source, input, output, and document. The report must give the following information:
* Your detailed information (Student Id, Full Name)
* Assignment Plan
* Environment to compile and run your program.
* Estimating the degree of completion level for each requirement.
* References (if any)

<font style='color:red'>**Any plagiarism, tricks, or any lie will have 0 points for the course grade.**</font>

---
# TEAM'S INFORMATION
## 1. Work assignment table

| Student ID | Full Name       |   General Tasks    | Detailed Tasks | Completion |
|:----------:| --------------- |:------------------:|:--------------:|:----------:|
|  22127174  | Ngô Văn Khải    |        GUI         |                |   100 %    |
|  22127322  | Lê Phước Phát   | Problem/Test Cases |                |   100 %    |
|  22127388  | Tô Quốc Thanh   |      Problem       |                |   100 %    |
|  22127441  | Thái Huyễn Tùng |        GUI         |                |   100 %    |

## 2. Self-evaluation of the completion rate

| No. | Details                                                       | Completion Rate |
|:---:| ------------------------------------------------------------- |:---------------:|
|  1  | Finish problem successfully                                   |      100 %      |
|  2  | GUI                                                           |      100 %      |
|  3  | Generate at least 5 test cases                                |      100 %      |
|  4  | Report algorithm, experiment with some reflection or comments |      100 %      |

