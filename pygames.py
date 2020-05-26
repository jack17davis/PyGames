from verticalcheckers import verticalcheckers 

def prompt():
    print("choose a game to play:")
    print("0 = exit")
    print("1 = vertical checkers")

def players():
    while True:
        print("who's playing?")
        print("0 = exit")
        print("1 = two humans")
        print("2 = a human and the default computer")
        print("3 = your player and the default computer")
        text = input()
        if text == str(0):
            return 0
        elif text == str(1):
            return 1
        elif text == str(2):
            return 2
        elif text == str(3):
            return 3
        else:
            print("program was not able to handle input \"" + text + "\"")

while True:
    prompt()
    text = input()
    if text == str(0):
        break
    elif text == str(1):
        print("playing vertical checkers")
        verticalcheckers(players())
    else:
        print("program was not able to handle input \"" + text + "\"")

print("exiting...")

