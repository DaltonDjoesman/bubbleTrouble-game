"""Craftpix asset loading helpers.

Scale factor
------------
``SPRITE_SCALE`` (default 2) is the single documented scale applied to character
and effect frames. Collision rects for player/bullet sprites MUST be derived
from the scaled surface via ``Surface.get_rect(...)``, not a hardcoded size.
"""
from __future__ import annotations

from pathlib import Path

import pygame

# Documented global scale for Craftpix character / effect frames (2× pixel art).
SPRITE_SCALE = 2
DEFAULT_CELL = 48

_cache: dict[tuple, pygame.Surface] = {}


def load_image(
    path: Path,
    *,
    scale: float | None = None,
    colorkey: tuple[int, int, int] | None = None,
    crop: bool = False,
) -> pygame.Surface:
    """Load a PNG with convert_alpha; optional colorkey, crop, and uniform scale."""
    if not path.is_file():
        raise FileNotFoundError(f"Missing asset: {path}")
    key = (str(path.resolve()), scale, colorkey, crop)
    if key in _cache:
        return _cache[key].copy()
    surface = pygame.image.load(str(path)).convert_alpha()
    if colorkey is not None:
        surface = _key_out_color(surface, colorkey)
    if crop:
        bounds = surface.get_bounding_rect()
        if bounds.width > 0 and bounds.height > 0:
            surface = surface.subsurface(bounds).copy()
    if scale is not None and scale != 1:
        w, h = surface.get_size()
        surface = pygame.transform.scale(
            surface, (max(1, int(w * scale)), max(1, int(h * scale)))
        )
    _cache[key] = surface
    return surface.copy()


def _key_out_color(
    surface: pygame.Surface,
    color: tuple[int, int, int],
    *,
    threshold: int = 12,
) -> pygame.Surface:
    """Set near-matching RGB pixels fully transparent (keeps true alpha art)."""
    out = surface.copy()
    tr, tg, tb = color
    w, h = out.get_size()
    for y in range(h):
        for x in range(w):
            r, g, b, _a = out.get_at((x, y))
            if (
                abs(r - tr) <= threshold
                and abs(g - tg) <= threshold
                and abs(b - tb) <= threshold
            ):
                out.set_at((x, y), (0, 0, 0, 0))
    return out


def cut_strip(
    surface: pygame.Surface,
    cell: int = DEFAULT_CELL,
    scale: int = SPRITE_SCALE,
) -> list[pygame.Surface]:
    """Slice a horizontal strip into ``cell×cell`` frames, then scale each."""
    frames: list[pygame.Surface] = []
    w, h = surface.get_size()
    out_size = (cell * scale, cell * scale)
    for col in range(max(1, w // cell)):
        cut = pygame.Surface((cell, cell), flags=pygame.SRCALPHA)
        cut.blit(surface, (0, 0), pygame.Rect(col * cell, 0, cell, min(cell, h)))
        frames.append(pygame.transform.scale(cut, out_size))
    return frames


def load_strip_frames(
    paths: list[Path],
    *,
    cell: int = DEFAULT_CELL,
    scale: int = SPRITE_SCALE,
) -> list[pygame.Surface]:
    """Load strip PNGs and return ordered scaled cell frames."""
    frames: list[pygame.Surface] = []
    for path in paths:
        if not path.is_file():
            raise FileNotFoundError(f"Missing asset: {path}")
        surface = pygame.image.load(str(path)).convert_alpha()
        frames.extend(cut_strip(surface, cell=cell, scale=scale))
    if not frames:
        raise ValueError(f"No frames loaded from {paths}")
    return frames
