from graphics import *
import time


class board:
    
    #constants
    boardWidth = 8
    boardHeight = 8
    squareSize = 75# Size of each square (pixels)
    textHeight = 50# Height of the text display at the top of the window (pixels)
    pieceColors = [color_rgb(50, 50, 250), color_rgb(230, 50, 50)]
    squareColors = [color_rgb(100, 220, 100), color_rgb(110, 240, 110)]
    win = []

    def __init__(self, name, boardWidth = 8, boardHeight = 8, squareSize = 75):
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight
        self.squareSize = squareSize
        self.textHeight = squareSize/2
        self.win = GraphWin(name, boardWidth * squareSize, self.textHeight + boardHeight * squareSize)
        self.win.setBackground("black")
        self.boardInit()

    def boardInit(self):
        flip = 1
        for i in range (0, self.boardWidth): #for every square
            if self.boardHeight %2 == 0:
                flip = 1 - flip
            for j in range(0,self.boardHeight):
                top = Point(i * self.squareSize, j * self.squareSize + self.textHeight)
                bot = Point((i + 1) * self.squareSize, (j + 1) * self.squareSize + self.textHeight)
                temp = Rectangle(top,bot)
                temp.setFill(self.pieceColors[flip])
                flip = 1 - flip
                temp.draw(self.win)
                #time.sleep(1)


    def close(self):
        self.win.close()

def main():
    myBoard = board("test")
    time.sleep(4)
    myBoard.close()

if __name__ == "__main__":
    main()



def getClickedSquare():
    while True:
        clickPos = win.getMouse()
        squareX = int(clickPos.x / squareSize)
        squareY = int((clickPos.y - textHeight) / squareSize)
        if squareX >= 0 and squareX < boardWidth and squareY >= 0 and squareY < boardHeight:
            return (squareX, squareY)