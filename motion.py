import runtime
import pygame as pg
import os
import defaultAttack

class Motion:
	"""Motion class is a way to animate over painting events and timers in a certain behaviour."""
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
			print(filePath)
			if (filePath[1]) != ".db":
				if (source != None):
				    frames.append(pg.transform.scale(pg.image.load(motionDir + "/" + fList[i]), (source.rect.width, source.rect.height)))
				else:
				    frames.append(pg.image.load(motionDir + "/" + fList[i]))
			i+=1
		i = 0
		framed = []
		#Get .image files (in alphabetical order) to set them as frames
		while (i<len(frames) and invert):
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
