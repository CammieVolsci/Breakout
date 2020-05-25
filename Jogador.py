import pygame, datetime, random

PLAYER_IMAGE = "assets/paddle.png"
BALL_IMAGE = "assets/ball.png"

class Paddle(pygame.sprite.Sprite):

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
    
    def teste_colisao(self,sprite):
        if(self.image!=0):
            return self.rect.colliderect(sprite.rect)            

class Ball():

    random.seed(datetime.time())  

    def __init__(self):
        self.x = random.randint(100,700)
        self.y = random.randint(300,550)
        self.mover_x = 7 * pow(-1,random.randint(1,2))
        self.mover_y = 7 * pow(-1,random.randint(1,2))
        self.image = pygame.image.load(BALL_IMAGE)
        self.rect = self.image.get_rect() 
        self.rect.x = self.x
        self.rect.y = self.y

    def desenhar(self,screen):
        screen.blit(self.image,(self.x,self.y))

    def movimento(self):                 
        self.x += self.mover_x
        self.y += self.mover_y

        if self.x <= 0:
            self.mover_x *= -1
        elif self.x >= 775:
            self.mover_x *= -1

        if self.y <= 0:
            self.mover_y *= -1
        elif self.y >= 625:
            self.x = random.randint(100,700)
            self.y = random.randint(300,550)
        
        self.rect.x = self.x
        self.rect.y = self.y       

class Blocks():

    def __init__(self,x,y,image):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def desenhar(self,screen):
        screen.blit(self.image,(self.x,self.y))   