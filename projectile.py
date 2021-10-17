import pygame as pg
import time as t

class Projectile(pg.sprite.Sprite):
    """
    Classe qui gère tous les porjectiles tirés dans le jeu
    Init :  - x,y : des entiers définissants les coordonées d'apparition
            - image : image affichée qui représentent le joueur
            - shooter : la classe de l'entité qui a tiré ce projectile
            - spd : la vitesse du projectile (int)

    Pour chaque fonction de cette classe :
        In : self = la classe actuelle du projectile lui-même
    """
    def __init__(self,x,y,image,shooter,spd):
        super().__init__()
        self.spd = spd # int / Vitesse du projectile
        self.image = image # type spécifique à pygame / Image représentant le projectile
        self.atk = 1 # int / Montant des dégats du projectile
        self.rect = self.image.get_rect() # type spécifique à pygame / Rectangle définissant le projectile
        self.rect.x = x # float / Coordonées horizontales du projectile
        self.rect.y = y # float / Coordonées verticales du projectile
        self.shooter = shooter # class / Classe de l'entité qui a tiré le projectile
        self.time = t.time() # float / Heure précise où le projectile a été tiré

    def remove(self):
        """
        Retire le projectile de la listes contenants tous les projectiles tirés donc supprime ce projectile
        In : self
            Utilisé : self.shooter
        Out : rien
        """
        self.shooter.projectiles.remove(self)

    def move_up(self):
        """
        Déplace le projectile vers le haut
        In : self
            Utilisé : self.rect, self.spd
        Out : rien
            Appels : remove()
        """
        self.rect.y -= self.spd
        if self.rect.y < 0 :
            self.remove()

    def delay(self):
        """
        Patiente avant de supprimer le projectile
        In : self
            Utilisé : self.shooter, self.time
        Out : rien
            Appels : remove() / class Game (depuis class du shooter) : check_player_hit()
        """
        self.shooter.game.check_player_hit()
        if t.time() > self.time + 0.5 :
            self.remove()
            self.shooter.spd = self.shooter.maxspd

    def get_atk(self):
        """
        Retourne la valeur de l'attaque du projectile
        In : self
            Utilisé : self.atk
        Out : self.atk
        """
        return self.atk