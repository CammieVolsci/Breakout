import pygame, Jogador
from pygame.locals import *

WHITE = (255,255,255)
BLACK = (0,0,0)

class BreakoutGame:

    window_width = None
    window_height = None   
    background = None
    displaysurf = None 
    run = True
    fps = None
    game_over = False

    basic_font = None
    small_font = None

    jogador = None
    bolinha = None

    def __init__(self):
        self.window_width = 800
        self.window_height = 650
        self.fps = 30   
        pygame.init()
        pygame.display.set_caption("Breakout")
        self.displaysurf = pygame.display.set_mode((self.window_width,self.window_height))  

    def handle_events(self):
        jogador = self.jogador

        for event in pygame.event.get():
            t = event.type
            if t in (KEYDOWN,KEYUP):
                k = event.key
            if t == QUIT:
                self.run = False
            elif t == KEYDOWN:
                if k == K_ESCAPE:
                    self.run = False
                if k == K_LEFT:
                    jogador.mover = -8
                elif k == K_RIGHT:
                    jogador.mover = 8
            elif t == KEYUP:
                if k == K_LEFT or k== K_RIGHT:
                    jogador.mover = 0
    
    def actors_update(self):
        jogador = self.jogador
        jogador.movimento()

    def actors_draw(self):
        jogador = self.jogador
        bolinha = self.bolinha

        jogador.desenhar(self.displaysurf)
        bolinha.desenhar(self.displaysurf)

    def loop(self):
        fpsclock = pygame.time.Clock()   
        self.jogador = Jogador.Paddle()
        self.bolinha = Jogador.Ball()

        while self.run:
            self.displaysurf.fill(BLACK) 

            self.handle_events()
            self.actors_update()
            self.actors_draw()           
            
            pygame.display.flip()
            pygame.display.update()  
            fpsclock.tick(self.fps)


def main():
    game = BreakoutGame()
    game.loop()

## MAIN ##
if __name__ == '__main__':
    main()
