class winningCondition:

    def __init__(self, name, point):
        self.name = name
        self.point = point

    def name(self):
        return self.name

    def point(self):
        return self.point


def getMapInfo(mapID):

    filename = str(mapID) + ".txt"
    
    def readFile(stage):
        # Read file then
        # return get_character from the string in the file
        pass

    def get_character(s):
        characters = {}
        user = ()
        for (char, coor) in s.split(";"):
            char = e[0]
            coor = e[1:].split(",")
            x =  int(coor[0])
            y = int(coor[1])
            characters[(x,y)] = char
            if "我" == char:
                user = (x,y)
        return characters, user

    def get_winnings(t):
        winningConditions = {}
        for i in t.split(";"):

            a = i[:].split(",")
            winchar = str (a[0])
            name =  str (a[1])
            point = (a[2])
            winningConditions[winchar] = winningCondition(name, point)
        return winningConditions

    # Pesudo Values
    user = (3, 5)
    characters = {(3, 5): "我", (3, 4): "马"}
    # characters_get((3,4)) if return None, no character is at this position
    winningConditions = {
        "马蹄": winningCondition("chestnut", 4),
        "马路": winningCondition("horse", 2)
    }
    return (characters, winningConditions, user)
getMapInfo(1)