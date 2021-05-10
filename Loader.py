import os
from importlib.machinery import SourceFileLoader

def loadMap(mapDir, p1, p2):
    """Loads the map, first player and second one, then retrieve the map object."""
    map = SourceFileLoader("pringles.loadedMap", mapDir).loadModule().Map()
    map.setJ1(SourceFileLoader("pringles.Player1", p1).loadModule().Player())
    map.setJ1(SourceFileLoader("pringles.Player2", p2).loadModule().Player())
    return map