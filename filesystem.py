class winningCondition:

    def __init__(self, name, point):
        self.name = name
        self.point = point

    def name(self) -> str:
        return self.name

    def point(self) -> str:
        return self.point

def get_character(s):
    characters = {}
    user = ()
    for e in s.split(";"):
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

def getMapInfo(mapID) -> tuple[dict, dict, tuple]:
    filename = str(mapID) + ".txt"
    
    f = open(filename, "r")
    lines = f.readlines()
        # Read file then
        # return get_character from the string in the file

def ConvDictToString(characters, winningConditons):
    convertedchar = ""
    convertedwin = ""
    for charkey in characters:
        convertedchar += f"{characters[charkey]}{charkey[0]},{charkey[1]};"

    for winkey in winningConditons:
        convertedwin += f"{winkey},{winningConditons[winkey].name},{winningConditons[winkey].point};"
    return convertedchar[:-1] + "\n" + convertedwin[:-1]
   

def writeToFile(filename, cdic, wcdic):
    def ConvDictToString(characters, winningConditons):

        convertedchar = ""
        convertedwin = ""
       
        for charkey in characters:
            convertedchar += f"{characters[charkey]}{charkey[0]},{charkey[1]};"

        for winkey in winningConditons:
            convertedwin += f"{winkey},{winningConditons[winkey].name},{winningConditons[winkey].point};"
        return convertedchar[:-1] + "\n" + convertedwin[:-1]
    # Test case
    print(ConvDictToString({(3, 5): "我", (3, 4): "马"}, {
        "马蹄": winningCondition("hoof", 4),
        "马路": winningCondition("road", 2)
    }))


    # Pesudo Values
    user = (3, 5)
    characters = {(3, 5): "我", (3, 4): "马"}
    # characters_get((3,4)) if return None, no character is at this position
    winningConditions = {
        "马蹄": winningCondition("hoof", 4),
        "马路": winningCondition("road", 2)
    }
    #store the winning condition as string "马蹄,chestnut,4;马路,road,2"
    #convert to a dict {"马蹄": {name: "chestnut", point: 4}, "马路": {name: "road", point: 2}} 
    return (characters.copy(), winningConditions.copy(), user)

# writeToFile(1)