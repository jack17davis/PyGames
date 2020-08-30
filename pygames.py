import sys
sys.path.insert(1, './Util') #add a path to utility files
sys.path.insert(2, './Vertical_Checkers')
from tabulate import tabulate
from Vertical_Checkers.verticalcheckers import verticalcheckers 

gameCodes = [['1', 'vertical checkers']]

playerCodes = [['0', 'human vs human game'],
                ['1', 'human vs computer file (without a provided file the default player will be used)'],
                ['2', 'computer vs computer']]

descTable = ["", """Vertical Checkers
            Each player is trying to get their pieces to the other end of the board first. Pieces may move 1 space forward, 1 to 
            the side, or jump forward over a piece or a series of spaces and pieces. Jumping over a piece does not destroy it as 
            in regular checkers. The key to winning is to make use of multi-jumps across a series of multiple pieces and spaces.
            """,
            """Game 2
            description..."""]

def menu():
    print("")
    print("")
    print("Usage:\t  python pygames.py <game code> <player code> [<player 1 file> <player 2 file>]")
    print("\t  python pygames <game code> desc")
    print("\t  python pygames desc")
    print("")
    print("examples: python pygames.py 1 1 my_file (starts a game of vertical checkers against my_file)")
    print("\t  python pygames 1 desc (gives description of vertical checkers)")
    print("")
    print("valid game codes:")
    print(tabulate(gameCodes,tablefmt="plain"))
    print("")
    print("valid player codes:")
    print(tabulate(playerCodes,tablefmt="plain"))

#main logic of pygames
length = len(sys.argv) - 1 #0 index is not an argument

if length < 2: # 0 or 1 arguments is invalid
    menu()
    if length == 1 and sys.argv[1] == "desc":
        for gameDesc in descTable:
            print(gameDesc)
    exit()

if sys.argv[2] == "desc": #if they're asking for a description
    try:
        print(descTable[int(sys.argv[1])])
    except:
        print("invalid game code")
    finally:
        exit()

try: #try to get the game code and player code
    gameCode = int(sys.argv[1])
    playerCode = int(sys.argv[2])
except:
    print("unexpected input")
    exit()

if gameCode == 1:
    print("playing vertical checkers")
    if length > 3:
        verticalcheckers(playerCode, p2file=sys.argv[3], p1file=sys.argv[4]) #p2 is the player at the bottom of the screen
    elif length > 2:
        verticalcheckers(playerCode, p2file=sys.argv[3])
    else:
        verticalcheckers(playerCode)
else: #nothing matched 
    menu()