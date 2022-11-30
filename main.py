from colorama import init
# from termcolor import cprint
from pynput import keyboard
from help import *
from map import Map

init()
# colored() will also work
# cprint("Hello World test","cyan")
# https://stackoverflow.com/questions/70480375/python-text-color-is-not-working-in-cmd-but-it-is-working-in-windows-terminal


class bcolors:
    # https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print("\n"*10)
class ter():

    @staticmethod
    def print(string: str, inputStr: str = None):
        ln = string.split("\n")
        lines = 10
        if inputStr:
            lines -= 1
        # print(str('\n' * (lines - len(ln))) + string + '\r', end='', flush=True)
        
        print("\x1B[9A" + string + '\r', end="")
        if inputStr:
            print()
            return input(inputStr)


# retrive and store high score data from firebase
class firebase():
    @staticmethod
    def getHighScores():
        return {"benny": 10, "peter": 2}


def loadStage(mapID):
    # get info from file system
    map = Map(mapID)

    def printMap(map: Map):
        mapString = map.getMap()
        ter.print(f"Stage: {mapID}\n" +
                  mapString +
                  f"\n{'':2}w{'':3}{'':3}r - Restart\na s d{'':1}{'':3}e - Exit")
    printMap(map)
    # info includes characters, win condition
    # dict containing char with a value tuple of coordinate xy
    # win condition contains (according to stage)

    # listener listen for wasd
    # https://stackoverflow.com/questions/11918999/key-listeners-in-python
    def on_press(key):
        if key == keyboard.Key.esc:
            return False  # stop listener
        try:
            k = key.char  # single-char keys
        except:
            k = key.name  # other keys
        if k in ["w", "a", "s", "d"]:
            # Move the character position
            map.moveCharacter(k)
            # Print Map
            printMap(map)
        elif k == "r":
            print("s")
        elif k == "e":
            return False
    # https://pynput.readthedocs.io/en/latest/keyboard.html

    def on_release(key):
        # print('{0} released'.format(key))
        if key in [keyboard.Key.esc, 'e']:
            return False
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
    # listener = keyboard.Listener(on_press=on_press)
    # listener.start()  # start to listen on a separate thread
    # listener.join()  # remove if main thread is polling self.keys


def mainMenu(name):
    hs = firebase.getHighScores()
    options = ["Play", "Exit", "gghgfg"]
    option = ter.print(
        f"""Main Menu
Welcome {name}

Highscores
===========""" + "".join(f"\n{name:10} {value: 4}"
                         for name, value in hs.items()) + "\n",
        bcolors.WARNING + "Options:\n" + "\n".join(f"{i:>4}   {options[i]}"
                                                   for i in range(len(options))) +
        "\nEnter Option: ")
    mapID = 1
    if option == "0":
        loadStage(mapID)
    else:
        print("exiting")
        exit()


def main():
    # Display Main Page
    name = ter.print(
        '''   ____   _        ____   
U /"___| |"|    U | __")u 
\| | u U | | u   \|  _ \/ 
 | |/__ \| |/__   | |_) | 
  \____| |_____|  |____/  
 _// \\\\  //  \\\\  _|| \\\\_  
(__)(__)(_")("_)(__) (__)
''' + "\nWelcome to Chinese Freshmore Programme", "Enter your name: ")
    mainMenu(name)


# main()
# mainMenu("Benny")
loadStage(1)
