from filesystem import getMapInfo


def dictToMap(dd: dict):
    s = "==================\n"
    ls = list(["。"] * 5 for a in range(5))
    for (x, y), char in dd.items():
        ls[5-y][5-x] = char
    for row in ls:
        s += "[ " + " ".join(row) + " ]\n"
    return s + "=================="


class Map():
    def __init__(self, mapID):
        self.mapID = mapID
        self.characters, self.winningConditions, self.user = getMapInfo(mapID)
        self.copy_user = self.user
        self.copy_characters = self.characters.copy()
        self.copy_winningConditions = self.winningConditions.copy()

    def restart(self) -> None:
        self.user = self.copy_user
        self.characters = self.copy_characters.copy()
        self.winningConditions = self.copy_winningConditions.copy()

    def getMap(self):
        return dictToMap(self.characters)

    def moveCharacter(self, key: str):
        def isBlocked(cor):
            # cor = (3,4)
            character = self.characters.get(cor)
            if character is None:
                # safely move
                return False
            else:
                #  Something is blocking u
                return True
        x, y = self.user

        if key == "w":
            # Check for top wall
            if y == 5:
                return False
            else:
                new_cor = (x, y+1)
                if isBlocked(new_cor):
                    # Check the item infront
                    ahead = (x, y+2)
                    if isBlocked(ahead):
                        return False
                    else:
                        if y+1 == 5:
                            return
                        else:
                            self.user = new_cor
                            self.updateCharacters(self.user, ahead)
                else:
                    self.user = new_cor

        elif key == "a":
            # Check for left wall
            if x == 5:
                return False
            else:
                new_cor = (x+1, y)
                if isBlocked(new_cor):
                    # Check the item infront
                    ahead = (x+2, y)
                    if isBlocked(ahead):
                        return False
                    else:
                        if x+1 == 5:
                            return
                        else:
                            self.user = new_cor
                            self.updateCharacters(self.user, ahead)
                else:
                    self.user = new_cor

        elif key == "s":
            # Check for bottom wall
            if y == 1:
                return False
            else:
                new_cor = (x, y-1)
                if isBlocked(new_cor):
                    # Check the item infront
                    ahead = (x, y-2)
                    if isBlocked(ahead):
                        return False
                    else:
                        if y-1 == 1:
                            return self.user
                        else:
                            self.user = new_cor
                            self.updateCharacters(self.user, ahead)
                else:
                    self.user = new_cor

        elif key == "d":
            # Check for right wall
            if x == 1:
                return False
            else:
                new_cor = (x-1, y)
                if isBlocked(new_cor):
                    # Check the item infront
                    ahead = (x-2, y)
                    if isBlocked(ahead):
                        return False
                    else:
                        if x-1 == 1:
                            return
                        else:
                            self.user = new_cor
                            self.updateCharacters(self.user, ahead)
                else:
                    self.user = new_cor

        self.updateCharacters((x, y), self.user)

    def updateCharacters(self, bcor, acor):
        char = self.characters[bcor]
        del self.characters[bcor]
        self.characters[acor] = char
