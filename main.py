from pynput import keyboard
from help import *
from map import Map
from tm import TerminalManager, colors
from firebase import get_highscores, get_user_scores_by_map
from typing import Literal
from pynput.keyboard import Key, KeyCode
# https://docs.python.org/3/library/queue.html
import threading
import queue

q = queue.Queue()


class GameManagement(TerminalManager):
    def __init__(self):
        super().__init__()
        self.map_id = 1
        self.name = "benny"
        self.highscore = None
        self.dual_mode = False

    # Pages
    def main(self) -> None:
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
            # Secret switch
            if name == "0":
                self.switch_inplace()
            else:
                self.name = name.lower()
            self.main_menu()

    def main_menu(self) -> None:
        # Title
        title = f"Main Menu\n\nWelcome {self.name}\n\n"
        # Highscore String
        hs_string = self.get_highscore_string() + "\n"

        def switch_dual():
            self.dual_mode = not self.dual_mode

        while True:
            # Options
            play_string = "Play Stage " + str(self.map_id)
            score = get_user_scores_by_map(self.name, self.map_id)
            if score:
                play_string += f" (scored {score}pt)"
            options = {"1": (play_string, self.game), "2": (
                f"Dual Mode ({self.dual_mode})", switch_dual), "0": ("Exit", exit)}
            options_string = GameManagement.option_printer(options)

            self.refresh_highscore()
            option = self.print(title + hs_string + options_string, True)
            # Option Handler
            if option in options:
                options.get(option)[1]()
            else:
                self.set_error("Invalid Option")

    def game(self) -> None:
        map = Map(self.map_id, self.dual_mode)
        title = f"Stage {self.map_id}"

        control_str = f"{'':2}w{'':3}{'':1}r - Restart\na s d{'':1}{'':1}e - Exit{'':3}"

        def print_map(map: Map, last_line: bool = False) -> None:
            map_str = map.get_map()

            ##
            tmp_map_str = map_str.split("\n")
            # range of phrases to complete
            tmp_map_str[0] += "     " + "PHRASES"
            i = 1
            for cn in map.winningConditions:
                if map.winningConditions[cn].won:
                    tmp_map_str[i] += "     " + cn + \
                        " (" + map.winningConditions[cn].name + ")"
                else:
                    tmp_map_str[i] += "     ## (" + \
                        map.winningConditions[cn].name + ")"
                i += 1
            tmp_map_str[i+1] += "     " + "TOTAL SCORE: " + \
                str(calculate_total_score(map.winningConditions))
            new_map_str = "\n".join(tmp_map_str)
            ##

            self.print(
                "\n".join([title, new_map_str, control_str]), last_line, False)
        self.clear()
        print_map(map)

        wasd_keys = ("w", "a", "s", "d")
        arrow_keys = (keyboard.Key.up, keyboard.Key.left,
                      keyboard.Key.down, keyboard.Key.right)
        arrow_controls = {key: char for key,
                          char in zip(arrow_keys, wasd_keys)}

        # https://stackoverflow.com/questions/11918999/key-listeners-in-python

        def on_press(key: KeyCode | Key | None) -> Literal[False] | None:
            if map.end:
                return False

            def move_character(k: str, user_id: int = 0) -> None:
                q.put((k, user_id))
            if key == keyboard.Key.esc:
                return False  # stop listener
            if key in arrow_keys:
                return move_character(arrow_controls[key], 1 if map.is_dual() else 0)
            try:
                k = key.char  # single-char keys
            except:
                k = key.name  # other keys
            if k in wasd_keys:
                return move_character(k)
            elif k == "r":
                map.restart()
                print_map(map)
            elif k == "e":
                return False

        # https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/

        def worker():
            while True:
                data = q.get()
                if data == False:
                    break
                (k, user_id) = data
                if map.move_character(k, user_id) == False:
                    self.set_error("Something is blocking you")
                if map.end:
                    self.set_error("Press WASD or Arrow Key to Continue......")
                    print_map(map)
                    break
                print_map(map)
                q.task_done()

        threading.Thread(target=worker, daemon=True).start()

        # https://pynput.readthedocs.io/en/latest/keyboard.html
        # def on_release(key):
        #     # print('{0} released'.format(key))
        #     if key in [keyboard.Key.esc, 'e']:
        #         print("")
        #         return False
        # with keyboard.Listener(
        #         on_press=on_press,
        #         on_release=on_release) as listener:
        #     listener.join()
        listener = keyboard.Listener(on_press=on_press)
        listener.start()  # start to listen on a separate thread
        listener.join()  # remove if main thread is polling self.keys
        if map.end is False:
            q.put(False)
            self.set_error("Press Enter to Continue......")
            print_map(map, True)

    # Other helpers

    def refresh_highscore(self) -> dict[str, int]:
        self.highscore = get_highscores()
        return self.highscore
    # get_highscores calls firebase and return a list of name: highscore

    def get_highscores(self) -> dict[str, int]:
        return self.highscore if self.highscore else self.refresh_highscore()

    # get_highscore_string return the highscore in string format for printing
    def get_highscore_string(self) -> str:
        title = "Highscores\n==========="
        highscores = self.get_highscores()
        highscore_string = ""
        # https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
        highscores = {k: v for k, v in sorted(
            highscores.items(), key=lambda item: item[1], reverse=True)}
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
    def option_printer(options: list) -> str:
        # options: [option]
        # Dic to List converter
        ls = list(map(lambda e: (e[0], e[1][0]), options.items()))
        return "{color}Options:\n{options_string}\nEnter Option: {white}".format(
            options_string='\n'.join(f"{i:>4}   {option}" for i, option in ls),
            color=colors.Yellow, white=colors.White)


pm = GameManagement()
pm.main()
