from pynput import keyboard
from help import *
from map import Map
from tm import TerminalManager
from firebase import get_highscores, get_user_map_scores, update_user_scores_by_map
from typing import Literal
from pynput.keyboard import Key, KeyCode
from om import OptionManager
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

        def switch_dual():
            self.dual_mode = not self.dual_mode

        while True:
            # Highscore String
            hs_string = self.get_highscore_string() + "\n"
            # Options
            play_string = "Play Stage " + str(self.map_id)

            map_score_dict = self.get_user_map_dic()

            score = map_score_dict.get(self.map_id)

            if score:
                play_string += f" (scored {score}pt)"

            om = OptionManager()
            om.add_option("1", play_string, self.game)
            om.add_option("2", f"Dual Mode ({self.dual_mode})", switch_dual)
            om.add_option("3", "Select Stage", self.stage_selection)

            # Check if user has played stage 1 & 2
            if map_score_dict.get(1) and map_score_dict.get(2):
                om.add_option("4", "Map Creator", self.map_creator)

            om.add_option("0", "Exit", exit)

            options_string = om.option_printer()

            self.refresh_highscore()

            string = title + hs_string + options_string
            option = om.input(string, self.print, self.set_error)
            om.get_option(option)()

    def game(self) -> None:
        map_id = self.map_id
        map = Map(map_id, self.dual_mode)
        title = f"Stage {map_id}"

        control_str = f"{'':2}w{'':3}{'':1}r - Restart\na s d{'':1}{'':1}e - Exit{'':3}"

        def print_map(map: Map, last_line: bool = False) -> None:
            map_str = map.get_map()
            ##
            spacing = "     "
            tmp_map_str = map_str.split("\n")
            # range of phrases to complete
            tmp_map_str[0] += spacing + "PHRASES"
            i = 1
            number_of_won = 0
            for cc in map.winningConditions:
                wc = map.winningConditions[cc]
                tmp_map_str[i] += spacing + (cc if wc.won else "##  ")
                tmp_map_str[i] += f" ({wc.name}) " + str(wc.point) + "pts"
                if wc.won:
                    number_of_won += 1
                i += 1
            tmp_map_str[i+1] += spacing + "TOTAL SCORE: " + \
                str(calculate_total_score(map.winningConditions))
            if number_of_won == len(map.winningConditions):
                tmp_map_str[i+1] += " 🎉🎉🎉"
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
                    self.set_error("Press Enter to Continue......")
                    print_map(map, True)
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

        # Update Score to Firebase
        total_score = calculate_total_score(map.winningConditions)
        update_user_scores_by_map(self.name, map_id, total_score)
        self.refresh_highscore()

        if map.end is False:
            q.put(False)
            self.set_error("Press Enter to Continue......")
            print_map(map, True)

    def map_creator(self) -> None:
        print("Map Creator")

    # Other helpers

    def refresh_highscore(self) -> dict[str, int]:
        self.highscore = get_highscores()
        return self.highscore
    # get_highscores calls firebase and return a list of name: highscore

    def get_highscores(self) -> dict[str, int]:
        return self.highscore if self.highscore else self.refresh_highscore()

    # get_highscore_string return the highscore in string format for printing
    def get_highscore_string(self) -> str:
        title = "Highscores \n==========="
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

    def get_user_map_dic(self):
        score_dict = {}
        all_scores = get_user_map_scores(self.name)
        for data in all_scores.each():
            score_dict[data.key()] = data.val()
        return score_dict

    def stage_selection(self):
        score_dict = self.get_user_map_dic()

        def get_score_string(map_id):
            score = score_dict.get(map_id)
            return f" (scored {score}pt)" if score else ""

        om = OptionManager()
        om.add_option("1", "Stage 1" + get_score_string(1), "1")
        om.add_option("2", "Stage 2" + get_score_string(2), "2")
        # TODO: Print All Stages Avaliable
        options_string = om.option_printer("Select Stage")
        stage = om.input(options_string, self.print, self.set_error)
        self.map_id = stage


pm = GameManagement()
pm.main()
