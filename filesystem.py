class winningCondition:

  def __init__(self, name, point):
    self.name = name
    self.point = point

  def name(self):
    return self.name

  def point(self):
    return self.point


def getMapInfo(mapID):
  filename = mapID + ".txt"
  print(filename)

  # Pesudo Values
  characters = {(3, 4): "c"}

  winningConditions = {
    "马蹄": winningCondition("chestnut", 4),
    "马路": winningCondition("horse", 2)
  }
  return (characters, winningConditions)
