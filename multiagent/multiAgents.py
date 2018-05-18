# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        #print gameState.generatePacmanSuccessor(legalMoves[chosenIndex])
        "Add more of your code here if you want to"
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.
          Here are some method calls that might be useful when implementing minimax.
          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1
          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action
          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        Pacman = 0
        Ghosts = range(1, gameState.getNumAgents())

        # Returns the maximum utility for pacman at a given {agent_state} and {depth}
        def max_utility(agent_state, depth):
            # If we're in the final state, then just return the score. 
            # Note: there is no tie in Pacman!
            if agent_state.isWin() or agent_state.isLose():
                return agent_state.getScore()

            # Else, calculate the minimum utility of the ghosts for all possible moves Pacman can make
            actions = agent_state.getLegalActions(Pacman)
            u, max_u = float("-inf"), float("-inf")
            max_action = Directions.STOP
            for action in actions:
                u = min_utility(agent_state.generateSuccessor(Pacman, action), depth, Ghosts[0])
                if u > max_u:
                    max_u = u
                    max_action = action
            # If we have explored all options, then return the action that gives maximum utility
            if depth == 0:
                return max_action
            # If not, then return the maximum *known* utility
            else:
                return max_u

        def min_utility(agent_state, depth, ghost):
            # If we're in the final state, then just return the score. 
            # Note: there is no tie in Pacman!
            if agent_state.isLose() or agent_state.isWin():
                return agent_state.getScore()

            # Find the next agent. It could be a ghost, or it could be Pacman.
            next_agent = ghost + 1
            if next_agent not in Ghosts:
              next_agent = Pacman

            # Now, find the utility for all possible ghost moves according to whose turn it is next
            actions = agent_state.getLegalActions(ghost)
            min_u = float("inf")
            u = min_u
            for action in actions:
                # If it is Pacman's turn next, then maximize it's utility
                if next_agent == Pacman: 
                    if depth == self.depth - 1:
                        u = self.evaluationFunction(agent_state.generateSuccessor(ghost, action))
                    else:
                        u = max_utility(agent_state.generateSuccessor(ghost, action), depth + 1)
                # Else, minimize the ghost's utility
                else:
                    u = min_utility(agent_state.generateSuccessor(ghost, action), depth, next_agent)

                # Return the minimum utility
                if u < min_u:
                    min_u = u
            return min_u

        # Return the maximum utility of Pacman!
        return max_utility(gameState, 0)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        Pacman = 0
        Ghosts = range(1, gameState.getNumAgents())        
        def max_utility(agent_state, depth, alpha, beta):
            # If we're in the final state, then just return the score. 
            # Note: there is no tie in Pacman!
            if agent_state.isWin() or agent_state.isLose():
                return agent_state.getScore()

            actions = agent_state.getLegalActions(Pacman)
            u, max_u = float("-inf"), float("-inf")
            max_action = Directions.STOP

            # Else, calculate minimum utility of ghosts
            for action in actions:
                u = min_utility(agent_state.generateSuccessor(Pacman, action), depth, Ghosts[0], alpha, beta)
                if u > max_u:
                    max_u = u
                    max_action = action

                # Pruning!
                alpha = max(alpha, max_u)
                if max_u > beta:
                    return max_u
                    
            # If we have explored all options, then return the action that gives maximum utility
            if depth == 0:
                return max_action
            # If not, then return the maximum *known* utility
            else:
                return max_u

        def min_utility(agent_state, depth, ghost, alpha, beta):
            # If we're in the final state, then just return the score. 
            # Note: there is no tie in Pacman!
            if agent_state.isLose() or agent_state.isWin():
                return agent_state.getScore()

            # Find the next agent. It could be a ghost, or it could be Pacman.
            next_agent = ghost + 1
            if next_agent not in Ghosts:
              next_agent = Pacman

            actions = agent_state.getLegalActions(ghost)
            u, min_u = float("inf"), float("inf")

            for action in actions:
                # If it is Pacman's turn, then maximize its utility.
                if next_agent == Pacman: 
                    if depth == self.depth - 1:
                        u = self.evaluationFunction(agent_state.generateSuccessor(ghost, action))
                    else:
                        u = max_utility(agent_state.generateSuccessor(ghost, action), depth + 1, alpha, beta)
                # If it is a ghost, then minimize its utility.
                else:
                    u = min_utility(agent_state.generateSuccessor(ghost, action), depth, next_agent, alpha, beta)
                if u < min_u:
                    min_u = u

                # Pruning!
                beta = min(beta, min_u)
                if min_u < alpha:
                    return min_u
            return min_u
        return max_utility(gameState, 0, float("-inf"), float("inf"))

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: This evaluation finds the nearest food and ghost w.r.t. Pacman, and returns a score accordingly.
      The score is increased if food is closer than a ghost, and decreased if a ghost is closer.
    """
    pacman_pos = currentGameState.getPacmanPosition()
    score = currentGameState.getScore()
    foods = currentGameState.getFood().asList()
    ghosts = currentGameState.getGhostStates()

    # Find nearest location of food
    nearest_food = min([util.manhattanDistance(food, pacman_pos) for food in foods])

    # Find nearest ghost
    nearest_ghost = min([util.manhattanDistance(ghost.getPosition(), pacman_pos) for ghost in ghosts])

    # If food is closer than a ghost, then we want to increase the score
    if nearest_food < nearest_ghost:
      score = score + 2

    # Else, we want to decrease the score
    # We take out more because ghosts are more dangerous than food is advantageous 
    else:
      score = score - 10
    return score 

# Abbreviation
better = betterEvaluationFunction

