import pygame
from consts import *
class Ball(pygame.sprite.Sprite):
    def __init__(self, image, x, y, vel):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center = (x, y))
        self.vel_x, self.vel_y = vel
    
    def update(self):

        if self.rect.left + self.vel_x <= 0 or self.rect.right + self.vel_x >= screenWidth:
            self.vel_x *= -1

        self.rect.x += self.vel_x
        
        #gravidade
        
        self.vel_y += GRAVITY

        if self.rect.bottom + self.vel_y > screenHeight:
            self.vel_y = -13
        
        self.rect.y += self.vel_y 
