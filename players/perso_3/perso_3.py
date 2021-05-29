#!/usr/bin/python3
import defaultPlayer
import motion

class Player(defaultPlayer.Player):
	"""Player base class, meant to be used in any player that have to be loaded."""

	def __init__(self):
		defaultPlayer.Player.__init__(self)
		self.leftMotion = motion.Motion("./players/perso_3/thanos_deplacement", self, speed = 0.1, invert = True)
		self.rightMotion = motion.Motion("./players/perso_3/thanos_deplacement", self, speed = 0.1)
		self.upMotion = motion.Motion("./players/perso_3/thanos_saut", self, speed = 0.4)
		self.downMotion = motion.Motion("./players/perso4_3/thanos_repos", self, yi=5)
		self.SAMotion = motion.Motion("./players/perso_3/thanos_attaque1", self, speed = 0.2)
		self.downMotion.setRollEnabled(False)