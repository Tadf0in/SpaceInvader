import pygame as pg
from projectile import Projectile

class Player(pg.sprite.Sprite):
    """
    Classe qui gère le joueur et ses interactions
    Init :  - screen : l'écran sur lequel afficher
            - image : image affichée qui représentent le joueur
            - pv : les points de vie initiaux du joueur (int)
            - game : la classe Game ou se déroule le jeu

    Pour chaque fonction de cette classe :
        In : self = la classe actuelle du joueur lui-même
    """
    def __init__(self,screen,image,pv,game):
        super().__init__()
        self.maxpv = pv # int / Points de vie maximaux du joueur
        self.pv = self.maxpv # int / Points de vie variables du joueur
        self.spd = 5 # int / Vitesse du joueur
        self.projectiles = pg.sprite.Group() # type spécifique à pygame / Listes des projectiles tirés par le boss
        self.img = image # type spécifique à pygame / Image représentant le joueur
        self.canfire = True # bool / True si le joueur peut tirer un projectile False sinon
        self.rect = self.img.get_rect() # type spécifique à pygame / Rectangle définissant le joueur
        self.rect.x = int(screen.get_width()/2) - int(screen.get_width()/5/2) # int / Coordonées horizontales du joueur
        self.rect.y = screen.get_height() - int(screen.get_width()/10) # int / Coordonées verticales du joueur
        self.game = game # class / Classe de la partie actuelle où se trouvent le boss
        self.name = 'player' # str / Nom de l'entité

    def move_right(self):
        """
        Déplace le joueur vers la droite
        In : self
            Utilisé : self.rect, self.spd
        Out : rien
        """
        self.rect.x += self.spd

    def move_left(self):
        """
        Déplace le joueur vers la gauche
        In : self
            Utilisé : self.rect, self.spd
        Out : rien
        """
        self.rect.x -= self.spd

    def move_up(self):
        """
        Déplace le joueur vers le haut
        In : self
            Utilisé : self.rect, self.spd
        Out : rien
        """
        self.rect.y -= self.spd

    def move_down(self):
        """
        Déplace le joueur vers le bas
        In : self
            Utilisé : self.rect, self.spd
        Out : rien
        """
        self.rect.y += self.spd

    def fire(self):
        """
        Fait apparaître un rojectile tiré par le joueur
        In : self
            Utilisé : self.canfire, self.projectiles, self.game
        Out : rien
            Appels classe Projectile() / class Sounds (depuis class Game) : play()
        """
        if self.canfire :
            image = pg.transform.scale(pg.image.load('SpaceInvader/images/projectile.png'),(125,50))
            projectile = Projectile(self.rect.x,self.rect.y, image, self, 30)
            self.projectiles.add(projectile)
            self.game.sounds.play('shot')
            self.game.score += 1

    def hit(self):
        """
        Explose le joueur
        In : self
            Utilisé : self.pv, self.img, self.game, self.spd, self.canfire
        Out : rien
            Appels : class Game : add_explosion()
        """
        self.pv -= 1
        if self.pv <= 0 :
            self.img = pg.transform.scale(pg.image.load('SpaceInvader/images/explosion.png'),(150,150))
            self.game.add_explosion(self.rect.x,self.rect.y,self)
            self.spd = 0
            self.canfire = False