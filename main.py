import pygame as pg
from game import Game
import time as t

pg.init() # Initialise le module pygame

# Règlales relatifs à la fenêtre
pg.display.set_caption("Space Invader")
icone = pg.image.load('SpaceInvader/images/icone.png')
pg.display.set_icon(icone)
screen = pg.display.set_mode((1280,720))

def start():
    """
    Crée une nouvelle classe Game pour commencer une nouvelle partie
    In : rien
    Out : La classe Game
    """
    pg.mixer.music.stop()
    game = Game(screen)
    game.sounds.playmusic('music')
    game.sounds.play('start')
    game.playing = True
    game.over = False
    
    for i in range(5):
        game.spawn_ennemy(20+i*200,10,'right')
    for i in range(5):
        game.spawn_ennemy(250+i*200,150,'left')
    return game

# Lancement du jeu
game = Game(screen)
game.playing = False
game.sounds.playmusic('menu')

font = pg.font.Font('SpaceInvader/fonts/Gameplay.ttf',24) # Police d'écriture utilisée

# Textes affichés dans le menu
fscore = open('SpaceInvader/bestscore.txt','r')
bestscore = int(fscore.read())
fscore.close()
print(bestscore)
bestscoretxt = font.render(f"Best : {bestscore}",1,(255,255,255))
lastscore = 0
lastscoretxt = font.render(f"Last : {lastscore}",1,(255,255,255))
touchetxt = font.render("Appuyez sur une touche pour commencer...",1,(255,255,255))


# Boucle principale, continue jusqu'à ce que l'utilisateur ferme la fenêtre ou appuie sur Echap
running = True
passage = 0
while running :
    # Affichage de l'arrière plan
    screen.blit(pg.transform.scale(pg.image.load('SpaceInvader/images/bg.png'),(screen.get_width(),screen.get_height())),(0,0))
    
    ## Gère l'affichage à l'écran (En jeu, menu principal, victoire ou game over)
    # En jeu
    if game.playing and not game.over :
        game.tick(screen)
    # Menu principal
    elif not game.playing and not game.over and not game.win :
        screen.blit(pg.image.load('SpaceInvader/images/title.png'),(280,-50))
        screen.blit(bestscoretxt,(30,20))
        screen.blit(lastscoretxt,(30,60))
        if int(str(int(t.time()))[9]) % 2 == 0:
            screen.blit(touchetxt,(325,500))
    # Victoire
    if game.win :
        screen.blit(pg.image.load('SpaceInvader/images/victory.png'),(300,0))
        if game.overtime + 2 < t.time() :
            game.win = False
            game.sounds.playmusic('menu')
            game.playing = False
            game.over = False
    # Game over
    elif game.over :
        screen.blit(pg.image.load('SpaceInvader/images/gameover.png'),(280,0))
        if game.overtime + 2 < t.time() :
            game.over = False
            game.sounds.playmusic('menu')
            game.win = False
    # Gère les best score et le last score affichés dans le menu
    if not game.playing :
        if game.score > bestscore : 
                bestscore = game.score
                fscore = open('SpaceInvader/bestscore.txt','w')
                fscore.write(str(bestscore))
                fscore.close()
                fscore = open('SpaceInvader/bestscore.txt','r')
                bestscore = int(fscore.read())
                fscore.close()
                bestscoretxt = font.render(f"Best : {bestscore}",1,(255,255,255))
        lastscore = game.score
        lastscoretxt = font.render(f"Last : {lastscore}",1,(255,255,255))
        
    # Regarde si une touche assignée au déplacement est appuyé, si oui : déclenche la fonction du mouvement correspondant
    game.axis_input()

    pg.display.update() # Actualise la fenêtre

    ## action input
    for event in pg.event.get():
        # Si la fenêtre est fermée ou si l'utilisateur appuie sur échappe alors arrête le jeu et termine la boucle principale
        if event.type == pg.QUIT or game.pressed.get(pg.K_ESCAPE) :
            pg.quit()
            running = False
            break

        # Enregistre toutes les touches appuyées dans un dictionnaire en les associant à True si elle restent appuyées
        elif event.type == pg.KEYDOWN :
            if not game.playing and not game.over and not game.win :
                game = start() # Si aucune touche n'a encore été appuyée alors lance la partie
            game.pressed[event.key] = True

            # Si c'est la touche espace qui est appuyée alors tire un projectile
            if event.key == pg.K_SPACE :
                game.player.fire()

        # Dès qu'une touche est relachée, elle est associée à False dans le dictionnaire des touches utilisées
        elif event.type == pg.KEYUP :
            game.pressed[event.key] = False
        
        passage += 1