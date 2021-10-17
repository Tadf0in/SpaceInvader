import pygame as pg
from ennemy import Ennemy
from projectile import Projectile
from random import randint

class Boss(Ennemy):
    """
    Classe qui gère le Boss du jeu
    Init :  - screen : l'écran sur lequel afficher
            - x,y : des entiers définissants les coordonées d'apparition 
            - image : image affichée qui représentent le boss
            - game : la classe Game ou se déroule le jeu
            - player : la classe Player qui affronte le boss
    
    Pour chaque fonction de cette classe :
        In : self = la classe actuelle du boss lui-même
    """
    def __init__(self,screen,x,y,image,game,player):
        super().__init__(screen,x,y,'right',image,game,player) # Hérite de la classe Ennemy()
        self.maxspd = 5 # int / Vitesse maximale et initiale du boss
        self.spd = self.maxspd # int / Vitesse variable du boss
        self.direction = 'right' # str / Direction empruntée par le boss
        self.maxpv = 24 # int / Points de vie maximaux du boss
        self.pv = self.maxpv # int / Points de vie variables du boss
        self.projectiles = pg.sprite.Group() # type spécifique à pygame / Listes des projectiles tirés par le boss
        self.game = game # class / Classe de la partie actuelle où se trouvent le boss
        self.player = player # class / Classe du joueur affrontant le boss

    def fire(self):
        """
        Le boss fait apparaitre un laser pour attaquer
        In : self
            Utilisé : self.spd, self.projectiles, self.game, self.direction
        Out : rien
            Appels : classe Projectile()
        """
        self.spd = 0
        image = pg.transform.rotate(pg.transform.scale(pg.image.load('SpaceInvader/images/bossprojectile.png'), (500, 160)),90)
        projectile = Projectile(self.rect.x + 120, self.rect.y + 200, image, self, 0)
        self.projectiles.add(projectile)
        self.game.sounds.play('bossshot')
        self.game.score += 50
        dir = randint(1,2)
        if dir == 1 :
            self.direction = 'right'
        else :
            self.direction = 'left'

    def health_bar(self):
        """
        Gère la jauge de vie du boss
        In : self
            Utilisé : self.screen
        Out : rien
        """
        color = (255,0,0)
        back_color = (200,200,200)
        pos = [40, 10, self.pv*50, 20]
        back_pos = [38, 8, self.maxpv*50+4, 24]
        pg.draw.rect(self.screen, back_color, back_pos)
        pg.draw.rect(self.screen, color, pos)

    def move_right(self):
        """
        Déplace le boss vers la droite
        In : self
            Utilisé : self.rect, self.screen, self.direction
        Out : rien
        """
        if self.rect.x >= self.screen.get_width() - 200 :
            self.direction = 'left'
        else :
            self.rect.x += self.spd

    def move_left(self):
        """
        Déplace le boss vers la gauche
        In : self
            Utilisé : self.rect, self.direction
        Out : rien
        """
        if self.rect.x <= -200 :
            self.direction = 'right'
        else :
            self.rect.x -= self.spd

    def move(self):
        """
        Gère les déplacements et arrêts du boss
        In : self
            Utilisé : self.direction
        Out : rien
            Appels : fire(), move_right(), move_left()
        """
        if randint(1,100) == 1 :
            self.fire()
        else :
            if self.direction == 'right' :
                self.move_right()
            elif self.direction == 'left' :
                self.move_left()
    
    def hit(self, amount):
        """
        Prend des dégats et perd des points de vie, explose si ses pv tombent à 0
        In : self / amount : montant des pv perdus (int)
            Utilisé : self.pv, self.game 
        Out : rien
            Appels : class Game : add_explosion()
        """
        self.pv -= amount
        self.game.score += 12
        if self.pv <= 0 :
            self.game.bossdead = True
            self.game.bossstage = False
            self.game.score += 500
            self.game.add_explosion(self.rect.x-50,self.rect.y-50,self,pg.transform.scale(pg.image.load('SpaceInvader/images/explosion.png'),(500,300)),'bossexplo')

    def check_collision(self):
        """
        Vérifie si le boss se fait toucher par un projectile
        In : self
            Utilisé : self.player, self.game, self.rect
        Out : rien
            Appels : hit() / class Sounds (depuis class Game) : play() / class Projectile : remove()
        """
        for projectile in self.player.projectiles :
            if projectile.rect.y <= self.rect.y + 200 :
                if projectile.rect.x < self.rect.x + 400 and projectile.rect.x > self.rect.x -95 :
                    self.game.sounds.play('hit')
                    projectile.remove()
                    self.hit(projectile.get_atk())
    