#import stdio
from board import *

def prompt():
    print("choose a game to play:")
    print("0 = exit")
    print("1 = vertical checkers")


while True:
    prompt()
    text = input()
    if text == str(0):
        break
    elif text == str(1):
        print("playing vertical checkers")
        #verticalcheckers()
    else:
        print("program was not able to handle input \"" + text + "\"")

print("exiting...")

