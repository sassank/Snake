# Add background image and music

import pygame
from pygame.locals import *
import time
import random

Taille = 40
ImageFond = (110, 110, 5)

#creation de l'objet pomme
class Pomme:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("assets/pomme.png").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,24)*Taille
        self.y = random.randint(1,19)*Taille

#création de l'objet serpent
class Serpent:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("assets/serpent.png").convert()
        self.direction = 'bas'

        self.length = 1
        self.x = [40]
        self.y = [40]
    
    # mouvements du serpent
    def move_left(self):
        self.direction = 'gauche'

    def move_right(self):
        self.direction = 'droite'

    def move_up(self):
        self.direction = 'haut'

    def move_down(self):
        self.direction = 'bas'

    def walk(self):
        # mise à jour de la longeur du serpent 
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'gauche':
            self.x[0] -= Taille
        if self.direction == 'droite':
            self.x[0] += Taille
        if self.direction == 'haut':
            self.y[0] -= Taille
        if self.direction == 'bas':
            self.y[0] += Taille

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

#mise en place du son dans le jeu
class Jeu:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Jeu du serpent")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((1050, 600))
        self.serpent = Serpent(self.surface)
        self.serpent.draw()
        self.pomme = Pomme(self.surface)
        self.pomme.draw()

    def play_background_music(self):
        pygame.mixer.music.load('assets/bg_music_1.mp3')
        pygame.mixer.music.play(-1, 0)

    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("assets/crash.mp3")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound("assets/ding.mp3")

        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.serpent = Serpent(self.surface)
        self.pomme = Pomme(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + Taille:
            if y1 >= y2 and y1 < y2 + Taille:
                return True
        return False

    def render_background(self):
        bg = pygame.image.load("assets/background.jpg")
        self.surface.blit(bg, (0,0))

    def play(self):
        self.render_background()
        self.serpent.walk()
        self.pomme.draw()
        self.display_score()
        pygame.display.flip()

        # mise en place du son lorsque le serpent mange une pomme
        if self.is_collision(self.serpent.x[0], self.serpent.y[0], self.pomme.x, self.pomme.y):
            self.play_sound("ding")
            self.serpent.increase_length()
            self.pomme.move()

        # mise en place du son lorsque le serpent se touche lui même
        for i in range(3, self.serpent.length):
            if self.is_collision(self.serpent.x[0], self.serpent.y[0], self.serpent.x[i], self.serpent.y[i]):
                self.play_sound('crash')
                raise "Collision"

    #affichage du score 
    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.serpent.length}",True,(200,200,200))
        self.surface.blit(score,(850,10))

    #Fonction fin de jeu et rejouer
    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Fin du jeu, vôtre score est de {self.serpent.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("Appuyez sur Entrer pour rejouer ou sur Echap pour quitter", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.serpent.move_left()

                        if event.key == K_RIGHT:
                            self.serpent.move_right()

                        if event.key == K_UP:
                            self.serpent.move_up()

                        if event.key == K_DOWN:
                            self.serpent.move_down()

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.25)

if __name__ == '__main__':
    game = Jeu()
    game.run()