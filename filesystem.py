class WinningCondition:

    def __init__(self, name, point):
        self.name = name
        self.point = point

    def name(self) -> str:
        return self.name

    def point(self) -> str:
        return self.point


def get_character(string: str):
    #  string example: "我1,1;马2,2"
    characters = {}
    user = ()
    for e in string.split(";"):
        char = e[0]
        x, y = e[1:].split(",")
        x = int(x)
        y = int(y)
        characters[(x, y)] = char
        if "我" == char:
            user = (x, y)
    #  TODO: Print Error if User is not found
    return characters, user


def get_winnings(string: str):
    # string example: "马蹄,chestnut,4;马路,road,2"
    winning_conditions = {}
    for i in string.split(";"):
        a = i.split(",")
        winning_character = str(a[0])
        name = str(a[1])
        point = int(a[2])
        winning_conditions[winning_character] = WinningCondition(name, point)
    return winning_conditions


def getMapInfo(mapID: str) -> tuple[dict, dict, tuple]:
    # Pesudo Values
    # user = (3, 5)
    # characters = {(3, 5): "我", (3, 4): "马"}
    # winningConditions = {
    #     "马蹄": winningCondition("hoof", 4),
    #     "马路": winningCondition("road", 2)
    # }
    # return (characters.copy(), winningConditions.copy(), user)
    with open(str(mapID) + ".txt", "r", encoding="utf8") as f:
        lines = f.read()
        (characterstring, winningstring) = lines.split("\n")
        characters, user = get_character(characterstring)
        winning_conditions = get_winnings(winningstring)
        return characters.copy(), winning_conditions.copy(), user


def dict_to_string(characters: dict[tuple[int, int], str], winning_conditions: dict[str, WinningCondition]):
    convertedchar = ""
    convertedwin = ""
    for charkey in characters:
        convertedchar += f"{characters[charkey]}{charkey[0]},{charkey[1]};"

    for winkey in winning_conditions:
        convertedwin += f"{winkey},{winning_conditions[winkey].name},{winning_conditions[winkey].point};"
    return convertedchar[:-1] + "\n" + convertedwin[:-1]


def write_map_to_file(map_id: str, characters: dict[tuple[int, int], str], winning_conditions: dict[str, WinningCondition]):
    data = dict_to_string(characters, winning_conditions)
    with open(str(map_id) + ".txt", "w", encoding="utf8") as f:
        f.write(data)


if __name__ == "__main__":
    # Write Test Cases
    characters = {(3, 5): "我", (3, 4): "马"}
    winning_conditions = {
        "马蹄": WinningCondition("hoof", 4),
        "马路": WinningCondition("road", 2)
    }
    print(getMapInfo(1))
    print(write_map_to_file(1, characters, winning_conditions))
