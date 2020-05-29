import actors, pygame, math, random, datetime
from pygame.locals import *

class StateMachine:

    def __init__(self):
        self.end = False
        self.next = None
        self.quit = False
        self.previous = None

class Textos:

    gameOverSurf = None
    gameOverRect = None

    resetSurf = None
    resetRect = None

    pontuacaoSurf = None
    pontuacaoRect = None

    vidasSurf = None
    vidasRect = None

    menuSurf = None
    menuRect = None

    white = (255,255,255)

    def __init__(self):
        pygame.init()          
        self.basic_font = pygame.font.Font('freesansbold.ttf',32)     
        self.small_font = pygame.font.Font('freesansbold.ttf',20)  

    def gameover(self):
        self.gameOverSurf = self.basic_font.render('Game Over',True,self.white)
        self.gameOverRect = self.gameOverSurf.get_rect()
        self.gameOverRect.center = (405,250)   

    def reset(self):
        self.resetSurf = self.basic_font.render('Pressione R para reiniciar',True,self.white)
        self.resetRect = self.resetSurf.get_rect()
        self.resetRect.center = (405,300) 

    def pontuacao(self,pontuacao_txt): 
        self.pontuacaoSurf = self.small_font.render('PONTOS: ' + pontuacao_txt,True,self.white)
        self.pontuacaoRect = self.pontuacaoSurf.get_rect()
        self.pontuacaoRect.center = (70,20)

    def vidas(self,vidas_txt):
        self.vidasSurf = self.small_font.render('VIDAS: ' + vidas_txt,True,self.white)
        self.vidasRect = self.vidasSurf.get_rect()
        self.vidasRect.center = (740,20)

    def menu_txt(self):
        self.menuSurf = self.basic_font.render('BREAKOUT',True,self.white)
        self.menuRect = self.menuSurf.get_rect()
        self.menuRect.center = (400,300)

class MainMenu(StateMachine,Textos):
    
    black = (0,0,0) 

    def __init__(self):
        StateMachine.__init__(self)
        Textos.__init__(self)
        self.next = 'game'

    def startup(self):
        pass

    def cleanup(self):
        pass

    def handle_events(self,event):
        if event.type == KEYDOWN:
            if event.key == K_x:
                self.end = True

    def update(self,displaysurf):
        self.menu_txt()
        displaysurf.fill(self.black) 
        displaysurf.blit(self.menuSurf,self.menuRect)

class Game(StateMachine,Textos):
   
    background = None
    game_over = False
    total_blocos = 45
    black = (0,0,0) 

    jogador = None
    bolinha = None
    bloco = []
    
    def __init__(self,**game_images):
        StateMachine.__init__(self)
        Textos.__init__(self)
        self.__dict__.update(game_images)        

    def startup(self):
        random.seed(datetime.time())   

        self.jogador = actors.Paddle(340,600,self.player_image)
        self.bolinha = actors.Ball(random.randint(300,600),random.randint(250,400),self.ball_image)

        for i in range(self.total_blocos):
            self.bloco.append(actors.Blocks(1 + 90*(i%9),35 + 35*math.floor(i/9),self.cores_blocos[math.floor(i/9)]))

    def cleanup(self):
        pass  

    def handle_events(self,event):
        jogador = self.jogador

        if event.type == KEYDOWN:
            if event.key == K_r and self.game_over:
                self.reseta_game()
            if event.key == K_LEFT and not self.game_over:
                jogador.mover = -9
            elif event.key == K_RIGHT and not self.game_over:
                jogador.mover = 9
        elif event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
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

    def actors_draw(self,displaysurf):
        jogador = self.jogador
        bolinha = self.bolinha
        bloco = self.bloco

        jogador.desenhar(displaysurf)
        bolinha.desenhar(displaysurf)

        for i in range(self.total_blocos):
            if(bloco[i].image!=0):
                bloco[i].desenhar(displaysurf)
    
    def reseta_game(self):
        self.bloco.clear()
        self.jogador.pontuacao = 0
        self.jogador.vidas = 5
        self.bolinha.x = 400
        self.bolinha.y = 350

        for i in range(self.total_blocos):
            self.bloco.append(actors.Blocks(1 + 90*(i%9),35 + 35*math.floor(i/9),self.cores_blocos[math.floor(i/9)]))

        self.game_over = False

    def update(self,displaysurf):   

        pontuacao_txt = str(self.jogador.pontuacao) 
        vidas_txt = str(self.jogador.vidas)

        self.gameover()
        self.reset()       
        self.pontuacao(pontuacao_txt)
        self.vidas(vidas_txt)       

        displaysurf.fill(self.black) 
        displaysurf.blit(self.pontuacaoSurf,self.pontuacaoRect) 
        displaysurf.blit(self.vidasSurf,self.vidasRect)

        if self.jogador.vidas <= 0:
            self.game_over = True
            displaysurf.blit(self.gameOverSurf,self.gameOverRect)
            displaysurf.blit(self.resetSurf,self.resetRect)

        self.actors_update()
        self.actors_draw(displaysurf)       
            
class BreakoutGame:

    state_dictionary = None
    state_name = None
    state = None

    def __init__(self,**settings):      
        self.__dict__.update(settings)
        self.end = False  
        pygame.display.set_caption("Breakout")   
        self.displaysurf = pygame.display.set_mode(self.size)
        self.fpsclock = pygame.time.Clock()            

    def setup_states(self,state_dictionary,start_state):
        self.state_dictionary = state_dictionary
        self.state_name = start_state
        self.state = self.state_dictionary[self.state_name]
        self.state.startup()

    def flip_state(self):
        self.state.end = False
        previous,self.state_name = self.state_name,self.state.next
        self.state.cleanup()
        self.state = self.state_dictionary[self.state_name]
        self.state.startup()
        self.state.previous = previous

    def update(self):
        if self.state.quit:
            self.end = True
        elif self.state.end:
            self.flip_state()

        self.state.update(self.displaysurf)

    def event_loop(self):

        for event in pygame.event.get():
            if event.type == QUIT:
                self.end = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.end = True
            self.state.handle_events(event)

    def loop(self):

        while not self.end:
            self.event_loop()
            self.update()

            pygame.display.flip()
            pygame.display.update()
            self.fpsclock.tick(self.fps)
            
def main():   
    settings = {
        'size' : (800,650),
        'fps' : 30,           
    }

    game_images = {
        'ball_image' : "assets/ball.png",
        'player_image' : "assets/paddle.png",        
        'cores_blocos' : ["assets/barrinha1.png","assets/barrinha2.png","assets/barrinha3.png",
        "assets/barrinha4.png","assets/barrinha5.png"]    
    }

    dicionario_estados = {
        'menu' : MainMenu(),
        'game' : Game(**game_images),
    }

    main_game = BreakoutGame(**settings)
    main_game.setup_states(dicionario_estados,'menu')
    main_game.loop()

## MAIN ##
if __name__ == '__main__':
    main()
