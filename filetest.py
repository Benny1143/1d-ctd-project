from filesystem import get_character, ConvDictToString, get_winnings
f = open("1.txt", "r", encoding="utf8")
lines = f.read()
(characterstring, winningstring) = lines.split("\n")
# print(characterstring)
characterDic, user = get_character(characterstring)
winningDic = get_winnings(winningstring)

f = open("1.txt", "w", encoding="utf8" )
f.write(ConvDictToString(characterDic, winningDic))
f.close()