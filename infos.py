#!/usr/bin/python3
import runtime
import pygame as pg

class InfosWindow(runtime.Widget):
	"""Displays information about the game"""
	_showing = False
	_rtm = runtime.Runtime()
	_win = None
	closed = True

	def __init__(self):
		runtime.Widget.__init__(self)
		self._rtm.addRoutine(self.postCheck)

	def postCheck(self):
		"""Runtime routine to tell when left"""
		if self.closed == True and self._rtm.running == True:
			self.closed = True
			self._rtm.quit()

	def popup(self):
		"""Shows th" win"""
		if self._rtm.running == False:
			self._win = pg.display.set_mode((710, 310))
			self._rtm.setWindow(self._win)
			self._rtm.addRoutine(self.postCheck)
			self.closed = False
			self.loadElements()
			self._rtm.execute()

	def loadElements(self):
		"""Loads UI elements"""
		l1 = runtime.Label()
		l1.text = "Comment jouer?"
		l1.font = pg.font.SysFont(None, 64)
		l1.color = (100, 100, 255)
		l1.rect.x = 10
		l1.rect.y = 5
		self._rtm.appendObject(l1)

		l2 = runtime.Label()
		l3 = runtime.Label()
		l4 = runtime.Label()
		l5 = runtime.Label()
		l6 = runtime.Label()
		l7 = runtime.Label()
		l8 = runtime.Label()
		l9 = runtime.Label()
		l10 = runtime.Label()

		l2.text = "Ici, deux joueurs s'affrontent en 1v1."
		l3.text	= "Chacun a un personnage avec différentes attaques. Cependant, il n'y en a seulement 4,"
		l4.text	= "pour les appeler, vérifiez vos touches.La barre de vie, les sauts, kicks et autres"
		l5.text	= "coups en tout genre seront vos seules options pour battre les doigts qui sont posés"
		l6.text	= "sur le même clavier."
		l7.text	= "Mais pourquoi ''Pringle's Fight''?"
		l8.text	= "De temps en temps, un Pringle se ballade sur votre écran, donnant accès à un coup spé-"
		l9.text	= "cial pour domminer votre concurant, seulement, vous avez 5 secondes pour l'activer et"
		l10.text	= "la touche à utiliser est choisie au hasard, alors la map vous montrera ses secrets!"

		listed = [l2, l3, l4, l5, l6, l7, l8, l9, l10]
		i = 0
		top = 68
		left = 15
		font = pg.font.SysFont(None, 24)
		while (i<len(listed)):
			listed[i].font = font
			listed[i].rect.y = i*26+top
			listed[i].rect.x = left
			self._rtm.appendObject(listed[i])
			i+=1