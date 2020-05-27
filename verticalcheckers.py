from board import *
import time

def verticalcheckers(playercode):
    if playercode == 0:
        return
    text = "Player 1 = 0\t Player 2 = 0"
    brd = board("vertical Checkers", text, 6, 6, 75)
    p1sPieces = [Location(0,0),Location(1,0),Location(2,0),Location(3,0),Location(4,0),Location(5,0),
                 Location(0,1),Location(1,1),Location(2,1),Location(3,1),Location(4,1),Location(5,1)]
    p2sPieces = [Location(0,4),Location(1,4),Location(2,4),Location(3,4),Location(4,4),Location(5,4),
                 Location(0,5),Location(1,5),Location(2,5),Location(3,5),Location(4,5),Location(5,5)]
    brd.playersInit(p1sPieces, p2sPieces)
    
    player = 1

    while True:
        humanTurn(brd, player)
        player = 2 - player + 1 

    brd.close()

def isvalid(brd, playerToMove, Lstart, Lend):
    if playerToMove != brd.get(Lstart) or Lstart == Lend or brd.get(Lend) != 0: #does the move logically make sense
        return False

    #list of potential valid moves
    
    #shift to left or right
    elif (Lstart.x + 1 == Lend.x and Lstart.y == Lend.y) or (Lstart.x - 1 == Lend.x and Lstart.y == Lend.y):
        return True
    #shift towards opponents goal
    elif (Lstart.x == Lend.x and Lstart.y + 1 == Lend.y and playerToMove == 1) or (Lstart.x == Lend.x and Lstart.y - 1 == Lend.y and playerToMove == 2): 
        return True
    else: #this move doesn't meet a valid move
        return False

def humanTurn(brd, playerToMove):
    startSelected = False
    start, click = Location(0,0), Location(0,0)

    while True: #loop infinitely until the user makes an acceptable move
        click = brd.getClickedSquare()
        if startSelected: #we have a complete move
            if isvalid(brd, playerToMove, start, click):
                break # we now have an acceptable move
            else:
                brd.deselect(start)
                startSelected = False
        else: # this is the first piece
            brd.select(click)
            start = click
            startSelected = True
    brd.makeMove(playerToMove, start, click)

def main():
    verticalcheckers(1)

if __name__ == "__main__":
    main()