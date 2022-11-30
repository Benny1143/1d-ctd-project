from filesystem import getMapInfo
from help import getMap
class Map():
  def __init__(self, mapID):
    self.mapID = mapID
    self.characters, self.winningConditions = getMapInfo(mapID)
  def printMap(self):
    getMap(self.characters)