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

	def __init__(self, bg = (255, 255, 255), progress_bg = (200, 200, 200), p_fg_a = (100, 100, 255), p_fg_b = (150, 150, 255), text_color = (0, 0, 0)):
		runtime.Widget.__init__(self)
		self.color = bg
		self.rect = pg.Rect((0, 0), (1200, 70))

		#Decorative text as long as we don't use custom names (yet)
		self._p1l.text = "J1"
		self._p2l.text = "J2"

		self._p1l.font = pg.font.SysFont(None, 54)
		self._p2l.font = self._p1l.font
		self._p1l.rect.x = 10

		self._p1l.color = text_color
		self._p2l.color = text_color

		#Make the progress bars for LPs
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

		self._p2p.foreground = p_fg_a
		self._p1p.foreground = p_fg_a
		self._p2p.background = progress_bg
		self._p1p.background = progress_bg

		self._second_foreground = p_fg_b

	def setP1Name(self, text):
		self._p1l.text = text
		self.makePaintUpdate = True

	def setP2Name(self, text):
		self._p2l.text = text
		self.makePaintUpdate = True

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
		if val <= 50:
			self._p1p.foreground = self._second_foreground
		self.makePaintUpdate = True

	def setLP2(self, val):
		"""Set the Life Points of the 2nd player and updates it's LP bar."""
		self._p2p.pos = val
		if val <= 50:
			self._p2p.foreground = self._second_foreground
		self.makePaintUpdate = True

	def setMLP1(self, val):
		"""Set the Maximum Life Points of the 1st player."""
		self._p1p.maximum = val
		if val >= 50:
			self._p1p.foreground = self._second_foreground
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
	"""Default map, used as base for any loaded map."""
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
	_fp = None
	_onExit = None
	_deathWas1 = None
	_hasDeath = False
	closed = True
	scaled = None
	_timerHint1 = pg.time.get_ticks()
	_timerHint2 = pg.time.get_ticks()

	def __init__(self, image_fp = "./maps/tlalok.image", win_size = (1200, 800), max_y = 790, min_y = 80, pop_border_padding = 10, bg = (255, 255, 255), progress_bg = (200, 200, 200), p_fg_a = (100, 100, 255), p_fg_b = (150, 150, 255), text_color = (0, 0, 0)):
		self._rtm.addRoutine(self.postCheck)
		self._fp = image_fp
		self._topBar = TopBar(bg, progress_bg, p_fg_a, p_fg_b, text_color)
		self.window_size = win_size
		self.max_y = max_y
		self.min_y = min_y
		self.pop_border_padding = pop_border_padding

	def setExitCB(self, func):
		self._onExit = func

	def handleDeath(self, player):
		self._deathWas1 = player
		self._rtm.clear()
		self.deathLoadElements()

	def deathLoadElements(self):
		label = runtime.Label()
		if self._deathWas1 == True:
			label.text = "Le joueur 1 a gagn??!"
		else:
			label.text = "Le joueur 2 a gagn??!"
		label.rect.x = 200
		label.rect.y = 100
		self._rtm.appendObject(label)
		button = runtime.Button()
		button.text = "Retour"
		button.rect.x = 200
		button.rect.y = 200
		button.setCallBack(self._onExit)
		self._rtm.appendObject(button)
		self._hasDeath = True

	def winPaint(self, win):
		"""The painting of the window"""
		if self._win != None and self._hasDeath == False:
			if self.scaled != None:
				self._win.blit(self.scaled, pg.Rect((0, 0), (self._win.get_width(), self._win.get_height())))
			#If no win was here went setting the fp, there's no scaled image, so we build it here.
			elif self._fp != None:
				self.scaled = pg.transform.scale(pg.image.load(self._fp), (self._win.get_width(), self._win.get_height()))
				self._win.blit(self.scaled, pg.Rect((0, 0), (self._win.get_width(), self._win.get_height())))
		elif self._win != None:
			pg.draw.rect(self._win, (255, 255, 255), self._win.get_rect())

	def setImage(self, fp):
		"""Set the map's image by it's path (fp)"""
		self._fp = fp
		if self._win != None:
			self.scaled = pg.transform.scale(pg.image.load(fp), (self._win.get_width(), self._win.get_height()))
		else:
			self.scaled = None

	def checkMovingAttacks(self):
		"""Check collisions of the moving attacks (e.g.: an arrow) of both players"""
		if self._hasDeath == True:
			return
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
		if self._hasDeath == True:
			return
		if (self._inAttack1 != None) and (self._j2.rect.colliderect(self._inAttack1.rect)) and ((pg.time.get_ticks() - self._timerHint2) > 100):
			print("Rect:", self._inAttack1.rect, ", Collision:", (self._j2.rect.colliderect(self._inAttack1.rect)))
			self._timerHint2 = pg.time.get_ticks()
			self._j2.touched(self._inAttack1)
			self._inAttack1 = None
		if (self._inAttack2 != None) and (self._j1.rect.colliderect(self._inAttack2.rect)) and ((pg.time.get_ticks() - self._timerHint1) > 100):
			self._timerHint1 = pg.time.get_ticks()
			self._j1.touched(self._inAttack2)
			self._inAttack2 = None

	def checkPlayersPos(self):
		"""Don't send the players out of the window! It checks and moves the players when needed to keep them in"""
		if self._hasDeath == True:
			return
		if (self._j1 != None):
			if (self._j1.rect.x+self._j1.rect.width)>(self._win.get_width()-self.pop_border_padding):
				self._j1.rect.x = self._win.get_width()-self.pop_border_padding-self._j1.rect.width
			elif self._j1.rect.x<self.pop_border_padding:
				self._j1.rect.x = self.pop_border_padding
		if (self._j2 != None):
			if (self._j2.rect.x+self._j2.rect.width)>(self._win.get_width()-self.pop_border_padding):
				self._j2.rect.x = self._win.get_width()-self.pop_border_padding-self._j2.rect.width
			elif self._j2.rect.x<self.pop_border_padding:
				self._j2.rect.x = self.pop_border_padding

	def checkOORAttacks(self):
		"""Check for Out Of Range attacks, when it goes out of th window, and remove it"""
		if self._hasDeath == True:
			return
        #Keep track of the objects to remove. We must remove them from the attacks lists. We store their indexes here
		toRm2 = []
		toRm1 = []
		i1 = 0
		i2 = 0
		for a in self._pendingAttacks1:
			if ((a.rect.x+a.rect.width)<=self.pop_border_padding) or (a.rect.x>(self._win.get_width()-self.pop_border_padding)):
				val = self._rtm.countObjects()
				a.remove()
				self._rtm.removeObject(a.RuntimeOUID)
				toRm1.append(i1)
			i1+=1
		for a in self._pendingAttacks2:
			if ((a.rect.x+a.rect.width)<self.pop_border_padding) or (a.rect.x>(self._win.get_width()-self.pop_border_padding)):
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
		self._pendingAttacks2.append(self._rtm.prependObject(attack))

	def handleMA2(self, attack):
		"""Callback to add a moving attack from P2"""
		self._pendingAttacks1.append(self._rtm.prependObject(attack))

	def handleSA1(self, r):
		"""Callback to add a satic attack from P1"""
		self._inAttack2 = r

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
		self._j1.setDeathCB(self.handleDeath)
		#Update UI's values
		self._topBar.setMLP1(self._j1.max_lp)
		self._topBar.setLP1(self._j1.max_lp)
		#Set player's values
		self._j1.isP1 = True
		self._j1.min_y = self.min_y
		self._j1.max_y = self.max_y
		self._j1.rect.x = self.pop_border_padding
		self._j1.rect.y = self.window_size[1] - self._j1.rect.y - self._j1.rect.height
		self.setupJ1Keys()
		self._j1 = self._rtm.appendObject(self._j1)
		self._topBar.setP1Name(self._j1.playerName)

	def setJ2(self, j):
		"""Sets the second player"""
		self._j2 = j
		self._j2.MACallBack = self.handleMA2
		self._j2.SACallBack = self.handleSA2
		self._j2.LPCallBack = self._topBar.setLP2
		self._j2.setDeathCB(self.handleDeath)
		self._topBar.setMLP2(self._j2.max_lp)
		self._topBar.setLP2(self._j2.max_lp)
		self._j2.isP1 = False
		self._j2.min_y = self.min_y
		self._j2.max_y = self.max_y
		self._j2.rect.x = self.window_size[0] - self.pop_border_padding - self._j2.rect.width
		self._j2.rect.y = self.window_size[1] - self._j2.rect.y - self._j2.rect.height
		self.setupJ2Keys()
		self._j2 = self._rtm.appendObject(self._j2)
		self._topBar.setP2Name(self._j2.playerName)

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

	def popup(self, shouldLoad = True):
		"""Setup the win and Runtime env."""
		if self._rtm.running == False:
			#Set the window
			self._win = pg.display.set_mode(self.window_size)
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

	def clear(self):
		self._rtm.clear()

	def loadElements(self):
		self._topBar = self._rtm.appendObject(self._topBar)