from filesystem import getMapInfo


def dictToMap(dd: dict):
    s = "=============\n"
    ls = list(["."] * 5 for a in range(5))
    for (x, y), char in dd.items():
        ls[y - 1][x - 1] = char
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
        x, y = self.user
        if key == "w":
            self.user = (x, y-1)
        elif key == "a":
            print("a")
        elif key == "s":
            print("s")
        elif key == "d":
            print("d")
        self.updateCharacters((x, y), self.user)

    def updateCharacters(self, bcor, acor):
        char = self.characters[bcor]
        del self.characters[bcor]
        self.characters[acor] = char
