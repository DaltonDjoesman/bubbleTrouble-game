"""Powerup pickups: TIME / STICKY / DRILL drops from ball kills."""
from __future__ import annotations

import random
from pathlib import Path

import pygame

from assets import load_image
from consts import (
    FLOOR_Y,
    GRAVITY,
    POWERUP_DROP_CHANCE,
    POWERUP_FALL_MAX,
    POWERUP_SIZE,
    POWERUP_SPRITES,
    SCREEN_WIDTH,
)

POWER_TYPES = ("TIME", "STICKY", "DRILL")


def _load_icon(path: Path) -> pygame.Surface:
    """Load icon onto a fixed POWERUP_SIZE canvas (no downscale)."""
    icon = load_image(path)
    canvas = pygame.Surface((POWERUP_SIZE, POWERUP_SIZE), flags=pygame.SRCALPHA)
    canvas.blit(icon, icon.get_rect(center=(POWERUP_SIZE // 2, POWERUP_SIZE // 2)))
    return canvas


class Powerup(pygame.sprite.Sprite):
    def __init__(self, kind: str, x: float, y: float) -> None:
        super().__init__()
        if kind not in POWER_TYPES:
            raise ValueError(f"Unknown powerup: {kind}")
        self.kind = kind
        self.image = _load_icon(POWERUP_SPRITES[kind])
        self.rect = self.image.get_rect(center=(int(x), int(y)))
        self.vel_y = 0.0

    def update(self, *_args, **_kwargs) -> None:
        self.vel_y = min(POWERUP_FALL_MAX, self.vel_y + GRAVITY * 0.6)
        self.rect.y += int(self.vel_y)
        if self.rect.bottom > FLOOR_Y:
            self.rect.bottom = FLOOR_Y
            self.vel_y = 0.0
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


def maybe_spawn_powerup(x: float, y: float) -> Powerup | None:
    """Roll for a random drop at the hit location."""
    if random.random() > POWERUP_DROP_CHANCE:
        return None
    kind = random.choice(POWER_TYPES)
    return Powerup(kind, x, y)
