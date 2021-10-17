import pygame as pg
from player import Player
from ennemy import Ennemy
from boss import Boss
from explosion import Explosion
from asteroid import Asteroid
from sounds import Sounds
import time as t
from random import randint

class Game():
    """
    Classe qui gère la partie actuelle du jeu
    Init : - screen : l'écran où la partie se déroule

    Pour chaque fonction de cette classe :
        In : self = la classe actuelle
    """
    def __init__(self,screen):
        self.playing = False # bool / True : En partie / False : Menu ou game over ou vicory
        self.over = False # bool / True : game over
        self.win = False # bool / True : victory
        self.player = Player(screen, pg.transform.scale(pg.image.load('SpaceInvader/images/player.png'),(130,110)), 1, self) # class / Class du joueur jouant la partie
        self.pressed = {} # dictionnaire associant toutes les touches pressées à un booléen True : préssée / False : relachée
        self.screen = screen # type spécifique à pygame / l'écran où la partie se déroule
        self.sounds = Sounds() # class / Classe qui gère l'audio du jeu
        self.bossstage = False # bool / True : Le joueur est en train de se battre contre le boss
        self.bossdead = False # bool / True : le boss est mort / False : le boss est vivant où non présent
        self.boss = None # class (définie dans spawn_boss()) / Classe qui gère le boss
        self.ennemies = pg.sprite.Group() # type spécifique à pygame / Liste des ennemies présents dans la partie
        self.explosions = pg.sprite.Group() # type spécifique à pygame / Liste des explosions présentes dans la partie
        self.asteroids = pg.sprite.Group() # type spécifique à pygame / Liste des astéroïdes présents dans la partie
        self.overtime = 0 # float / Heure précise où la partie se termine
        self.score = 0 # int / Score de la partie
        self.font = pg.font.Font('SpaceInvader/fonts/Gameplay.ttf',24) # type spécifique à pygame / Police d'écriture utilisée dans le jeu
    
    def tick(self,screen):
        """
        Fonction principale éxécutée à chaque tick 
        In : self, screen = l'écran où la partie se déroule
            Utilisé : self.player, self.font, self.score, self.bossstage, self.boss, self.ennemies, self.player, self.explosions, self.asteroids
        Out : rien
            Appels : - classe actuelle : check_player_collision(), spawn_asteroid()
                     - class Boss : move(), check_collision(), health_bar()
                     - class Ennemy : move(), check_collision()
                     - class Projectile : delay(), move_up()
                     - class Explosion : delay()
                     - class Asteroid : rotate(), move(), check_collision()
        """
        screen.blit(self.player.img,(self.player.rect))
        scoretxt = self.font.render(str(self.score),1,(255,255,255))
        screen.blit(scoretxt,(30,40))

        # phase de boss
        if self.bossstage :
            # gestion du boss
            screen.blit(self.boss.image, self.boss.rect)
            self.boss.move()
            for projectile in self.boss.projectiles :
                projectile.delay()
            self.boss.projectiles.draw(screen)
            self.boss.check_collision()
            self.boss.health_bar()
        # phase d'une vague
        else :
            # gestion des ennemies
            for ennemy in self.ennemies :
                ennemy.move()
                ennemy.check_collision()
            self.ennemies.draw(screen)
        
        # vérifie si le joueur entre en collision avec une entité sauf si le boss a été tué 
        if not self.bossdead : # évite un game over après avoir tué le boss
            self.check_player_collision()

        # getsion des projectiles
        for projectile in self.player.projectiles :
            projectile.move_up()
        self.player.projectiles.draw(screen)

        #gestion des explosion
        for explosion in self.explosions :
            explosion.delay()
        self.explosions.draw(screen)

        # 1 chance sur 100 de faire apparaître un astéroïde
        if randint(1,100) == 1 :
            self.spawn_asteroid()
        # gestion des astéroïdes
        for asteroid in self.asteroids :
            asteroid.rotate()
            asteroid.move()
            asteroid.check_collision()
        self.asteroids.draw(screen)

    def devtools(self):
        """
        Facilite les tests lors du développement / Désactivée pour le vrai jeu
        """
        ## DEV TOOLS
        # c -> Passe direct au boss
        if self.pressed.get(pg.K_c) :
            for ennemy in self.ennemies :
                self.ennemies.remove(ennemy)
                self.clear()
        # x -> Met le boss a 1pv 
        elif self.pressed.get(pg.K_x):
            if self.bossstage :
                self.boss.pv = 1
        
        # a -> Fait apparaître un astéroïde
        elif self.pressed.get(pg.K_a) :
            self.spawn_asteroid()
    
    def axis_input(self):
        """
        Gère les touches que l'on garde appuyées / Déplacement avec zqsd ou avec les flèches
        In : self
            Utilisé : self.pressed
        Out : rien
            Appels : class Player : move_right(), move_left(), move_up(), move_down()
        """
        if (self.pressed.get(pg.K_d) or self.pressed.get(pg.K_RIGHT))and self.player.rect.x < self.screen.get_width() - self.player.rect.width :
            self.player.move_right()
        if (self.pressed.get(pg.K_q) or self.pressed.get(pg.K_LEFT)) and self.player.rect.x > 0 :
            self.player.move_left()
        if (self.pressed.get(pg.K_z) or self.pressed.get(pg.K_UP)) and self.player.rect.y > 0 :
            self.player.move_up()
        if (self.pressed.get(pg.K_s) or self.pressed.get(pg.K_DOWN)) and self.player.rect.y < self.screen.get_height() - self.player.rect.height :
            self.player.move_down()
        #self.devtools()

    def spawn_ennemy(self,x,y,dir):
        """
        Fait apparaître un ennemy / Crée une nouvelle classe Ennemy()
        In : self, x,y = coordonées d'apparition, dir = direction initiale empruntée (str, 'left' ou 'right')
            Utilisé : self.screen, self.player, self.ennemies
        Out : rien
            Appels : nouvelle classe Ennemy()
        """
        image = pg.transform.scale(pg.image.load('SpaceInvader/images/ennemy.png'), (200, 200))
        self.ennemies.add(Ennemy(self.screen,x,y,dir,image,self,self.player))

    def spawn_boss(self):
        """
        Fait apparaître le boss / Crée une nouvelle classe Boss()
        In : self
            Utilisé : self.boss, self.bossstage, self.screen, self.player
        Out : rien
            Appels : nouvelle classe Boss()
        """
        image = pg.transform.scale(pg.image.load('SpaceInvader/images/boss.png'), (400, 200))
        self.boss = Boss(self.screen,randint(-200,1080), 50, image, self, self.player)
        self.bossstage = True
    
    def spawn_asteroid(self):
        """
        Fait apparaître un astéroïde / Crée une nouvelle class Asteroid()
        In : self
            Utilisé : self.asteroids, self.sounds
        Out : rien
            Appels : class Sounds : play()
        """
        self.asteroids.add(Asteroid(self))
        self.sounds.play('asteroid')

    def clear(self):
        """
        Fait apparaître le boss si il n'y a plus d'ennemies
        In : self
            Utilisé : self.ennemies
        Out : rien
            Appels : spawn_boss()
        """
        if len(self.ennemies) == 0 :
            self.spawn_boss()
    
    def check_player_hit(self):
        """
        Vérifie si le joueur se fait toucher par un tir du boss
        In : self
            Utilisé : self.boss, self.player
        Out :
            Appels : class Player : hit()
        """
        for projectile in self.boss.projectiles :
            if projectile.rect.x < self.player.rect.x + 100 and projectile.rect.x > self.player.rect.x - 100 :
                self.player.hit()
    
    def check_player_collision(self):
        """
        Vérifie si le joueur entre en collision avec un autre entité (boss, ennemy, astéroïde)
        In :self
            Utilisé : self.bossstage, self.boss, self.player, self.ennemies, self.asteroids
        Out : rien
            Appels : class Player : hit()
        """
        if self.bossstage :
            if self.boss.rect.y + 200 > self.player.rect.y + 50 :
                if self.boss.rect.x < self.player.rect.x + 100 and self.boss.rect.x > self.player.rect.x - 350 :
                    self.player.hit()
        else :
            for ennemy in self.ennemies :
                if ennemy.rect.y < self.player.rect.y + 70 and ennemy.rect.y > self.player.rect.y - 160 :
                    if ennemy.rect.x < self.player.rect.x + 90 and ennemy.rect.x > self.player.rect.x - 160 :
                        self.ennemies.remove(ennemy)
                        self.player.hit()

        # Test de la fonction collide_rect() pour la collision joueur <-> astéroïde mais la vérification de coordonées est plus efficace
        for asteroid in self.asteroids :
            if pg.sprite.collide_rect(self.player,asteroid) :
                self.player.hit()

    def victory(self):
        """
        Annonce la victoire et termine la partie
        In : self
            Utilisé : self.sounds, self.overtime, self.win
        Out : rien
            Appels : class Sounds : play()
        """
        pg.mixer.music.stop()
        self.sounds.play('win')
        self.overtime = t.time()
        self.win = True

    def game_over(self):
        """
        Annonce le gameover et termine la partie
        In : self
            Utilisé : self.sounds, self.overtime, self.over, self.playing
        Out : rien
            Appels : class Sounds : stopall(), play()
        """
        pg.mixer.music.stop()
        self.sounds.stopall()
        self.sounds.play('gameover')
        self.overtime = t.time()
        self.playing = False
        self.over = True
    
    def add_explosion(self,x,y,explosed,image=None,sound='explosion'):
        """
        Ajoute une explosion / Créé une nouvelle classe Explosion()
        In : self, x,y = x,y = coordonées d'apparition, explosed = classe de l'entité qui explose, image = image représentant l'explosion, sound = son joué lors de l'explosion
            Utilisé : self.explosions
        Out : rien
            Appels : nouvelle classe Explosion()
        """
        time = t.time()
        self.explosions.add(Explosion(x,y,time,explosed,self,image,sound))