#!/usr/bin/python3
import runtime
import pygame as pg
import os
import defaultAttack

class Motion:
	_frames = None
	_pos = -1
	_pi = 1
	_timer = pg.time.get_ticks()
	_enableRoll = True
	_enableInvert = False
	_enablePos = False
	_src = None
	_speed = None
	_sourceY = 5
	_firstFrame = True

	def __init__(self, motionDir, source = None, xi = [], yi = 0, speed = 0.05, invert = False):
		fList = os.listdir(motionDir)
		frames = []
		i = 0
		#Get .image files (in alphabetical order) to set them as frames
		while i<len(fList):
			filePath = os.path.splitext(fList[i])
			#if filePath[1] == ".image":
			if (source != None):
				frames.append(pg.transform.scale(pg.image.load(motionDir + "/" + fList[i]), (source.rect.width, source.rect.height)))
			else:
				frames.append(pg.image.load(motionDir + "/" + fList[i]))
			i+=1
		i = 0
		framed = []
		#Get .image files (in alphabetical order) to set them as frames
		while (i<len(fList) and invert):
			framed.append(pg.transform.flip(frames[i], True, False))
			i+=1
		if (invert):
			frames = framed
		self._frames = frames
		self._speed = speed
		self._src = source
		if (source != None):
			self._xi = xi
			self._yi = yi
			if yi != 0:
				self._enablePos = True

	def setRollEnabled(self, ena):
		"""Disbale, or enable the "Roll". When the motion rich the limit of frames for the animation, if roll is set, it will go back to the first frame."""
		self._enableRoll = ena

	def setInvertEnabled(self, ena):
		"""Disable, or enable invertion of frames at end of motion, to make the changes in the opposite way. Incompatible with Roll."""
		self._enableInvert = ena

	def reset(self):
		"""Rolls back the motion to the beginning, by restarting at the first frame. Notice that it is applied on render func, this will not automatically make the update on the surface."""
		self._pos = 0
		self._firstFrame = True
		self._src.rect.y = self._sourceY + (self._pos * self._yi) + 25

	def updatePos(self):
		"""Used to update the frame to be used during the rendering"""
		if ((pg.time.get_ticks() - self._timer)/1000) > self._speed:
			if (self._firstFrame == True) and (self._src != None) and (self._enablePos):
				self._sourceY = self._src.rect.y
			if self._enableInvert:
				self._pos += 1*self._pi
				if (self._pos == len(self._frames)):
					self._pos -= 1
					self._pi = -self._pi
				elif self._pos == -1:
					self._pos += 1
					self._pi = -self._pi
				self._timer = pg.time.get_ticks()
			else:
				self._pos += 1
				if (self._src != None):
					self._src.rect.y = self._src.rect.y - self._yi
				if (self._pos == len(self._frames)):
					self._firstFrame = False
					if self._enableRoll:
						self._pos = 0
					else:
						self._pos -= 1
				self._timer = pg.time.get_ticks()

	def render(self, target, rect):
		"""Render to a pygame.Surface the current frame to make the 'motion'"""
		self.updatePos()
		if (target != None) and ((not self._frames) == False):
			if self._enablePos:
				target.blit(self._frames[self._pos], pg.Rect((rect.x, self._sourceY - (self._pos * self._yi)), (rect.width, rect.height)))
			else:
				target.blit(self._frames[self._pos], rect)

class Player(runtime.Widget):
	_xi = 0
	_yi = 2
	_lockAcc = False
	_lockFunc = None
	_old = None

	#Player's keys to be used
	leftKey = pg.K_LEFT
	rightKey = pg.K_RIGHT
	upKey = pg.K_UP
	downKey = pg.K_DOWN
	saKey = pg.K_PLUS
	maKey = pg.K_SPACE

	#For internal updates
	sourceTicks = pg.time.get_ticks()
	updateTimer = True

	#Max and min y that the player can rich. The y is handled into the player to be able to make the jump move
	max_y = 0
	min_y = 0

	#Player's motions
	leftMotion = None
	rightMotion = None
	downMotion = None
	upMotion = None
	SAMotion = None
	MAMotion = None

	#Callback to add attacks and such for updates
	MACallBack = None
	SACallBack = None
	LPCallBack = None

	#Used for attacks' timeout, directions and reload
	_lastTime = pg.time.get_ticks()
	_saTime = pg.time.get_ticks()
	_usingSA = False
	_toRight = False

	#The LPs
	_lp = 100
	max_lp = 100

	def __init__(self):
		runtime.Widget.__init__(self)
		self.leftMotion = Motion("./players/perso_2/right", self, speed = 0.1, invert = True)
		self.rightMotion = Motion("./players/perso_2/right", self, speed = 0.1)
		self.upMotion = Motion("./players/perso_2/fly", self, speed = 0.2)
		self.downMotion = Motion("./players/perso_2/down", self, yi=5)
		self.SAMotion = Motion("./players/perso_2/attaque", self)
		self.downMotion.setRollEnabled(False)

	def moveUp(self):
		"""Jump handler, move up"""
		if self._lockAcc == False:
			#First lock all
			self._lockAcc = True
			self._lockFunc = self.moveUp
			self._yi = 3
			self._old = "u"
		elif self._old == "u":
			#Then move to top, but not too fast
			if ((pg.time.get_ticks() - self.sourceTicks)/1000)>0.0025:
				#We go to the top
				if (self.rect.y > self.min_y) and (self._yi > 0):
					self.rect.y = self.rect.y - self._yi

				#We went to the top, then we get back on the floor
				elif (self.max_y > (self.rect.y + self.rect.height)):
					if (self._yi > 0):
						self._yi = -self._yi-1
					self.rect.y = self.rect.y - self._yi
					if ((self.rect.y + self.rect.height) < self.min_y):
						self.rect.y = self.min_y - self.rect.height

				#Else, it means that we riched the bottom, and we no more need to make this move, and so to
				else:
					self._lockAcc = False
					self._lockFunc = None
				self.updateTimer = True

	def moveLeft(self):
		"""Move to the left func handler"""
		if self._lockAcc == False:
			self._lockAcc = True
			self._lockFunc = None
			self._toRight = False
			#Don't let players go too fast!
			if (((pg.time.get_ticks() - self.sourceTicks)/1000)>0.02) or (self._old != "l"):
				self.rect.x = self.rect.x -5
				self.updateTimer = True
			self._old = "l"

	def moveRight(self):
		"""Move to the right func handler"""
		if self._lockAcc == False:
			self._lockAcc = True
			self._lockFunc = None
			self._toRight = True
			#To don't let players go too fast
			if (((pg.time.get_ticks() - self.sourceTicks)/1000)>0.02) or (self._old != "r"):
				self.rect.x = self.rect.x +5
				self.updateTimer = True
			self._old = "r"

	def moveDown(self):
		"""Get on the floor func handler"""
		if self._lockAcc == False:
			#We lock during "2 runs", one time this is called, so we lock then the second update will cause this to be called and we then unlock.
			#So the players can't get on the floor and move in the same time, or attack.
			self._lockAcc = True
			self._lockFunc = self.moveDown
			self._old = "d"
		elif self._old == "d":
			self._lockAcc = False
			self._lockFunc = None

	def generateSA(self):
		"""Function that generates, and updates the static attack."""
		if self.SACallBack != None:
			#Don't let players attack too fast
			if (self._usingSA == False) and (((pg.time.get_ticks() - self._saTime)/1000) > 0.10):
				#self.SACallBack(att)
				att = defaultAttack.Attack
				att.degs = 20
				att.degs = self.rect
				self._usingSA = True
				self._saTime = pg.time.get_ticks()
				self._lastTime = pg.time.get_ticks()
				print("Attack!")
			else:
				self._usingSA = False
				#Set to nothing to make it ignored, this will no more be an attack.
				self.SACallBack(None)

	def generateMA(self):
		"""Function that generates a moving attack (e.g. an arrow)."""
		#Use the timer to don't make too much attacks too fast
		if (self.MACallBack != None) and (((pg.time.get_ticks() - self._lastTime)/1000) > 0.2):
			self._lastTime = pg.time.get_ticks()
            #Set to the left or the right, be careful...
			att = defaultAttack.MovingAttack(self._toRight)
			att.image = pg.image.load("./players/perso_2/mvg.png")
			att.rect.y = self.rect.y + (self.rect.height - att.rect.height)/2
			if self._toRight:
				att.rect.x = self.rect.x + self.rect.width
			else:
				att.rect.x = self.rect.x - att.rect.width
				att.image = pg.transform.flip(att.image, True, False)
			self.MACallBack(att)

	def processAttackTimers(self):
		"""Func used to process SA timing out"""
		if self._usingSA == True:
			if (pg.time.get_ticks() - self._saTime) > 0.1:
				self.generateSA()

	def removeSA(self):
		self.generateSA()

	def touched(self, att):
		"""Handles attacks from the opponent"""
		#If there's the callback, we update the life points
		if (self.LPCallBack != None):
			self._lp-=att.degs
			self.LPCallBack(self._lp)

	def update(self, event):
		if event == None or event.type == pg.KEYDOWN:
			pressed_keys = pg.key.get_pressed()
            #We store it to know if it was previously down, which means that the Y is under the window rect. So we then have to bring it back
			wasDown = bool(self._old == "d")

			#If no lock, no action needs to run again
			if self._lockAcc == False:
				#Process the moves
				if pressed_keys[self.downKey]:
					self.moveDown()
				if pressed_keys[self.upKey]:
					self.moveUp()
				if pressed_keys[self.leftKey]:
					self.moveLeft()
				if pressed_keys[self.rightKey]:
					self.moveRight()
				#Process attack actions
			else:
				#Call the lock function, it will unlock when it'll no more need to be,
				if self._lockFunc != None:
					self._lockFunc()
				else:
					#if it doesn't exists, it means that it was just to block other moves func, so remove the lock.
					self._lockAcc = False

			#Process keys to attack
			if pressed_keys[self.saKey]:
				self.generateSA()
			elif pressed_keys[self.maKey]:
				self.generateMA()

			#For functions that requires timer, such as move left or right to don't let the players go too fast
			if self.updateTimer:
				self.sourceTicks = pg.time.get_ticks()
				self.updateTimer = False
			#We guess there's an update that must be done
			self.makePaintUpdate = True
			self.processAttackTimers()

			#Bring the right Y if needed
			if wasDown and (self._old != "d"):
				self.downMotion.reset()
			#We MUST share the events! Else the other player become buggy, it does not move as expected...
			return True
		self.processAttackTimers()
		#We MUST share the events! Else the other player become buggy...
		return True

	def customPaint(self):
		#We MUST not have 2+ motions painting in the same time! Do you imagine how much ugly it could be??

		#If touched, it is more important than any other animations
		if self._old == "t" and self.touchedMotion != None:
			self.touchedMotion.render(self.window, self.rect)

		#Paint the move's motion
		elif self._old == "u" and self.upMotion != None:
			self.upMotion.render(self.window, self.rect)
		elif self._old == "d" and self.downMotion != None:
			self.downMotion.render(self.window, self.rect)
		elif self._old == "r" and self.rightMotion != None:
			self.rightMotion.render(self.window, self.rect)
		elif self._old == "l" and self.leftMotion != None:
			self.leftMotion.render(self.window, self.rect)

		#Process the attack's motion
		elif self._old == "s" and self.SAMotion != None:
			self.SAMotion.render(self.window, self.rect)
		elif self._old == "m" and self.MAMotion != None:
			self.MAMotion.render(self.window, self.rect)
		else:
			#We just fill with a dark rectangle...
			pg.draw.rect(self.window, (0, 0, 0), self.rect)