import pygame
pygame.init()

class SpriteObject(pygame.sprite.Sprite):
    rect = pygame.Rect((0, 0), (200, 200))
    image = None

    def __init__(self):
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self)

       #On défini la surface et on génère une image
       self.image = pygame.Surface([self.rect.width, self.rect.height])
       #On rempli l'image
       self.image.fill((0, 0, 0))
       #On peut redéfinir la taille en fonction de l'image
       #self.rect = self.image.get_rect()

    def setWindow(self, target):
        self.window = target

    def customPaint(self):
        #On peut utiliser autres chose que ce qui est en dessous
        self.window.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, event):
        #On fait des choses en fontcon du type d'événements
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                print("collided")
        if (event.type == pygame.KEYDOWN):
            self.rect.x = self.rect.x +2
        self.customPaint()
        #Pour savoir si les autres éléments qui sont en dessous doivent aussi recevoir l'événement
        return False

class Runtime:
    objectList = []
    target_win = None
    keepRunning = True

    def appendObject(self, obj):
        obj.setWindow(self.target_win)
        self.objectList.append(obj)

    def setWindow(self, win):
        self.target_win = win
        for obj in self.objectList:
            obj.setWindow(win)
            obj.update()

    def paintWindow(self):
        #Mettre à jour la fenêtre
        pygame.draw.rect(window, (200, 200, 200),(0, 0, 300, 600))
        pygame.draw.rect(window, (255, 255, 255),(300, 0, 300, 600))

    def quit(self):
        self.keepRunning = False;

    def exec(self):
        # Main Loop
        while self.keepRunning:
            #Events handler. On filtre les événements, puis on les envoi vers les objets concernés
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(1)
                else:
                    self.paintWindow()
                    #Envoyer les événements aux objets
                    run = True
                    i = 0
                    while run:
                        if self.objectList[i] != None:
                            run = self.objectList[i].update(event)
                        else:
                            run = False
                        i+=1
            pygame.display.update()

pygame.display.set_caption('Crash!')
window = pygame.display.set_mode((600, 600))

rtm = Runtime()
rtm.setWindow(window)
rtm.appendObject(SpriteObject())
rtm.exec()
