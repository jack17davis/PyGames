import verticalcheckers
from board import Location 
from datetime import datetime

startTime = datetime(1999,6,6,12,30,0,0,None) #just some initial value
timeLimit = 0

# Check whether time limit has been reached
def outOfTime():
    duration = datetime.now() - startTime
    return duration.seconds + duration.microseconds * 1e-6 >= timeLimit

def getMoveOptions(brd,playerToMove):

    moveList = []
    for i in range (brd.boardWidth):
        for j in range (brd.boardHeight):
            #print("checking location: " + str(Location(i,j)))
            if playerToMove == brd.get(Location(i,j)): #check every location on the board for a piece that this player owns
                #print("\t One of our pieces has been found!")
                if brd.get(Location(i - 1, j)) == 0: #the piece can move to the left
                    #print("\t\t it can move to the left. Adding move option " + str(Location(i,j)) + "->" + str(Location(i-1,j)))
                    moveList.append((Location(i, j),Location(i - 1, j)))
 
                if brd.get(Location(i + 1, j)) == 0: #the piece can move to the right
                    #print("\t\t it can move to the right. Adding move option " + str(Location(i,j)) + "->" + str(Location(i+1,j)))
                    moveList.append((Location(i, j),Location(i + 1, j)))

                Lstart = Location(i,j)
                Lend = Location(i, brd.boardHeight) if playerToMove == 1 else Location(i, 0)  #farthest the piece could move vertically
                dist = abs(Lend.y - Lstart.y)
                dir = 1 if playerToMove == 1 else -1 #allows us to use the same code for player 1 and player 2

                #check directly in front of the piece
                if brd.get(Location(Lstart.x, Lstart.y + 1 * dir)) == 0:
                    #print("\t\t it can move forward. Adding move option " + str(Location(i,j)) + "->" + str(Location(Lstart.x, Lstart.y + 1 * dir)))
                    moveList.append((Lstart,Location(Lstart.x, Lstart.y + 1 * dir)))

                for jmp in range (1, dist + 1): #check every space that's part of the jump
                    if jmp % 2 == 1 and brd.get(Location(Lstart.x, Lstart.y + jmp * dir)) == 0: #there isn't a piece to jump over
                        break
                    if jmp % 2 == 0 and brd.get(Location(Lstart.x, Lstart.y + jmp * dir)) != 0: #if there's a piece in the way a multi-jump isn't possible
                        break
                    if jmp % 2 == 0 and brd.get(Location(Lstart.x, Lstart.y + jmp * dir)) == 0: #if there's an open space we could jump there
                        #print("\t\t it can jump " + str(jmp) + " spaces forward. Adding move option " + str(Location(i,j)) + "->" + str(Location(Lstart.x, Lstart.y + jmp * dir)))
                        moveList.append((Lstart,Location(Lstart.x, Lstart.y + jmp * dir)))
    
    return moveList

def makeMove(brd, playerToMove, move):
    (L1,L2) = move
    temp = brd.copy()
    temp.makeMove(playerToMove, L1,L2)
    return temp

def getScore(brd):
    sum = 0
    for i in range (brd.boardWidth):
        for j in range (brd.boardHeight):
            if brd.get(Location(i,j)) == 1: #we've found one of player 1's pieces
                sum -= Location(i,j).distTo(Location(i,brd.boardHeight-1))
            elif brd.get(Location(i,j)) == 2: #we've found one of player 2's pieces
                sum += Location(i,j).distTo(Location(i,0))
    return sum

def getMove(brd, playerToMove, givenTimeLimit):
    #intialize global time variables for timer
    global startTime, timeLimit 
    startTime = datetime.now()
    timeLimit = givenTimeLimit
    
    moveList = getMoveOptions(brd, playerToMove)
    scoreList = []

    bestMoveSoFar = moveList[0]

    for move in moveList: #evaluate each state 1 move away
        projectedState = makeMove(brd, playerToMove, move)
        scoreList.append(getScore(projectedState))
    
        #may be useful for debugging
        #temp = getScore(projectedState)
        #scoreList.append(temp)
        #(L1,L2) = move
        #print("possible move(" + str(temp) + "): " + str(L1) + "->" + str(L2))

        if outOfTime(): #default in case we run out of time
            return bestMoveSoFar

    if playerToMove == 1: #if player 1 we should make the highest score move
        bestMoveSoFar = moveList[scoreList.index(max(scoreList))]
    else: #if player 2 we should make the lowest score move
        bestMoveSoFar = moveList[scoreList.index(min(scoreList))]
    
    return bestMoveSoFar