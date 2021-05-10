import runtime
import pygame as pg
import clickableItem as cbi
import os

class PlayerChooser(runtime.Widget):
    """Window to let the users choose their player."""
    _showing = False
    _rtm = runtime.Runtime()
    _win = None
    _callBack = None
    _fp1 = ""
    _fp2 = ""
    closed = True
    _hasError = False

    def __init__(self):
        runtime.Widget.__init__(self)
        self._rtm.setPaintCallBack(self.winPaint)
        self._rtm.addRoutine(self.postCheck)

    def postCheck(self):
        """Runtime routine to know when window is left."""
        if self.closed == True and self._rtm.running == True:
            self.closed = True
            self._rtm.quit()

    def popup(self):
        """Shows the win"""
        if self._rtm.running == False:
            self._win = pg.display.set_mode((800, 800))
            self._rtm.setWindow(self._win)
            self._rtm.addRoutine(self.postCheck)
            self.closed = False
            self.loadElements()
            self._rtm.execute()

    def onItemClick(self, fp):
        """Callback to store the players chosen."""
        #Store the map
        self._fp = fp

    def handleNext(self):
        """Calls callback when everyone chose their player."""
        if self._callBack != None:
            if (self._fp2 != "" and self._fp1 != ""):
                self._callBack(self._fp)
            else:
                self._hasError = True
                self.makePaintUpdate = True

    def winPaint(self,  win):
        """Paints the window"""
        pg.draw.rect(win, (200, 200, 200),(0, 0, win.get_rect().width, win.get_rect().height))

    def loadElements(self):
        """Loads and displays UI elements."""
        j1 = runtime.Label()
        j1.text = "Choisissez la map!"
        j1.font = pg.font.SysFont(None, 64)
        j1.rect.x = 20
        self._rtm.appendObject(j1)

        btn = runtime.Button()
        btn.text = "Suivant >"
        btn.font = pg.font.SysFont(None, 32)
        btn.rect.x = 595
        btn.rect.y = 5
        btn.setCallBack(self.handleNext)
        self._rtm.appendObject(btn)

        mapList = os.listdir("./players/profiles")
        compatible = {}
        i = 0

        while i<len(mapList):
            filePath = os.path.splitext(mapList[i])
            if filePath[1] == ".image":
                if os.path.exists("./players/profiles/" + filePath[0] + ".field"):
                    try:
                        f = open("./players/profiles/" + filePath[0] + ".field", "r")
                        data = str(f.read()).split("\n")
                        if len(data) >= 2:
                            compatible["./players/profiles/" + filePath[0] + ".image"] = data[0]
                        f.close()
                    except:
                        ""
                else:
                    print("./players/profiles/" + filePath[0] + ".field", "has incoherent data when coupled with files")
            i+=1
        keys = list(compatible.keys())
        values = list(compatible.values())

        left = 20
        top = 60
        spacing = 5
        row = 0
        column = 0
        i = 0
        items = []
        while i<len(keys):
            it = ClickableItem(values[i])
            it.setImage(keys[i])
            it.makePaintUpdate = True
            it.setCallBack(self.onItemClick)
            it.setX(column*150 + spacing*column + left)
            it.setY(row*170 + spacing*row + top)
            column += 1
            if column == 4:
                column = 0
                row += 1
            items.append(it)
            self._rtm.appendObject(it)
            i+=1