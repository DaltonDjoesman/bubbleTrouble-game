import pygame
from consts import *

class Player(pygame.sprite.Sprite):
    def __init__(self,x, y):
        super().__init__()
        self.runSprites = self.get_sprites(runSprites, 120, 80)
        self.image = self.runSprites[0]
        self.rect = pygame.Rect(0, 0 , 120, 80)
        self.rect.center = (x, y)
        self.vel_x = 8
        self.index = 0
        self.indexSpeed = 0.15

    def animation(self):
        if self.index >= len(self.runSprites):
            self.index = 0
        self.image = self.runSprites[int(self.index)]
        self.index += self.indexSpeed
        
    def update(self):
        dx = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_d] == True:
            dx += self.vel_x
        elif key[pygame.K_a] == True:
            dx -= self.vel_x

        if self.rect.left + dx < 0 or self.rect.right + dx > screenWidth:
            dx = 0
        
        
        self.rect.x += dx  
        self.animation()
    
    def get_sprites(self, path, size_x, size_y):
        surface = pygame.image.load(path)
        tile_amount_x = int(surface.get_size()[0]/size_x)
        tile_amount_y = 1
        sprites = []

        for row in range(tile_amount_y):
            for col in range(tile_amount_x):
                x = col*size_x
                y = row*size_y
                new_surf = pygame.transform.scale(pygame.Surface((size_x, size_y), flags = pygame.SRCALPHA), (120*4, 80*4))
                new_surf.blit(surface, (0,0), pygame.Rect(x,y, size_x, size_y))
                sprites.append(new_surf)
        return sprites
        
