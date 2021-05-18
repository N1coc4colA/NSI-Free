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
    _label1 = None
    _label2 = None
    _button = None
    _endedCb = None

    def __init__(self):
        runtime.Widget.__init__(self)
        self._rtm.setPaintCallBack(self.winPaint)
        self._rtm.addRoutine(self.postCheck)

    def postCheck(self):
        """Runtime routine to know when window is left."""
        if self.closed == True and self._rtm.running == True:
            self.closed = True
            self._rtm.quit()
            if (self._endedCb != None):
                self._endedCb()

    def setEndCallBack(self, func):
        self._endedCb = func

    def popup(self):
        """Shows the win"""
        if self._rtm.running == False:
            self._rtm.clear()
            self._rtm.clear()
            self._win = pg.display.set_mode((800, 800))
            self._rtm.setWindow(self._win)
            self._rtm.addRoutine(self.postCheck)
            self.closed = False
            self.loadElements()
            self._rtm.execute()

    def setCallBack(self, func):
        self._callBack = func

    def onItemClick1(self, fp):
        """Callback to store the players chosen."""
        #Show the chosen map
        f = open(os.path.splitext(fp)[0] + ".field", "r")
        splitted = str(f.read()).split("\n")
        self._label1.text = "Joueur 1: " + splitted[0]
        #Store the map
        self._fp1 = "./players/" + splitted[1] + "/" + splitted[1] + ".py"
        #Change button's color to say that user can click on it
        if self._fp2 != "" and self._fp1 != "":
            self._button.background = (100, 100, 255)
            self._button.background_clicked = (175, 175, 255)

    def onItemClick2(self, fp):
        """Callback to store the players chosen."""
        #Store the map
        self._fp2 = "./players/" + os.path.splitext(fp)[0].split("/")[0] + "/" + os.path.splitext(fp)[0].split("/")[0] + ".py"
        #Show the chosen map
        f = open(os.path.splitext(fp)[0] + ".field", "r")
        self._label2.text = "Joueur 2: " + str(f.read()).split("\n")[0]
        if self._fp2 != "" and self._fp1 != "":
            self._button.background = (100, 100, 255)
            self._button.background_clicked = (175, 175, 255)

    def handleNext(self):
        """Calls callback when everyone chose their player."""
        if self._callBack != None:
            if (self._fp2 != "" and self._fp1 != ""):
                self._callBack(self._fp1, self._fp2)
            else:
                self._hasError = True
                self.makePaintUpdate = True

    def winPaint(self,  win):
        """Paints the window"""
        pg.draw.rect(win, (200, 200, 200),(0, 0, win.get_rect().width, win.get_rect().height))

    def generateClickablesFrom(self, dicted, cb, left = 20):
        keys = list(dicted.keys())
        values = list(dicted.values())
        top = 60
        spacing = 5
        row = 0
        column = 0
        i = 0
        while i<len(keys):
            it = cbi.ClickableItem(values[i])
            it.setImage(keys[i])
            it.makePaintUpdate = True
            it.setCallBack(cb)
            it.setX(column*150 + spacing*column + left)
            it.setY(row*170 + spacing*row + top)
            column += 1
            if column == 2:
                column = 0
                row += 1
            self._rtm.appendObject(it)
            i+=1

    def loadElements(self):
        """Loads and displays UI elements."""
        j1 = runtime.Label()
        j1.text = "Choisissez un joueur!"
        j1.font = pg.font.SysFont(None, 64)
        j1.rect.x = 20
        self._rtm.appendObject(j1)

        #Put the button
        self._button = runtime.Button()
        self._button.text = "Suivant >"
        self._button.font = pg.font.SysFont(None, 32)
        self._button.rect.x = 595
        self._button.rect.y = 5
        self._button.setCallBack(self.handleNext)
        self._button.background = (255, 100, 100)
        self._button.background_clicked = (255, 180, 180)
        self._rtm.appendObject(self._button)

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

        #Load the clickables
        self.generateClickablesFrom(compatible, self.onItemClick1)
        self.generateClickablesFrom(compatible, self.onItemClick2, 400)

        #Show the labels to let users know which player have been chosen
        self._label1 = runtime.Label()
        self._label1.text = "Choisissez le J1"
        self._label1.font = pg.font.SysFont(None, 40)
        self._label1.color = (100, 100, 255)
        self._label1.rect.x = 5
        self._label1.rect.y = self._win.get_rect().height - self._label1.rect.height
        self._rtm.appendObject(self._label1)

        self._label2 = runtime.Label()
        self._label2.text = "Choisissez une J2"
        self._label2.font = pg.font.SysFont(None, 40)
        self._label2.color = (100, 100, 255)
        self._label2.rect.x = 400
        self._label2.rect.y = self._win.get_rect().height - self._label2.rect.height
        self._rtm.appendObject(self._label2)