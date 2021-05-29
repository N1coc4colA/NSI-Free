#!/usr/bin/python3 -tt
import pygame
import keys, maps, infos
import playerchooser
import Loader
import runtime as rtm

surfaceW = 800 #Dimension de la fenêtre / Largeur
surfaceH = 600 #Dimension de la fenêtre / Longueur

class Menu:
	playCallBack = None
	howToCallBack = None
	commandsCallBack = None
	quitCallBack = None

	""" Création et gestion des boutons d'un menu """
	def __init__(self):
		self.couleurs = dict(
            normal=(0, 200, 0),
            survol=(0, 200, 200),
        )

	def load(self, *groupes):
		pygame.font.init()
		font = pygame.font.SysFont("Helvetica", 24, bold=True)
        # noms des menus et commandes associées
		items = (
            ('JOUER', self.playCallBack),
            ('COMMENT JOUER ?', self.howToCallBack),
            ('COMMANDES', self.commandsCallBack),
            ('QUITTER', self.quitCallBack)
        )
		x = 400
		y = 100
		self._boutons = []
		for texte, cmd in items:
			mb = MenuBouton(
                texte,
                self.couleurs['normal'],
                font,
                x,
                y,
                250,
                50,
                cmd
            )
			self._boutons.append(mb)
			y += 120
			for groupe in groupes:
				groupe.add(mb)

	def update(self, events):
		clicGauche, *_ = pygame.mouse.get_pressed()
		posPointeur = pygame.mouse.get_pos()
		for bouton in self._boutons :
			# Si le pointeur souris est au-dessus d'un bouton
			if bouton.rect.collidepoint(*posPointeur):
				# Changement du curseur par un quelconque
				pygame.mouse.set_cursor(*pygame.cursors.broken_x)
				# Changement de la couleur du bouton
				bouton.dessiner(self.couleurs['survol'])
				# Si le clic gauche a été pressé
				if clicGauche:
                    # Appel de la fonction du bouton
					bouton.executerCommande()
				break
			else:
                # Le pointeur n'est pas au-dessus du bouton
				bouton.dessiner(self.couleurs['normal'])
		else:
            # Le pointeur n'est pas au-dessus d'un des boutons
            # initialisation au pointeur par défaut
			pygame.mouse.set_cursor(*pygame.cursors.arrow)

	def detruire(self):
		pygame.mouse.set_cursor(*pygame.cursors.arrow) # initialisation du pointeur



class MenuBouton(pygame.sprite.Sprite):
    """ Création d'un simple bouton rectangulaire """
    def __init__(self, texte, couleur, font, x, y, largeur, hauteur, commande):
        super().__init__()
        self._commande = commande

        self.image = pygame.Surface((largeur, hauteur))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.texte = font.render(texte, True, (0, 0, 0))
        self.rectTexte = self.texte.get_rect()
        self.rectTexte.center = (largeur/2, hauteur/2)

        self.dessiner(couleur)

    def dessiner(self, couleur):
        self.image.fill(couleur)
        self.image.blit(self.texte, self.rectTexte)

    def executerCommande(self):
        # Appel de la commande du bouton
        if self._commande:
            self._commande()

class Jeu :
    """ Simulacre de l'interface du jeu """
    def __init__(self, jeu, *groupes):
        self._fenetre = jeu.fenetre
        jeu.fond = (0, 0, 0)

        from itertools import cycle
        couleurs = [(0, 48, i) for i in range(0, 256, 15)]
        couleurs.extend(sorted(couleurs[1:-1], reverse=True))
        self._couleurTexte = cycle(couleurs)

        self._font = pygame.font.SysFont("Helvetica", 36, bold=True)
        self.creerTexte()
        self.rectTexte = self.texte.get_rect()
        self.rectTexte.center = (surfaceW/2, surfaceH/2)
        # Création d'un event
        self._CLIGNOTER = pygame.USEREVENT + 1
        pygame.time.set_timer(self._CLIGNOTER, 80)

    def creerTexte(self) :
        self.texte = self._font.render(
            "LE JEU EST EN COURS D'EXÉCUTION",
            True,
            next(self._couleurTexte)
        )

    def update(self, events):
        self._fenetre.blit(self.texte, self.rectTexte)
        for event in events :
            if event.type == self._CLIGNOTER:
                self.creerTexte()
                break

    def detruire(self):
        pygame.time.set_timer(self._CLIGNOTER, 0) # désactivation du timer

class Application:
	""" Classe maîtresse gérant les différentes interfaces du jeu """
	_keys = keys.KeysSettings()
	_maps = maps.MapChooser()
	_infos = infos.InfosWindow()
	_pC = playerchooser.PlayerChooser()
	_mapPath = ""
	_pp1 = ""
	_pp2 = ""

	def __init__(self):
		pygame.init()
		pygame.display.set_caption("Pringle's Fight")

		self.fond = (150,)*3

		self.fenetre = pygame.display.set_mode((surfaceW,surfaceH))
        # Groupe de sprites utilisé pour l'affichage
		self.groupeGlobal = pygame.sprite.Group()
		self.statut = True

        #Mise en place des fonctions de retours
		self._infos.setReturnCallBack(self.retour_au_menu)
		self._keys.setReturnCallBack(self.retour_au_menu)
		self._maps.setReturnCallBack(self.retour_au_menu)
		self._maps.setCallBack(self.handlePlayerChooser)
		self._pC.setReturnCallBack(self.retour_au_menu)
		self._pC.setCallBack(self.handleMapLaunch)

	def _initialiser(self):
		try:
			self.ecran.detruire()
            # Suppression de tous les sprites du groupe
			self.groupeGlobal.empty()
		except AttributeError:
			pass

	def setMapPath(self, fp):
		self._mapPath = fp

	def retour_au_menu(self):
		#Else we get issue while getting back from Runtime instances
		self.statut = False
		self.update()
		self.reset()
		self.menu()
		self.revenir_menu()

	def reset(self):
		self._pC.reset()
		self._maps.reset()
		del self.fenetre
		self.fenetre = pygame.display.set_mode((surfaceW,surfaceH))
		self.groupeGlobal = pygame.sprite.Group()
		self.statut = True

	def menu(self):
        # Affichage du menu

		self._initialiser()
		self.ecran = Menu()

		self.ecran.commandsCallBack = self._keys.popup
		self.ecran.playCallBack = self._maps.popup
		self.ecran.howToCallBack = self._infos.popup
		self.ecran.quitCallBack = self.quitter

		self.ecran.load(self.groupeGlobal)

	def processMapLeave(self):
		self._mapPath = ""
		self._maps.reset()
		self.retour_au_menu()

	def handlePlayerChooser(self, fp):
		"""n"""
		self._mapPath = fp
		self._pC.popup()

	def handleMapLaunch(self, fp1, fp2):
		self._pp1 = fp1
		self._pp2 = fp2
		curr_map = Loader.loadMap(self._mapPath, self._pp1, self._pp2)
		curr_map.setExitCB(self.retour_au_menu)
		curr_map.popup()

	def jeu(self):
        # Affichage du jeu
		self._initialiser()
		self.ecran = Jeu(self, self.groupeGlobal)

	def comment_jouer(self):
        #Affichage des commandes pour jouer
		self._initialiser()
		self.ecran = Jeu(self, self.groupeGlobal)

	def quitter(self):
		pygame.display.quit()
		pygame.quit()

	def update(self):
		events = pygame.event.get()

		for event in events:
			if event.type == pygame.QUIT:
				self.statut = False
				return

		if self.statut == True:
			self.fenetre.fill(self.fond)
			self.ecran.update(events)
			self.groupeGlobal.update()
			self.groupeGlobal.draw(self.fenetre)
			pygame.display.update()

	def revenir_menu(self):
		clock = pygame.time.Clock()
		app.statut = True
		timer = pygame.time.get_ticks()
		while app.statut:
			if (pygame.time.get_ticks() - timer) >= 30:
				app.update()
		self.quitter()

app = Application()
app.menu()
app.revenir_menu()

#pygame.quit()
