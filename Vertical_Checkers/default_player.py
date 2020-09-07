import verticalcheckers
from board import distance
from datetime import datetime

startTime = datetime(1999,6,6,12,30,0,0,None) #just some initial value
timeLimit = 0
boardWidth = 0
boardHeight = 0

# Check whether time limit has been reached
def outOfTime():
    duration = datetime.now() - startTime
    return duration.seconds + duration.microseconds * 1e-6 >= timeLimit

def getMoveOptions(brd,playerToMove):

    moveList = []
    for i in range (boardWidth):
        for j in range (boardHeight):
            #print("checking location: " + str(Location(i,j)))
            if playerToMove == brd[i][j]: #check every location on the board for a piece that this player owns
                #print("\t One of our pieces has been found!")
                if i - 1 >= 0 and brd[i - 1][j] == 0: #the piece can move to the left
                    #print("\t\t it can move to the left. Adding move option " + str(Location(i,j)) + "->" + str(Location(i-1,j)))
                    moveList.append(((i, j),(i - 1, j)))
 
                if i + 1 < boardWidth and brd[i + 1][j] == 0: #the piece can move to the right
                    #print("\t\t it can move to the right. Adding move option " + str(Location(i,j)) + "->" + str(Location(i+1,j)))
                    moveList.append(((i, j),(i + 1, j)))

                Lstart = (i,j)
                Lend = (i, boardHeight) if playerToMove == 1 else (i, 0)  #farthest the piece could move vertically
                dist = abs(Lend[1] - Lstart[1])
                dir = 1 if playerToMove == 1 else -1 #allows us to use the same code for player 1 and player 2

                #check directly in front of the piece
                if brd[Lstart[0]][Lstart[1] + 1 * dir] == 0:
                    #print("\t\t it can move forward. Adding move option " + str(Location(i,j)) + "->" + str(Location(Lstart[0], Lstart[1] + 1 * dir)))
                    moveList.append((Lstart,(Lstart[0], Lstart[1] + 1 * dir)))

                for jmp in range (1, dist + 1): #check every space that's part of the jump
                    if Lstart[1] + jmp * dir not in range (boardHeight):
                        break
                    if jmp % 2 == 1 and brd[Lstart[0]][Lstart[1] + jmp * dir] == 0: #there isn't a piece to jump over
                        break
                    if jmp % 2 == 0 and brd[Lstart[0]][Lstart[1] + jmp * dir] != 0: #if there's a piece in the way a multi-jump isn't possible
                        break
                    if jmp % 2 == 0 and brd[Lstart[0]][Lstart[1] + jmp * dir] == 0: #if there's an open space we could jump there
                        #print("\t\t it can jump " + str(jmp) + " spaces forward. Adding move option " + str(Location(i,j)) + "->" + str(Location(Lstart[0], Lstart[1] + jmp * dir)))
                        moveList.append((Lstart,(Lstart[0], Lstart[1] + jmp * dir)))
    
    return moveList

def makeMove(brd, playerToMove, move):
    (L1,L2) = move
    temp = brd.copy()

    temp[L1[0]][L1[1]] = 0
    temp[L2[0]][L2[1]] = playerToMove
    return temp

def getScore(brd):
    sum = 0
    for i in range (boardWidth):
        for j in range (boardHeight):
            if brd[i][j] == 1: #we've found one of player 1's pieces
                sum -= distance((i,j),(i, boardHeight - 1))
            elif brd[i][j] == 2: #we've found one of player 2's pieces
                sum += distance((i,j),(i,0))
    return sum

def getMove(brd, playerToMove, givenTimeLimit):
    #intialize global time variables for timer
    global startTime, timeLimit, boardWidth, boardHeight
    startTime = datetime.now()
    timeLimit = givenTimeLimit
    boardWidth, boardHeight = brd.boardWidth, brd.boardHeight
    
    moveList = getMoveOptions(brd.toArray(), playerToMove)
    scoreList = []

    #if no possible moves, we lost
    if len(moveList) == 0:
        return None

    bestMoveSoFar = moveList[0]

    for move in moveList: #evaluate each state 1 move away
        projectedState = makeMove(brd.toArray(), playerToMove, move)
        scoreList.append(getScore(projectedState))
    
        #may be useful for debugging
        #temp = getScore(projectedState)
        #scoreList.append(temp)
        #(L1,L2) = move
        #print("possible move: " + str(L1) + "->" + str(L2))

        if outOfTime(): #default in case we run out of time
            return bestMoveSoFar

    if playerToMove == 1: #if player 1 we should make the highest score move
        bestMoveSoFar = moveList[scoreList.index(max(scoreList))]
    else: #if player 2 we should make the lowest score move
        bestMoveSoFar = moveList[scoreList.index(min(scoreList))]
    
    (L1,L2) = bestMoveSoFar
    #print("decided on move: "+ str(L1) + "->" + str(L2))
    return bestMoveSoFar