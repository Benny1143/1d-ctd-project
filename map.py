from filesystem import getMapInfo
from typing import Literal
import colors


def dict_to_map(dd: dict) -> str:
    s = "==================\n"
    ls = list(["。"] * 5 for a in range(5))
    for (x, y), char in dd.items():
        ls[5-y][5-x] = char
    for row in ls:
        s += "[ " + " ".join(row) + " ]\n"
    return s + "=================="


class Map():
    def __init__(self, mapID, dual: bool = False):
        self.dual = dual
        self.mapID = mapID
        self.characters, self.winningConditions, user = getMapInfo(mapID)
        if type(user) == list:
            self.user = user
        elif type(user) == tuple:
            self.user = [user]
            if dual:
                # TODO: Search for empty space
                cor = (1, 1)
                self.user.append(cor)
                self.characters[cor] = "他"
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

        elif key == "a":
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

        elif key == "d":
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

        # Update user coordinates
        self.user[user_id] = user
        self.updateCharacters((x, y), user)

    def updateCharacters(self, bcor: tuple, acor: tuple) -> None:
        char = self.characters[bcor]
        del self.characters[bcor]
        self.characters[acor] = char
