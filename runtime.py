#!/usr/bin/python3

import pygame, sys
pygame.init()

class Widget(pygame.sprite.Sprite):
    rect = pygame.Rect((0, 0), (200, 200))
    image = None
    makePaintUpdate = False

    def __init__(self):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)
       self.window = None

       self.image = pygame.Surface([self.rect.width, self.rect.height])
       #On rempli l'image
       self.image.fill((0, 0, 0))
       #self.rect = self.image.get_rect()

    def setWindow(self, target):
        self.window = target

    def customPaint(self):
        if self.window != None:
            self.window.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, event):
        return True

class Picture(Widget):
    def __init__(self):
        Widget.__init__(self)

    def customPaint(self):
        size = self.image.get_size()
        pygame.draw.rect(pygame.Surface(size, pygame.SRCALPHA), (255, 255, 255), (0, 0, *size), border_radius=roundness)

class ProgressBar(Widget):
    maximum = 10
    pos = 3
    background = (0, 0, 0)
    foreground = (255, 0, 0)

    def __init__(self):
        Widget.__init__(self)

    def update(self, event):
        return True

    def customPaint(self):
        if self.window != None:
            pygame.draw.rect(self.window, self.background, self.rect)
            pygame.draw.rect(self.window, self.foreground, pygame.Rect((self.rect.x, self.rect.y), ((self.pos*self.rect.width/self.maximum), self.rect.height)))

class Label(Widget):
    text = "Bonjour"
    font = pygame.font.SysFont(None, 104)
    color = (0, 0, 0)

    def __init__(self):
        Widget.__init__(self)
        self.rect = pygame.Rect((0, 0), (200, 50))

    def customPaint(self):
        if self.window != None:
            self.image = self.font.render(self.text, True, self.color)
            self.window.blit(self.image, (self.rect.x, self.rect.y))

    def setText(self, t):
        self.makePaintUpdate = True
        self.text = t

    def update(self, event):
        return True

class Button(Label):
    clicked = False
    background = (100, 100, 255)
    background_clicked = (175, 175, 255)
    _callBack = None

    def __init__(self):
        Label.__init__(self)
        self.font = pygame.font.SysFont(None, 54)

    def setCallBack(self, func):
        self._callBack = func

    def customPaint(self):
        if self.window != None:
            if self.clicked:
                pygame.draw.rect(self.window, self.background_clicked, self.rect)
            else:
                pygame.draw.rect(self.window, self.background, self.rect)
            self.image = self.font.render(self.text, True, self.color)
            text_width, text_height = self.font.size(self.text)
            self.window.blit(self.image, (self.rect.x + ((self.rect.width-text_width)/2), self.rect.y + ((self.rect.height-text_height)/2)))

    def update(self, event):
        if event != None and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.clicked = True
                self.makePaintUpdate = True
            else:
                if self.clicked:
                    self.clicked = False
                    self.makePaintUpdate = True
                    return True
            return False
        elif event != None and event.type == pygame.MOUSEBUTTONUP:
            if self.clicked:
                self.clicked = False
                self.makePaintUpdate = True
                if self._callBack != None:
                    self._callBack()
            return False
        return True

class SpriteObject(Widget):
    leftKey = pygame.K_LEFT
    rightKey = pygame.K_RIGHT
    upKey = pygame.K_UP
    downKey = pygame.K_DOWN
    sourceTicks = pygame.time.get_ticks()
    updateTimer = True

    def __init__(self):
        Widget.__init__(self)

    def handleLeft(self):
        if ((pygame.time.get_ticks() - self.sourceTicks)/1000)>0.05:
            self.rect.x = self.rect.x -2
            self.updateTimer = True

    def handleRight(self):
        if ((pygame.time.get_ticks() - self.sourceTicks)/1000)>0.05:
            self.rect.x = self.rect.x +2
            self.updateTimer = True

    def handleUp(self):
        ""

    def handleDown(self):
        ""

    def update(self, event):
        if event == None or event.type == pygame.KEYDOWN:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[self.leftKey]:
                self.handleLeft()
            if pressed_keys[self.rightKey]:
                self.handleRight()
            if pressed_keys[self.upKey]:
                self.handleUp()
            if pressed_keys[self.downKey]:
                self.handleDown()
            if self.updateTimer:
                self.sourceTicks = pygame.time.get_ticks()
                self.updateTimer = False
            self.makePaintUpdate = True
            return (event != None)
        return False

class Scene(Widget):
    scaled = None

    def __init__(self):
        Widget.__init__(self)

    def setImage(self, path):
        self.image = pygame.image.load(path)
        if self.window != None:
            self.scaled = pygame.transform.scale(self.image, (self.window.get_width(), self.window.get_height()))

    def customPaint(self):
        if self.scaled != None:
            if self.window != None:
                self.window.blit(self.scaled, self.rect)

    def update(self, event):
        if self.window != None:
            if self.window.get_height != self.rect.height or self.window.get_width != self.rect.width:
                self.rect.width = self.window.get_width()
                self.rect.height = self.window.get_height()
                if self.image != None:
                    self.scaled = pygame.transform.scale(self.image, (self.window.get_width(), self.window.get_height()))
                return True
        return True


class Runtime:
    objectList = []
    target_win = None
    running = False
    forceRePaint = False
    _firstLoad = True
    _routines = []
    _leaveCallBack = None
    _paintCallBack = None

    def countObjects(self):
        return len(self.objectList)

    def appendObject(self, obj):
        obj.setWindow(self.target_win)
        self.objectList.append(obj)

    def setWindow(self, win):
        self.target_win = win
        for obj in self.objectList:
            obj.setWindow(win)
            obj.update()

    def setPaintCallBack(self, func):
        self._paintCallBack = func

    def paintWindow(self):
        if self._paintCallBack == None:
            pygame.draw.rect(self.target_win, (200, 200, 200),(0, 0, self.target_win.get_rect().width/2, self.target_win.get_rect().height))
            pygame.draw.rect(self.target_win, (255, 255, 255),(self.target_win.get_rect().width/2, 0, self.target_win.get_rect().width/2, self.target_win.get_rect().height))
        else:
            self._paintCallBack(self.target_win)

    def addRoutine(self, func):
        self._routines.append(func)

    def quit(self):
        self.running = False;

    def setEndCallBack(self, func):
        self._leaveCallBack = func

    def execute(self):
        # Main Loop
        self.running = True
        while self.running:
            for routine in self._routines:
                routine()

            eventList = pygame.event.get()
            shouldRePaint = False
            if not eventList or self._firstLoad:
                run = True
                i = 0
                while run and i<len(self.objectList):
                    if self.objectList[i] != None:
                        run = self.objectList[i].update(None)
                        if self.objectList[i].makePaintUpdate == True:
                            shouldUpdate = True
                    else:
                        run = False
                    i+=1
            else:
                #Share the events
                for event in eventList:
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit(1)
                    else:
                        run = True
                        i = 0
                        #If an object accepts it, it means others must not get it: stop the loop
                        while run and i<len(self.objectList):
                            if self.objectList[i] != None:
                                run = self.objectList[i].update(event)
                                if self.objectList[i].makePaintUpdate == True:
                                    shouldUpdate = True
                            else:
                                run = False
                            i+=1
            #Make new paintings if needed
            if (shouldRePaint == True) or (self.forceRePaint == True) or (self._firstLoad == True) :
                if self._firstLoad:
                    self._firstLoad = False
                self.paintWindow()
                continuePainting = True
                j = 0
                while continuePainting and j<len(self.objectList):
                    if self.objectList[j] != None:
                        self.objectList[j].customPaint()
                        self.objectList[j].makePaintUpdate = False
                    else:
                        continuePainting = False
                    j+=1

            pygame.display.update()
        if self._leaveCallBack != None:
            self._leaveCallBack()

"""
        TEMPLATE:
pygame.display.set_caption('Crash!')
window = pygame.display.set_mode((600, 600))
scene = Scene()
rtm = Runtime()
rtm.setWindow(window)
#rtm.appendObject(SpriteObject())
rtm.appendObject(scene)
scene.setImage("./backgrounds//bamboo.png")
rtm.execute()
"""