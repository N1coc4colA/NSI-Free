import os
from importlib.machinery import SourceFileLoader

def loadMap(mapDir, p1, p2):
    """Loads the map, first player and second one, then retrieve the map object."""

    print("Map to load:", mapDir, "\nP1P:", p1, "\nP2P:", p2)

    #Load source files to make the players and the map
    map = SourceFileLoader("pringles.loadedMap", mapDir).load_module().Map()
    if map != None:
        map.clear()
    if p1 != "" and map != None:
        map.setJ1(SourceFileLoader("pringles.Player1", p1).load_module().Player())
    if p2 != "" and map != None:
        map.setJ1(SourceFileLoader("pringles.Player2", p2).load_module().Player())
    return map