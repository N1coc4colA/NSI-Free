#!/usr/bin/python3
import defaultPlayer
import motion

class Player(defaultPlayer.Player):
	"""Player base class, meant to be used in any player that have to be loaded."""

	def __init__(self):
		defaultPlayer.Player.__init__(self)
		self.leftMotion = motion.Motion("./players/perso4/avancer", self, speed = 0.2, invert = True)
		self.rightMotion = motion.Motion("./players/perso4/avancer", self, speed = 0.2)
		self.upMotion = motion.Motion("./players/perso4/sauter", self, speed = 0.2)
		self.downMotion = motion.Motion("./players/perso4/down", self, yi=5)
		self.SAMotion = motion.Motion("./players/perso4/spe_main", self, speed = 0.2)
		self.downMotion.setRollEnabled(False)