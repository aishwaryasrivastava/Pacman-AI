Pacman AI
----
An AI agent for Pacman that uses search algorithms to find it's goal. 
1. To see the depth-first search algorithm, use the command ```python py/pacman.py -l mediumMaze -p SearchAgent -a fn=dfs```
2. To see the breadth-first search algorithm, use ```python py/pacman.py -l mediumMaze -p SearchAgent -a fn=bfs```
3. To see the A* search algorithm using the Manhattan heuristic, use ```python py/pacman.py -l mediumMaze -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic```