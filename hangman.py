import pygame
import random

WIDTH = 500
HEIGHT = 500

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

lines = [
        #start of vertical beam, the "pole"
        ((WIDTH / 3,HEIGHT / 6),
        ((WIDTH / 3)+10,HEIGHT / 6),
        ((WIDTH / 3)+10,(HEIGHT / 6)*5),
        (WIDTH / 3,(HEIGHT / 6)*5)), 
        
        #start of horizontal beam
        (((WIDTH / 3)+10,HEIGHT / 6),
        ((WIDTH / 3)*2,HEIGHT / 6),
        ((WIDTH / 3)*2,(HEIGHT / 6)+10),
        ((WIDTH / 3)+10,(HEIGHT / 6)+10)),
            
            ((20,20),(20,30),(30,30),(30,20)),
            
            ((20,20),(20,30),(30,30),(30,20)),
            
            ((20,20),(20,30),(30,30),(30,20)),
            
            ((20,20),(20,30),(30,30),(30,20)),
            
            ((20,20),(20,30),(30,30),(30,20)),
            
            ((20,20),(20,30),(30,30),(30,20))]

class hangman():
    def __init__(self,word):
        self.good_guesses  = [];
        self.wrong_guesses = [];
        self.word_to_guess = word
    def make_guess(self,guess):
        if(guess in self.word_to_guess):
            self.good_guesses += guess
        else:
            self.wrong_guesses += guess
    def draw(self):
        for p in lines[0:len(self.wrong_guesses)]:
            pygame.draw.polygon(screen, (255,255,255),p)
    def is_game_over(self):
        return len(self.wrong_guesses) >= 8
    def is_game_won(self):
        return not '.' in self.get_progress()
    def get_progress(self):
        temp = ''
        for c in self.word_to_guess:
            if c in self.good_guesses:
                temp += c
            else:
                temp += '.'
        return temp#self.word_to_guess
        
h = hangman('baguette')
while not h.is_game_over() and not h.is_game_won():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    guess = str(input('guess'))[0]
    h.make_guess(guess)
    h.draw()
    print(h.get_progress())
    pygame.display.update()

pygame.quit()
