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



def check_win(char, coord, all_char, win_cond):
    #char: str character moved
    #coord: tuple coordinate of character moved
    #all_char: dictionary of all characters with coordinates
    #win_cond: dictionary of key object
    
    # unpack coord tuple
    x, y = coord
    
    # compile list of words
    ls = []

    # check left of char
    if all_char.get((x-1, y)) != None:
        left_char = all_char.get((x-1, y))
        ls.append(left_char + char)
    # check top of char
    if all_char.get((x, y+1)) != None:
        top_char = all_char.get((x, y+1))
        ls.append(top_char + char)
    # check right of char
    if all_char.get((x+1, y)) != None:
        right_char = all_char.get((x+1, y))
        ls.append(char + right_char)
    # check bottom of char
    if all_char.get((x, y-1)) != None:
        bottom_char = all_char.get((x, y-1))
        ls.append(char + bottom_char)
    
    # call function to count points
    return count_points(ls, win_cond)
    pass

def count_points(ls, win_cond):
    #ls: list of phrase that exist
    #win_cond: dictionary of of key object
    
    # initialise total points
    total_points = 0

    # iterate over the ls of possible phrases
    for i in ls:
        if i in win_cond:
            # total_points += win_cond[i].point
            # When wc is not matched
            if win_cond.won is False:
                win_cond.matched()
                total_point += win_cond[i].point
    return total_points




#check_win("c", (1,1), {(1,2): "d", (2,1): "e"}, {})