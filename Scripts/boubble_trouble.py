import pygame
 
#tamanho da janela
screenWidth = 800
screenHigth = 600
pygame.display.set_caption("game")
screen = pygame.display.set_mode((screenWidth, screenHigth))
clock = pygame.time.Clock()
FPS = 60

#imagens baixadas
circleImage = pygame.image.load("breakout image/bola branca.png").convert_alpha()


#redimensionar a imagem
circleImage_width, circleImage_hight = circleImage.get_size()
fator = 0.1
newCircle_lenght = (int(circleImage_width*fator), int(circleImage_hight*fator))
circleImage = pygame.transform.scale(circleImage, newCircle_lenght)

#game fisics
GRAVITY = 0.3

class Ball:
    def __init__(self, imagem, x, y):
        self.image = imagem
        self.rect = self.image.get_rect(center = (x, y))
        self.vel_x = 2
        self.vel_y = 0
    
    def move(self):

        if self.rect.left + self.vel_x <= 0 or self.rect.right + self.vel_x >= screenWidth:
            self.vel_x *= -1


        self.rect.x += self.vel_x
        
        #gravidade
        
        self.vel_y += GRAVITY

        if self.rect.bottom + self.vel_y > screenHigth:
            self.vel_y = -13
        
        self.rect.y += self.vel_y 

    def draw(self):
        screen.blit(self.image, self.rect.topleft)
        pygame.draw.rect(screen, (255,0,0), self.rect, 2)
    
class Bullet:
    def __init__(self):
        
        pass

class Player:
    def __init__(self,x, y):
        self.rect = pygame.Rect(0, 0 , 50, 80)
        self.rect.center = (x, y)
        self.vel_x = 8
    def movimentation(self, bolinha):
        dx = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_d] == True:
            dx += self.vel_x
        elif key[pygame.K_a] == True:
            dx -= self.vel_x

        if self.rect.left + dx < 0 or self.rect.right + dx > screenWidth:
            dx = 0
        
        if self.rect.colliderect(bolinha.rect):
            pygame.quit()
        
        self.rect.x += dx
    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
    


#personagens
bolinha = Ball(circleImage, screenWidth//2, screenHigth//2)
jogador = Player(screenWidth//2, screenHigth-20)

run = True
while run:
    screen.fill((0,0,0))
    clock.tick(FPS)
    #bolinha
    bolinha.move()
    bolinha.draw()

    jogador.movimentation(bolinha)
    jogador.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()