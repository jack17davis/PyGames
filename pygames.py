import sys
from verticalcheckers import verticalcheckers 

def players():
    text = sys.argv[2] if len(sys.argv) > 2 else ""
    while True:
        if text == str(0):
            return 0
        elif text == str(1):
            return 1
        elif text == str(2):
            return 2
        elif text == str(3):
            return 3
        else:
            print("invaild input \"" + text + "\"")
        print("who's playing?")
        print("0 = exit")
        print("1 = two humans")
        print("2 = a human and the default computer")
        print("3 = your player and the default computer")
        text = input()

text = sys.argv[1] if len(sys.argv) > 2 else ""

while True:
    if text == str(0):
        break
    elif text == str(1):
        print("playing vertical checkers")
        if len(sys.argv) > 4:
            verticalcheckers(players(), p2file=sys.argv[3], p1file=sys.argv[4]) #p2 is the player at the bottom of the screen
        elif len(sys.argv) > 3:
            verticalcheckers(players(), p2file=sys.argv[3])
        else:
            verticalcheckers(players())
    else:
        print("invaild input \"" + text + "\"")
    print("choose a game to play:")
    print("0 = exit")
    print("1 = vertical checkers")
    text = input()


print("exiting...")

