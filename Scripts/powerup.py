"""Powerup pickups: TIME / STICKY / DRILL drops from ball kills."""
from __future__ import annotations

import random

import pygame

from consts import (
    GRAVITY,
    POWERUP_DROP_CHANCE,
    POWERUP_FALL_MAX,
    POWERUP_SIZE,
    screenHeight,
    screenWidth,
)

POWER_TYPES = ("TIME", "STICKY", "DRILL")

_COLORS = {
    "TIME": ((40, 200, 255), (180, 240, 255)),
    "STICKY": ((40, 220, 100), (160, 255, 180)),
    "DRILL": ((255, 180, 40), (255, 230, 140)),
}


class Powerup(pygame.sprite.Sprite):
    def __init__(self, kind: str, x: float, y: float) -> None:
        super().__init__()
        if kind not in POWER_TYPES:
            raise ValueError(f"Unknown powerup: {kind}")
        self.kind = kind
        fill, edge = _COLORS[kind]
        size = POWERUP_SIZE
        image = pygame.Surface((size, size), flags=pygame.SRCALPHA)
        pygame.draw.rect(image, fill, image.get_rect(), border_radius=4)
        pygame.draw.rect(image, edge, image.get_rect(), width=2, border_radius=4)
        # Simple letter mark
        mark = kind[0]
        font = pygame.font.Font(None, 22)
        label = font.render(mark, True, edge)
        image.blit(label, label.get_rect(center=(size // 2, size // 2)))
        self.image = image
        self.rect = self.image.get_rect(center=(int(x), int(y)))
        self.vel_y = 0.0

    def update(self, *_args, **_kwargs) -> None:
        self.vel_y = min(POWERUP_FALL_MAX, self.vel_y + GRAVITY * 0.6)
        self.rect.y += int(self.vel_y)
        floor = screenHeight - 8 - self.rect.height
        if self.rect.top > floor:
            self.rect.top = floor
            self.vel_y = 0.0
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screenWidth:
            self.rect.right = screenWidth


def maybe_spawn_powerup(x: float, y: float) -> Powerup | None:
    """Roll for a random drop at the hit location."""
    if random.random() > POWERUP_DROP_CHANCE:
        return None
    kind = random.choice(POWER_TYPES)
    return Powerup(kind, x, y)
