#################################################################################
#     File Name           :     solveTicTacToe.py
#     Created By          :     Chen Guanying 
#     Creation Date       :     [2017-03-18 19:17]
#     Last Modified       :     [2017-03-18 19:17]
#     Description         :      
#################################################################################

import copy
import util 
import sys
import random
import time
from optparse import OptionParser

class GameState:
    """
      Game state of 3-Board Misere Tic-Tac-Toe
      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your search agents. Please do not remove anything, 
      however.
    """
    def __init__(self):
        """
          Represent 3 boards with lists of boolean value 
          True stands for X in that position
        """
        self.boards = [[False, False, False, False, False, False, False, False, False],
                        [False, False, False, False, False, False, False, False, False],
                        [False, False, False, False, False, False, False, False, False]]

    def generateSuccessor(self, action):
        """
          Input: Legal Action
          Output: Successor State
        """
        suceessorState = copy.deepcopy(self)
        ASCII_OF_A = 65
        boardIndex = ord(action[0]) - ASCII_OF_A
        pos = int(action[1])
        suceessorState.boards[boardIndex][pos] = True
        return suceessorState

    # Get all valid actions in 3 boards
    def getLegalActions(self, gameRules):
        """
          Input: GameRules
          Output: Legal Actions (Actions not in dead board) 
        """
        ASCII_OF_A = 65
        actions = []
        for b in range(3):
            if gameRules.deadTest(self.boards[b]): continue
            for i in range(9):
                if not self.boards[b][i]:
                    actions.append( chr(b+ASCII_OF_A) + str(i) )
        return actions

    # Print living boards
    def printBoards(self, gameRules):
        """
          Input: GameRules
          Print the current boards to the standard output
          Dead boards will not be printed
        """
        titles = ["A", "B", "C"]
        boardTitle = ""
        boardsString = ""
        for row in range(3):
            for boardIndex in range(3):
                # dead board will not be printed
                if gameRules.deadTest(self.boards[boardIndex]): continue
                if row == 0: boardTitle += titles[boardIndex] + "      "
                for i in range(3):
                    index = 3 * row + i
                    if self.boards[boardIndex][index]: 
                        boardsString += "X "
                    else:
                        boardsString += str(index) + " "
                boardsString += " "
            boardsString += "\n"
        print(boardTitle)
        print(boardsString)

class GameRules:
    """
      This class defines the rules in 3-Board Misere Tic-Tac-Toe. 
      You can add more rules in this class, e.g the fingerprint (patterns).
      However, please do not remove anything.
    """
    def __init__(self):
        """ 
          You can initialize some variables here, but please do not modify the input parameters.
        """
        {}
        
    def deadTest(self, board):
        """
          Check whether a board is a dead board
        """
        if board[0] and board[4] and board[8]:
            return True
        if board[2] and board[4] and board[6]:
            return True
        for i in range(3):
            #check every row
            row = i * 3
            if board[row] and board[row+1] and board[row+2]:
                return True
            #check every column
            if board[i] and board[i+3] and board[i+6]:
                return True
        return False

    def isGameOver(self, boards):
        """
          Check whether the game is over  
        """
        return self.deadTest(boards[0]) and self.deadTest(boards[1]) and self.deadTest(boards[2])

class TicTacToeAgent():
    """
      When move first, the TicTacToeAgent should be able to chooses an action to always beat 
      the second player.

      You have to implement the function getAction(self, gameState, gameRules), which returns the 
      optimal action (guarantee to win) given the gameState and the gameRules. The return action
      should be a string consists of a letter [A, B, C] and a number [0-8], e.g. A8. 

      You are welcome to add more helper functions in this class to help you. You can also add the
      helper function in class GameRules, as function getAction() will take GameRules as input.
      
      However, please don't modify the name and input parameters of the function getAction(), 
      because autograder will call this function to check your algorithm.
    """
    def __init__(self):
        """ 
          You can initialize some variables here, but please do not modify the input parameters.
        """
        self.maxTimeOut = 30
        #self.depth = 5
        self.winnerSet = []
        self.loserSet = []

    def evalGame(self, gameState, gameRules, returnValue):
        #contains dictionary of 102 non-isomorphic positions
        #winning combos = c2, a, b2, bc
        #win returns true, lose returns false

        a=2
        b=3
        c=5
        d=7

        winners = [c*c, a, b*b, b*c]
        evaluation = 1

        nonisomorphicC =  [[[False, False, False], [False, False, False], [False, False, False]]]
        nonisomorphicCC =  [[[False, False, False], [False, True, False], [False, False, False]]]
        nonisomorphic1 =  [[[False, True, False], [False, False, False], [False, False, False]],
                        [[True, False, False], [False, False, False], [False, False, False]],
                        [[True, False, False], [False, False, True], [False, True, False]]
                        ]

        nonisomorphicA =  [[[True, False, False], [False, False, False], [False, False, True]],
                        [[False, True, False], [True, False, False], [False, False, False]],
                        [[False, True, False], [False, False, False], [False, True, False]],
                        [[True, True, False], [False, False, False], [True, False, False]],
                        [[True, False, True], [False, True, False], [False, False, False]],
                        [[True, False, True], [False, False, False], [False, True, False]],
                        [[True, False, False], [False, True, True], [False, False, False]],
                        [[True, True, False], [True, True, False], [False, False, False]],
                        [[True, True, False], [True, False, True], [False, False, False]],
                        [[True, True, False], [True, False, False], [False, False, True]],
                        [[True, True, False], [False, False, False], [False, True, True]],
                        [[True, False, True], [False, False, False], [True, False, True]],
                        [[False, True, False], [True, False, True], [False, True, False]],
                        [[True, True, False], [False, True, True], [True, False, False]],
                        [[True, True, False], [False, False, True], [True, True, False]],
                        [[True, True, False], [False, False, True], [True, False, True]],
                        [[True, True, False], [True, False, True], [False, True, True]]
                        ]
        nonisomorphicB =  [[[True, False, True], [False, False, False], [False, False, False]],
                        [[True, False, False], [False, True, False], [False, False, False]],
                        [[True, False, False], [False, False, True], [False, False, False]],
                        [[False, True, False], [False, True, False], [False, False, False]],
                        [[True, True, False], [True, False, False], [False, False, False]],
                        [[False, True, False], [True, False, True], [False, False, False]],
                        [[True, True, False], [False, True, True], [False, False, False]],
                        [[True, True, False], [False, True, False], [True, False, False]],
                        [[True, True, False], [False, False, True], [True, False, False]],
                        [[True, True, False], [False, False, False], [True, True, False]],
                        [[True, True, False], [False, False, False], [True, False, True]],
                        [[True, False, True], [False, True, False], [False, True, False]],
                        [[True, False, False], [False, True, True], [False, True, False]],
                        [[True, True, False], [True, False, True], [False, True, False]],
                        [[True, True, False], [True, False, True], [False, False, True]]
                        ]
        nonisomorphicAD =  [[[True, True, False], [False, False, False], [False, False, False]]]
        nonisomorphicD =  [[[True, True, False], [False, False, True], [False, False, False]],
                        [[True, True, False], [False, False, False], [False, True, False]],
                        [[True, True, False], [False, False, False], [False, False, True]]
                        ]
        nonisomorphicAB =  [[[True, True, False], [False, True, False], [False, False, False]],
                        [[True, False, True], [False, False, False], [True, False, False]],
                        [[False, True, False], [True, True, False], [False, False, False]],
                        [[True, True, False], [False, False, True], [False, True, False]],
                        [[True, True, False], [False, False, True], [False, False, True]]
                        ]

        for board in gameState.boards:
            #break board into 2d array if required
            if 3!=len(board):
                board = [board[i:i+3] for i in range(0, len(board), 3)]

            if gameRules.deadTest(board[0] + board[1] + board[2]):
                continue
            else:
                #rotate board to match with 102 nonisompophic ways
                found = False
                multiple = 0

                for i in range(4):
                    if found:
                        continue
                    if board in nonisomorphicC:
                        multiple = c
                        found = True
                    elif board in nonisomorphicCC:
                        multiple = c * c
                        found = True
                    elif board in nonisomorphic1:
                        multiple = 1
                        found = True
                    elif board in nonisomorphicA:
                        multiple = a
                        found = True
                    elif board in nonisomorphicAB:
                        multiple = a * b
                        found = True
                    elif board in nonisomorphicB:
                        multiple = b
                        found = True
                    elif board in nonisomorphicD:
                        multiple = d
                        found = True
                    elif board in nonisomorphicAD:
                        multiple = a * d
                        found = True

                    if found:
                        continue

                    #flip board
                    board = list(reversed(board))
                    if board in nonisomorphicC:
                        multiple = c
                        found = True
                    elif board in nonisomorphicCC:
                        multiple = c * c
                        found = True
                    elif board in nonisomorphic1:
                        multiple = 1
                        found = True
                    elif board in nonisomorphicA:
                        multiple = a
                        found = True
                    elif board in nonisomorphicAB:
                        multiple = a * b
                        found = True
                    elif board in nonisomorphicB:
                        multiple = b
                        found = True
                    elif board in nonisomorphicD:
                        multiple = d
                        found = True
                    elif board in nonisomorphicAD:
                        multiple = a * d
                        found = True

                    #flip board back
                    board = list(reversed(board))
                    #board = list(map(list, zip(*board)))

                    #rotate board
                    board = list(map(list, zip(*board)))[::-1]

                if multiple == 0:
                    print("board not found" + str(board))
                else:
                    evaluation = evaluation * multiple

        #a2 = 1, b3 = b, b2 c = c, c3 = ac2, b2d = d, cd = ad, d2 = c2
        simplified = [(a*a,1),(b*b*b,b),(b*b*c,c),(c*c*c,a*c*c),(b*b*d,d),(c*d,a*d),(d*d,c*c)]
        divisorsFound = True

        while divisorsFound:
            divisorsFound = False
            for divisor, substitute in simplified:
                if evaluation % divisor ==0:
                    evaluation = int(evaluation / divisor * substitute)
                    divisorsFound = True

        #print(evaluation) 
        if returnValue:
            return evaluation
        else:
            return (0<winners.count(evaluation))

    def getAction(self, gameState, gameRules):

        def playerValue(gameState, gameRules, player):
            actions = gameState.getLegalActions(gameRules)
            tempAction = actions[0]

            for action in random.sample(actions, len(actions)):
                newGameState = gameState.generateSuccessor(action)
                evalNumber = self.evalGame(newGameState, gameRules, True)
                #don't explore an action that loses the game
                if gameRules.isGameOver(newGameState.boards):
                    continue
                #don't explore an action that previously lost
                if evalNumber in self.loserSet:
                    continue
                #use any action that previously won
                if evalNumber in self.winnerSet:
                    return (player, action)
                #change player with new board
                winnerPlayer, winnerAction = minimaxDecision(newGameState, gameRules, not player)
                
                #if player:
                #    winnerPlayer, winnerAction = minimaxDecision(newGameState, gameRules, not player, d+1, muteOutput)
                #else:
                #    winnerPlayer, winnerAction = minimaxDecision(newGameState, gameRules, not player, d, muteOutput)
                #only accept a sure thing win, don't explore the same losing state twice
                if winnerPlayer == player:
                    if 0==len(self.winnerSet) or evalNumber not in self.winnerSet:
                        self.winnerSet.append(evalNumber)
                    return (player, action)
                elif evalNumber not in self.loserSet:
                    self.loserSet.append(evalNumber)

            return (not player, tempAction)

        #depending on whose move and depth, either maximise or minimise
        def minimaxDecision(gameState, gameRules, player):
            if gameRules.isGameOver(gameState.boards):
                #if the game is over, it's the current player's win
                return (player, '')
            return playerValue(gameState, gameRules, player)

        start_time = time.time()
        timed_func = util.TimeoutFunction(minimaxDecision, int(self.maxTimeOut))
        try:
            winnerPlayer, winnerAction = timed_func(gameState, gameRules, True)

        except util.TimeoutFunctionException:
            print("Move Timeout!")
            winnerAction = random.choice(gameState.getLegalActions(gameRules))

        return winnerAction

        util.raiseNotDefined()


class randomAgent():
    """
      This randomAgent randomly choose an action among the legal actions
      You can set the first player or second player to be random Agent, so that you don't need to
      play the game when debugging the code. (Time-saving!)
      If you like, you can also set both players to be randomAgent, then you can happily see two 
      random agents fight with each other.
    """

    def getAction(self, gameState, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return random.choice(actions)

class keyboardAgent():
    """
      This keyboardAgent return the action based on the keyboard input
      It will check whether the input actions is legal or not.
    """

    def checkUserInput(self, gameState, action, gameRules):
        actions = gameState.getLegalActions(gameRules)
        return action in actions

    def getAction(self, gameState, gameRules):

        action = input("Your move: ")
        while not self.checkUserInput(gameState, action, gameRules):
            print("Invalid move, please input again")
            action = input("Your move: ")
        return action 

class Game():
    """
      The Game class manages the control flow of the 3-Board Misere Tic-Tac-Toe
    """
    def __init__(self, numOfGames, muteOutput, randomAI, AIforHuman):
        """
          Settings of the number of games, whether to mute the output, max timeout
          Set the Agent type for both the first and second players. 
        """
        self.numOfGames  = numOfGames
        self.muteOutput  = muteOutput
        self.maxTimeOut  = 30

        self.AIforHuman  = AIforHuman
        self.gameRules   = GameRules()
        self.AIPlayer    = TicTacToeAgent()

        if randomAI:
            self.AIPlayer = randomAgent()
        else:
            self.AIPlayer = TicTacToeAgent()
        if AIforHuman:
            self.HumanAgent = TicTacToeAgent()
            #self.HumanAgent = randomAgent()
        else:
            self.HumanAgent = keyboardAgent()

    def run(self):
        """
          Run a certain number of games, and count the number of wins
          The max timeout for a single move for the first player (your AI) is 30 seconds. If your AI 
          exceed this time limit, this function will throw an error prompt and return. 
        """
        numOfWins = 0;
        for i in range(self.numOfGames):
            gameState = GameState()
            agentIndex = 0 # 0 for First Player (AI), 1 for Second Player (Human)
            while True:
                if agentIndex == 0: 
                    timed_func = util.TimeoutFunction(self.AIPlayer.getAction, int(self.maxTimeOut))
                    try:
                        start_time = time.time()
                        action = timed_func(gameState, self.gameRules)
                    except util.TimeoutFunctionException:
                        print("ERROR: Player %d timed out on a single move, Max %d Seconds!" % (agentIndex, self.maxTimeOut))
                        return False

                    if not self.muteOutput:
                        print("Player 1 (AI): %s" % action)
                else:
                    action = self.HumanAgent.getAction(gameState, self.gameRules)
                    if not self.muteOutput:
                        print("Player 2 (Human): %s" % action)
                gameState = gameState.generateSuccessor(action)
                if self.gameRules.isGameOver(gameState.boards):
                    break
                if not self.muteOutput:
                    gameState.printBoards(self.gameRules)

                agentIndex  = (agentIndex + 1) % 2
            if agentIndex == 0:
                print("****player 2 wins game %d!!****" % (i+1))
            else:
                numOfWins += 1
                print("****Player 1 wins game %d!!****" % (i+1))

        print("\n****Player 1 wins %d/%d games.**** \n" % (numOfWins, self.numOfGames))


if __name__ == "__main__":
    """
      main function
      -n: Indicates the number of games
      -m: If specified, the program will mute the output
      -r: If specified, the first player will be the randomAgent, otherwise, use TicTacToeAgent
      -a: If specified, the second player will be the randomAgent, otherwise, use keyboardAgent
    """
    # Uncomment the following line to generate the same random numbers (useful for debugging)
    #random.seed(1)  
    parser = OptionParser()
    parser.add_option("-n", dest="numOfGames", default=1, type="int")
    parser.add_option("-m", dest="muteOutput", action="store_true", default=False)
    parser.add_option("-r", dest="randomAI", action="store_true", default=False)
    parser.add_option("-a", dest="AIforHuman", action="store_true", default=False)
    (options, args) = parser.parse_args()
    ticTacToeGame = Game(options.numOfGames, options.muteOutput, options.randomAI, options.AIforHuman)
    ticTacToeGame.run()
