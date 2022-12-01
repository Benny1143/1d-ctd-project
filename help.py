# Create a funtion that prints out the map which is a 5 x 5 grid
# The function will take in a dict which contains (characters: (x,y))
# dd = {"c": (3, 5)}


# =============
# [ . . . . . ]
# [ . . . . . ]
# [ . . . . . ]
# [ . . . . . ]
# [ . . c . . ]
# =============
# def dictToMap(dd: dict):
#   s = "=============\n"
#   ls = list(["."] * 5 for a in range(5))
#   for (x, y), char in dd.items():
#     ls[y - 1][x - 1] = char
#   for row in ls:
#     s += "[ " + " ".join(row) + " ]\n"
#   return s + "============="


def get_character(s: str):
    dic = {}
    for e in s.split(";"):
        char = e[0]
        cor = e[1:].split(",")
        x = int(cor[0])
        y = int(cor[1])
        dic[(x, y)] = char
    return dic


# print(get_character("c1,1;b2,2"))


def readFile(stage):
    # Read file then
    # returb get_character from the string in the file
    pass
# print(readFile(1))



def hello(char, coord, all_charwin_cond):
    pass
