#!/usr/bin/python3
import runtime
import pygame as pg
import os
import defaultAttack
import motion

class Player(runtime.Widget):
	"""Player base class, meant to be used in any player that have to be loaded."""
	_xi = 0
	_yi = 2
    #At the beginnig, we use this before the first move
	_firstPaint = True

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

	#Public "API", commonly, it's what's used but you might want to reimplement some funcs, but mainly these members fit the needs
	leftMotion = None
	rightMotion = None
	downMotion = None
	upMotion = None
	SAMotion = None
	MAMotion = None

	move_up_speed = 2.5
	move_down_indent = 1
	move_left_speed = 20
	move_left_indent = 5
	move_right_speed = 20
	move_right_indent = 5
	sa_cool_down = 400
	ma_cool_down = 2000
	ma_p1 = "./players/perso_2/mvg.png"
	ma_p2 = None

	def __init__(self):
		runtime.Widget.__init__(self)
		
		self._lockAcc = False
		self._lockFunc = None
		self._old = None
		#Used for painting and such
		self.isP1 = None
		self._goingDown = False

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
			if (pg.time.get_ticks() - self.sourceTicks)>self.move_up_speed:
				#We go to the top
				if (self.rect.y > self.min_y) and (self._yi > 0):
					self.rect.y = self.rect.y - self._yi

				#We went to the top, then we get back on the floor
				elif (self.max_y > (self.rect.y + self.rect.height)):
					if (self._yi > 0):
						self._yi = -self._yi - self.move_down_indent
					self.rect.y = self.rect.y - self._yi
					if ((self.rect.y + self.rect.height) < self.min_y):
						self.rect.y = self.min_y - self.rect.height

				#Else, it means that we riched the bottom, and we no more need to make this move, and so to
				else:
					self._lockAcc = False
					self._lockFunc = None
				#Put it in the old direction
				print("Reach")
				if self._toRight:
					self.moveRight()
				else:
					self.moveLeft()
				self.updateTimer = True

	def moveLeft(self):
		"""Move to the left func handler"""
		if self._lockAcc == False:
			self._lockAcc = True
			self._lockFunc = None
			self._toRight = False

			#We might need to reset the y pos!
			if self._old == "d":
				self.rect.height = self._oldH
				self.rect.x = self.max_y - self.rect.height

			#Don't let players go too fast!
			if (pg.time.get_ticks() - self.sourceTicks)>self.move_left_speed or (self._old != "l"):
				self.rect.x = self.rect.x - self.move_left_indent
				self.updateTimer = True
			self._old = "l"

	def moveRight(self):
		"""Move to the right func handler"""
		if self._lockAcc == False:
			self._lockAcc = True
			self._lockFunc = None
			self._toRight = True

			#We might need to reset the y pos!
			if self._old == "d":
				self.rect.height = self._oldH
				self.rect.x = self.max_y - self.rect.height

			#To don't let players go too fast
			if (pg.time.get_ticks() - self.sourceTicks)>self.move_right_speed or (self._old != "r"):
				self.rect.x = self.rect.x + self.move_right_indent
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
			self._oldH = self.rect.height
		elif self._old == "d":
			self._lockAcc = False
			self._lockFunc = None

	def generateSA(self):
		"""Function that generates, and updates the static attack."""
		if self._lockAcc == False:
			self._lockAcc = True
			if self.SACallBack != None:
				#Don't let players attack too fast
				if (self._usingSA == False) and (pg.time.get_ticks() - self._saTime) > self.sa_cool_down:
					att = defaultAttack.Attack
					att.degs = 20
					att.rect = self.rect
					self._saTime = pg.time.get_ticks()
					self._lastTime = pg.time.get_ticks()
					self.SACallBack(att)
				else:
					self._usingSA = False
					#Set to nothing to make it ignored, this will no more be an attack.
					self.SACallBack(None)
			self._old = "s"
		elif self._old == "s":
			self._lockAcc = False

	def generateMA(self):
		"""Function that generates a moving attack (e.g. an arrow)."""
		#Use the timer to don't make too much attacks too fast
		if (self.MACallBack != None) and (pg.time.get_ticks() - self._lastTime) > self.ma_cool_down and (self._goingDown == False):
			self._lastTime = pg.time.get_ticks()
            #Set to the left or the right, be careful...
			att = defaultAttack.MovingAttack(self._toRight)
			if self.ma_p1 != None:
				att.image = pg.image.load(self.ma_p1)
			if self.ma_p2 != None:
				att.setFrameDir(self.ma_p2)
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
		"""Event handler"""
		if event == None or event.type == pg.KEYDOWN:

			if self._old == "s" and self.SAMotion != None and self.SAMotion.animEnded() == True:
				self._lockFunc = None
				self._lockAcc = False
				if self._toRight:
					self.moveRight()
				else:
					self.moveLeft()

        #At the beginning, there's no move , so if it's P1 or P2, choose right or left motion.
			if (self._firstPaint):
				if (self._firstPaint and self.isP1):
					self.moveRight()
				else:
					self.moveLeft()
				self._firstPaint = False

			pressed_keys = pg.key.get_pressed()
            #We store it to know if it was previously down, which means that the Y is under the window rect. So we then have to bring it back
			wasDown = bool(self._old == "d")

			#Process keys to attack BEFORE the moves ones. Else there's a litigation about which animation have to run.
			if pressed_keys[self.saKey]:
				self.generateSA()
			elif pressed_keys[self.maKey]:
				self.generateMA()

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
				self._goingDown = False

			#We MUST share the events! Else the other player become buggy, it does not move as expected...
			return True
		self.processAttackTimers()

		#We MUST share the events! Else the other player become buggy...
		return True

	def customPaint(self):
		"""Painting handler"""
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
