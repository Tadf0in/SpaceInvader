import pygame as pg

class Ennemy(pg.sprite.Sprite):
    """
    Classe qui gère un ennemy dans le jeu
    Init :  - screen : l'écran sur lequel afficher
            - x,y : des entiers définissants les coordonées d'apparition 
            - image : image affichée qui représentent l'ennemy
            - game : la classe Game ou se déroule le jeu
            - player : la classe Player qui affronte l'ennemy
    
    Pour chaque fonction de cette classe :
        In : self = la classe actuelle de l'ennemy lui-même
    """
    def __init__(self,screen,x,y,direction,image,game,player):
        super().__init__()
        self.maxpv = 1 # int / Maximum des points de vie atteignables par l'ennmy
        self.pv = self.maxpv # int / Points de vie variables de l'ennemy
        self.atk = 1 # int / Attaque de l'ennemy
        self.spd = 2 # int / Vitesse de l'ennemy
        self.projectiles = pg.sprite.Group() # type spécifique à pygame / Listes des projectiles envoyés par l'ennemy
        self.image = image # type spécifique à pygame / Image représentant l'ennemy
        self.rect = self.image.get_rect() # type spécifique à pygame / Rectangle définissant l'ennemy
        self.rect.x = x # float / Coordonées horizontales de l'ennemy
        self.rect.y = y # float / Coordonées verticales de l'ennemy
        self.direction = direction # str 'left' ou 'right' / Direction
        self.screen = screen # type spécifique à pygame / Ecran où est affiché les ennemies
        self.game = game # class / Classe de la partie actuelle où se trouvent les ennemies
        self.player = player # class / Classe du joueur affrontant les ennemies
        self.name = 'ennemy' # str / Nom de l'entité

    def remove(self):
        """
        Fait exploser l'ennemy
        In : self
            Utilisé : self.game
        Out : rien
            Appels : class Game : add_explosion(), clear()
        """
        self.game.add_explosion(self.rect.x+25,self.rect.y+25,self)
        self.game.ennemies.remove(self)
        self.game.clear()
        self.game.score += 25
    
    def move_down(self):
        """
        Descend l'ennemy d'un cran vers le bas
        In : self
            Utilisé : self.rect, self.direction
        Out : rien
        """
        self.rect.y += self.spd * 70
        if self.direction == 'left' :
            self.direction = 'right'
        elif self.direction == 'right' :
            self.direction = 'left'

    def move_right(self):
        """
        Déplace l'ennemy vers la droite ou vers le bas
        In : self
            Utilisé : self.rect, self.spd, self.screen
        Out : rien
            Appels : move_down()
        """
        if self.rect.x >= self.screen.get_width() - 200 :
            self.move_down()
        else :
            self.rect.x += self.spd

    def move_left(self):
        """
        Déplace l'ennemy vers la gauche ou vers le bas
        In : self
            Utilisé : self.rect, self.spd
        Out : rien
            Appels : move_down()
        """
        if self.rect.x <= 0 :
            self.move_down()
        else :
            self.rect.x -= self.spd

    def move(self):
        """
        Gère tous les déplacements de l'ennemy
        In : self
            Utilisé : self.direction
        Out : rien
            Appels : move_right(), move_left()
        """
        if self.direction == 'right' :
            self.move_right()
        elif self.direction == 'left' :
            self.move_left()

    def check_collision(self):
        """
        Vérifie si l'ennemy est touché par un projectile
        In : self
            Utilisé : self.rect, self.player, self.game
        Out : rien
            Appels : remove() / class Game : game_over() / class Projectile : remove()
        """
        for projectile in self.player.projectiles :
            if projectile.rect.y < self.rect.y + 200 and projectile.rect.y > self.rect.y :
                if projectile.rect.x < self.rect.x + 200 and projectile.rect.x > self.rect.x - 95 :
                    projectile.remove()
                    self.remove()
        if self.rect.y > 500 :
            self.remove()
            self.game.game_over()

