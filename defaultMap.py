#!/usr/bin/python3
import runtime
import keys
import pygame as pg

class TopBar(runtime.Widget):
	"""A top bar with player's name and LP, that's a widget."""
	_p1l = runtime.Label()
	_p2l = runtime.Label()
	_p2p = None
	_p1p = None

	def __init__(self):
		runtime.Widget.__init__(self)
		self.color = (255, 255, 255)
		self.rect = pg.Rect((0, 0), (1200, 70))

		self._p1l.text = "J1"
		self._p2l.text = "J2"

		self._p1l.font = pg.font.SysFont(None, 54)
		self._p2l.font = self._p1l.font
		self._p1l.rect.x = 10

		self._p1p = runtime.ProgressBar()
		self._p1p.maximum = 100
		self._p1p.pos = 100
		self._p1p.rect.width = 150
		self._p1p.rect.height = 20
		self._p1p.rect.y = 40
		self._p1p.rect.x = 10

		self._p2p = runtime.ProgressBar()
		self._p2p.maximum = 100
		self._p2p.pos = 100
		self._p2p.rect.width = 150
		self._p2p.rect.height = 20
		self._p2p.rect.y = 40
		self._p2p.rect.x = 1040
		self._p2l.rect.x = self.rect.width - self._p2l.rect.width - 10
		self._p2p.rect.x = self.rect.width - self._p2p.rect.width - 10

		self._p2p.foreground = (100, 100, 255)
		self._p2p.background = (200, 200, 200)
		self._p1p.foreground = (100, 100, 255)
		self._p1p.background = (200, 200, 200)

	def customPaint(self):
		"""Paints the widget"""
		if self.window != None:
			#Generate the painting by each level. The first is the widget itself as it contains the others.
			super().customPaint()
			self._p1l.customPaint()
			self._p2l.customPaint()
			self._p1p.customPaint()
			self._p2p.customPaint()

	def setLP1(self, val):
		"""Set Life Points of the 1st player and updates it's LP bar."""
		self._p1p.pos = val
		self.makePaintUpdate = True

	def setLP2(self, val):
		"""Set the Life Points of the 2nd player and updates it's LP bar."""
		self._p2p.pos = val
		self.makePaintUpdate = True

	def setMLP1(self, val):
		"""Set the Maximum Life Points of the 1st player."""
		self._p1p.maximum = val
		self.makePaintUpdate = True

	def setMLP2(self, val):
		"""Set the Maximum Life Points of the 1st player."""
		self._p2p.maximum = val
		self.makePaintUpdate = True

	def setWindow(self, win):
		self.window = win
		#Set for the content too, they need it to be drawn.
		self._p1l.setWindow(win)
		self._p2l.setWindow(win)
		self._p1p.setWindow(win)
		self._p2p.setWindow(win)

	def paintCheck(self):
		"""Generates the makePaintUpdate state of the widget by know the makePaintUpdate of children and itself."""
		return (self.makePaintUpdate or self._p1l.makePaintUpdate or self._p1p.makePaintUpdate or self._p2l.makePaintUpdate or self._p2p.makePaintUpdate)

	def update(self, event):
		if (self._p1l.update(event)):
			if (self._p1p.update(event)):
				if (self._p2l.update(event)):
					if (self._p2p.update(event)):
						self.makePaintUpdate = self.paintCheck()
						return super().update(event)
		self.makePaintUpdate = self.paintCheck()
		return False

class Map:
	_showing = False
	_rtm = runtime.Runtime()
	_win = None
	_topBar = None
	_oldW = 0
	_j1 = None
	_j2 = None
	_pendingAttacks1 = []
	_pendingAttacks2 = []
	_inAttack1 = None
	_inAttack2 = None
	_fp = "./maps/tlalok.image"
	closed = True
	scaled = None

	def __init__(self):
		self._rtm.addRoutine(self.postCheck)
		self._topBar = TopBar()

	def winPaint(self, win):
		"""The painting of the window"""
		if self._win != None:
			if self.scaled != None:
				self._win.blit(self.scaled, pg.Rect((0, 0), (self._win.get_width(), self._win.get_height())))
			#If no win was here went setting the fp, there's no scaled image, so we build it here.
			elif self._fp != None:
				self.scaled = pg.transform.scale(pg.image.load(self._fp), (self._win.get_width(), self._win.get_height()))
				self._win.blit(self.scaled, pg.Rect((0, 0), (self._win.get_width(), self._win.get_height())))

	def setImage(self, fp):
		"""Set the map's image by it's path (fp)"""
		self._fp = fp
		if self._win != None:
			self.scaled = pg.transform.scale(pg.image.load(fp), (self._win.get_width(), self._win.get_height()))
		else:
			self.scaled = None

	def checkMovingAttacks(self):
		"""Check collisions of the moving attacks (e.g.: an arrow) of both players"""
        #Keep track of the objects to remove. We must remove them from the attacks lists. We store their indexes here
		toRm2 = []
		toRm1 = []
		i1 = 0
		i2 = 0
        #Check each list
		if (self._j2 != None):
			for a in self._pendingAttacks1:
				#If you give a static attack into a moving one, the moving one gets destroyed.
				if (self._inAttack2 != None) and (self._inAttack2.rect.colliderect(a.rect)):
					self._inAttack2 = None
					a.destruction()
				#Else, maybe it just touched the player
				elif self._j1.rect.colliderect(a.rect):
					self._j1.touched(a)
					a.destruction()
				if a.destructionFinished == True:
					a.remove()
					self._rtm.removeObject(a.RuntimeOUID)
					toRm1.append(i1)
				i1+=1
		#Check for the other player
		if (self._j1 != None):
			for a in self._pendingAttacks2:
				if (self._inAttack1 != None) and (self._inAttack1.rect.colliderect(a.rect)):
					self._inAttack1 = None
					a.destruction()
				elif self._j2.rect.colliderect(a.rect):
					self._j2.touched(a)
					a.destruction()
				if a.destructionFinished == True:
					a.remove()
					self._rtm.removeObject(a.RuntimeOUID)
					toRm2.append(i2)
				i2+=1

		#Then remove the ones that we no more need.
		i = 0
		j = 0
		while i<len(toRm1):
			self._pendingAttacks1.pop(toRm1[i+j])
			j-=1
			i+=1
		i = 0
		j = 0
		while i<len(toRm2):
			self._pendingAttacks2.pop(toRm2[i+j])
			j-=1
			i+=1

	def checkStaticAttacks(self):
		"""Check collisions of "Static" attack, such as a kick, for both players"""
		if (self._inAttack1 != None) and (self._j2.rect.colliderect(self._inAttack1.rect)):
			self._j2.touched(self._inAttack1)
			self._j1.removeSA()
			print("shot!")
		if (self._inAttack2 != None) and (self._j1.rect.colliderect(self._inAttack2.rect)):
			self._j1.touched(self._inAttack2)
			self._j2removeSA()
			print("shot!")

	def checkPlayersPos(self):
		"""Don't send the players out of the window! It checks and moves the players when needed to keep them in"""
		if (self._j1 != None):
			if (self._j1.rect.x+self._j1.rect.width)>(self._win.get_width()-10):
				self._j1.rect.x = self._win.get_width()-10-self._j1.rect.width
			elif self._j1.rect.x<10:
				self._j1.rect.x = 10
		if (self._j2 != None):
			if (self._j2.rect.x+self._j2.rect.width)>(self._win.get_width()-10):
				self._j2.rect.x = self._win.get_width()-10-self._j2.rect.width
			elif self._j2.rect.x<10:
				self._j2.rect.x = 10

	def checkOORAttacks(self):
		"""Check for Out Of Range attacks, when it goes out of th window, and remove it"""
        #Keep track of the objects to remove. We must remove them from the attacks lists. We store their indexes here
		toRm2 = []
		toRm1 = []
		i1 = 0
		i2 = 0
		for a in self._pendingAttacks1:
			if ((a.rect.x+a.rect.width)<=10) or (a.rect.x>(self._win.get_width()-10)):
				val = self._rtm.countObjects()
				a.remove()
				self._rtm.removeObject(a.RuntimeOUID)
				toRm1.append(i1)
			i1+=1
		for a in self._pendingAttacks2:
			if ((a.rect.x+a.rect.width)<10) or (a.rect.x>(self._win.get_width()-10)):
				val = self._rtm.countObjects()
				a.remove()
				self._rtm.removeObject(a.RuntimeOUID)
				toRm2.append(i2)
			i2+=1

		#Then remove the ones that we no more need.
		i = 0
		j = 0
		while i<len(toRm1):
			self._pendingAttacks1.pop(toRm1[i+j])
			j-=1
			i+=1
		i = 0
		j = 0
		while i<len(toRm2):
			self._pendingAttacks2.pop(toRm2[i+j])
			j-=1
			i+=1

	def postCheck(self):
		"""To notify the other objects that have access to this instance that it closed the win."""
		if self.closed == True and self._rtm.running == True:
			self.closed = True
			self._rtm.quit()

	def handleMA1(self, attack):
		"""Callback to add a moving attack from P1"""
		self._pendingAttacks2.append(self._rtm.appendObject(attack))

	def handleMA2(self, attack):
		"""Callback to add a moving attack from P2"""
		self._pendingAttacks1.append(self._rtm.appendObject(attack))

	def handleSA1(self, r):
		"""Callback to add a satic attack from P1"""
		self._inAttack2 = r
		print("Attacking P2!")

	def handleSA2(self, r):
		"""Callback to add a satic attack from P2"""
		self._inAttack1 = r

	def setJ1(self, j):
		"""Sets the first player"""
		self._j1 = j
		#Set the callbacks
		self._j1.MACallBack = self.handleMA1
		self._j1.SACallBack = self.handleSA1
		self._j1.LPCallBack = self._topBar.setLP1
		#Update UI's values
		self._topBar.setMLP1(self._j1.max_lp)
		self._topBar.setLP1(self._j1.max_lp)
		#Set player's values
		self._j1.isP1 = True
		self._j1.min_y = 80
		self._j1.max_y = 790
		self._j1.rect.x = 10
		self._j1.rect.y = 800 - self._j1.rect.y - self._j1.rect.height
		self.setupJ1Keys()
		self._j1 = self._rtm.appendObject(self._j1)

	def setJ2(self, j):
		"""Sets the second player"""
		self._j2 = j
		self._j2.MACallBack = self.handleMA2
		self._j2.SACallBack = self.handleSA2
		self._j2.LPCallBack = self._topBar.setLP2
		self._topBar.setMLP2(self._j2.max_lp)
		self._topBar.setLP2(self._j2.max_lp)
		self._j2.isP1 = False
		self._j2.min_y = 80
		self._j2.max_y = 790
		self._j2.rect.x = 1200 - 10 - self._j2.rect.width
		self._j2.rect.y = 800 - self._j2.rect.y - self._j2.rect.height
		self.setupJ2Keys()
		self._j2 = self._rtm.appendObject(self._j2)

	def setupJ1Keys(self):
		"""Get keys that have been set in configuration for the first player."""
		self._j1.leftKey =  keys.switcher["p1_left"]
		self._j1.rightKey = keys.switcher["p1_right"]
		self._j1.downKey =  keys.switcher["p1_down"]
		self._j1.upKey =    keys.switcher["p1_up"]
		self._j1.saKey =    keys.switcher["p1_at1"]
		self._j1.maKey =    keys.switcher["p1_at2"]

	def setupJ2Keys(self):
		"""Get keys that have been set in configuration for the second player."""
		self._j2.leftKey =  keys.switcher["p2_left"]
		self._j2.rightKey = keys.switcher["p2_right"]
		self._j2.downKey =  keys.switcher["p2_down"]
		self._j2.upKey =    keys.switcher["p2_up"]
		self._j2.saKey =    keys.switcher["p2_at1"]
		self._j2.maKey =    keys.switcher["p2_at2"]

	def deadCallBack(self, isP1):
		"""Makes a player dead and draw who won on the win"""
		pass

	def popup(self):
		"""Setup the win and Runtime env."""
		if self._rtm.running == False:
			#Set the window
			self._win = pg.display.set_mode((1200, 800))
			self._rtm.setWindow(self._win)
			#Add our routines
			self._rtm.addRoutine(self.postCheck)
			self._rtm.addRoutine(self.checkStaticAttacks)
			self._rtm.addRoutine(self.checkMovingAttacks)
			self._rtm.addRoutine(self.checkPlayersPos)
			self._rtm.addMidRoutine(self.checkOORAttacks)
			self._rtm.setPaintCallBack(self.winPaint)
			#Set the needed values
			self._rtm.afterPropagationUpdate = True
			self.closed = False
			self.loadElements()
			self._rtm.execute()

	def loadElements(self):
		self._topBar = self._rtm.appendObject(self._topBar)

import defaultPlayer

m = Map()
m.setJ1(defaultPlayer.Player())
m.setJ2(defaultPlayer.Player())
m.popup()