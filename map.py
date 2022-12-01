from filesystem import getMapInfo


def dictToMap(dd: dict):
    s = "=============\n"
    ls = list(["。"] * 5 for a in range(5))
    for (x, y), char in dd.items():
        ls[5-y][5-x] = char
    for row in ls:
        s += "[ " + " ".join(row) + " ]\n"
    return s + "============="


class Map():
    def __init__(self, mapID):
        self.mapID = mapID
        self.characters, self.winningConditions, self.user = getMapInfo(mapID)

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
                return
            new_cor = (x, y+1)
            if isBlocked(new_cor):
                # Check the item infront
                ahead = (x, y+1)
                if isBlocked(ahead):
                    return
                else:
                    self.user = new_cor
                    self.updateCharacters(self.user, ahead)

        elif key == "a":
            # Check for left wall
            if x == 1:
                return
            new_cor = (x-1, y)
            if isBlocked(new_cor):
                # Check the item infront
                ahead = (x-2,y)
                if isBlocked(ahead):
                    return
                else:
                    self.user = new_cor
                    self.updateCharacters(self.user, ahead)

        elif key == "s":
            # Check for bottom wall
            if y == 1:
                return
            new_cor = (x, y-1)
            if isBlocked(new_cor):
                # Check the item infront
                ahead = (x, y-2)
                if isBlocked(ahead):
                    return
                else:
                    self.user = new_cor
                    self.updateCharacters(self.user, ahead)

        elif key == "d":
            # Check for right wall
            if x == 5:
                return 
            new_cor = (x+1, y)
            if isBlocked(new_cor):
                # Check the item infront
                ahead = (x+2, y)
                if isBlocked(ahead):
                    return
                else:
                    self.user = new_cor
                    self.updateCharacters(self.user, ahead)

        self.updateCharacters((x, y), self.user)

    def updateCharacters(self, bcor, acor):
        char = self.characters[bcor]
        del self.characters[bcor]
        self.characters[acor] = char
