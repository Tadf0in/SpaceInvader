from pygame import mixer

class Sounds :
    """
    Classe qui gère l'audio du jeu
    Init : rien
    
    Pour chaque fonction de cette classe :
        In : self = la classe actuelle
    """
    def __init__(self):
        self.sounds = { # Dictionnaire associant un mot clé à un son
            'gameover': mixer.Sound('SpaceInvader/sounds/gameover.wav'),
            'explosion': mixer.Sound('SpaceInvader/sounds/explosion.wav'),
            'bossexplo': mixer.Sound('SpaceInvader/sounds/bossexplo.wav'),
            'shot': mixer.Sound('SpaceInvader/sounds/shot.wav'),
            'start': mixer.Sound('SpaceInvader/sounds/start.wav'),
            'hit': mixer.Sound('SpaceInvader/sounds/hit.wav'),
            'win': mixer.Sound('SpaceInvader/sounds/win.wav'),
            'asteroid': mixer.Sound('SpaceInvader/sounds/asteroid.wav'),
            'bossshot': mixer.Sound('SpaceInvader/sounds/bossshot.mp3'),
        }

        self.musics = { # Dictionnaire associant un mot clé à une musique
            'music': 'SpaceInvader/sounds/music.mp3',
            'menu': 'SpaceInvader/sounds/menu.mp3'
        }

        #sounds = ['gameover','eplosion','bossexplo','shot','start','hit','win']
        #for sound in sounds :
        #    self.add_sound(sound)
    
    def add_sound(self,sound):
        self.sounds[sound] = mixer.Sound(f'sounds/{sound}.wav')
    
    def play(self, sound):
        """
        Joue un son
        In : self, sound = le nom du son à jouer (str, par défaut : 'music') 
            Utilisé : self.sounds
        Out : rien
        """
        self.sounds[sound].play()
    
    def stop(self, sound):
        """
        Arrete de jouer un son
        In : self, sound = le nom du son à arrêter (str)
            Utilisé : self.sounds
        Out : rien
        """
        self.sounds[sound].stop()
    
    def playmusic(self,music='music'):
        """
        Joue de la musique
        In : self, music = le nom de la musique à jouer (str)
            Utilisé : self.musics
        Out : rien
        """
        mixer.music.load(self.musics[music])
        mixer.music.play(-1)
    
    def stopall(self):
        """
        Coupe tous les sons
        In : self
            Utilisé : self.sounds
        Out : rien
            Appels : stop()
        """
        mixer.music.stop()
        for sound in self.sounds :
            self.stop(sound)
