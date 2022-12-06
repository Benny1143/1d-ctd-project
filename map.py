from filesystem import get_map_info
from typing import Literal
import colors
from help import check_win


def dict_to_map(dd: dict) -> str:
    s = "==================\n"
    ls = list(["。"] * 5 for a in range(5))
    for (x, y), char in dd.items():
        ls[5-y][x-1] = char
    for row in ls:
        s += "[ " + " ".join(row) + " ]\n"
    return s + "=================="


class Map():
    def __init__(self, mapID, dual: bool = False):
        self.dual = dual
        self.mapID = mapID
        self.characters, self.winningConditions, user = get_map_info(mapID)
        self.end = False
        if type(user) == list:
            self.user = user
        elif type(user) == tuple:
            self.user = [user]
            if dual:
                coordinate = (1, 1)
                while True:
                    if not self.characters.get(coordinate):
                        self.user.append(coordinate)
                        self.characters[coordinate] = "他"
                        break
                    x, y = coordinate
                    if x <= 5:
                        x += 1
                    elif y <= 5:
                        y += 1
                    else:
                        print("Error: Unable to add second player")
                        exit()
                    coordinate = x, y
        else:
            print(colors.Red + "Invalid User" + colors.White)
        self.copy_user = self.user.copy()
        self.copy_characters = self.characters.copy()
        self.copy_winningConditions = self.winningConditions.copy()

    def restart(self) -> None:
        self.user = self.copy_user
        self.characters = self.copy_characters.copy()
        self.winningConditions = self.copy_winningConditions.copy()

    def get_map(self) -> str:
        return dict_to_map(self.characters)

    def get_characters(self) -> dict:
        return self.characters

    def is_dual(self) -> bool:
        return self.dual

    def move_character(self, key: str, user_id: int = 0) -> Literal[False] | None:
        def is_blocked(cor: tuple) -> bool:
            return not not self.characters.get(cor)

        def is_character(cor: tuple) -> bool:
            return self.characters.get(cor) in ["我", "他"]

        def check_winning(coordinate: tuple[int, int]):
            characters = self.characters
            winning_conditions = self.winningConditions
            character = characters.get(coordinate)
            changes = check_win(character, coordinate,
                                characters, winning_conditions)
            if changes:
                # Check if all winning conditions is sastify
                for name in winning_conditions:
                    wc = winning_conditions[name]
                    if not wc.won:
                        return
                self.end = True

        user = self.user[user_id]
        x, y = user

        if key == "w":
            # Check for top wall
            if y == 5:
                return False
            else:
                user = (x, y+1)
                if is_blocked(user):
                    # Check the item infront
                    ahead = (x, y+2)
                    if is_character(user) or is_blocked(ahead):
                        return False
                    else:
                        if y+1 == 5:
                            return False
                        self.updateCharacters(user, ahead)
                        check_winning(ahead)
        elif key == "d":
            # Check for left wall
            if x == 5:
                return False
            else:
                user = (x+1, y)
                if is_blocked(user):
                    # Check the item infront
                    ahead = (x+2, y)
                    if is_character(user) or is_blocked(ahead):
                        return False
                    else:
                        if x+1 == 5:
                            return False
                        self.updateCharacters(user, ahead)
                        check_winning(ahead)

        elif key == "s":
            # Check for bottom wall
            if y == 1:
                return False
            else:
                user = (x, y-1)
                if is_blocked(user):
                    # Check the item infront
                    ahead = (x, y-2)
                    if is_character(user) or is_blocked(ahead):
                        return False
                    else:
                        if y-1 == 1:
                            return False
                        self.updateCharacters(user, ahead)
                        check_winning(ahead)

        elif key == "a":
            # Check for right wall
            if x == 1:
                return False
            else:
                user = (x-1, y)
                if is_blocked(user):
                    # Check the item infront
                    ahead = (x-2, y)
                    if is_character(user) or is_blocked(ahead):
                        return False
                    else:
                        if x-1 == 1:
                            return False
                        self.updateCharacters(user, ahead)
                        check_winning(ahead)

        # Update user coordinates
        self.user[user_id] = user
        self.updateCharacters((x, y), user)

    def updateCharacters(self, bcor: tuple, acor: tuple) -> None:
        char = self.characters[bcor]
        del self.characters[bcor]
        self.characters[acor] = char
