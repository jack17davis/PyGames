from graphics import *
import time

pieceColors = [color_rgb(240 ,240,0),color_rgb(50, 50, 250), color_rgb(230, 50, 50)]
squareColors = [color_rgb(127, 0, 0), color_rgb(255, 255, 255)]

def distance(a,b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

class board:
    
    #Initializes board object
    def __init__(self, name, startingText = "", boardWidth = 8, boardHeight = 8, squareSize = 75, visible = True):
        self.visible = visible
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight
        self.squareSize = squareSize
        self.textHeight = squareSize/2
        if self.visible:
            self.win = GraphWin(name, boardWidth * squareSize, self.textHeight + boardHeight * squareSize)
            self._textInit(startingText)
            self._boardInit()

    def _textInit(self, startingText):
        self.text = Text(Point(self.boardWidth * self.squareSize / 2, self.textHeight / 2), startingText)
        self.text.setTextColor(color_rgb(255,255,255))
        self.text.draw(self.win)
        self.win.setBackground("black")

    # local function used to create tiles
    def _boardInit(self):
        for i in range (0, self.boardWidth): #for every square
            for j in range(0,self.boardHeight):
                top = Point(i * self.squareSize, j * self.squareSize + self.textHeight)
                bot = Point((i + 1) * self.squareSize, (j + 1) * self.squareSize + self.textHeight)
                temp = Rectangle(top,bot)
                temp.setFill(squareColors[1 if (i + j) % 2 == 1 else 0]) #alternate colors to get a checkered board
                temp.draw(self.win)

    #clear board and add players at the given locations
    #expects arrays of pairs
    def playersInit(self, p1sPieces, p2sPieces):
        self.clearBoard() # remove all existing pieces

        #add all of player one's pieces to the board
        for piece in p1sPieces:
            if piece[0] < 0 or piece[0] >= self.boardWidth or piece[1] < 0 or piece[1] >= self.boardHeight:
                raise Exception('piece is off of the board: ' + str(piece))
            elif self.pieces[piece[0]][piece[1]] != 0: #if there's already a piece here
                raise Exception('At least two pieces at: ' + str(piece))
            else:
                #player 1 has a piece here so draw it
                self.pieces[piece[0]][piece[1]] = 1
                if self.visible:
                    newPiece = Circle(Point((0.5 + piece[0]) * self.squareSize, (0.5 + piece[1]) * self.squareSize + self.textHeight), self.squareSize * 2 / 5)
                    newPiece.setFill(pieceColors[1])
                    newPiece.setWidth(3)
                    newPiece.draw(self.win)

        #add all of player two's pieces to the board
        for piece in p2sPieces:
            if piece[0] < 0 or piece[0] >= self.boardWidth or piece[1] < 0 or piece[1] >= self.boardHeight:
                raise Exception('piece is off of the board: ' + str(piece))
            elif self.pieces[piece[0]][piece[1]] != 0: #if there's already a piece here
                raise Exception('At least two pieces at: ' + str(piece))
            else:
                #player 2 has a piece here so draw it
                self.pieces[piece[0]][piece[1]] = 2
                if self.visible:
                    newPiece = Circle(Point((0.5 + piece[0]) * self.squareSize, (0.5 + piece[1]) * self.squareSize + self.textHeight), self.squareSize * 2 / 5)
                    newPiece.setFill(pieceColors[2])
                    newPiece.setWidth(3)
                    newPiece.draw(self.win)

    #move a piece from location L1 to location L2, raises exception if a piece isn't found at L1
    def makeMove(self, L1, L2):
        #corner cases
        if L1[0] < 0 or L1[0] >= self.boardWidth or L1[1] < 0 or L1[1] >= self.boardHeight:
            raise Exception('invalid starting location: ' + str(L1))
        elif self.pieces[L1[0]][L1[1]] == 0:
            raise Exception('No piece found at starting location: '+ str(L1))
        elif L2[0] < 0 or L2[0] >= self.boardWidth or L2[1] < 0 or L2[1] >= self.boardHeight or self.pieces[L2[0]][L2[1]] != 0:
            raise Exception('invalid ending location: ' + str(L1))
        else: #move is okay

            player = self.pieces[L1[0]][L1[1]] #figure out who the piece belongs to

            #update internal pieces
            self.pieces[L1[0]][L1[1]] = 0
            self.pieces[L2[0]][L2[1]] = player

            if self.visible:

                #cover up where the piece was
                top = Point(L1[0] * self.squareSize, L1[1] * self.squareSize + self.textHeight)
                bot = Point((L1[0] + 1) * self.squareSize, (L1[1] + 1) * self.squareSize + self.textHeight)
                temp = Rectangle(top,bot)
                temp.setFill(squareColors[1 if (L1[0] + L1[1]) % 2 == 1 else 0]) #to keep color alternation
                temp.draw(self.win)

                #add the piece in its new location
                newPiece = Circle(Point((0.5 + L2[0]) * self.squareSize, (0.5 + L2[1]) * self.squareSize + self.textHeight), self.squareSize * 2 / 5)
                newPiece.setFill(pieceColors[player])
                newPiece.setWidth(3)
                newPiece.draw(self.win)

    #clear board of all players
    def clearBoard(self):
        #intialize array to all zeros
        # 0 = empty space
        # 1 = player 1
        # 2 = player 2
        self.pieces = []
        for i in range(self.boardHeight):
            row = [0] * self.boardWidth
            self.pieces += [row]

    #set text at the top of the board
    def setText(self,text):
        if self.visible:
            self.text.setText(text)

    #returns the location of the tile the user has clicked on
    def getClickedSquare(self):
        if not self.visible:
            return
        else:
            while True: #wait until the user clicks
                clickPos = self.win.getMouse()
                squareX = int(clickPos.x / self.squareSize)
                squareY = int((clickPos.y - self.textHeight) / self.squareSize)
                if squareX >= 0 and squareX < self.boardWidth and squareY >= 0 and squareY < self.boardHeight:
                    return (squareX, squareY)

    #highlights a square
    def select(self, x, y):
        if not self.visible:
            return
        else:
            if x < 0 or x >= self.boardWidth or y < 0 or y >= self.boardHeight:
                raise Exception('invalid location: ' + str((x,y)))
            elif self.pieces[x][y] != 1 and self.pieces[x][y] != 2:
                raise Exception('No piece at' + str((x,y)))
            #draw a highlighted background
            top = Point(x * self.squareSize, y * self.squareSize + self.textHeight)
            bot = Point((x + 1) * self.squareSize, (y + 1) * self.squareSize + self.textHeight)
            temp = Rectangle(top,bot)
            temp.setFill(pieceColors[0])
            temp.draw(self.win)

            #redraw the player
            newPiece = Circle(Point((0.5 + x) * self.squareSize, (0.5 + y) * self.squareSize + self.textHeight), self.squareSize * 2 / 5)
            newPiece.setFill(pieceColors[self.pieces[x][y]])
            newPiece.setWidth(3)
            newPiece.draw(self.win)

    #redraws a square (even if the given square isn't selected)
    def deselect(self, x, y):
        if not self.visible:
            return
        else:
            if x < 0 or x >= self.boardWidth or y < 0 or y >= self.boardHeight:
                    raise Exception('invalid location: ' + str(L(x,y)))
            #recolor the background
            top = Point(x * self.squareSize, y * self.squareSize + self.textHeight)
            bot = Point((x + 1) * self.squareSize, (y + 1) * self.squareSize + self.textHeight)
            temp = Rectangle(top,bot)
            temp.setFill(squareColors[1 if (x + y) % 2 == 1 else 0])
            temp.draw(self.win)

            #redraw the player
            newPiece = Circle(Point((0.5 + x) * self.squareSize, (0.5 + y) * self.squareSize + self.textHeight), self.squareSize * 2 / 5)
            newPiece.setFill(pieceColors[self.pieces[x][y]])
            newPiece.setWidth(3)
            newPiece.draw(self.win)

    def removePiece(self, x, y):
        if self.get(x,y) == 0:
            return
        else:
            if self.visible:
                #cover up where the piece was
                top = Point(x * self.squareSize, y * self.squareSize + self.textHeight)
                bot = Point((x + 1) * self.squareSize, (y + 1) * self.squareSize + self.textHeight)
                temp = Rectangle(top,bot)
                temp.setFill(squareColors[1 if (x + y) % 2 == 1 else 0]) #to keep color alternation
                temp.draw(self.win)
            self.pieces[x][y] = 0
            return

    #close the board
    def close(self):
        if self.visible:
            self.win.close()

    # returns the value at L
    #-1 = invalid input
    # 0 = empty space
    # 1 = player 1
    # 2 = player 2
    def get(self, x, y):
        if x < 0 or x >= self.boardWidth or y < 0 or y >= self.boardHeight:
            return -1
        return self.pieces[x][y]   

    def copy(self):
        temp = board("", "", self.boardWidth, self.boardHeight,self.squareSize, visible=False)
        p1sPieces, p2sPieces = [], []
        for x in range (self.boardWidth):
            for y in range (self.boardHeight):
                if self.pieces[x][y] == 1:
                    p1sPieces.append((x,y))
                elif self.pieces[x][y] == 2:
                    p2sPieces.append((x,y))
        temp.playersInit(p1sPieces,p2sPieces)
        return temp

    def __str__(self):
        returner = ""
        for row in self.pieces:
            returner += str(row) + '\n'
        return returner

def main():
    myBoard = board("testing", startingText="Loading...")
    p1sPieces = [(0,0),(0,2),(1,1),(2,0)]
    p2sPieces = [(7,7),(7,5),(6,6),(5,7)]
    myBoard.playersInit(p1sPieces, p2sPieces) 

    time.sleep(1)
    myBoard.makeMove(p1sPieces[0], (0,1))
    myBoard.makeMove(p2sPieces[3], (6,5))
    
    print(myBoard)

    myBoard.select(0,2)
    myBoard.select(0,1)
    myBoard.select(6,5)
    myBoard.select(7,7)

    time.sleep(10)
    myBoard.deselect(0,2)
    myBoard.deselect(0,1)
    myBoard.deselect(6,5)
    myBoard.deselect(7,7)

    myBoard.setText("Test Complete")
    time.sleep(1)
    myBoard.close()

if __name__ == "__main__":
    main()