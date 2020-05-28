from board import *
from datetime import datetime
import time
import importlib

boardWidth = 6
boardHeight = 6
timeLimit = 3.0

def verticalcheckers(playercode, boardSize = 6, p1file = "default_player", p2file = "default_player"):
    if playercode == 0: #0 = quit
        return

    #initialize the game
    text = "Player 1 = 0\t Player 2 = 0"
    scores = [0, 0, 0]
    global boardWidth, boardHeight
    boardWidth = boardSize
    boardHeight = boardSize
    brd = board("Vertical Checkers", text, boardWidth, boardHeight, 75)
    p1sPieces, p2sPieces = [], []
    for x in range (boardWidth):
        for y in range (int(boardHeight/3)):
            p1sPieces.append(Location(x,y))
            p2sPieces.append(Location(x,boardHeight-y-1))
            scores[0] += 1 #score[0] is our max score
    brd.playersInit(p1sPieces, p2sPieces)
    player = 1 #player 1 starts first

    if playercode == 1: #human vs human
        while True:
            _humanTurn(brd, player)
            text = _updateText(brd,text, scores)
            if len(text) < 3:
                return int(text) #let the caller know who won for score keeping purposes
            player = 2 - player + 1 #switch turns
    
    if playercode == 2: #human vs computer
        while True:
            _humanTurn(brd, player)

            #update board and switch turns
            text = _updateText(brd, text, scores)
            if len(text) < 3:
                return int(text) #let the caller know who won for score keeping purposes
            player = 2 - player + 1 #switch turns

            _computerTurn(brd,player)

            #update board and switch turns
            text = _updateText(brd, text, scores)
            if len(text) < 3:
                return int(text) #let the caller know who won for score keeping purposes
            player = 2 - player + 1 #switch turns
    
    if playercode == 3: #computer vs computer

        while True:
            _computerTurn(brd, player, p1file)

            #update board and switch turns
            text = _updateText(brd, text, scores)
            if len(text) < 3:
                return int(text) #let the caller know who won for score keeping purposes
            player = 2 - player + 1 #switch turns

            _computerTurn(brd,player, p2file)

            #update board and switch turns
            text = _updateText(brd, text, scores)
            if len(text) < 3:
                return int(text) #let the caller know who won for score keeping purposes
            player = 2 - player + 1 #switch turns
        
        brd.close()
        return 1

    #any other input should just return
    brd.close()
    return

#updates scores, determines if a player has won, return new text
#if a player has won return a string with the player who has won (1 or 2)
def _updateText(brd,text,scores):
    for i in range (boardWidth):
        if brd.get(Location(i,0)) == 2: #player 2 has scored a point
            scores[2] += 1
            if scores[2] < scores[0]: #but they haven't won yet
                brd.removePiece(Location(i,0))
            else: #player 2 has won
                brd.setText("Player 2 has won")
                time.sleep(1)
                brd.close()
                return "2" #used to denote end of game
        if brd.get(Location(i, boardWidth - 1)) == 1: #player 1 has scored a point
            scores[1] +=  1
            if scores[1] < scores[0]: #but they haven't won yet
                brd.removePiece(Location(i, boardWidth - 1))
            else: #player 1 has won
                brd.setText("Player 1 has won")
                time.sleep(2)
                brd.close()
                return "1" #used to denote end of game
    text = "Player 1 = " + str(scores[1]) + "\t Player 2 = " + str(scores[2])
    brd.setText(text)
    return text

#checks whether a given player's move is valid or not          
def _isvalid(brd, playerToMove, Lstart, Lend):
    if (Lstart.x < 0 or Lstart.x >= brd.boardWidth or Lstart.y < 0 or Lstart.y >= brd.boardHeight or #make sure Lstart is in bounds
    Lend.x < 0 or Lend.x >= brd.boardWidth or Lend.y < 0 or Lend.y >= brd.boardHeight or #make sure Lend is in bounds
    playerToMove != brd.get(Lstart) or Lstart == Lend or brd.get(Lend) != 0):
        return False

    #list of potential valid moves
    
    #shift to left or right
    elif (Lstart.x + 1 == Lend.x and Lstart.y == Lend.y) or (Lstart.x - 1 == Lend.x and Lstart.y == Lend.y):
        return True

    #shift towards opponents goal
    elif (Lstart.x == Lend.x and Lstart.y + 1 == Lend.y and playerToMove == 1) or (Lstart.x == Lend.x and Lstart.y - 1 == Lend.y and playerToMove == 2): 
        return True

    #jumps
    elif Lstart.x == Lend.x and abs(Lend.y - Lstart.y) % 2 == 0: #positions are in the same column and an even number of positions away
        dist = abs(Lend.y - Lstart.y)
        dir = 1 if playerToMove == 1 else -1 #allows us to use the same code for player 1 and player 2

        for i in range (1, dist): #check every space that's part of the jump
            if i % 2 == 1 and brd.get(Location(Lstart.x, Lstart.y + i * dir)) == 0: #there isn't a piece to jump over
                return False
            if i % 2 == 0 and brd.get(Location(Lstart.x, Lstart.y + i * dir)) != 0: #if there's a piece in the way a multi-jump isn't possible
                return False
        return True

    #this move isn't a valid move
    return False

#opens a file and calls getMove() on the file
#then makes the move returned if it is legal otherwise a default move
def _computerTurn(brd, playerToMove, filename = "default_player"):
    player = importlib.import_module(filename)
    startTime = datetime.now() #start a timer
    attemptedMove = player.getMove(brd, player, timeLimit)
    duration = datetime.now() - startTime #end the timer

    #check time
    if duration.seconds + duration.microseconds * 1e-6 >= timeLimit + 0.2:
        print("Time violation by player " + str(playerToMove))
        _makeDefaultMove(brd, playerToMove)
        return
    
    #check validity of move
    if _isvalid(brd, playerToMove, attemptedMove[0], attemptedMove[1]): #the computer's move is acceptable
        brd.makeMove(playerToMove, attemptedMove[0], attemptedMove[1])
        return
    else:
        print("Move violation by player " + str(playerToMove))
        _makeDefaultMove(brd, playerToMove)
        return

#returns the first legal move it finds
#note: as implemented currently it does not look for a jump
def _makeDefaultMove(brd, playerToMove):
    directions = [[1,0,], [-1,0], [0,1], [0,-1]]
    for i in range (brd.boardWidth):
        for j in range (brd.boardHeight):
            if playerToMove == brd.get(Location(i,j)): #check every location on the board for a piece that this player owns
                for direction in directions: #when we find one, find a direction it can move
                    if _isvalid(brd,playerToMove, Location(i, j), Location(i + direction[0], j + direction[1])):
                        brd.makeMove(playerToMove, Location(i, j), Location(i + direction[0], j + direction[1]))
                        return
    #no possible move was found
    print("Error: _makeDefaultMove couldn't find any possible moves!!!") #hopefully this never happens
    return

#reads and interprets user's mouse input
def _humanTurn(brd, playerToMove):
    startSelected = False
    start, click = Location(0,0), Location(0,0)

    while True: #loop infinitely until the user makes an acceptable move
        click = brd.getClickedSquare()
        if startSelected: #we have a complete move
            if _isvalid(brd, playerToMove, start, click):
                break # we now have an acceptable move
            else:
                brd.deselect(start)
                startSelected = False
        else: # this is the first piece
            if brd.get(click) == 0: #if there's no piece here
                continue
            brd.select(click)
            start = click
            startSelected = True
    brd.makeMove(playerToMove, start, click)

if __name__ == "__main__":
    verticalcheckers(3,6)