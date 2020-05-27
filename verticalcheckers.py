from board import *
import time

boardWidth = 6
boardHeight = 6

def verticalcheckers(playercode, boardSize = 6):
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
        brd.close()
        return 1
    
    if playercode == 3: #user's file vs computer
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
    if playerToMove != brd.get(Lstart) or Lstart == Lend or brd.get(Lend) != 0: #does the move logically make sense
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
    verticalcheckers(1,6)