"""Short-lived muzzle / shoot flash at the player's gun height."""
from __future__ import annotations

import pygame

from assets import load_image
from consts import SHOOT_EFFECT_FRAMES, SHOOT_EFFECT_MS, SHOOT_EFFECT_SCALE


class ShootEffect(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self._frames = [
            load_image(path, scale=SHOOT_EFFECT_SCALE) for path in SHOOT_EFFECT_FRAMES
        ]
        self._index = 0
        self._born = pygame.time.get_ticks()
        self.image = self._frames[0]
        self.rect = self.image.get_rect(midbottom=(x, y))

    def update(self) -> None:
        elapsed = pygame.time.get_ticks() - self._born
        if elapsed >= SHOOT_EFFECT_MS:
            self.kill()
            return
        # Swap to second frame halfway through the flash
        idx = 1 if elapsed >= SHOOT_EFFECT_MS // 2 and len(self._frames) > 1 else 0
        if idx != self._index:
            self._index = idx
            midbottom = self.rect.midbottom
            self.image = self._frames[idx]
            self.rect = self.image.get_rect(midbottom=midbottom)
