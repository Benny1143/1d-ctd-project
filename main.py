from pynput import keyboard
from help import *
from map import Map
from tm import TerminalManager, colors


class ter():

    @staticmethod
    def print(string: str, inputStr: str = None):
        ln = string.split("\n")
        lines = 10
        if inputStr:
            lines -= 1
        # print(str('\n' * (lines - len(ln))) + string + '\r', end='', flush=True)

        # print("\x1B[9A" + string + '\r', end="")
        print(string, end="")
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


class GameManagement(TerminalManager):
    def __init__(self):
        super().__init__()
        self.map_id = 1
        self.name = "Benny"
        self.highscore = None

    # Pages
    def main(self):
        page_string = '''   ____   _        ____   
U /"___| |"|    U | __")u 
\| | u U | | u   \|  _ \/ 
 | |/__ \| |/__   | |_) | 
  \____| |_____|  |____/  
 _// \\\\  //  \\\\  _|| \\\\_  
(__)(__)(_")("_)(__) (__)
Welcome to Chinese Freshmore Programme 
Enter your name (1-7 characters): '''
        while True:
            # Restrict name input to 7 characters
            name = self.print(page_string, True)
            if len(name) > 7 or len(name) == 0:
                self.set_error("Invalid String Length")
                continue
            self.name = name
            self.main_menu()

    def main_menu(self):
        while True:
            self.refresh_highscore()
            # Title
            title = f"Main Menu\n\nWelcome {self.name}\n\n"
            # Highscore String
            hs_string = self.get_highscore_string() + "\n"
            # Options
            options = {"1": ("Play", self.game), "0": ("Exit", exit)}
            options_string = GameManagement.option_printer(options)
            # Option String
            option = self.print(title + hs_string + options_string, True)
            # Option Handler
            if option in options:
                options.get(option)[1]()
            else:
                self.set_error("Invalid Option")

    def game(self):
        map = Map(self.map_id)

    # Other helpers

    def refresh_highscore(self):
        self.highscore = firebase.getHighScores()
        return self.highscore
    # get_highscores calls firebase and return a list of name: highscore

    def get_highscores(self):
        return self.highscore if self.highscore else self.refresh_highscore()

    # get_highscore_string return the highscore in string format for printing
    def get_highscore_string(self):
        title = "Highscores\n==========="
        highscores = self.get_highscores()
        highscore_string = ""
        hs_keys = list(highscores.keys())
        for i in range(3):
            if (i + 1) > len(hs_keys):
                highscore_string += "\n"
                continue
            name = hs_keys[i]
            score = highscores[hs_keys[i]]
            highscore_string += f"\n{name:8}{score:3}"
        return title + (highscore_string if highscore_string else "\nNil") + "\n"

    # get_highscore_string takes in a list of {(i, option)}
    # returns the formatted string
    @staticmethod
    def option_printer(options: list):
        # options: [option]
        # Dic to List converter
        ls = list(map(lambda e: (e[0], e[1][0]), options.items()))
        return "{color}Options:\n{options_string}\nEnter Option: {white}".format(
            options_string='\n'.join(f"{i:>4}   {option}" for i, option in ls),
            color=colors.Yellow, white=colors.White)


pm = GameManagement()
pm.main_menu()
