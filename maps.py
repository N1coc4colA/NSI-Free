#!/usr/bin/python3
import runtime
import pygame as pg
import os

class ClickableItem(runtime.Widget):
    clicked = False
    highlighted = (100, 100, 100)
    background = (150, 150, 150)
    scaled = None
    label = None
    _fp = None
    _callBack = None
    _ft = True

    def __init__(self, name):
        runtime.Widget.__init__(self)
        self.label = runtime.Label()
        self.label.text = name
        self.label.font = pg.font.SysFont(None, 40)
        self.label.color = (255, 255, 255)

    def setCallBack(self, func):
        self._callBack = func

    def setImage(self, path):
        self._fp = path
        if self.window != None:
            self.scaled = pg.transform.scale(pg.image.load(path), (100, 100))

    def setX(self, v):
        self.rect = pg.Rect((v, self.rect.y), (120, 160))

    def setY(self, v):
        self.rect = pg.Rect((self.rect.x, v), (120, 160))

    def setText(self, t):
        self.label.setText(t)
        self.makePaintUpdate = True

    def customPaint(self):
		#In case the widget is moved
        if self.label.rect.x != (self.rect.x + 10):
            self.label.rect.x = (self.rect.x + 10)
        if self.label.rect.width != (self.rect.width - 20):
            self.label.rect.width = (self.rect.width - 20)
        if self.label.rect.y != (self.rect.y + 120):
            self.label.rect.y = (self.rect.y + 120)
        if self.scaled == None:
            self.setImage(self._fp)
        if self._ft:
            print(self.rect)
            self._ft = False
        if self.clicked:
           pg.draw.rect(self.window, self.highlighted, self.rect)
        else:
           pg.draw.rect(self.window, self.background, self.rect)
        if self.scaled != None:
            if self.window != None:
                self.window.blit(self.scaled, pg.Rect((self.rect.x + 10, self.rect.y + 5), (100, 100)))
        self.label.customPaint()

    def update(self, event):
        if self.label.window == None and self.window != None:
            self.label.window = self.window

        if event != None and event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pg.mouse.get_pos()):
                self.clicked = True
                self.makePaintUpdate = True
                return False
            else:
                if self.clicked:
                    self.clicked = False
                    self.makePaintUpdate = True
                return True

        elif event != None and event.type == pg.MOUSEBUTTONUP:
            if self.clicked:
                self.clicked = False
                self.makePaintUpdate = True
                if self._callBack != None:
                    self._callBack(self._fp)
            return (self.rect.collidepoint(pg.mouse.get_pos()) == False)

        else:
            if self.label.update(event) == False:
                self.makePaintUpdate = True
                return False
            return True

class MapChooser(runtime.Widget):
    _showing = False
    _rtm = runtime.Runtime()
    _win = None
    _callBack = None
    closed = True

    def __init__(self):
        runtime.Widget.__init__(self)
        self._rtm.setPaintCallBack(self.winPaint)
        self._rtm.addRoutine(self.postCheck)

    def postCheck(self):
        if self.closed == True and self._rtm.running == True:
            self.closed = True
            self._rtm.quit()

    def popup(self):
        if self._rtm.running == False:
            self._win = pg.display.set_mode((800, 800))
            self._rtm.setWindow(self._win)
            self._rtm.addRoutine(self.postCheck)
            self.closed = False
            self.loadElements()
            self._rtm.execute()

    def onItemClick(self, fp):
        if self._callBack != None:
            self._callBack(fp)

    def winPaint(self,  win):
        pg.draw.rect(win, (200, 200, 200),(0, 0, win.get_rect().width, win.get_rect().height))

    def loadElements(self):
        j1 = runtime.Label()
        j1.text = "Choisissez la map!"
        j1.font = pg.font.SysFont(None, 64)
        j1.rect.x = 20
        self._rtm.appendObject(j1)

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
                    print("./maps/" + filePath[0] + ".field", "does not exists")
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
