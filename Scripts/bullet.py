from __future__ import annotations

import pygame

from assets import load_image
from consts import (
    CEILING_Y,
    CHAIN_LINK_SPRITE,
    CHAIN_TIP_SPRITE,
    LASER_GROW_SPEED,
    LASER_WIDTH,
)

# Mode tints applied via BLEND_RGBA_MULT after optional grayscale
_HARPOON_TINT = (235, 235, 242, 255)  # light cool steel gray
_TIP_TINT = (230, 230, 236, 255)  # tip always gray (all modes)
_STICKY_TINT = (80, 255, 140, 255)
_DRILL_TINT = (255, 200, 60, 255)
# Tip ~1.8× shaft width so the arrow head reads clearly
_TIP_WIDTH_SCALE = 1.8


def _to_grayscale(surface: pygame.Surface) -> pygame.Surface:
    """Desaturate RGB (keep alpha) so gold links read as neutral metal."""
    out = surface.copy()
    w, h = out.get_size()
    for y in range(h):
        for x in range(w):
            r, g, b, a = out.get_at((x, y))
            if a == 0:
                continue
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            out.set_at((x, y), (gray, gray, gray, a))
    return out


def _apply_mode_tint(surface: pygame.Surface, mode: str) -> pygame.Surface:
    if mode == "sticky":
        tinted = surface.copy()
        tinted.fill(_STICKY_TINT, special_flags=pygame.BLEND_RGBA_MULT)
        return tinted
    if mode == "drill":
        tinted = surface.copy()
        tinted.fill(_DRILL_TINT, special_flags=pygame.BLEND_RGBA_MULT)
        return tinted
    # Default harpoon: gray steel
    gray = _to_grayscale(surface)
    gray.fill(_HARPOON_TINT, special_flags=pygame.BLEND_RGBA_MULT)
    return gray


def _prepare_link(mode: str) -> pygame.Surface:
    """Load cropped chain link, scale to LASER_WIDTH, tint by mode."""
    link = load_image(CHAIN_LINK_SPRITE, crop=True)
    tw, th = link.get_size()
    if tw != LASER_WIDTH:
        scale = LASER_WIDTH / max(1, tw)
        link = pygame.transform.scale(
            link, (LASER_WIDTH, max(1, int(th * scale)))
        )
    return _apply_mode_tint(link, mode)


def _prepare_tip(_mode: str) -> pygame.Surface:
    """Load arrow-head tip; always gray steel, larger than the chain shaft."""
    tip = load_image(CHAIN_TIP_SPRITE, crop=True)
    target_w = max(LASER_WIDTH + 2, int(round(LASER_WIDTH * _TIP_WIDTH_SCALE)))
    tw, th = tip.get_size()
    if tw != target_w:
        scale = target_w / max(1, tw)
        tip = pygame.transform.scale(
            tip, (target_w, max(1, int(th * scale)))
        )
    # Tip stays gray in every weapon mode
    gray = _to_grayscale(tip)
    gray.fill(_TIP_TINT, special_flags=pygame.BLEND_RGBA_MULT)
    return gray


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
        self._tip = _prepare_tip(self.mode)

        self.x = x
        self.base_y = base_y
        self.owner_id = owner_id
        self.top = base_y - 1  # start with 1px height, grow upward
        self.planted = False  # sticky: finished growing, waiting for ball
        self.spawned_at = pygame.time.get_ticks()
        self._rebuild()

    def _rebuild(self) -> None:
        height = max(1, self.base_y - self.top)
        tip_h = self._tip.get_height()
        tip_w = self._tip.get_width()
        link_w = self._link.get_width()
        lh = self._link.get_height()
        width = max(tip_w, link_w)

        image = pygame.Surface((width, height), flags=pygame.SRCALPHA)

        # Tip at top (clip if beam shorter than tip)
        tip_draw_h = min(tip_h, height)
        if tip_draw_h > 0:
            if tip_draw_h < tip_h:
                tip_src = self._tip.subsurface((0, 0, tip_w, tip_draw_h))
            else:
                tip_src = self._tip
            image.blit(tip_src, ((width - tip_w) // 2, 0))

        # Chain tiles below tip, from bottom of tip down to player
        body_top = tip_draw_h
        body_h = height - body_top
        if body_h > 0:
            link_x = (width - link_w) // 2
            y = height
            while y > body_top:
                chunk = min(lh, y - body_top)
                y -= chunk
                if chunk < lh:
                    src = self._link.subsurface((0, lh - chunk, link_w, chunk))
                else:
                    src = self._link
                image.blit(src, (link_x, y))

        self.image = image
        self.rect = self.image.get_rect(midbottom=(self.x, self.base_y))

    def update(self, solids: list[pygame.Rect] | None = None) -> None:
        # Sticky stays put once planted
        if self.mode == "sticky" and self.planted:
            return

        self.top -= LASER_GROW_SPEED
        hit_ceiling = self.top <= CEILING_Y
        if hit_ceiling:
            self.top = CEILING_Y
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
