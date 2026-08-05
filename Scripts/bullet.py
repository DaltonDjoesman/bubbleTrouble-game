from __future__ import annotations

import pygame

from assets import load_image
from consts import CHAIN_LINK_SPRITE, LASER_GROW_SPEED, LASER_WIDTH

# Mode tints applied via BLEND_RGBA_MULT (harpoon = natural metal, no tint)
_STICKY_TINT = (80, 255, 140, 255)
_DRILL_TINT = (255, 200, 60, 255)


def _prepare_link(mode: str) -> pygame.Surface:
    """Load cropped chain link, scale to LASER_WIDTH, optionally tint by mode."""
    link = load_image(CHAIN_LINK_SPRITE, crop=True)
    tw, th = link.get_size()
    if tw != LASER_WIDTH:
        scale = LASER_WIDTH / max(1, tw)
        link = pygame.transform.scale(
            link, (LASER_WIDTH, max(1, int(th * scale)))
        )
    if mode == "sticky":
        tinted = link.copy()
        tinted.fill(_STICKY_TINT, special_flags=pygame.BLEND_RGBA_MULT)
        return tinted
    if mode == "drill":
        tinted = link.copy()
        tinted.fill(_DRILL_TINT, special_flags=pygame.BLEND_RGBA_MULT)
        return tinted
    return link


class Bullet(pygame.sprite.Sprite):
    """Growing upward harpoon (classic Bubble Trouble style).

    Modes:
      harpoon — despawn on first ball or solid/ceiling
      sticky  — grow then stay until a ball hits
      drill   — pierce balls; stop on solid/ceiling
    """

    def __init__(
        self,
        x: int,
        base_y: int,
        mode: str = "harpoon",
        *,
        owner_id: int = 1,
    ) -> None:
        super().__init__()
        self.mode = mode if mode in ("harpoon", "sticky", "drill") else "harpoon"
        self._link = _prepare_link(self.mode)

        self.x = x
        self.base_y = base_y
        self.owner_id = owner_id
        self.top = base_y - 1  # start with 1px height, grow upward
        self.planted = False  # sticky: finished growing, waiting for ball
        self.spawned_at = pygame.time.get_ticks()
        self._rebuild()

    def _rebuild(self) -> None:
        height = max(1, self.base_y - self.top)
        lw = self._link.get_width()
        lh = self._link.get_height()
        image = pygame.Surface((lw, height), flags=pygame.SRCALPHA)
        # Tile from bottom (player) upward so a partial tile sits at the tip
        y = height
        while y > 0:
            chunk = min(lh, y)
            y -= chunk
            if chunk < lh:
                src = self._link.subsurface((0, 0, lw, chunk))
            else:
                src = self._link
            image.blit(src, (0, y))
        self.image = image
        self.rect = self.image.get_rect(midbottom=(self.x, self.base_y))

    def update(self, solids: list[pygame.Rect] | None = None) -> None:
        # Sticky stays put once planted
        if self.mode == "sticky" and self.planted:
            return

        self.top -= LASER_GROW_SPEED
        hit_ceiling = self.top <= 0
        if hit_ceiling:
            self.top = 0
            self._rebuild()
            if self.mode == "sticky":
                self.planted = True
                return
            self.kill()
            return

        self._rebuild()
        for solid in solids or []:
            if self.rect.colliderect(solid):
                # Snap top to solid bottom so the beam doesn't overlap
                self.top = solid.bottom
                self._rebuild()
                if self.mode == "sticky":
                    self.planted = True
                    return
                self.kill()
                return
