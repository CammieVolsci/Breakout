import pygame, Jogador, math
from pygame.locals import *

WHITE = (255,255,255)
BLACK = (0,0,0)
CORES_BLOCOS = ["assets/barrinha1.png","assets/barrinha2.png","assets/barrinha3.png","assets/barrinha4.png","assets/barrinha5.png"]

class BreakoutGame:

    window_width = None
    window_height = None   
    background = None
    displaysurf = None 
    run = True
    fps = 30
    game_over = False
    total_blocos = 45

    basic_font = None
    small_font = None

    jogador = None
    bolinha = None
    bloco = []

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
                    jogador.mover = -9
                elif k == K_RIGHT:
                    jogador.mover = 9
            elif t == KEYUP:
                if k == K_LEFT or k== K_RIGHT:
                    jogador.mover = 0
    
    def actors_update(self):
        jogador = self.jogador
        bolinha = self.bolinha

        if jogador.teste_colisao(bolinha):
            bolinha.mover_y *= -1

        jogador.movimento()
        bolinha.movimento()

    def actors_draw(self):
        jogador = self.jogador
        bolinha = self.bolinha
        bloco = self.bloco

        jogador.desenhar(self.displaysurf)
        bolinha.desenhar(self.displaysurf)

        for i in range(self.total_blocos):
            bloco[i].desenhar(self.displaysurf)

    def loop(self):
        fpsclock = pygame.time.Clock()   
        self.jogador = Jogador.Paddle()
        self.bolinha = Jogador.Ball()

        for i in range(self.total_blocos):
            self.bloco.append(Jogador.Blocks(1 + 90*(i%9),50 + 35*math.floor(i/9),CORES_BLOCOS[math.floor(i/9)]))

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
