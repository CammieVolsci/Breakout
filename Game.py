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
        self.basic_font = pygame.font.Font('freesansbold.ttf',32)     
        self.small_font = pygame.font.Font('freesansbold.ttf',20)    

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
                if k == K_r and self.game_over:
                    self.reset()
                if k == K_LEFT and not self.game_over:
                    jogador.mover = -9
                elif k == K_RIGHT and not self.game_over:
                    jogador.mover = 9
            elif t == KEYUP:
                if k == K_LEFT or k== K_RIGHT:
                    jogador.mover = 0
    
    def actors_update(self):
        jogador = self.jogador
        bolinha = self.bolinha
        bloco = self.bloco

        if bolinha.lost == True:
            jogador.vidas -= 1
            bolinha.lost = False

        if jogador.teste_colisao(bolinha):
            bolinha.mover_y *= -1

        for i in range(self.total_blocos):
            if bloco[i].rect!=0 and bolinha.teste_colisao(bloco[i]):
                bloco[i].kill()
                jogador.pontuacao += 10
                bolinha.mover_y *= -1

        jogador.movimento()

        if not self.game_over:
            bolinha.movimento()

    def actors_draw(self):
        jogador = self.jogador
        bolinha = self.bolinha
        bloco = self.bloco

        jogador.desenhar(self.displaysurf)
        bolinha.desenhar(self.displaysurf)

        for i in range(self.total_blocos):
            if(bloco[i].image!=0):
                bloco[i].desenhar(self.displaysurf)
    
    def reset(self):
        self.bloco.clear()
        self.jogador.pontuacao = 0
        self.jogador.vidas = 5
        self.bolinha.x = 400
        self.bolinha.y = 350

        for i in range(self.total_blocos):
            self.bloco.append(Jogador.Blocks(1 + 90*(i%9),35 + 35*math.floor(i/9),CORES_BLOCOS[math.floor(i/9)]))

        self.game_over = False

    def loop(self):
        fpsclock = pygame.time.Clock()   
        self.jogador = Jogador.Paddle()
        self.bolinha = Jogador.Ball()

        for i in range(self.total_blocos):
            self.bloco.append(Jogador.Blocks(1 + 90*(i%9),35 + 35*math.floor(i/9),CORES_BLOCOS[math.floor(i/9)]))

        gameOverSurf = self.basic_font.render('Game Over',True,WHITE)
        gameOverRect = gameOverSurf.get_rect()
        gameOverRect.center = (405,250)   

        resetSurf = self.basic_font.render('Pressione R para reiniciar',True,WHITE)
        resetRect = resetSurf.get_rect()
        resetRect.center = (405,300)  

        while self.run:
            pontuacao_txt = str(self.jogador.pontuacao) 
            vidas_txt = str(self.jogador.vidas)

            pontuacaoSurf = self.small_font.render('PONTOS: ' + pontuacao_txt,True,WHITE)
            pontuacaoRect = pontuacaoSurf.get_rect()
            pontuacaoRect.center = (70,20)

            vidasSurf = self.small_font.render('VIDAS: ' + vidas_txt,True,WHITE)
            vidasRect = vidasSurf.get_rect()
            vidasRect.center = (740,20)

            self.displaysurf.fill(BLACK) 
            self.displaysurf.blit(pontuacaoSurf,pontuacaoRect) 
            self.displaysurf.blit(vidasSurf,vidasRect)

            if self.jogador.vidas <= 0:
                self.game_over = True
                self.displaysurf.blit(gameOverSurf,gameOverRect)
                self.displaysurf.blit(resetSurf,resetRect)

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
