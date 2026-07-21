import pygame
from consts import *
from player import Player
from bolinha import Ball
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("game")
        #personagens

        self.bolas = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        #redimensionar a imagem
        circleImage = pygame.image.load(bolaSprite).convert_alpha()
        circleImage_width, circleImage_hight = circleImage.get_size()
        fator = 0.1
        newCircle_lenght = (int(circleImage_width*fator), int(circleImage_hight*fator))
        circleImage = pygame.transform.scale(circleImage, newCircle_lenght)

        self.bolas.add( Ball(circleImage, screenWidth//2, screenHeight//2, (2, 0)))
        self.bolas.add( Ball(circleImage, screenWidth//2 + 10, screenHeight//2, (-2, 0)))

        self.player.add(Player(screenWidth//2, screenHeight-45))

    def runGame(self):
        run = True
        while run:
            self.screen.fill((0,0,0))
            self.clock.tick(FPS)
            #bolinha
            self.bolas.draw(self.screen)
            self.bolas.update()

            #player
            self.player.draw(self.screen)
            self.player.update()

            for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    run = False
            pygame.display.update()

jogo = Game()
jogo.runGame()