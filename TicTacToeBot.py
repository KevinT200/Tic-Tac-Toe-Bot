import tkinter as tk
import time
import math
import numpy as np

root = tk.Tk()

botPlayer = ""

gameFont = ("Arial", 36)

def startUp():
    global startupLabel
    global Obutton
    global passAndPlayButton
    global Xbutton
    global board
    global logic
    startupLabel = tk.Label(text="Choose Gamemode", font = gameFont)
    Obutton = tk.Button(text="Play as O", font = gameFont, command=ObuttonPressed)
    passAndPlayButton = tk.Button(text="Pass and Play", font = gameFont, command=PAPbuttonPressed)
    Xbutton = tk.Button(text="Play as X", font = gameFont, command=XbuttonPressed)
    startupLabel.grid(row=0, column=1)
    Xbutton.grid(row=1, column=0)
    passAndPlayButton.grid(row=1, column=1)
    Obutton.grid(row=1, column=2)
    try:
        for i in range(3):
            for j in range(3):
               if board[i][j] != "":
                    board[i][j].grid_forget()
                    logic.playAgainButton.grid_forget()
                    logic.optionsButton.grid_forget()
    except:
        pass


def ObuttonPressed():
    global botPlayer
    botPlayer = "X"
    startupLabel.grid_forget()
    Obutton.grid_forget()
    passAndPlayButton.grid_forget()
    Xbutton.grid_forget()
    continueStartGame()

def XbuttonPressed():
    global botPlayer
    botPlayer = "O"
    startupLabel.grid_forget()
    Obutton.grid_forget()
    passAndPlayButton.grid_forget()
    Xbutton.grid_forget()
    continueStartGame()

def PAPbuttonPressed():
    global botPlayer
    botPlayer = ""
    startupLabel.grid_forget()
    Obutton.grid_forget()
    passAndPlayButton.grid_forget()
    Xbutton.grid_forget()
    continueStartGame()
    

class miniMaxBot():
    def __init__(self):
        self.logicBoard = [["" for i in range(3)] for i in range(3)]
        self.getWinningCombinations()

    def miniMax(self, isMax, depthBoard, currentPlayer, depth):
        playableMoves = self.getAvailableMoves(depthBoard)
        scoreResults = self.score(depthBoard)
        if scoreResults != 0 or len(playableMoves) == 0:
            return scoreResults
        scores = []
        moves = []
        for x in playableMoves:
            possibleGame = depthBoard
            possibleGame[x[0]][x[1]] = currentPlayer
            if currentPlayer == "X":
                moves.append(x)
                scores.append(self.miniMax(True, possibleGame, "O", depth + 1))
                possibleGame[x[0]][x[1]] = ""
            else:
                moves.append(x)
                scores.append(self.miniMax(False, possibleGame, "X", depth + 1))
                possibleGame[x[0]][x[1]] = ""
        if depth == 0:
            if isMax:
                maxScore = max(scores)
                maxScoreLocation = scores.index(maxScore)
                bestMove = moves[maxScoreLocation]
                return (maxScore, bestMove[0], bestMove[1])
            else:
                minScore = min(scores)
                minScoreLocation = scores.index(minScore)
                bestMove = moves[minScoreLocation]
                return (minScore, bestMove[0], bestMove[1])
        else:
            if isMax:
                return (max(scores))
            else:
                return (min(scores))
    
    def getAvailableMoves(self, currentBoard):
        availableMoves = []
        for x in range(len(currentBoard)):
            for y in range(len(currentBoard[x])):
                if currentBoard[x][y] == "":
                    availableMoves.append((x, y))
        return availableMoves
    
    def getWinningCombinations(self):
        self.rows = [[(row, col) for col in range(3)] for row in range(3)]
        self.columns = [[(row, col) for row in range(3)] for col in range(3)]
        self.firstDiagonal = [(i, x)for i, x in enumerate(range(3))]
        self.secondDiagonal = [(i, x) for i, x in enumerate(reversed(range(3)))]

    def score(self, b):
        for row in range(3) :    
            if (b[row][0] == b[row][1] and b[row][1] == b[row][2]) :       
                if (b[row][0] == "O") :
                    return 10
                elif (b[row][0] == "X") :
                    return -10
    
        for col in range(3) :
            if (b[0][col] == b[1][col] and b[1][col] == b[2][col]) :
            
                if (b[0][col] == "O") :
                    return 10
                elif (b[0][col] == "X") :
                    return -10
    
        if (b[0][0] == b[1][1] and b[1][1] == b[2][2]) :
            if (b[0][0] == "O") :
                return 10
            elif (b[0][0] == "X") :
                return -10
    
        if (b[0][2] == b[1][1] and b[1][1] == b[2][0]) :
        
            if (b[0][2] == "O") :
                return 10
            elif (b[0][2] == "X") :
                return -10
    
        return 0

class makeButton():
    def __init__(self, row, col):
        self.row = row
        self.col = col
        button = tk.Button(text="", font=gameFont, height=3, width=6, command=lambda:logic.play(self.row, self.col))
        board[self.row][self.col] = button
        button.grid(row=row + 1, column=col)

class ticTacToeBoard():
    def __init__(self):
        self.topLabel = tk.Label(text="Ready?", font=gameFont)
        self.topLabel.grid(row = 0, column=1)
        for row in range(3):
            for col in range(3):
                makeButton(row, col)


class ticTacToeLogic():
    def __init__(self):
        self.has_winner = False
        self.tie = False
        self.getWinningCombinations()
        self.players = {"player1":"X", "player2": "O"}
        self.currentPlayer = self.players["player1"]
        self.winner = ""

    def nextPlayer(self):
        if self.currentPlayer == self.players["player1"]:
            self.currentPlayer = self.players["player2"]
        elif self.currentPlayer == self.players["player2"]:
            self.currentPlayer = self.players["player1"]

    def isValid(self, row, column):
        if board[row][column].cget("text") == "":
            return True
        else:
            return False
    
    def play(self, row, column):
        if self.isValid(row, column) and not self.checkForWin():
            board[row][column].config(text=self.currentPlayer)
            self.checkForWin()
            self.checkForTie()
            self.nextPlayer()
            self.changeTopLabel()
            self.resetLogicBoard()
            if botPlayer == "X" and self.currentPlayer == "X":
                result = bot.miniMax(False, bot.logicBoard, self.currentPlayer, 0)
                self.play(result[1], result[2])
            elif botPlayer == "O" and self.currentPlayer == "O":
                try:
                    result = bot.miniMax(True, bot.logicBoard, self.currentPlayer, 0)
                    self.play(result[1], result[2])
                except:
                    pass

    
    def getWinningCombinations(self):
        self.rows = [[(row, col) for col in range(3)] for row in range(3)]
        self.columns = [[(row, col) for row in range(3)] for col in range(3)]
        self.firstDiagonal = [(i, x)for i, x in enumerate(range(3))]
        self.secondDiagonal = [(i, x) for i, x in enumerate(reversed(range(3)))]
        return self.firstDiagonal + self.secondDiagonal + self.rows + self. columns
    
    def checkForWin(self):
        for i, x in enumerate(self.rows):
            if board[x[0][0]][x[0][1]].cget("text") == board[x[1][0]][x[1][1]].cget("text") and board[x[1][0]][x[1][1]].cget("text") == board[x[2][0]][x[2][1]].cget("text") and board[x[0][0]][x[0][1]].cget("text") != "":
                self.has_winner = True
                self.winner = board[x[0][0]][x[0][1]].cget("text")
        for i, x in enumerate(self.columns):
            if board[x[0][0]][x[0][1]].cget("text") == board[x[1][0]][x[1][1]].cget("text") and board[x[1][0]][x[1][1]].cget("text") == board[x[2][0]][x[2][1]].cget("text") and board[x[0][0]][x[0][1]].cget("text") != "":
                self.has_winner = True
                self.winner = board[x[0][0]][x[0][1]].cget("text")
        if board[self.firstDiagonal[0][0]][self.firstDiagonal[0][1]].cget("text") == board[self.firstDiagonal[1][0]][self.firstDiagonal[1][1]].cget("text") and board[self.firstDiagonal[1][0]][self.firstDiagonal[1][1]].cget("text") == board[self.firstDiagonal[2][0]][self.firstDiagonal[2][1]].cget("text") and board[self.firstDiagonal[0][0]][self.firstDiagonal[0][1]].cget("text") != "":
                self.has_winner = True
                self.winner = board[self.firstDiagonal[0][0]][self.firstDiagonal[0][1]].cget("text")
        if board[self.secondDiagonal[0][0]][self.secondDiagonal[0][1]].cget("text") == board[self.secondDiagonal[1][0]][self.secondDiagonal[1][1]].cget("text") and board[self.secondDiagonal[1][0]][self.secondDiagonal[1][1]].cget("text") == board[self.secondDiagonal[2][0]][self.secondDiagonal[2][1]].cget("text") and board[self.secondDiagonal[0][0]][self.secondDiagonal[0][1]].cget("text") != "":
            self.has_winner = True
            self.winner = board[self.secondDiagonal[0][0]][self.secondDiagonal[0][1]].cget("text")
        return self.has_winner
    
    def checkForTie(self):
        self.tie = True
        for x in board:
            for y in x:
                if y.cget("text") == "":
                    self.tie = False
                    return self.tie
                    pass
        return self.tie

    def changeTopLabel(self):
        if self.has_winner == False and self.tie == False:
            boardDisplay.topLabel.configure(text=self.currentPlayer + "'s turn")
        elif self.has_winner == True:
            boardDisplay.topLabel.configure(text=str(self.winner) + " is the winner", font=("Arial", 18))
            self.playAgainButton = tk.Button(text="Play Again!", width=10, height=2, font=("Arial", 20), command=restartGame)
            self.playAgainButton.grid(row=0, column=0)
            self.optionsButton = tk.Button(text = "Options", width=10, height=2, font=("Arial", 20), command=startUp)
            self.optionsButton.grid(row=0, column=2)
        else:
            boardDisplay.topLabel.configure(text="TIE!")
            self.playAgainButton = tk.Button(text="Play Again!", width=10, height=2, font=("Arial", 20), command=restartGame)
            self.playAgainButton.grid(row=0, column=0)
            self.optionsButton = tk.Button(text = "Options", width=10, height=2, font=("Arial", 20), command=startUp)
            self.optionsButton.grid(row=0, column=2)

    def resetLogicBoard(self):
        for row in range(3):
            for col in range(3):
                bot.logicBoard[row][col] = board[row][col].cget("text")

def startGame():
    startUp()

def continueStartGame():
    global boardDisplay
    global logic
    global bot
    global board
    global botPlayer
    try:
        logic.playAgainButton.grid_forget()
        boardDisplay.topLabel.grid_forget()
    except:
        pass
    board = [[[] for i in range(3)]for i in range(3)]
    bot = miniMaxBot()
    boardDisplay = ticTacToeBoard()
    logic = ticTacToeLogic()
    logic.getWinningCombinations()
    if botPlayer == "X":
        result = bot.miniMax(False, bot.logicBoard, logic.currentPlayer, 0)
        logic.play(result[1], result[2])


def restartGame():
    global boardDisplay
    global logic
    global board
    global bot
    logic.playAgainButton.grid_forget()
    logic.optionsButton.grid_forget()
    boardDisplay.topLabel.grid_forget()
    board = [[[] for i in range(3)]for i in range(3)]
    bot = miniMaxBot()
    boardDisplay = ticTacToeBoard()
    logic = ticTacToeLogic()
    if botPlayer == "X":
        result = bot.miniMax(False, bot.logicBoard, logic.currentPlayer, 0)
        logic.play(result[1], result[2])

    

startGame()
root.mainloop()