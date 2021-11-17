import pygame
import random
pygame.init()


class hangman():
    def __init__(self,word):
        self.good_guesses  = 0;
        self.wrong_guesses = 0;
        self.word_to_guess = word
    def make_guess(self,guess):
        if(guess in word):
            self.good_guesses += 1
        else:
            self.wrong_guesses += 1
    def draw():
            pass
    
screen = pygame.display.set_mode((500, 500))
h = hangman()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
    h.draw()
    pygame.display.update()
pygame.quit()
