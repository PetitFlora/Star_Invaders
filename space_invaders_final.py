import pygame # importation de la librairie pygame
import random
import space
import sys # pour fermer correctement l'application

# Initialisation de Pygame
pygame.init()

# Création de la fenêtre
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Star Invaders")

# Chargement de l'image de fond
fond = pygame.image.load('bg.png')

# Chargement de la musique et des effets sonores
musique_menu = "./son/menu.wav"
musique_bataille = "./son/battle.wav"

tir = pygame.mixer.Sound("./son/tir.wav")
explosion = pygame.mixer.Sound("./son/explosion.wav")

# Horloge pour limiter les FPS
clock = pygame.time.Clock()

class Jeu():
    """Classe principal du jeu."""

    def __init__(self):
        """Initialise le jeu Star Invaders."""
        # Instanciation des classe
        self.menu = space.Menu()
        self.niveaux = space.Niveau(1)
        self.player = space.Joueur("X-Wing")
        self.tir = space.Balle(self.player, True)

        # Création des ennemis
        self.type_ennemis = space.stats_vaisseaux_ennemis_e
        self.listeEnnemis = [space.Ennemi(self.type_ennemis) for _ in range(space.Ennemi.NbEnnemis)]
        self.listeTirEnnemis = [space.Balle(ennemi, False) for ennemi in self.listeEnnemis]

        # Liste des bonus
        self.listeBonus = []
        self.listeBonusActifs = []

        # Musique
        self.musique_actuelle = None

    def changer_musique(self, nouvelle_musique):
        """Change la musique de fond."""
        if self.musique_actuelle != nouvelle_musique:
            pygame.mixer.music.load(nouvelle_musique)
            pygame.mixer.music.play(-1)
            self.musique_actuelle = nouvelle_musique

    def gestion_evenements(self):
        """Gère les événements du jeu."""
        for event in pygame.event.get(): # parcours de tous les event pygame dans cette fenêtre
            if event.type == pygame.QUIT: # si l'événement est le clic sur la fermeture de la fenêtre
                pygame.quit()
                sys.exit() # pour fermer correctement

            # gestion du menu    
            elif self.menu.nom_menu in ['home', 'level', 'infini', 'level_rebelle', 'level_empire', 'infini_rebelle', 'infini_empire']:
                self.menu.gestion_evenements_menu(event)
                if self.menu.nom_menu == 'inf_r':
                    self.player = space.Joueur(self.menu.choix_rebelles[self.menu.j])
                    self.tir = space.Balle(self.player, True)
                    self.type_ennemis = space.stats_vaisseaux_ennemis_e
                    self.listeEnnemis = [space.Ennemi(self.type_ennemis) for _ in range(space.Ennemi.NbEnnemis)]
                    self.listeTirEnnemis = [space.Balle(ennemi, False) for ennemi in self.listeEnnemis]

                elif self.menu.nom_menu == 'inf_e':
                    self.player = space.Joueur(self.menu.choix_empire[self.menu.j])
                    self.tir = space.Balle(self.player, True)
                    self.type_ennemis = space.stats_vaisseaux_ennemis_r
                    self.listeEnnemis = [space.Ennemi(self.type_ennemis) for _ in range(space.Ennemi.NbEnnemis)]
                    self.listeTirEnnemis = [space.Balle(ennemi, False) for ennemi in self.listeEnnemis]

                elif self.menu.nom_menu == 'lev_r':
                    self.player = space.Joueur(self.menu.choix_rebelles[self.menu.j//2])
                    self.tir = space.Balle(self.player, True)
                    self.type_ennemis = space.stats_vaisseaux_ennemis_e
                    self.listeEnnemis = [space.Ennemi(self.type_ennemis) for _ in range(space.Ennemi.NbEnnemis)]
                    self.listeTirEnnemis = [space.Balle(ennemi, False) for ennemi in self.listeEnnemis]
                    self.niveaux = space.Niveau(self.menu.j +1)

                elif self.menu.nom_menu == 'lev_e':
                    self.player = space.Joueur(self.menu.choix_empire[self.menu.j//2])
                    self.tir = space.Balle(self.player, True)
                    self.type_ennemis = space.stats_vaisseaux_ennemis_r
                    self.listeEnnemis = [space.Ennemi(self.type_ennemis) for _ in range(space.Ennemi.NbEnnemis)]
                    self.listeTirEnnemis = [space.Balle(ennemi, False) for ennemi in self.listeEnnemis]
                    self.niveaux = space.Niveau(self.menu.j +1)
            
            # gestion du clavier
            elif event.type == pygame.KEYDOWN: # si une touche a été tapée KEYUP quand on relache la touche
                if event.key == pygame.K_LEFT: # si la touche est la fleche gauche
                    self.player.sens = "gauche" # on déplace le vaisseau de sur la gauche
                elif event.key == pygame.K_RIGHT: # si la touche est la fleche droite
                    self.player.sens = "droite" # on déplace le vaisseau de sur la droite
                elif event.key == pygame.K_SPACE and self.tir.etat != "tiree": # espace pour tirer
                    tir.play()
                    self.tir.etat = "tiree"

    def gestion_collisions(self):
        """Gère les gestion des collisions entre les différents éléments du jeu."""
        for ennemi, tir_ennemi in zip(self.listeEnnemis, self.listeTirEnnemis):
            tir_ennemi.etat = "tiree"
            tir_ennemi.cooldown(self.type_ennemis)

            if self.tir.toucher(ennemi):
                self.tir.__init__(self.player, True)
                ennemi.nb_vie -= 1
                if ennemi.nb_vie <= 0:
                    explosion.play()
                    if self.menu.nom_menu in ['inf_r', 'inf_e']:
                        if random.random() < 0.3:  # 30% de chance d'apparition d'un bonus
                            bonus = space.Bonus(ennemi.x, ennemi.y, self.player)
                            self.listeBonus.append(bonus)

                    ennemi.disparaitre(self.type_ennemis)
                    if self.menu.nom_menu in ['lev_r', 'lev_e']:
                        self.niveaux.nb_vaisseaux -= 1
                        if self.niveaux.nb_vaisseaux < 4:
                            self.listeEnnemis.remove(ennemi)
                            self.listeTirEnnemis.remove(tir_ennemi)
                        if self.niveaux.nb_vaisseaux <= 0:
                            self.menu.nom_menu = 'home'

                    tir_ennemi.disparaitre()
                    self.player.marquer()

            if tir_ennemi.toucher(self.player) and not self.player.bouclier:
                tir_ennemi.disparaitre()
                self.player.perdre_vie()

            ennemi.collisions()

        # Gestion des bonus
        for bonus in self.listeBonus:
            bonus.deplacer()
            if bonus.toucher(self.player):
                bonus.effet_bonus()
                self.listeBonusActifs.append(bonus)
                self.listeBonus.remove(bonus)
            elif bonus.y > 600:  # Si le bonus sort de l'écran
                self.listeBonus.remove(bonus)

        # Vérifier les bonus actifs et réinitialiser leur effet si nécessaire
        for bonus in self.listeBonusActifs[:]:
            bonus.actif()
            if not bonus.actif():
                bonus.reset_bonus()
                self.listeBonusActifs.remove(bonus)

    def mise_a_jour(self):
        """Met à jour les éléments du jeu."""
        # menu
        if self.menu.nom_menu in ['home', 'level', 'infini', 'level_rebelle', 'level_empire', 'infini_rebelle', 'infini_empire']:
            self.changer_musique(musique_menu)
            return
        # jeu
        else:
            self.changer_musique(musique_bataille)
            self.player.deplacer()
            self.tir.bouger()
            self.player.x = max(0, min(800 - self.player.image.get_width(), self.player.x))

            for ennemi, tir_ennemi in zip(self.listeEnnemis, self.listeTirEnnemis):
                ennemi.avancer()
                tir_ennemi.bouger()

            for bonus in self.listeBonus:
                bonus.deplacer()

    def dessin(self):
        """Dessine les éléments du jeu."""
        # menu
        if self.menu.nom_menu in ['home', 'level', 'infini', 'level_rebelle', 'level_empire', 'infini_rebelle', 'infini_empire']:
            getattr(self.menu, f"afficher_{self.menu.nom_menu}")(screen)
        # jeu
        else:
            screen.blit(fond, (0, 0))
            screen.blit(self.player.image, (self.player.x, self.player.y))
            screen.blit(self.tir.image, (self.tir.x, self.tir.y)) if self.tir.etat == "tiree" else None

            for ennemi, tir_ennemi in zip(self.listeEnnemis, self.listeTirEnnemis):
                screen.blit(ennemi.image, (ennemi.x, ennemi.y))
                screen.blit(tir_ennemi.image, (tir_ennemi.x, tir_ennemi.y)) if tir_ennemi.etat == "tiree" else None

            for bonus in self.listeBonus:
                screen.blit(bonus.image, (bonus.x, bonus.y))

            self.player.info_niveaux(screen)

        pygame.display.update()

jeu = Jeu()

# Boucle principale du jeu
running = True
while running:
    jeu.gestion_evenements()
    jeu.gestion_collisions()
    jeu.mise_a_jour()
    jeu.dessin()

    if jeu.player.vie <= 0:
        running = False

    clock.tick(60)

pygame.quit()
sys.exit()