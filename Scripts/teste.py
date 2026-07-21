import pygame

# Inicializar o Pygame
pygame.init()

# Tamanho da janela
screenWidth = 800
screenHigth = 600
pygame.display.set_caption("Linda's Game")
screen = pygame.display.set_mode((screenWidth, screenHigth))
clock = pygame.time.Clock()
FPS = 60

# Imagens baixadas
circleImage = pygame.image.load("breakout image/bola branca.png").convert_alpha()

# Redimensionar a imagem
circleImage_width, circleImage_hight = circleImage.get_size()
fator = 0.1
newCircle_lenght = (int(circleImage_width * fator), int(circleImage_hight * fator))
circleImage = pygame.transform.scale(circleImage, newCircle_lenght)

# Game physics
GRAVITY = 0.3  # Gravidade reduzida para suavizar a queda

class Ball:
    def __init__(self, imagem, x, y):
        self.image = imagem
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_x = 0
        self.vel_y = -7  # Reduzi a velocidade inicial do salto para não começar muito rápido

    def move(self):
        # Rebater nas paredes laterais
        if self.rect.left + self.vel_x <= 0 or self.rect.right + self.vel_x >= screenWidth:
            self.vel_x *= -1

        self.rect.x += self.vel_x

        # Aplicar gravidade
        self.vel_y += GRAVITY

        # Colisão com o chão
        if self.rect.bottom + self.vel_y > screenHigth:
            self.rect.bottom = screenHigth  # Garante que a bola não atravesse o chão
            self.vel_y = -self.vel_y  # Reduz a velocidade a cada quicada

        self.rect.y += self.vel_y

    def draw(self):
        screen.blit(self.image, self.rect.topleft)
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)


# Criar bola
bolinha = Ball(circleImage, screenWidth // 2, screenHigth // 2)

# Loop do jogo
run = True
while run:
    screen.fill((0, 0, 0))
    clock.tick(FPS)

    # Atualizar bola
    bolinha.move()
    bolinha.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
