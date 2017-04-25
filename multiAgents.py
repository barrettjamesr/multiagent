from util import manhattanDistance
from game import Directions
import random, util
import sys

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
        prevFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        prevCapsules = currentGameState.getCapsules()
        newCapsules = successorGameState.getCapsules()

        #return maximum available number if you've won
        if successorGameState.isWin():
          return float('inf')

        utility = successorGameState.getScore()

        #subtract for ghost distance except under scared timer
        for ghostState in newGhostStates:
          mDistance = manhattanDistance(ghostState.configuration.getPosition(), newPos)
          if ghostState.scaredTimer <= 1:
            #be careful when ghost is close
            if 5 > mDistance:
              utility -= (10-mDistance)
            #when he's super close, follow the advice of the Monty Python knights and RUN AWAY!
            elif 2 > mDistance:
              utility -= 100

        #eat food if you can
        if (currentGameState.getNumFood() > successorGameState.getNumFood()):
          utility += 20
        #eat capsules if you can
        if (newPos in newCapsules):
          utility += 50
        for capsule in newCapsules:
          utility -= manhattanDistance(capsule, newPos)

        #eat closest food first, all others are pretty much irrelevant
        closestFood = float('inf')
        for food in newFood.asList():
          closestFood = min(manhattanDistance(food, newPos), closestFood)
        utility -= closestFood

        #waiting for the ghost to eat you is bad
        if Directions.STOP == action:
          utility -= 5

        return utility
        #return successorGameState.getScore()

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

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """

        def minValue(gameState, ghost, d):
          val = float('inf')

          # find the action that is best for the ghost (what that action is doesn't matter)
          for action in gameState.getLegalActions(ghost):
            tempState =gameState.generateSuccessor(ghost, action)
            tempVal, action = minimaxDecision(tempState, ghost +1, d)

            if tempVal < val:
              val = tempVal

          return val

        def maxValue(gameState, d):
          val = float('-inf')
          #default move is stop
          bestAction = 'Stop'

          #find best action for Pacman, and return it along with the eval function
          for action in gameState.getLegalActions(0):
            tempState =gameState.generateSuccessor(0, action)
            tempVal, tempAction = minimaxDecision(tempState, 1, d)
            if tempVal > val:
              val = tempVal
              bestAction = action

          return (val, bestAction)

        #depending on whose move and depth, either maximise or minimise
        def minimaxDecision(gameState, agent, d):
          #each player gets on move for each depth
          if agent >= gameState.getNumAgents():
            agent = 0
            d += 1
          #return eval fn when game finished or depth reached
          if (gameState.isWin() or gameState.isLose() or self.depth < d):
            return (self.evaluationFunction(gameState), '')
          #pacman's move gets max value, the ghosts get min value          
          if 0 == agent:
            return maxValue(gameState, d)
          else:
            return (minValue(gameState, agent, d), '')

        #first depth = 1, first agent = pacman (zero)
        d = 1
        firstAgent = 0
        value, action = minimaxDecision(gameState, firstAgent, d)
        return action

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        def minValue(gameState, ghost, d, alpha, beta):
          val = float('inf')

          for action in gameState.getLegalActions(ghost):
            tempState =gameState.generateSuccessor(ghost, action)
            tempVal, action = abPruning(tempState, ghost +1, d, alpha, beta)
            if tempVal < val:
              val = tempVal
            if val < alpha:
                return val
            beta = min(beta, tempVal)

          return val

        def maxValue(gameState, d, alpha, beta):
          val = float('-inf')
          #default best move is stop
          bestAction = 'Stop'

          for action in gameState.getLegalActions(0):
            tempState =gameState.generateSuccessor(0, action)
            tempVal, tempAction = abPruning(tempState, 1, d, alpha, beta)
            if tempVal > val:
              val = tempVal
              bestAction = action
            if val > beta:
                return (val, action)
            alpha = max(alpha, tempVal)
          return (val, bestAction)

        #depending on whose move and depth, either maximise or minimise
        def abPruning(gameState, agent, d, alpha, beta):
          #each player gets on move for each depth
          if agent >= gameState.getNumAgents():
            agent = 0
            d += 1
          #return eval fn when game finished or depth reached
          if (gameState.isWin() or gameState.isLose() or self.depth < d):
            return (self.evaluationFunction(gameState), '')
          #pacman's move gets max value, the ghosts get min value          
          if 0 == agent:
            return maxValue(gameState, d, alpha, beta)
          else:
            return (minValue(gameState, agent, d, alpha, beta), '')

        #first depth = 1, first agent = pacman (zero)
        d = 1
        firstAgent = 0
        value, action = abPruning(gameState, firstAgent, d, float('-inf'), float('inf'))
        return action

        util.raiseNotDefined()
        

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

        def expectiValue(gameState, ghost, d):
          val = 0
          legalActions = gameState.getLegalActions(ghost)

          #sum all values
          for action in legalActions:
            tempState =gameState.generateSuccessor(ghost, action)
            tempVal, action = expectimaxDecision(tempState, ghost +1, d)
            val += tempVal

          #return average utility value
          return val / len(legalActions)

        def maxValue(gameState, d):
          val = float('-inf')
          #default best move is stop
          bestAction = 'Stop'

          for action in gameState.getLegalActions(0):
            tempState =gameState.generateSuccessor(0, action)
            tempVal, tempAction = expectimaxDecision(tempState, 1, d)
            if tempVal > val:
              val = tempVal
              bestAction = action

          return (val, bestAction)

        #depending on whose move and depth, either maximise or minimise
        def expectimaxDecision(gameState, agent, d):
          #each player gets on move for each depth
          if agent >= gameState.getNumAgents():
            agent = 0
            d += 1
          #return eval fn when game finished or depth reached
          if (gameState.isWin() or gameState.isLose() or self.depth < d):
            return (self.evaluationFunction(gameState), '')
          #pacman's move gets max value, the ghosts get min value          
          if 0 == agent:
            return maxValue(gameState, d)
          else:
            return (expectiValue(gameState, agent, d), '')

        #first depth = 1, first agent = pacman (zero)
        d = 1
        firstAgent = 0
        value, action = expectimaxDecision(gameState, firstAgent, d)
        return action

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  evaluation = currentGameState.getScore()
  #return maximum available number if you've won
  if currentGameState.isWin():
    return float('inf')
  newPos = currentGameState.getPacmanPosition()
  #subtract for ghost distance except under scared timer
  for ghostState in currentGameState.getGhostStates():
    mDistance = manhattanDistance(ghostState.configuration.getPosition(), newPos)
    if ghostState.scaredTimer <= 1:
      #be careful when ghost is close
      if 5 > mDistance:
        evaluation -= (10-mDistance)
      #when he's super close, follow the advice of the Monty Python knights and RUN AWAY!
      elif 2 > mDistance:
        evaluation -= 100
  #try to get close to capsules
  for capsule in currentGameState.getCapsules():
    evaluation -= manhattanDistance(capsule, newPos)
  sumClosestFood = 0
  closestFood = float('inf')
  #reduce distance to closest food as highest priority, but to avoid stalemate, also reduce distance to ALL food.
  for food in currentGameState.getFood().asList():
    closestFood = min(manhattanDistance(food, newPos), closestFood)
    sumClosestFood -= manhattanDistance(food, newPos)/10
  #by including the number of food it benefits states which actually eat a food, causing the closest food to be further away.
  evaluation -= closestFood + currentGameState.getNumFood() * 5 - sumClosestFood

  return evaluation
  util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

