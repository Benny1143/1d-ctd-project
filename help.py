def check_win(char, coord, all_char, win_cond):
    # char: str character moved
    # coord: tuple new coordinate of character moved to
    # all_char: dictionary of all characters with coordinates
    # win_cond: dictionary of all winning phrase

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

    # call function to ammend attribute of the phrase and tell if there are any changes made
    changes = update_win_state(ls, win_cond)

    # return boolean only??
    return changes


def update_win_state(ls, win_cond):
    # ls: list of phrase that exist
    # win_cond: dictionary of of key object

    # initialise no change
    changes = False

    # iterate over the ls of possible phrases
    for i in ls:
        # if phrase is in dictionary of phrase
        if i in win_cond:
            # check if the phrase is double counted
            if win_cond[i].won is False:
                # call method .matched to count the score ONCE
                win_cond[i].matched()
                # return boolean to indicate if any change has been made, be it 1 change or many changes
                changes = True
    return changes

#check_win("c", (1,1), {(1,2): "d", (2,1): "e"}, {})


def calculate_total_score(win_cond):
    total = 0
    for i in win_cond:
        if win_cond[i].won:
            total += win_cond[i].point
    return total
