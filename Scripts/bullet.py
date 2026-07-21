from __future__ import annotations

import pygame

from consts import BULLET_SCALE, BULLET_SPEED, BULLET_SPRITE


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        surface = pygame.image.load(BULLET_SPRITE).convert_alpha()
        w, h = surface.get_size()
        self.image = pygame.transform.scale(
            surface, (max(1, int(w * BULLET_SCALE)), max(1, int(h * BULLET_SCALE)))
        )
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_y = -BULLET_SPEED

    def update(self) -> None:
        self.rect.y += self.vel_y
        if self.rect.bottom < 0:
            self.kill()
