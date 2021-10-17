import pygame as pg
import time as t

class Explosion(pg.sprite.Sprite):
    """
    Classe qui gère les explosions présentent dans le jeu
    Init :  - x,y : des entiers définissants les coordonées d'apparition 
            - time : l'heure précise où la classe est appelée
            - explosed : la classe de l'entité qui explose
            - game : la classe Game ou se déroule le jeu
            - image : image affichée qui représentent le joueur
            - sound : le son qui va être joué en même temps que l'explosion

    Pour chaque fonction de cette classe :
        In : self = la classe actuelle de l'explosion elle-même
    """
    def __init__(self,x,y,time,explosed,game,image,sound='explosion'):
        super().__init__()
        if image == None :
            self.image = pg.transform.scale(pg.image.load('SpaceInvader/images/explosion.png'),(150,150))
        else :
            self.image = image # type spécifique à pygame / Image représentant l'explosion
        self.rect = self.image.get_rect() # type spécifique à pygame / Rectangle définissant l'explosion
        self.rect.x = x # float / Coordonées horizontales de l'explosion
        self.rect.y = y # float / Coordonées verticales de l'explosion
        self.time = time # float / Heure précise où la classe est appelée
        self.explosed = explosed # class / Classe de l'entité qui exploses
        self.sound = sound # str / Nom du son à jouer, par défaut le son 'explosion'
        self.game = game # class / Classe de la partie actuelle où se trouve les explosions

        self.game.sounds.play(self.sound)
    
    def delay(self):
        """
        Patiente avant de retirer l'explosion
        In : self
            Utilisé : self.explosed, self.game, self.sound, self.time
        Out : rien
            Appels : class Game : victory() si le c'est le boss qui explose, game_over() si c'est le joueur qui explose
        """
        if self.explosed.name == 'player' :
            if t.time() > self.time + 1 :
                self.game.explosions.remove(self)
                self.game.game_over()
        elif self.sound == 'bossexplo':
            if t.time() > self.time + 2 :
                self.game.explosions.remove(self)
                self.game.victory()
        elif t.time() > self.time + 0.5 :
            self.game.explosions.remove(self)
            