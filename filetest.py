from filesystem import get_character, dict_to_string, get_winnings
f = open("1.txt", "r", encoding="utf8")
lines = f.read()
(characterstring, winningstring) = lines.split("\n")
# print(characterstring)
characterDic, user = get_character(characterstring)
winningDic = get_winnings(winningstring)

f = open("1.txt", "w", encoding="utf8" )
f.write(dict_to_string(characterDic, winningDic))
f.close()