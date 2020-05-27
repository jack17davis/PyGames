from board import *
import time

def verticalcheckers(playercode):
    if playercode == 0:
        return
    brd = board("vertical Checkers", "Player 1 = 0\t Player 2 = 0", 6, 6, 75)
    p1sPieces = [Location(0,0),Location(1,0),Location(2,0),Location(3,0),Location(4,0),Location(5,0),
                 Location(0,1),Location(1,1),Location(2,1),Location(3,1),Location(4,1),Location(5,1)]
    p2sPieces = [Location(0,4),Location(1,4),Location(2,4),Location(3,4),Location(4,4),Location(5,4),
                 Location(0,5),Location(1,5),Location(2,5),Location(3,5),Location(4,5),Location(5,5)]
    brd.playersInit(p1sPieces, p2sPieces)
    time.sleep(4)
    brd.close()

def humanTurn(playerToMove):
    



def main():
    verticalcheckers(1)

if __name__ == "__main__":
    main()