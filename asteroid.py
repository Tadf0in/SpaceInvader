import pygame as pg
from random import randint
import time as t

class Asteroid(pg.sprite.Sprite):
    """
    Classe qui gère un astéroïde présent dans les jeu
    Init :  - game : la classe Game ou se déroule le jeu

    Pour chaque fonction de cette classe :
        In : self = la classe actuelle de l'astéroïde lui-même
    """
    def __init__(self,game):
        super().__init__()
        self.img = pg.image.load('SpaceInvader/images/asteroide.png') # type spécifique à pygame / Image initiale de l'astéroïde
        self.image = pg.transform.scale(self.img,(randint(100,200),randint(100,200))) # type spécifique à pygame / Image variable de l'astéroïde
        self.rect = self.image.get_rect() # type spécifique à pygame / Rectangle définissant l'astéroïde
        
        self.rect.y = randint(-200,400) # float / Coordonées verticales de l'astéroïde
        if self.rect.y < 0 :
            self.rect.x = randint(-20,1300) # float / Coordonées horizontales de l'astéroïde
            self.spd = 10 # int / Vitesse de l'astéroïde
        elif randint(1,2) == 1 :
            self.rect.x = -200 # float / Coordonées horizontales de l'astéroïde
            self.spd = 10 # int / Vitesse de l'astéroïde
        else :
            self.rect.x = 1280 # float / Coordonées horizontales de l'astéroïde
            self.spd = -10 # int / Vitesse de l'astéroïde
        
        self.game = game # class / Classe de la partie actuelle où se trouve les astéroïdes
        self.game.score += 20
        self.time = t.time() # float / Heure précise où la classe est appelée
        self.angle = 0 # int / Angle d'orientation initial de l'image (self.image)
        self.rotation = randint(1,2) # int al"atoire entre 1 ou 2 / Vitesse de rotation de l'astéroïde
        
    def remove(self):
        """
        Retire l'astéroïde de la listes contenants tous les astéroïdes tirés donc le supprime
        In : self
            Utilisé : self.game
        Out : rien
        """
        self.game.asteroids.remove(self)
        
    def rotate(self):
        """
        Tourne l'astéroïde dans le sens horaire de la valeur de sa vitesse de rotation
        In : self
            Utilisé : self.rotation, self.angle, self.image
        Out : rien
        """
        self.angle += self.rotation
        self.image = pg.transform.rotozoom(self.img,self.angle,1)
    
    def move(self):
        """
        Déplace l'astéroïde
        In : self
            Utilisé : self.spd, self. rect, self.rotation
        Out : rien
            Appels : remove()
        """
        self.rect.x += self.spd
        self.rect.y += self.rotation * 0.5
        if self.rect.y > 720 or self.rect.x > 1281 or self.rect.x < -201:
            self.remove()
    
    def check_collision(self):
        """
        Vérifie si un projectile du joueur touche l'astéroïde, si c'est le cas alors supprime ce projectile
        In : self
            Utilisé : self.game, self.rect
        Out : rien
            Appels : class Projectile : remove()
        """
        for projectile in self.game.player.projectiles :
            if projectile.rect.y < self.rect.y + 200 and projectile.rect.y > self.rect.y :
                if projectile.rect.x < self.rect.x + self.rect.width and projectile.rect.x + 80 > self.rect.x :
                    projectile.remove()
    