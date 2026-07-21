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


def load_image(path: Path, *, scale: float | None = None) -> pygame.Surface:
    """Load a PNG with convert_alpha; optional uniform scale. Cached by path+scale."""
    key = (str(path.resolve()), scale)
    if key in _cache:
        return _cache[key].copy()
    surface = pygame.image.load(str(path)).convert_alpha()
    if scale is not None and scale != 1:
        w, h = surface.get_size()
        surface = pygame.transform.scale(
            surface, (max(1, int(w * scale)), max(1, int(h * scale)))
        )
    _cache[key] = surface
    return surface.copy()


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
        surface = pygame.image.load(str(path)).convert_alpha()
        frames.extend(cut_strip(surface, cell=cell, scale=scale))
    if not frames:
        raise ValueError(f"No frames loaded from {paths}")
    return frames


def load_folder_frames(
    folder: Path,
    prefix: str,
    *,
    cell: int = DEFAULT_CELL,
    scale: int = SPRITE_SCALE,
) -> list[pygame.Surface]:
    """Load ordered frame lists from a folder (Idle/Run/Jump/…), not only grids.

    Matches ``{prefix}*.png`` in natural numeric order (Idle1, Idle2, …),
    cutting each file as a horizontal strip when wider than ``cell``.
    """
    paths = sorted(
        folder.glob(f"{prefix}*.png"),
        key=lambda p: _natural_key(p.stem),
    )
    if not paths:
        raise ValueError(f"No frames matching {prefix!r} in {folder}")
    return load_strip_frames(paths, cell=cell, scale=scale)


def _natural_key(stem: str) -> tuple:
    """Sort Idle1, Idle2, … / 4_1, 4_2 before lexical surprises."""
    parts: list = []
    num = ""
    for ch in stem:
        if ch.isdigit():
            num += ch
        else:
            if num:
                parts.append(int(num))
                num = ""
            parts.append(ch)
    if num:
        parts.append(int(num))
    return tuple(parts)
