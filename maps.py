#!/usr/bin/python3
import runtime
import pygame as pg
import clickableItem as cbi
import os

class MapChooser(runtime.Widget):
    """Lets the user choose the map he wants to play with. The replies with callback to load the map."""
    _showing = False
    _rtm = runtime.Runtime()
    _win = None
    _callBack = None
    _fp = ""
    _hasError = False
    _button = None
    _label = None
    closed = True

    def __init__(self):
        runtime.Widget.__init__(self)
        self._rtm.setPaintCallBack(self.winPaint)
        self._rtm.addRoutine(self.postCheck)

    def postCheck(self):
        """Runtime routine to know when the win is closed."""
        if self.closed == True and self._rtm.running == True:
            self.closed = True
            self._rtm.quit()

    def popup(self):
        """Shows the map chooser win"""
        if self._rtm.running == False:
            self._win = pg.display.set_mode((800, 800))
            self._rtm.setWindow(self._win)
            self._rtm.addRoutine(self.postCheck)
            self.closed = False
            self.loadElements()
            self._rtm.execute()

    def setCallBack(self, func):
        self._callBack = func

    def onItemClick(self, fp):
        """Click callback to update last map selected."""
        #Store the map
        self._fp = fp
        if (self._fp != ""):
            self._button.background =(100, 100, 255)
            self._button.background_clicked = (175, 175, 255)

            #Show the chosen map
            f = open(os.path.splitext(fp)[0] + ".field", "r")
            self._label.text = "Map choisie: " + str(f.read()).split("\n")[0]

    def handleNext(self):
        """Call callback when a map have been chosen."""
        if self._callBack != None:
            if self._fp != "":
                self._callBack(self._fp)

    def reset(self):
        self._hasError = False
        self._fp = ""

    def winPaint(self,  win):
        pg.draw.rect(win, (200, 200, 200),(0, 0, win.get_rect().width, win.get_rect().height))
        if (self._hasError):
            font = pygame.font.SysFont(None, 24)
            color = (255, 0, 0)
            image = font.render("Vous n'avez toujours pas choisi de map!", True, color)
            text_width, text_height = font.size(self.text)
            win.blit(image, (rect.x + ((rect.width-text_width)/2), rect.heiht - text_height - 5))

    def loadElements(self):
        """Loads UI elements"""
        j1 = runtime.Label()
        j1.text = "Choisissez la map!"
        j1.font = pg.font.SysFont(None, 64)
        j1.rect.x = 20
        self._rtm.appendObject(j1)

        self._button = runtime.Button()
        self._button.text = "Suivant >"
        self._button.font = pg.font.SysFont(None, 32)
        self._button.rect.x = 595
        self._button.rect.y = 5
        self._button.setCallBack(self.handleNext)
        self._button.background = (255, 100, 100)
        self._button.background_clicked = (255, 180, 180)
        self._rtm.appendObject(self._button)

        self._label = runtime.Label()
        self._label.text = "Choisissez une map"
        self._label.font = pg.font.SysFont(None, 40)
        self._label.color = (100, 100, 255)
        self._label.rect.x = 5
        self._label.rect.y = self._win.get_rect().height - self._label.rect.height
        self._rtm.appendObject(self._label)

        mapList = os.listdir("./maps")
        compatible = {}
        i = 0

        while i<len(mapList):
            filePath = os.path.splitext(mapList[i])
            if filePath[1] == ".image":
                if os.path.exists("./maps/" + filePath[0] + ".field"):
                    try:
                        f = open("./maps/" + filePath[0] + ".field", "r")
                        data = str(f.read()).split("\n")
                        if len(data) >= 2:
                            compatible["./maps/" + filePath[0] + ".image"] = data[0]
                        f.close()
                    except:
                        ""
                else:
                    print("./maps/" + filePath[0] + ".field", "has incoherent data when coupled with files")
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
            it = cbi.ClickableItem(values[i])
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
