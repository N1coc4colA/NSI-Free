#!/usr/bin/python3
import runtime
import pygame as pg

global switcher

switcher = {
"p1_left": pg.K_LEFT,
"p1_right": pg.K_RIGHT,
"p1_up": pg.K_UP,
"p1_down": pg.K_DOWN,
"p1_at1": pg.K_KP_MINUS,
"p1_at2": pg.K_KP_PLUS,
"p1_at3": pg.K_KP_ENTER,
"p2_left": pg.K_q,
"p2_right": pg.K_d,
"p2_up": pg.K_z,
"p2_down": pg.K_s,
"p2_at1": pg.K_TAB,
"p2_at2": pg.K_a,
"p2_at3": pg.K_e
}

class KeyButton(runtime.Button):
    keyID = -1
    _holds = False
    _lastKey = None
    def __init__(self):
        runtime.Button.__init__(self)
        self.setCallBack(self.onClicked)

    def customPaint(self):
        super().customPaint()

    def setKey(self, key_id):
        self.makePaintUpdate = True
        self.text = pg.key.name(key_id)
        self.keyID = key_id

    def onClicked(self):
        ""
        if self.keyID != -1 and self._lastKey != None:
            ""
            global switcher
            switcher[self.keyID] = self._lastKey
            self.text = pg.key.name(self._lastKey)
        self.makePaintUpdate = True
        self._holds = False
    
    def update(self, event):
        if super().update(event) == True:
            if event != None and event.type == pg.KEYDOWN and self.clicked:
                self._lastKey = event.key
                return False
        return True

class KeysSettings(runtime.Widget):
    _showing = False
    _rtm = runtime.Runtime()
    _win = None
    closed = True

    def __init__(self):
        runtime.Widget.__init__(self)
        self._rtm.addRoutine(self.postCheck)

    def postCheck(self):
        if self.closed == True and self._rtm.running == True:
            self.closed = True
            self._rtm.quit()

    def popup(self):
        if self._rtm.running == False:
            self._win = pg.display.set_mode((600, 600))
            self._rtm.setWindow(self._win)
            self._rtm.addRoutine(self.postCheck)
            self.closed = False
            self.loadElements()
            self._rtm.execute()

    def loadElements(self):
        j1 = runtime.Label()
        j2 = runtime.Label()

        list1 = []
        list2 = []
        for i in range(0, 14):
            list1.append(KeyButton())
        for i in range(0, 7):
            list2.append(runtime.Label())

        j1.text = "Joueur 1"
        j2.text = "Joueur 2"
        j1.font = pg.font.SysFont(None, 64)
        j2.font = pg.font.SysFont(None, 64)
        j1.rect.x = 20
        j2.rect.x = 320
        
        list2[0].text = "Aller à gauche";
        list2[1].text = "Aller à droite";
        list2[2].text = "Sauter";
        list2[3].text = "Se baisser";
        list2[4].text = "Attaque 1";
        list2[5].text = "Attaque 2";
        list2[6].text = "Attaque 3";
        
        global switcher
        keys = list(switcher.values())
        
        self._rtm.appendObject(j1)
        self._rtm.appendObject(j2)
        for i in range (0, 14):
            list1[i].rect.height = 40
            list1[i].setKey(keys[i])
            self._rtm.appendObject(list1[i])
        for i in range(0, 7):
            list2[i].rect.height = 20
            self._rtm.appendObject(list2[i])

        topBase = 60
        padding = 10
        for i in range(0, 7):
            list2[i].font = pg.font.SysFont(None, 20)
            list1[i].font = pg.font.SysFont(None, 40)
            list1[i+7].font = pg.font.SysFont(None, 40)
            list2[i].rect.x = 20
            list2[i].rect.y = topBase + i*60 + i*padding
            list1[i].rect.x = 20
            list1[i+7].rect.x = 320
            y = list2[i].rect.y + 20
            list1[i].rect.y = y
            list1[i+7].rect.y = y