import pygame
import random
from collections import namedtuple
import pygame.freetype

# Initialisation de pygame
pygame.init()
pygame.freetype.init()

# Initialisation des constantes
X_MIN, Y_MIN, X_MAX, Y_MAX = 0, 100, 736, 300
NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
JAUNE = (249, 236, 0)
BASE_FONT = pygame.freetype.SysFont(None, 20)
MENU_FONT = pygame.freetype.SysFont(None, 40)
TITLE_FONT = pygame.freetype.SysFont(None, 80)

# Préchargement des images
IMAGES = {
    # Vaisseaux joueur
    "X-Wing": pygame.image.load("./joueur/x-wing.png"),
    "Y-Wing": pygame.image.load("./joueur/y-wing.png"),
    "Faucon": pygame.image.load("./joueur/faucon.png"),
    "Tie-Fighter": pygame.image.load("./joueur/tie-fighter.png"),
    "Tie-Bombardier": pygame.image.load("./joueur/tie-bombardier.png"),
    "Destroyer Imperial": pygame.image.load("./joueur/Imperial_destroyer.png"),

    # Vaisseaux ennemis
    "X-Wing Ennemi": pygame.image.load("./ennemi/x-wing.png"),
    "Y-Wing Ennemi": pygame.image.load("./ennemi/y-wing.png"),
    "Faucon Ennemi": pygame.image.load("./ennemi/faucon.png"),
    "Tie-Fighter Ennemi": pygame.image.load("./ennemi/tie-fighter.png"),
    "Tie-Bombardier Ennemi": pygame.image.load("./ennemi/tie-bombardier.png"),
    "Destroyer Imperial Ennemi": pygame.image.load("./ennemi/Imperial_destroyer.png"),

    # Tirs
    "Tirs Vert": pygame.image.load('./joueur/tirs_vert.png'),
    "Tirs Rouge": pygame.image.load('./joueur/tirs_rouge.png'),
    "Tirs Vert Ennemi": pygame.image.load('./ennemi/tirs_vert.png'),
    "Tirs Rouge Ennemi": pygame.image.load('./ennemi/tirs_rouge.png'),

    # Menu
    "Menu BG Home": pygame.image.load('menu_bg_home.png'),
    "Menu BG": pygame.image.load('menu_bg.png'),
    "Retour": pygame.image.load('retour.png'),
    "Rebelles": pygame.image.load('rebelles.png'),
    "Empire": pygame.image.load('empire.png'),
    
    # Bonus
    "Bonus Plus Vitesse": pygame.image.load('./bonus/+_vitesse.png'),
    "Bonus Moins Vitesse": pygame.image.load('./bonus/-_vitesse.png'),
    "Bonus Vie": pygame.image.load('./bonus/vie.png'),
    "Bonus Bouclier": pygame.image.load('./bonus/bouclier.png')
}

## Statistiques des vaisseaux

# Vaisseaux joueur
StatsVaisseaux = namedtuple('StatsVaisseaux', 
    ['image', 'vitesse', 'balle'])

stats_vaisseaux = {
    "X-Wing": StatsVaisseaux(IMAGES["X-Wing"], 2.5, 1),
    "Y-Wing": StatsVaisseaux(IMAGES["Y-Wing"], 1.25, 1),
    "Faucon": StatsVaisseaux(IMAGES["Faucon"], 1.875, 1),
    "Tie-Fighter": StatsVaisseaux(IMAGES["Tie-Fighter"], 2.5, 2),
    "Tie-Bombardier": StatsVaisseaux(IMAGES["Tie-Bombardier"], 1.25, 2),
    "Destroyer Imperial": StatsVaisseaux(IMAGES["Destroyer Imperial"], 1.875, 2)
}

# Vaisseaux ennemis
StatsVaisseauxEnnemis = namedtuple('StatsVaisseauxEnnemis', 
    ['image', 'vitesse_x', 'vitesse_y', 'puissance_tir', 'vitesse_tir', 'vie', 'balle'])

stats_vaisseaux_ennemis_r = {
    "X-Wing Ennemi": StatsVaisseauxEnnemis(IMAGES["X-Wing Ennemi"], 0.5, 1.5, 1, 400, 1, 1),
    "Y-Wing Ennemi": StatsVaisseauxEnnemis(IMAGES["Y-Wing Ennemi"], 0.25, 1, 2, 800, 2, 1),
    "Faucon Ennemi": StatsVaisseauxEnnemis(IMAGES["Faucon Ennemi"], 0.375, 1, 1, 600, 1, 1)
}

stats_vaisseaux_ennemis_e = {
    "Tie-Fighter Ennemi": StatsVaisseauxEnnemis(IMAGES["Tie-Fighter Ennemi"], 0.5, 1.5, 1, 400, 1, 2),
    "Tie-Bombardier Ennemi": StatsVaisseauxEnnemis(IMAGES["Tie-Bombardier Ennemi"], 0.25, 1, 2, 800, 2, 2),
    "Destroyer Imperial Ennemi": StatsVaisseauxEnnemis(IMAGES["Destroyer Imperial Ennemi"], 0.375, 1, 1, 600, 1, 2)
}

StatsBonus = namedtuple('StatsBonus', 
    ['image','duree'])

stats_bonus = {
    "Bonus Plus Vitesse": StatsBonus(IMAGES["Bonus Plus Vitesse"], 600),
    "Bonus Moins Vitesse": StatsBonus(IMAGES["Bonus Moins Vitesse"], 600),
    "Bonus Vie": StatsBonus(IMAGES["Bonus Vie"], 0),
    "Bonus Bouclier": StatsBonus(IMAGES["Bonus Bouclier"], 600)
}

class Joueur():
    """Classe pour représenter le vaisseau du joueur."""

    def __init__(self, type):
        """
        Initialise un objet Joueur.

        Args:
            type (str): Le type de vaisseau du joueur.
        """
        self.type = type
        self.type_stats = stats_vaisseaux[type]
        self.image = self.type_stats.image
        self.x = 400
        self.y = 500
        self.balle = self.type_stats.balle
        self.vitesse = self.type_stats.vitesse
        self.bouclier = False
        self.sens = None
        self.score = 0
        self.vie = 5

    def deplacer(self):
        """Déplace le vaisseau du joueur selon sa direction."""
        if self.sens == "gauche":
            self.x -= self.vitesse
        elif self.sens == "droite":
            self.x += self.vitesse
            
    def marquer(self):
        """Augmente le score du joueur de 1."""
        self.score += 1
    
    def perdre_vie(self):
        """Décrémente la vie du joueur de 1."""
        self.vie -= 1
    
    def info_niveaux(self, screen):
        """Affiche les informations du joueur à l'écran.

        Args:
            screen (pygame.Surface): Surface sur laquelle dessiner.
        """
        pygame.draw.rect(screen, NOIR, (0, 0, 800, 100))
        
        score_text, score_rect = BASE_FONT.render(f"Score: {self.score}", BLANC)
        score_rect.topleft = (20, 40)
        screen.blit(score_text, score_rect)

        vie_text, vie_rect = BASE_FONT.render(f"Vie: {self.vie}", BLANC)
        vie_rect.topleft = (270, 40)
        screen.blit(vie_text, vie_rect)

        if self.bouclier:
            bouclier_text, bouclier_rect = BASE_FONT.render(f"Bouclier actif", BLANC)
            bouclier_rect.topleft = (520, 40)
            screen.blit(bouclier_text, bouclier_rect)


class Balle():
    """Classe pour représenter une balle tirée par un joueur ou un ennemi."""

    def __init__(self, tireur, joueur):
        """Initialise une balle.

        Args:
            tireur (object): L'objet qui tire la balle.
            joueur (bool): Indique si la balle est tirée par le joueur (True) ou par un ennemi (False).
        """
        self.tireur = tireur
        self.x = self.tireur.x + 27
        self.etat = "chargee"
        self.joueur = joueur  # True si le tir est celui du joueur, False si c'est celui d'un ennemi
        if self.joueur:
            self.y = tireur.y - 5
            self.vitesse = 10
            self.image = IMAGES[f"Tirs {'Vert' if tireur.balle == 1 else 'Rouge'}"]
        else:
            self.y = tireur.y + 37
            self.vitesse = 3
            self.recharge = tireur.vitesse_tir
            self.image = IMAGES[f"Tirs {'Vert Ennemi' if tireur.balle == 1 else 'Rouge Ennemi'}"]

    def bouger(self):
        """Déplace la balle sur l'écran selon si elle est tirée ou non."""
        if self.joueur:
            if self.etat == "chargee":
                self.x = self.tireur.x + 27
            elif self.y > 100:
                self.y -= self.vitesse
            else:
                self.etat = "chargee"
                self.y = 495
        else:
            if self.etat == "chargee":
                self.x = self.tireur.x + 27
                self.y = self.tireur.y + 37
            else:
                if self.y < 600:
                    self.y += self.vitesse
                else:
                    self.etat = "chargee"

    def cooldown(self, type):
        """Gère le temps de recharge de la balle.

        Args:
            type (str): Type de vaisseau tireur.
        """
        self.recharge -= 1
        if self.recharge == 0:
            self.recharge = Ennemi(type).vitesse_tir
            self.bouger()

    def disparaitre(self):
        """Réinitialise la balle à son état initial."""
        self.__init__(self.tireur, self.joueur)

    def toucher(self, ennemi):
        """Vérifie si la balle touche un ennemi.

        Args:
            ennemi (object): L'ennemi à vérifier.

        Returns:
            bool: True si la balle touche l'ennemi, sinon False.
        """
        return (ennemi.x <= self.x <= ennemi.x + ennemi.image.get_width() or
                ennemi.x <= self.x + self.image.get_width() <= ennemi.x + ennemi.image.get_width()) and \
               ennemi.y <= self.y <= ennemi.y + ennemi.image.get_height()


class Ennemi():
    """Classe représentant les ennemis dans le jeu."""
    NbEnnemis = 4
    def __init__(self, type):
        """Initialise un ennemi.

        Args:
            type (dict): Dictionnaire des statistiques du type d'ennemi.
        """
        self.x = random.randint(0, 736)
        self.y = 101
        type_stats = random.choice(list(type.values()))
        self.puissance_tir = type_stats.puissance_tir
        self.vitesse_tir = type_stats.vitesse_tir
        self.nb_vie = type_stats.vie
        self.vitesse_x = type_stats.vitesse_x
        self.vitesse_y = type_stats.vitesse_y
        self.image = type_stats.image
        self.balle = type_stats.balle

    def avancer(self):
        """Déplace l'ennemi sur l'écran."""
        self.y += self.vitesse_y
        self.x += self.vitesse_x

    def disparaitre(self, type):
        """Réinitialise l'ennemi.

        Args:
            type (dict): Dictionnaire des statistiques du type d'ennemi.
        """
        self.__init__(type)

    def collisions(self):
        """Gère les collisions de l'ennemi avec les bords de l'écran."""
        if self.y >= Y_MAX or self.y <= Y_MIN:
            self.vitesse_y = -self.vitesse_y
        if self.x <= X_MIN or self.x >= X_MAX:
            self.vitesse_x = -self.vitesse_x


class Bonus():
    """Classe représentant un bonus dans le jeu."""

    def __init__(self, x, y, player):
        """Initialise un bonus.

        Args:
            x (int): Position x du bonus.
            y (int): Position y du bonus.
            player (Joueur): Le joueur qui peut recevoir le bonus.
        """
        self.x = x
        self.y = y
        self.player = player
        self.vitesse = 1.5
        self.type, type_bonus = random.choice(list(stats_bonus.items()))
        self.image = type_bonus.image
        self.duree = type_bonus.duree
        self.temps_restant = self.duree

    def effet_bonus(self):
        """Applique l'effet du bonus au joueur."""
        if self.type == 'Bonus Plus Vitesse':
            self.player.vitesse += 2
        elif self.type == 'Bonus Moins Vitesse':
            self.player.vitesse -= 1.5
        elif self.type == 'Bonus Vie':
            self.player.vie += 1
        elif self.type == 'Bonus Bouclier':
            self.player.bouclier = True

    def reset_bonus(self):
        """Réinitialise l'effet du bonus sur le joueur."""
        if self.type == 'Bonus Plus Vitesse':
            self.player.vitesse -= 2
        elif self.type == 'Bonus Moins Vitesse':
            self.player.vitesse += 1.5
        elif self.type == 'Bonus Vie':
            pass
        elif self.type == 'Bonus Bouclier':
            self.player.bouclier = False
    
    def actif(self):
        """Vérifie si le bonus est encore actif.

        Returns:
            bool: True si le bonus est actif, sinon False.
        """
        self.temps_restant -= 1
        return self.temps_restant > 0

    def deplacer(self):
        """Déplace le bonus sur l'écran."""
        self.y += self.vitesse

    def toucher(self, player):
        """Vérifie si le bonus touche le joueur.

        Args:
            player (object): Le joueur à vérifier.

        Returns:
            bool: True si le bonus touche le joueur, sinon False.
        """
        return (player.x <= self.x <= player.x + player.image.get_width() or
                player.x <= self.x + self.image.get_width() <= player.x + player.image.get_width()) and \
               player.y <= self.y <= player.y + player.image.get_height()


class Menu():
    """Classe gérant l'affichage du menu du jeu."""

    def __init__(self):
        """Initialise le menu."""
        self.nom_menu = 'home'
        self.best_score = 0
        self.background_home = IMAGES["Menu BG Home"]
        self.background_menu = IMAGES["Menu BG"]

        self.retour = IMAGES["Retour"]
        self.retour_rect = self.retour.get_rect(topleft = (20, 20))

        self.level_rect = pygame.Rect(300, 325, 200, 50)
        self.infinite_rect = pygame.Rect(300, 425, 200, 50)

        self.rebels_image = IMAGES["Rebelles"]
        self.empire_image = IMAGES["Empire"]
        self.rebels_rect = pygame.Rect(197, 250, 128, 128)
        self.empire_rect = pygame.Rect(475, 250, 128, 128)

        self.niveaux_rect = [pygame.Rect(300, 200, 200, 50), 
                             pygame.Rect(300, 270, 200, 50),
                             pygame.Rect(300, 340, 200, 50),
                             pygame.Rect(300, 410, 200, 50),
                             pygame.Rect(300, 480, 200, 50)]
        
        self.vaisseau_inf = [pygame.Rect(200, 200, 90, 90),
                             pygame.Rect(350, 200, 90, 90),
                             pygame.Rect(500, 200, 90, 90)]

        self.vaisseaux_rebelles = ["X-Wing Ennemi", "Y-Wing Ennemi", "Faucon Ennemi"]
        self.vaisseaux_empire = ["Tie-Fighter Ennemi", "Tie-Bombardier Ennemi", "Destroyer Imperial Ennemi"]
        self.choix_rebelles = ["X-Wing", "Y-Wing", "Faucon"]
        self.choix_empire = ["Tie-Fighter", "Tie-Bombardier", "Destroyer Imperial"]
        self.j = 0

    def afficher_home(self, screen):
        """Affiche le menu principal.

        Args:
            screen (pygame.Surface): Surface sur laquelle dessiner.
        """
        screen.blit(self.background_home, (0, 0))
        level_text, level_rect = MENU_FONT.render("Niveaux", BLANC)
        level_rect.center = self.level_rect.center
        screen.blit(level_text, level_rect)

        infinite_text, infinite_rect = MENU_FONT.render("Infini", BLANC)
        infinite_rect.center = self.infinite_rect.center
        screen.blit(infinite_text, infinite_rect)

    def afficher_level(self, screen):
        """Affiche le menu de sélection du mode de niveaux.

        Args:
            screen (pygame.Surface): Surface sur laquelle dessiner.
        """
        screen.blit(self.background_menu, (0, 0))
        title_text, title_rect = TITLE_FONT.render("Niveaux", BLANC)
        title_rect.center = (400, 100)
        screen.blit(title_text, title_rect)
        
        screen.blit(self.rebels_image, self.rebels_rect.topleft)
        screen.blit(self.empire_image, self.empire_rect.topleft)
        screen.blit(self.retour, self.retour_rect.topleft)

    def afficher_level_rebelle(self, screen):
        """Affiche le menu de sélection des niveaux rebelles.

        Args:
            screen (pygame.Surface): Surface sur laquelle dessiner.
        """
        screen.blit(self.background_menu, (0, 0))
        title_text, title_rect = TITLE_FONT.render("Niveaux Rebelle", BLANC)
        title_rect.center = (400, 100)
        screen.blit(title_text, title_rect)

        for i in range(5):
            level_rect = self.niveaux_rect[i]
            pygame.draw.rect(screen, JAUNE, level_rect, 5, border_radius = 10)
            level_text, level_text_rect = MENU_FONT.render(f"Niveau {i + 1}", BLANC)
            level_text_rect.center = level_rect.center
            screen.blit(level_text, level_text_rect)
        screen.blit(self.retour, self.retour_rect.topleft)

    def afficher_level_empire(self, screen):
        """Affiche le menu de sélection des niveaux empire.

        Args:
            screen (pygame.Surface): Surface sur laquelle dessiner.
        """
        screen.blit(self.background_menu, (0, 0))
        title_text, title_rect = TITLE_FONT.render("Niveaux Empire", BLANC)
        title_rect.center = (400, 100)
        screen.blit(title_text, title_rect)

        for i in range(5):
            level_rect = self.niveaux_rect[i]
            pygame.draw.rect(screen, JAUNE, level_rect, 5, border_radius = 10)
            level_text, level_text_rect = MENU_FONT.render(f"Niveau {i + 1}", BLANC)
            level_text_rect.center = level_rect.center
            screen.blit(level_text, level_text_rect)
        screen.blit(self.retour, self.retour_rect.topleft)

    def afficher_infini(self, screen):
        """Affiche le menu de mode infini.

        Args:
            screen (pygame.Surface): Surface sur laquelle dessiner.
        """
        screen.blit(self.background_menu, (0, 0))
        title_text, title_rect = MENU_FONT.render("Infini", BLANC)
        title_rect.center = (400, 50)
        screen.blit(title_text, title_rect)
        
        screen.blit(self.rebels_image, self.rebels_rect.topleft)
        screen.blit(self.empire_image, self.empire_rect.topleft)
        screen.blit(self.retour, self.retour_rect.topleft)

    def afficher_infini_rebelle(self, screen):
        """Affiche le menu de sélection du vaisseau infini rebelle.

        Args:
            screen (pygame.Surface): Surface sur laquelle dessiner.
        """
        screen.blit(self.background_menu, (0, 0))
        title_text, title_rect =MENU_FONT.render("Infini Rebelle", BLANC)
        title_rect.center = (400, 50)
        screen.blit(title_text, title_rect)
        screen.blit(self.retour, self.retour_rect.topleft)

        for i in range(3):
            level_rect = self.vaisseau_inf[i]
            pygame.draw.rect(screen, JAUNE, level_rect, 5, border_radius = 10)
            vaisseau = IMAGES[self.choix_rebelles[i]]
            vaisseau_rect = vaisseau.get_rect(center = level_rect.center)
            screen.blit(vaisseau, vaisseau_rect.topleft)

    def afficher_infini_empire(self, screen):
        """Affiche le menu de sélection du vaisseau infini empire.

        Args:
            screen (pygame.Surface): Surface sur laquelle dessiner.
        """
        screen.blit(self.background_menu, (0, 0))
        title_text, title_rect = MENU_FONT.render("Infini Empire", BLANC)
        title_rect.center = (400, 50)
        screen.blit(title_text, title_rect)
        screen.blit(self.retour, self.retour_rect.topleft)

        for i in range(3):
            level_rect = self.vaisseau_inf[i]
            pygame.draw.rect(screen, JAUNE, level_rect, 5, border_radius = 10)
            vaisseau = IMAGES[self.choix_empire[i]]
            vaisseau_rect = vaisseau.get_rect(center = level_rect.center)
            screen.blit(vaisseau, vaisseau_rect.topleft)

    def gestion_evenements_menu(self, event):
        """Gère le lien entre les menu

        Args:
            event (pygame.event.Event): L'événement à gérer.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.nom_menu == 'home':
                if self.level_rect.collidepoint(event.pos):
                    self.nom_menu = 'level'
                elif self.infinite_rect.collidepoint(event.pos):
                    self.nom_menu = 'infini'

            elif self.nom_menu == 'level':
                if self.rebels_rect.collidepoint(event.pos):
                    self.nom_menu = 'level_rebelle'
                elif self.empire_rect.collidepoint(event.pos):
                    self.nom_menu = 'level_empire'
                elif self.retour_rect.collidepoint(event.pos):
                    self.nom_menu = 'home'

            elif self.nom_menu == 'infini':
                if self.rebels_rect.collidepoint(event.pos):
                    self.nom_menu = 'infini_rebelle'
                elif self.empire_rect.collidepoint(event.pos):
                    self.nom_menu = 'infini_empire'
                elif self.retour_rect.collidepoint(event.pos):
                    self.nom_menu = 'home'
            
            elif self.nom_menu == 'level_rebelle':
                for i, niv in enumerate(self.niveaux_rect):
                    if niv.collidepoint(event.pos):
                        self.j = i
                        self.nom_menu = "lev_r"
                if self.retour_rect.collidepoint(event.pos):
                    self.nom_menu = 'level'

            elif self.nom_menu == 'level_empire':
                for i, niv in enumerate(self.niveaux_rect):
                    if niv.collidepoint(event.pos):
                        self.j = i
                        self.nom_menu = "lev_e"
                if self.retour_rect.collidepoint(event.pos):
                    self.nom_menu = 'level'

            elif self.nom_menu == 'infini_rebelle':
                for i, inf in enumerate(self.vaisseau_inf):
                    if inf.collidepoint(event.pos):
                        self.j = i
                        self.nom_menu = "inf_r"
                        
                if self.retour_rect.collidepoint(event.pos):
                    self.nom_menu = 'infini'

            elif self.nom_menu == 'infini_empire':
                for i, inf in enumerate(self.vaisseau_inf):
                    if inf.collidepoint(event.pos):
                        self.j = i
                        self.nom_menu = "inf_e"
                if self.retour_rect.collidepoint(event.pos):
                    self.nom_menu = 'infini'


class Niveau():
    """Classe représentant les niveaux du jeu."""
    def __init__(self, level):
        """Initialise un niveau.

        Args:
            level (int): Numéro du niveau.
        """
        self.level = level
        if self.level == 1:
            self.nb_vaisseaux = 12
        if self.level == 2:
            self.nb_vaisseaux = 16
        if self.level == 3:
            self.nb_vaisseaux = 24
        if self.level == 4:
            self.nb_vaisseaux = 36
        if self.level == 5:
            self.nb_vaisseaux = 52
