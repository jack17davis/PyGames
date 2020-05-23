from graphics import *
import time

pieceColors = [color_rgb(50, 50, 250), color_rgb(230, 50, 50)]
squareColors = [color_rgb(127, 0, 0), color_rgb(255, 255, 255)] # need to make these more different

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
        return 5

    def makeMove(self, L1, L2):
        return True

    def clearBoard(self):
        return 1

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

def main():
    myBoard = board("test")
    time.sleep(4)
    myBoard.close()

if __name__ == "__main__":
    main()



