import pygame
import random
pygame.init()


class hangman():
    def __init__(self,word):
        self.good_guesses  = [];
        self.wrong_guesses = [];
        self.word_to_guess = word
    def make_guess(self,guess):
        if(guess in self.word_to_guess):
            print('good')
            self.good_guesses += guess
        else:
            print('bad')
            self.wrong_guesses += guess
    def draw(self):
        pass
    def get_progress(self):
        return self.word_to_guess
        
screen = pygame.display.set_mode((500, 500))
h = hangman('baguette')
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
    guess = str(input('guess'))[0]
    h.make_guess(guess)
    h.draw()
    pygame.display.update()
pygame.quit()
