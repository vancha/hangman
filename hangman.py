import pygame
import random

WIDTH = 500
HEIGHT = 500

FONT_SIZE = WIDTH // 10
pygame.init()
#pygame.font.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
hangmanfont = pygame.font.SysFont('Comic Sans MS', FONT_SIZE)
#steps:
#1: rope + horizontalbeam + vertical beam + beam stand
#2: head
#3: body
#4: left-arm
#5: right-arm
#6: left-leg
#7: right-leg
lines = [
        #start of vertical beam, the "pole"
        ((WIDTH / 3,HEIGHT / 6),
        ((WIDTH / 3)+10,HEIGHT / 6),
        ((WIDTH / 3)+10,(HEIGHT / 6)*5),
        (WIDTH / 3,(HEIGHT / 6)*5),
        (WIDTH / 3,HEIGHT / 6),
        ((WIDTH / 3)+10,HEIGHT / 6),
        ((WIDTH / 3)*2,HEIGHT / 6),
        ((WIDTH / 3)*2,(HEIGHT / 6)+10),
        ((WIDTH / 3)+10,(HEIGHT / 6)+10),
        ((WIDTH / 3)+10,HEIGHT / 6)),
        
        
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
        self.show_progress()
            
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
        return temp
    
    def show_progress(self):
        textsurface = hangmanfont.render(self.get_progress(), False, (255, 255, 255))
        screen.blit(textsurface,(WIDTH/3,HEIGHT-40))
        
h = hangman('baguette')
while not h.is_game_over() and not h.is_game_won():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            screen.fill((0,0,0))
            h.make_guess(pygame.key.name(event.key))
            h.draw()
            pygame.display.update()
   

pygame.quit()
