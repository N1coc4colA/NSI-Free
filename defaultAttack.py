#!/usr/bin/python3
import pygame as pg
import time

class Attack():
	"""Abstract clas for the attack sys and it's derivates."""
	def __init__(self):
		self.degs = 1
		self.rect = pg.Rect((0, 0), (32, 32))
		self.destructionFinished = False

class MovingAttack(Attack):
	"""MovingAttack is used for shurikens, fireballs, and such."""
	image = None
	destructionFrames = []
	enablePosUpdateOnDraw = True

	def __init__(self, toRight, speed = 0.005, indice = 3):
		Attack.__init__(self)
		self.window = None
		self.color = (0, 0, 0)
		#self.rect = pg.Rect((0, 0), (32, 32))
		if toRight == True:
			self._indice = indice
		else:
			self._indice = -indice

		self.RuntimeOUID = -1
		self.makePaintUpdate = False
		self._shouldDest = False
		self._currDest = 0
		self._speed = speed
		self._oldTime = pg.time.get_ticks()

	def destruction(self):
		"""Changes the painting and stops the move to animate the destruction of the attack."""
		self._shouldDest = True
		self._oldTime = time.time()
		self._indice = 0

	def remove(self):
		"""Called when going OOR or at end of destruction animation, it must destroy itself."""
		del self

	def setWindow(self, target):
		self.window = target

	def setOUID(self, v):
		"""See Runtime module and it's Runtime class, needed behaviour for object tracking."""
		self.RuntimeOUID = v

	def posUpdate(self):
		"""Generates the position updates (X, Y)"""
		if (((pg.time.get_ticks() - self._oldTime)/1000) > self._speed):
			self.rect.x = self.rect.x + self._indice
			self.makePaintUpdate = True
			self._oldTime = pg.time.get_ticks()

	def customPaint(self):
		"""Paints the moving attack"""
		#Use at painting cause we have an issue with the update handling in Runtime or in our classes
		if self.enablePosUpdateOnDraw == True:
			self.posUpdate()
		if self.window != None:
			if (self._shouldDest) and ((not self.destructionFrames) == False):
				self.window.blit(self.destructionFrames[self._currDest], (self.rect.x, self.rect.y))
			elif self.image != None:
				self.window.blit(self.image, (self.rect.x, self.rect.y))
			else:
				pg.draw.rect(self.window, (0, 0, 0), self.rect)

	def update(self, event):
		"""Process events and other internal data to generate this object's updates of internal data."""
		if self._shouldDest:
			if (not self.destructionFrames) == False:
				if (self._currDest < len(self.destructionFrames)):
					if (((pg.time.get_ticks() - self._oldTime)/1000) > self._speed):
						self.makePaintUpdate = True
						self._currDest += 1
						self._oldTime = pg.time.get_ticks()
				else:
					self.destructionFinished = True
			else:
				self.destructionFinished = True
		else:
			self.posUpdate()
		return True