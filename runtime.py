#!/usr/bin/python3

import pygame, sys
import defaultAttack
pygame.init()

class Widget():
    def __init__(self):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)
       self.window = None
       self.color = (0, 0, 0)
       self.rect = pygame.Rect((0, 0), (200, 200))
       self.makePaintUpdate = False
       self.RuntimeOUID = -1

    def setWindow(self, target):
        self.window = target

    def setOUID(self, t):
        self.RuntimeOUID = t

    def customPaint(self):
        if self.window != None:
            pygame.draw.rect(self.window, self.color, self.rect)

    def update(self, event):
        return True

class Picture(Widget):
    def __init__(self):
        Widget.__init__(self)

    def customPaint(self):
        size = self.image.get_size()
        pygame.draw.rect(pygame.Surface(size, pygame.SRCALPHA), (255, 255, 255), (0, 0, size), border_radius=roundness)

class ProgressBar(Widget):
    def __init__(self):
        Widget.__init__(self)
        self.rect = pygame.Rect((0, 0), (200, 200))
        self.maximum = 10
        self.pos = 3
        self.foreground = (255, 0, 0)
        self.background = (0, 0, 0)
        self.minimum = 0

    def update(self, event):
        return True

    def customPaint(self):
        if self.window != None:
            pygame.draw.rect(self.window, self.background, self.rect)
            if (self.pos >= self.minimum):
                pygame.draw.rect(self.window, self.foreground, pygame.Rect((self.rect.x, self.rect.y), ((self.pos*self.rect.width/self.maximum), self.rect.height)))

class Label(Widget):
    text = "Bonjour"
    font = pygame.font.SysFont(None, 104)

    def __init__(self):
        Widget.__init__(self)
        self.rect = pygame.Rect((0, 0), (200, 50))
        self.color = (0, 0, 0)

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
                return False
            else:
                if self.clicked:
                    self.clicked = False
                    self.makePaintUpdate = True
                return True
        elif event != None and event.type == pygame.MOUSEBUTTONUP:
            if self.clicked:
                self.clicked = False
                self.makePaintUpdate = True
                if self._callBack != None:
                    self._callBack()
                return False
            return True
        return True

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

    def __init__(self):
        self._firstLoad = True
        self._routines = []
        self._mroutines = []
        self._oneShotRoutines = []
        self._leaveCallBack = None
        self._paintCallBack = None
        self._ouid = 0
        self._fromInternalNeedsRepaint = False
        self.target_win = None
        self.running = False
        self.forceRePaint = False
        self.afterPropagationUpdate = False

    def __exit(self):
        if self.target_win != None:
            pygame.display.quit()
            del self.target_win

        # Ensure pg.init() was done. Else it might give strange purposes in some cases, when you play between multiple windows
        pygame.init()

        if self._leaveCallBack != None:
            self._leaveCallBack()

    def countObjects(self):
        return len(self.objectList)

    def appendObject(self, obj):
        obj.setWindow(self.target_win)
        obj.setOUID(self._ouid)
        self._ouid += 1
        self.objectList.append(obj)
        return obj

    def prependObject(self, obj):
        obj.setWindow(self.target_win)
        obj.setOUID(self._ouid)
        self._ouid += 1
        self.objectList.insert(0, obj)
        return obj

    def removeObject(self, ouid):
        if ouid != -1:
            i = 0
            nf = True
            while (nf == True) and (i<len(self.objectList)):
                if (self.objectList[i].RuntimeOUID == ouid):
                    self.objectList.pop(i)
                    nf = False
                i+=1
        if not nf:
            #We have to ensure that the object disappear from the surface, so repaint all
            self._fromInternalNeedsRepaint = True

    def setWindow(self, win):
        self.target_win = win
        for obj in self.objectList:
            obj.setWindow(win)
            obj.update(None)

    def setPaintCallBack(self, func):
        self._paintCallBack = func

    def paintWindow(self):
        if self._paintCallBack == None:
            pygame.draw.rect(self.target_win, (200, 200, 200), (0, 0, self.target_win.get_rect().width/2, self.target_win.get_rect().height))
            pygame.draw.rect(self.target_win, (255, 255, 255), (self.target_win.get_rect().width/2, 0, self.target_win.get_rect().width/2, self.target_win.get_rect().height))
        else:
            self._paintCallBack(self.target_win)

    def addRoutine(self, func):
        self._routines.append(func)

    def addMidRoutine(self, func):
        self._mroutines.append(func)

    def addOSR(self, func):
        self._oneShotRoutines.append(func)

    def quit(self):
        self.running = False;

    def setEndCallBack(self, func):
        self._leaveCallBack = func

    def clear(self):
        self._ouid = 0
        self.objectList.clear()
        self._firstLoad = True

    def execute(self):
        # Main Loop
        self.running = True

        while self.running:
            for routine in self._routines:
                routine()

            for osr in self._oneShotRoutines:
                osr()
            if (not self._oneShotRoutines) == False:
                self._oneShotRoutines.clear()

            if self.running == False:
                break

            eventList = pygame.event.get()
            shouldRePaint = False
            if not eventList or self._firstLoad:
                run = True
                i = 0
                while run and i<len(self.objectList):
                    if self.objectList[i] != None:
                        run = self.objectList[i].update(None)
                        if self.objectList[i].makePaintUpdate == True:
                            shouldRePaint = True
                    else:
                        run = False
                    if self.running == False:
                        break
                    i+=1
                if self.running == False:
                    break
            else:
                #Share the events
                for event in eventList:
                    if event.type == pygame.QUIT:
                        if self._leaveCallBack == None:
                            pygame.quit()
                            quit(1)
                        else:
                            self._leaveCallBack()
                            break
                    else:
                        run = True
                        propagate = False
                        i = 0
                        #If an object accepts it, it means others must not get it: stop the loop, or if propagation is enabled, update other with empty things.
                        while run and i<len(self.objectList):
                            if self.objectList[i] != None:
                                if propagate and self.afterPropagationUpdate:
                                    propagate = self.objectList[i].update(None)
                                    if self.objectList[i].makePaintUpdate == True:
                                         shouldRePaint = True
                                else:
                                    run = self.objectList[i].update(event)
                                    if (self.afterPropagationUpdate == True) and (run == False):
                                         propagate = self.objectList[i].update(None)
                                         if self.objectList[i].makePaintUpdate == True:
                                              shouldRePaint = True
                                         propagate = True
                                         run = True
                                    if self.objectList[i].makePaintUpdate == True:
                                         shouldRePaint = True
                            else:
                                run = False
                            if self.running == False:
                                break
                            i+=1
            #Mid routines, for example, if you want to remove something that have been updated before it gets painted
            for mrtn in self._mroutines:
                mrtn()

            if self.running == False:
                break

            #Make new paintings if needed
            if (shouldRePaint == True) or (self.forceRePaint == True) or (self._firstLoad == True) or (self._fromInternalNeedsRepaint == True):
                if self._firstLoad:
                    self._firstLoad = False

                if self.running == False:
                    break
                self.paintWindow()
                continuePainting = True

                if self.running == False:
                    break

                j = 0
                while continuePainting and j<len(self.objectList):
                    if self.objectList[j] != None:
                        self.objectList[j].customPaint()
                        self.objectList[j].makePaintUpdate = False
                    else:
                        continuePainting = False

                    if self.running == False:
                        break
                    j+=1

                if self.running == False:
                    break;

            pygame.display.update()
        self.__exit()

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