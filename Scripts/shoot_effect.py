"""Short-lived muzzle flash at the gun tip (Craftpix shoot-effect cells)."""
from __future__ import annotations

import pygame

from assets import load_strip_frames
from consts import SHOOT_EFFECT_FRAMES, SHOOT_EFFECT_MS, SHOOT_EFFECT_SCALE

# Cap flash height so it reads as a spark, not a second gun
_MAX_FLASH_H = 20


def _make_flash(cell: pygame.Surface) -> pygame.Surface:
    bounds = cell.get_bounding_rect(min_alpha=1)
    if bounds.width <= 0 or bounds.height <= 0:
        return cell
    cropped = cell.subsurface(bounds).copy()
    # Horizontal slash → vertical puff above the muzzle
    flash = pygame.transform.rotate(cropped, 90)
    if flash.get_height() > _MAX_FLASH_H:
        w = max(1, int(flash.get_width() * (_MAX_FLASH_H / flash.get_height())))
        flash = pygame.transform.scale(flash, (w, _MAX_FLASH_H))
    return flash


class ShootEffect(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        # Strips are 48×48 cells — never blit the whole 288×48 sheet
        cells = load_strip_frames(SHOOT_EFFECT_FRAMES, scale=SHOOT_EFFECT_SCALE)
        picked = cells[1:3] if len(cells) >= 3 else cells[:1]
        self._frames = [_make_flash(cell) for cell in picked]
        self._index = 0
        self._born = pygame.time.get_ticks()
        self.image = self._frames[0]
        self.rect = self.image.get_rect(midbottom=(x, y))

    def update(self) -> None:
        elapsed = pygame.time.get_ticks() - self._born
        if elapsed >= SHOOT_EFFECT_MS:
            self.kill()
            return
        idx = 1 if elapsed >= SHOOT_EFFECT_MS // 2 and len(self._frames) > 1 else 0
        if idx != self._index:
            self._index = idx
            midbottom = self.rect.midbottom
            self.image = self._frames[idx]
            self.rect = self.image.get_rect(midbottom=midbottom)
