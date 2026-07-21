from __future__ import annotations

import pygame

from assets import load_image
from consts import BULLET_SPRITE, LASER_GROW_SPEED, LASER_WIDTH


class Bullet(pygame.sprite.Sprite):
    """Growing upward laser (classic Bubble Trouble style)."""

    def __init__(self, x: int, base_y: int) -> None:
        super().__init__()
        tip = load_image(BULLET_SPRITE)
        tw, th = tip.get_size()
        # Narrow tip used at the leading edge; beam is stretched below it
        tip_w = LASER_WIDTH
        tip_h = max(2, int(th * (LASER_WIDTH / max(1, tw))))
        self._tip = pygame.transform.scale(tip, (tip_w, tip_h))
        self._beam_color = self._tip.get_at((tip_w // 2, tip_h // 2))

        self.x = x
        self.base_y = base_y
        self.top = base_y - 1  # start with 1px height, grow upward
        self._rebuild()

    def _rebuild(self) -> None:
        height = max(1, self.base_y - self.top)
        image = pygame.Surface((LASER_WIDTH, height), flags=pygame.SRCALPHA)
        # Beam body (stretch color from tip)
        if height > self._tip.get_height():
            body_h = height - self._tip.get_height()
            body = pygame.Surface((LASER_WIDTH, body_h), flags=pygame.SRCALPHA)
            body.fill(self._beam_color)
            image.blit(body, (0, self._tip.get_height()))
        image.blit(self._tip, (0, 0))
        self.image = image
        # Collision rect derived from the scaled/composited laser surface
        self.rect = self.image.get_rect(midbottom=(self.x, self.base_y))

    def update(self, solids: list[pygame.Rect] | None = None) -> None:
        self.top -= LASER_GROW_SPEED
        if self.top <= 0:
            self.kill()
            return
        self._rebuild()
        for solid in solids or []:
            if self.rect.colliderect(solid):
                self.kill()
                return
