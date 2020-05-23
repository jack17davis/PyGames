from graphics import *
import time

pieceColors = [color_rgb(127,127,127),color_rgb(50, 50, 250), color_rgb(230, 50, 50)]
squareColors = [color_rgb(127, 0, 0), color_rgb(255, 255, 255)]

class Location:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

class board:
    
    def __init__(self, name, boardWidth = 8, boardHeight = 8, squareSize = 75):
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight
        self.squareSize = squareSize
        self.textHeight = squareSize/2
        self.win = GraphWin(name, boardWidth * squareSize, self.textHeight + boardHeight * squareSize)
        self.win.setBackground("black")
        self._boardInit()

    def _boardInit(self):
        for i in range (0, self.boardWidth): #for every square
            for j in range(0,self.boardHeight):
                top = Point(i * self.squareSize, j * self.squareSize + self.textHeight)
                bot = Point((i + 1) * self.squareSize, (j + 1) * self.squareSize + self.textHeight)
                temp = Rectangle(top,bot)
                temp.setFill(squareColors[1 if (i + j) % 2 == 1 else 0]) #alternate colors to get a checkered board
                temp.draw(self.win)
                #time.sleep(1)

    def playersInit(self, p1sPieces, p2sPieces):
        self.clearBoard() # remove all existing pieces
        for piece in p1sPieces: #add all of player one's pieces to the board
            if piece.x < 0 or piece.x >= self.boardWidth or piece.y < 0 or piece.y >= self.boardHeight:
                raise Exception('invalid piece: ' + str(piece))
            elif self.pieces[piece.x][piece.y] != 0: #if there's already a piece here
                raise Exception('At least two pieces at: ' + str(piece))
            else:
                self.pieces[piece.x][piece.y] = 1 #player 1 has a piece here so draw it
                newPiece = Circle(Point((0.5 + piece.x) * self.squareSize, (0.5 + piece.y) * self.squareSize + self.textHeight), self.squareSize * 2 / 5)
                newPiece.setFill(pieceColors[1])
                newPiece.setWidth(3)
                newPiece.draw(self.win)

        for piece in p2sPieces: #add all of player two's pieces to the board
            if piece.x < 0 or piece.x >= self.boardWidth or piece.y < 0 or piece.y >= self.boardHeight:
                raise Exception('invalid piece: ' + str(piece))
            elif self.pieces[piece.x][piece.y] != 0: #if there's already a piece here
                raise Exception('At least two pieces at: ' + str(piece))
            else:
                self.pieces[piece.x][piece.y] = 2 #player 1 has a piece here so draw it
                newPiece = Circle(Point((0.5 + piece.x) * self.squareSize, (0.5 + piece.y) * self.squareSize + self.textHeight), self.squareSize * 2 / 5)
                newPiece.setFill(pieceColors[2])
                newPiece.setWidth(3)
                newPiece.draw(self.win)


    def makeMove(self, L1, L2):
        return True

    def clearBoard(self):
        #intialize array to all zeros
        # 0 = empty space
        # 1 = player 1
        # 2 = player 2
        self.pieces = []
        for i in range(self.boardHeight):
            row = [0] * self.boardWidth
            self.pieces += [row]

    def setText(self,text):
        return text

    def getClickedSquare(self):
        while True:
            clickPos = self.win.getMouse()
            squareX = int(clickPos.x / self.squareSize)
            squareY = int((clickPos.y - self.textHeight) / self.squareSize)
            if squareX >= 0 and squareX < self.boardWidth and squareY >= 0 and squareY < self.boardHeight:
                return Location(squareX, squareY)

    def close(self):
        self.win.close()

    #def __getitem__(self, index):
        
    #def __setitme__(self, index, newVal):

def main():
    myBoard = board("test")
    #myBoard.playersInit([Location(1,2),Location(50000000,3)], [Location(0,0)]) #Location out of bounds
    #myBoard.playersInit([(1,2),(5,3)], [(0,0)]) #using tuples
    p1sPieces = [Location(0,0),Location(0,2),Location(1,1),Location(2,0)]
    p2sPieces = [Location(7,7),Location(7,5),Location(6,6),Location(5,7)]
    myBoard.playersInit(p1sPieces, p2sPieces)
    time.sleep(4)
    myBoard.close()

if __name__ == "__main__":
    main()



