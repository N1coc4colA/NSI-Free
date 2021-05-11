#!/usr/bin/python3
import runtime
import pygame as pg
import os

class ClickableItem(runtime.Widget):
    """ClickableItem is a widget close to Runtime.Button, it has text, an image, and can be clicked."""
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
        """Callback when clicked"""
        self._callBack = func

    def setImage(self, path):
        """Image to show in the widget, loaded by path"""
        self._fp = path
        if self.window != None:
            self.scaled = pg.transform.scale(pg.image.load(path), (100, 100))

    def setX(self, v):
        """To fix C copy behaviour struggling when accessing member objects"""
        self.rect = pg.Rect((v, self.rect.y), (120, 160))

    def setY(self, v):
        """To fix C copy behaviour struggling when accessing member objects"""
        self.rect = pg.Rect((self.rect.x, v), (120, 160))

    def setText(self, t):
        """Sets the text that will be displayed"""
        self.label.setText(t)
        self.makePaintUpdate = True

    def customPaint(self):
        """Custom widget painting"""
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
        """Event handler"""
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