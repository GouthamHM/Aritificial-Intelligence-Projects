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
        ghostDistances = [util.manhattanDistance(newPos,ghost.configuration.pos) for ghost in newGhostStates]
        foodDistances = [manhattanDistance(food, newPos) for food in newFood.asList()]
        "*** YOUR CODE HERE ***"
        #if all foods are over fallback to prev logic
        if not foodDistances:
            return successorGameState.getScore()
        else:
            if min(ghostDistances):
                return successorGameState.getScore() - (3./min(ghostDistances))\
                           - (min(foodDistances)) - 5*(len(foodDistances))
            else:
                return successorGameState.getScore()-(min(foodDistances))



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
      multi-agent searchers.  Any   methods defined here will be available
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
    def isPacMan(self, agentIndex):
        if not agentIndex:
            return True
        return False

    def value(self, state, agentIndex, currDepth):
        # Check for terminal states
        if state.isLose() or state.isWin() or currDepth == self.depth*self.agents_len:
            return self.evaluationFunction(state)
        if self.isPacMan(agentIndex):
            return self.maxValue(state,agentIndex,currDepth)[0]
        else:
            return self.minValue(state,agentIndex, currDepth)[0]

    def minValue(self,state,agentIndex,currDepth):
        v, action = float('inf'), Directions.STOP
        nextAgentIndex = (currDepth + 1) % self.agents_len
        for nextAction in state.getLegalActions(agentIndex):
            succesor_value = self.value(state.generateSuccessor(agentIndex, nextAction),nextAgentIndex, currDepth+1)
            v = min([v,succesor_value])
            if v == succesor_value:
                action = nextAction
        return v, action

    def maxValue(self,state,agentIndex,currDepth):
        v, action = float('-inf'), Directions.STOP
        nextAgentIndex = (currDepth + 1) % self.agents_len
        for nextAction in state.getLegalActions(agentIndex):
            succesor_value = self.value(state.generateSuccessor(agentIndex, nextAction),nextAgentIndex, currDepth+1)
            v = max([v,succesor_value])
            if v == succesor_value:
                action = nextAction
        return v, action

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
        "*** YOUR CODE HERE ***"
        self.agents_len = gameState.getNumAgents()
        value, path = self.maxValue(state=gameState,agentIndex=self.index,currDepth=0)
        return path


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def isPacMan(self, agentIndex):
        if not agentIndex:
            return True
        return False

    def value(self, state, agentIndex, currDepth, alpha, beta):
        # Check for terminal states
        if state.isLose() or state.isWin() or currDepth == self.depth*self.agents_len:
            return self.evaluationFunction(state)
        if self.isPacMan(agentIndex):
            return self.maxValue(state,agentIndex,currDepth,alpha,beta)[0]
        else:
            return self.minValue(state,agentIndex, currDepth,alpha,beta)[0]

    def minValue(self,state,agentIndex,currDepth,alpha,beta):
        v, action = float('inf'), Directions.STOP
        nextAgentIndex = (currDepth+1) % self.agents_len
        for nextAction in state.getLegalActions(agentIndex):
            succesor_value = self.value(state.generateSuccessor(agentIndex, nextAction),nextAgentIndex, currDepth+1,alpha,beta)
            v = min([v,succesor_value])
            if v == succesor_value:
                action = nextAction
            if v < alpha:
                return v,action
            beta = min(beta,v)
        return v, action

    def maxValue(self,state,agentIndex,currDepth,alpha,beta):
        v, action = float('-inf'), Directions.STOP
        nextAgentIndex = (currDepth + 1) % self.agents_len
        for nextAction in state.getLegalActions(agentIndex):
            succesor_value = self.value(state.generateSuccessor(agentIndex, nextAction),nextAgentIndex, currDepth+1,alpha,beta)
            v = max([v,succesor_value])
            if v == succesor_value:
                action = nextAction
            if v > beta:
                return v,action
            alpha = max(alpha,v)
        return v, action

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
        "*** YOUR CODE HERE ***"
        self.agents_len = gameState.getNumAgents()
        alpha = float('-inf')
        beta = float('inf')
        value, path = self.maxValue(state=gameState,agentIndex=self.index,currDepth=0,alpha=alpha,beta=beta)
        return path

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def isPacMan(self, agentIndex):
        if not agentIndex:
            return True
        return False

    def value(self, state, agentIndex, currDepth):
        # Check for terminal states
        if state.isLose() or state.isWin() or currDepth == self.depth*self.agents_len:
            return self.evaluationFunction(state)
        if self.isPacMan(agentIndex):
            return self.maxValue(state,agentIndex,currDepth)[0]
        else:
            return self.expecValue(state,agentIndex, currDepth)

    def expecValue(self,state,agentIndex,currDepth):
        vSum = 0.0
        vCount = 0
        nextAgentIndex = (currDepth + 1) % self.agents_len
        for nextAction in state.getLegalActions(agentIndex):
            succesor_value = self.value(state.generateSuccessor(agentIndex,nextAction),nextAgentIndex, currDepth+1)
            vSum += succesor_value
            vCount += 1
        return vSum/vCount

    def maxValue(self,state,agentIndex,currDepth):
        v, action = float('-inf'), Directions.STOP
        nextAgentIndex = (currDepth + 1) % self.agents_len
        for nextAction in state.getLegalActions(agentIndex):
            succesor_value = self.value(state.generateSuccessor(agentIndex, nextAction),nextAgentIndex, currDepth+1)
            v = max([v,succesor_value])
            if v == succesor_value:
                action = nextAction
        return v, action

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
        "*** YOUR CODE HERE ***"
        self.agents_len = gameState.getNumAgents()
        value, path = self.maxValue(state=gameState,agentIndex=self.index,currDepth=0)
        return path

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
      Here I will add addtional twp features and add penalty accordingly
      1. len(capsules): Number of capsules I add this so that pacman acquires as many capsules as possible
      2. min(capsuleDistances): Find the nearest capsule and try to reach that.

      Prev features as used in 1:
      1. Reciprocal of ghostDistance:  To stay away from the ghosts
      2. min(foodDistance): To acquire the nearest food
      3. len(foodDistance: To get all foods ASAP
    """
    newPos = currentGameState.getPacmanPosition()
    newGhostStates = currentGameState.getGhostStates()
    ghostDistances = [util.manhattanDistance(newPos, ghost.configuration.pos) for ghost in newGhostStates]
    foodDistances = [manhattanDistance(food, newPos) for food in currentGameState.getFood().asList()]
    no_capsules = 0
    mincapsuleDistances = 0.0
    if currentGameState.data.capsules:
        capsuleDistances = [manhattanDistance(capsule, newPos) for capsule in currentGameState.getCapsules()]
        mincapsuleDistances = min(capsuleDistances)
        no_capsules = len(capsuleDistances)

    if not foodDistances:
        return currentGameState.getScore()
    else:
        if min(ghostDistances):
            return currentGameState.getScore() - (4. / min(ghostDistances)) \
                   - (min(foodDistances)) - 2 * (len(foodDistances)) - 3.0*(mincapsuleDistances)-4.0*(no_capsules)
        else:
            return currentGameState.getScore() - (min(foodDistances))

# Abbreviation
better = betterEvaluationFunction

