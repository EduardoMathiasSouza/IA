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
from game import Directions, Actions
import random, util

from game import Agent
from pacman import GameState

def CID(currentGameState, items):
    walls = currentGameState.getWalls()

    start = currentGameState.getPacmanPosition()
    dist = {start: 0}

    visited = {start}

    queue = util.Queue()
    queue.push(start)

    while not queue.isEmpty():
        pos = x, y = queue.pop()

        if pos in items: return dist[pos]

        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            dx, dy = Actions.directionToVector(action)
            next_pos = nextx, nexty = int(x + dx), int(y + dy)

            if not walls[nextx][nexty] and next_pos not in visited:
                queue.push(next_pos)
                visited.add(next_pos)
                dist[next_pos] = dist[pos] + 1

    return None


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
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

        infinity = float('inf')
        ghostPositions = successorGameState.getGhostPositions()

        for ghostPosition in ghostPositions:
            if manhattanDistance(newPos, ghostPosition) < 2: return -infinity

        numFood = currentGameState.getNumFood()
        newNumFood = successorGameState.getNumFood()
        if newNumFood < numFood: return infinity

        min_distance = infinity
        for food in newFood.asList():
            distance = manhattanDistance(newPos, food)
            min_distance = min(min_distance, distance)
        return 1.0 / min_distance

def scoreEvaluationFunction(currentGameState: GameState):
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
        
    def isTerminalState(self, gameState):
        return gameState.isWin() or gameState.isLose()

    def isPacman(self, agent):
        return agent == 0

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    def maxValue(self, gameState, agent, depth):
        max_value = float("-inf")
        for action in gameState.getLegalActions(agent):
            successor = gameState.generateSuccessor(agent, action)
            v = self.minimax(successor, agent+1, depth)
            max_value = max(max_value, v)
            if depth == 1 and max_value == v: 
                self.action = action
        return max_value

    def minValue(self, gameState, agent, depth):
        min_value = float("inf")
        for action in gameState.getLegalActions(agent):
            successor = gameState.generateSuccessor(agent, action)
            v = self.minimax(successor, agent+1, depth)
            min_value = min(min_value, v)
        return min_value

    def minimax(self, gameState, agent=0, depth=0):
        agent = agent % gameState.getNumAgents()

        if self.isTerminalState(gameState):
            return self.evaluationFunction(gameState)

        if self.isPacman(agent):
            if depth < self.depth:
                return self.maxValue(gameState, agent, depth+1)
            else:
                return self.evaluationFunction(gameState)
        else:
            return self.minValue(gameState, agent, depth)

    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        self.minimax(gameState)
        return self.action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def maxValue(self, gameState, agent, depth, alpha, beta):
        max_value = float("-inf")
        for action in gameState.getLegalActions(agent):
            successor = gameState.generateSuccessor(agent, action)
            v = self.minimax(successor, agent + 1, depth, alpha, beta)
            max_value = max(max_value, v)
            if depth == 1 and max_value == v: 
                self.action = action
            if max_value > beta: 
                return max_value
            alpha = max(alpha, max_value)
        return max_value

    def minValue(self, gameState, agent, depth, alpha, beta):
        min_value = float("inf")
        for action in gameState.getLegalActions(agent):
            successor = gameState.generateSuccessor(agent, action)
            v = self.minimax(successor, agent + 1, depth, alpha, beta)
            min_value = min(min_value, v)
            if min_value < alpha: return min_value
            beta = min(beta, min_value)
        return min_value

    def minimax(self, gameState, agent=0, depth=0,alpha=float("-inf"), beta=float("inf")):
        agent = agent % gameState.getNumAgents()
        if self.isTerminalState(gameState):
            return self.evaluationFunction(gameState)
        if self.isPacman(agent):
            if depth < self.depth:
                return self.maxValue(gameState, agent, depth+1, alpha, beta)
            else:
                return self.evaluationFunction(gameState)
        else:
            return self.minValue(gameState, agent, depth, alpha, beta)

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        self.minimax(gameState)
        return self.action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def maxValue(self, gameState, agent, depth):
        max_value = float("-inf")
        for action in gameState.getLegalActions(agent):
            successor = gameState.generateSuccessor(agent, action)
            v = self.expectimax(successor, agent+1, depth)
            max_value = max(max_value, v)
            if depth == 1 and max_value == v: self.action = action
        return max_value

    def probability(self, legalActions):
        return 1.0 / len(legalActions)

    def expValue(self, gameState, agent, depth):
        legalActions = gameState.getLegalActions(agent)
        v = 0
        for action in legalActions:
            successor = gameState.generateSuccessor(agent, action)
            p = self.probability(legalActions)
            v += p * self.expectimax(successor, agent+1, depth)
        return v

    def expectimax(self, gameState, agent=0, depth=0):

        agent = agent % gameState.getNumAgents()

        if self.isTerminalState(gameState):
            return self.evaluationFunction(gameState)

        if self.isPacman(agent):
            if depth < self.depth:
                return self.maxValue(gameState, agent, depth+1)
            else:
                return self.evaluationFunction(gameState)
        else:
            return self.expValue(gameState, agent, depth)

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction
          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        self.expectimax(gameState)
        return self.action

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    infinity = float('inf')
    position = currentGameState.getPacmanPosition()
    score = currentGameState.getScore()
    ghostStates = currentGameState.getGhostStates()
    foodList = currentGameState.getFood().asList()
    capsuleList = currentGameState.getCapsules()

    if currentGameState.isWin(): 
        return infinity
    if currentGameState.isLose(): 
        return -infinity

    for ghost in ghostStates:
        dist = manhattanDistance(position, ghost.getPosition())
        if ghost.scaredTimer > 6 and dist < 2:
            return infinity
        elif ghost.scaredTimer < 5 and dist < 2:
            return -infinity

    foodDistance = 1.0/CID(currentGameState, foodList)
    capsuleDistance = CID(currentGameState, capsuleList)
    if capsuleDistance is None:
        capsuleDistance = 0.0 
    else:
        capsuleDistance= 1.0/capsuleDistance

    return 10.0*foodDistance + 5.0*score + 0.5*capsuleDistance

# Abbreviation
better = betterEvaluationFunction
