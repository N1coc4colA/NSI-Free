﻿import runtime
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
    _label1 = None
    _label2 = None

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
            self._rtm.clear()
            self._win = pg.display.set_mode((800, 800))
            self._rtm.setWindow(self._win)
            self._rtm.addRoutine(self.postCheck)
            self.closed = False
            self.loadElements()
            self._rtm.execute()

    def onItemClick1(self, fp):
        """Callback to store the players chosen."""
        #Store the map
        self._fp1 = fp
        #Show the chosen map
        f = open(os.path.splitext(fp)[0] + ".field", "r")
        self._label1.text = "Joueur 1: " + str(f.read()).split("\n")[0]

    def onItemClick2(self, fp):
        """Callback to store the players chosen."""
        #Store the map
        self._fp2 = fp
        #Show the chosen map
        f = open(os.path.splitext(fp)[0] + ".field", "r")
        self._label2.text = "Joueur 2: " + str(f.read()).split("\n")[0]

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
        j1.text = "Choisissez un joueur!"
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
        while i<len(keys):
            it = cbi.ClickableItem(values[i])
            it.setImage(keys[i])
            it.makePaintUpdate = True
            it.setCallBack(self.onItemClick)
            it.setX(column*150 + spacing*column + left)
            it.setY(row*170 + spacing*row + top)
            column += 1
            if column == 2:
                column = 0
                row += 1
            items.append(it)
            self._rtm.appendObject(it)
            i+=1

        left = 400
        while i<len(keys):
            it = cbi.ClickableItem(values[i])
            it.setImage(keys[i])
            it.makePaintUpdate = True
            it.setCallBack(self.onItemClick)
            it.setX(column*150 + spacing*column + left)
            it.setY(row*170 + spacing*row + top)
            column += 1
            if column == 2:
                column = 0
                row += 1
            items.append(it)
            self._rtm.appendObject(it)
            i+=1

        self._label1 = runtime.Label()
        self._label1.text = "Choisissez une map"
        self._label1.font = pg.font.SysFont(None, 40)
        self._label1.color = (100, 100, 255)
        self._label1.rect.x = 5
        self._label1.rect.y = self._win.get_rect().height - self._label1.rect.height
        self._rtm.appendObject(self._label1)

        self._label2 = runtime.Label()
        self._label2.text = "Choisissez une map"
        self._label2.font = pg.font.SysFont(None, 40)
        self._label2.color = (100, 100, 255)
        self._label2.rect.x = 5
        self._label2.rect.y = self._win.get_rect().height - self._label2.rect.height
        self._rtm.appendObject(self._label2)