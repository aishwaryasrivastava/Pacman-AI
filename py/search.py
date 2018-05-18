# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
      """
      Returns the start state for the search problem
      """
      util.raiseNotDefined()

    def isGoalState(self, state):
      """
      state: Search state

      Returns True if and only if the state is a valid goal state
      """
      util.raiseNotDefined()

    def getSuccessors(self, state):
      """
      state: Search state

      For a given state, this should return a list of triples,
      (successor, action, stepCost), where 'successor' is a
      successor to the current state, 'action' is the action
      required to get there, and 'stepCost' is the incremental
      cost of expanding to that successor
      """
      util.raiseNotDefined()

    def getCostOfActions(self, actions):
      """
      actions: A list of actions to take

      This method returns the total cost of a particular sequence of actions.  The sequence must
      be composed of legal moves
      """
      util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem): 
    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in.

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    util.raiseNotDefined()
    """
    
    openset = [problem.getStartState()]    # stack
    closedset = [problem.getStartState()]    # visited
    parents = {}    # maps a state to it's parent state 
    while len(openset) > 0:
        state = openset.pop()
        if problem.isGoalState(state):
            print "Found goal!"
            actions = []
            while not state == problem.getStartState():
                state, action = parents[state]
                actions = [action] + actions
            return actions

        else:
            for (next_state, action, cost) in problem.getSuccessors(state):
                if next_state not in closedset:
                    openset.append(next_state)
                    closedset.append(next_state)
                    parents[next_state] = state, action
    
    util.raiseNotDefined()
    
    
  

def breadthFirstSearch(problem):
	
    "Search the shallowest nodes in the search tree first. [p 81]"
    openset = [problem.getStartState()]    # queue (instead of stack)
    closedset = [problem.getStartState()]    # visited
    parents = {}    # maps a state to it's parent state 
    while len(openset) > 0:
        state = openset.pop(0)	# dequeue
        if problem.isGoalState(state):
            print "Found goal!"
            actions = []
            while not state == problem.getStartState():
                state, action = parents[state]
                actions = [action] + actions
            return actions

        else:
            for (next_state, action, cost) in problem.getSuccessors(state):
                if next_state not in closedset:
                    openset.append(next_state)
                    closedset.append(next_state)
                    parents[next_state] = state, action
    
    util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

# Extra credit - inadmissable heuristic
def euclideanHeuristicSqrd(state, problem = None):
	goal = (1,1)
	return ((state[0] - goal[0])**2 + (state[1]-goal[1])**2)

from heapq import heappush, heappop
def aStarSearch(problem, heuristic=nullHeuristic):
    closedset = []	# visited
    openset = []	# discovered, but not visited
    parents = {}	# maps a state to its parent state
    # gscore: maps a state to the cost of getting to it from the start node
    gscore = {problem.getStartState(): 0}	
    # fscore: maps a state to the cost of getting to the goal from the start node through it
    fscore = {problem.getStartState(): heuristic(problem.getStartState(), problem)}	
    heappush(openset, (fscore[problem.getStartState()], problem.getStartState()))

    while len(openset) > 0:
    	# Get the state having the lowest fscore (heappop returns a (fscore[state], state) pair)
    	_,state = heappop(openset)
    	if problem.isGoalState(state):
    	    print "Found goal!"
            actions = []
            while not state == problem.getStartState():
                state, action = parents[state]
                actions = [action] + actions

            return actions

        closedset.append(state)

        for (next_state, action, cost) in problem.getSuccessors(state):
        	if next_state in closedset:
        		# Ignore this state if it is already visited
        		continue

        	tentative_gscore = gscore[state] + cost    # Distance from start to next_state
        	if next_state in gscore.keys() and tentative_gscore >= gscore[next_state]:
        		# This is a costlier path - so ignore it
        		continue
            
            # If not visited and not costlier, then record it!
        	parents[next_state] = state, action
        	gscore[next_state] = tentative_gscore
        	fscore[next_state] = gscore[next_state] + heuristic(next_state, problem)
            # Mark as visited
        	if next_state not in openset:
        		heappush(openset, (fscore[next_state], next_state))
    
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
