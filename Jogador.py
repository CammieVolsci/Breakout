import pygame

PLAYER_IMAGE = "assets/paddle.png"
BALL_IMAGE = "assets/ball.png"

class Paddle():

    def __init__(self):
        self.x = 340
        self.y = 580
        self.mover = 0
        self.image = pygame.image.load(PLAYER_IMAGE)
        self.rect = self.image.get_rect() 
        self.rect.x = self.x
        self.rect.y = self.y
    
    def desenhar(self,screen):
        screen.blit(self.image,(self.x,self.y))

    def movimento(self):
        self.x += self.mover

        if self.x <= 0:
            self.x = 0
        elif self.x >= 680:
            self.x = 680
        
        self.rect.x = self.x
        self.rect.y = self.y

class Ball():

    def __init__(self):
        self.x = 380
        self.y = 550
        self.mover = 0
        self.image = pygame.image.load(BALL_IMAGE)
        self.rect = self.image.get_rect() 
        self.rect.x = self.x
        self.rect.y = self.y

    def desenhar(self,screen):
            screen.blit(self.image,(self.x,self.y))
