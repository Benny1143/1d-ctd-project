class winningCondition:

    def __init__(self, name, point):
        self.name = name
        self.point = point
        self.won = False

    def name(self):
        return self.name

    def point(self):
        return self.point

    def won(self):
        return self.won
        
    def matched(self):
        self.won = True


def getMapInfo(mapID):
    filename = str(mapID) + ".txt"
    # Fill in, uncomment this section
    # characters, user = get_characters()
    # winningConditions = get_winnings()

    # Pesudo Values
    user = (3, 5)
    characters = {(3, 5): "我", (3, 4): "马"}
    # characters.get((3,4)) if return None, no character is at this position
    winningConditions = {
        "马蹄": winningCondition("chestnut", 4),
        "马路": winningCondition("horse", 2)
    }
    return (characters, winningConditions, user)
