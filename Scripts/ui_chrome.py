"""Shared cyberpunk UI chrome: tokens, fonts, and draw helpers."""
from __future__ import annotations

from pathlib import Path

import pygame

from consts import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    UI_BORDER,
    UI_FG,
    UI_FONT_BOLD,
    UI_FONT_REGULAR,
    UI_FONT_SIZE,
    UI_FONT_SMALL_SIZE,
    UI_FONT_TITLE_SIZE,
    UI_IDLE,
    UI_IDLE_BORDER,
    UI_MUTED,
    UI_NEON_CYAN,
    UI_NEON_GOLD,
    UI_NEON_MAGENTA,
    UI_OVERLAY,
    UI_SCREEN,
    UI_SURFACE,
    UI_SURFACE_RAISED,
)

# Layout bands (800×600 shell)
HEADER_H = 112
FOOTER_H = 72
CONTENT_TOP = HEADER_H
CONTENT_BOTTOM = SCREEN_HEIGHT - FOOTER_H

_scanline_cache: pygame.Surface | None = None
_fonts_loaded = False
_font: pygame.font.Font | None = None
_big_font: pygame.font.Font | None = None
_small_font: pygame.font.Font | None = None
_title_font: pygame.font.Font | None = None


def _try_font(path: Path, size: int) -> pygame.font.Font | None:
    if not path.is_file():
        return None
    try:
        return pygame.font.Font(str(path), size)
    except pygame.error:
        return None


def load_ui_fonts() -> tuple[pygame.font.Font, pygame.font.Font, pygame.font.Font]:
    """Load bundled mono fonts once; fall back to pygame default."""
    global _fonts_loaded, _font, _big_font, _small_font, _title_font
    if _fonts_loaded and _font and _big_font and _small_font:
        return _font, _big_font, _small_font

    regular = _try_font(UI_FONT_REGULAR, UI_FONT_SIZE)
    bold = _try_font(UI_FONT_BOLD, UI_FONT_TITLE_SIZE)
    bold_body = _try_font(UI_FONT_BOLD, UI_FONT_SIZE)
    small = _try_font(UI_FONT_REGULAR, UI_FONT_SMALL_SIZE)

    _font = regular or pygame.font.Font(None, 28)
    _big_font = bold or bold_body or pygame.font.Font(None, 52)
    _small_font = small or pygame.font.Font(None, 20)
    _title_font = bold or _big_font
    _fonts_loaded = True
    return _font, _big_font, _small_font


def get_title_font() -> pygame.font.Font:
    if not _fonts_loaded:
        load_ui_fonts()
    assert _title_font is not None
    return _title_font


def get_small_font() -> pygame.font.Font:
    if not _fonts_loaded:
        load_ui_fonts()
    assert _small_font is not None
    return _small_font


def draw_screen_bg(surf: pygame.Surface) -> None:
    """Dark cyberpunk fill for menu / overlay backdrop."""
    surf.fill(UI_SCREEN)


def _scanlines() -> pygame.Surface:
    global _scanline_cache
    if _scanline_cache is None:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.SRCALPHA)
        for y in range(0, SCREEN_HEIGHT, 4):
            pygame.draw.line(overlay, (0, 0, 0, 36), (0, y + 2), (SCREEN_WIDTH, y + 2))
        _scanline_cache = overlay
    return _scanline_cache


def draw_scanlines(surf: pygame.Surface) -> None:
    """Subtle CRT scanline overlay (cached)."""
    surf.blit(_scanlines(), (0, 0))


def draw_title_glow(
    surf: pygame.Surface,
    text: str,
    center: tuple[int, int],
    *,
    color: tuple[int, int, int] = UI_NEON_CYAN,
    font: pygame.font.Font | None = None,
) -> pygame.Rect:
    """Title with soft cyan glow via offset multi-pass blit."""
    f = font or get_title_font()
    base = f.render(text, True, color)
    rect = base.get_rect(center=center)
    for dx, dy, alpha in (
        (-2, 0, 50),
        (2, 0, 50),
        (0, -2, 50),
        (0, 2, 50),
        (-1, -1, 35),
        (1, 1, 35),
    ):
        g = f.render(text, True, color)
        g.set_alpha(alpha)
        surf.blit(g, (rect.x + dx, rect.y + dy))
    surf.blit(base, rect)
    return rect


def draw_header_brand(
    surf: pygame.Surface,
    *,
    title: str = "BUBBLE TROUBLE",
    subtitle: str | None = None,
) -> None:
    """Top shell band: brand title + optional magenta subtitle."""
    band = pygame.Rect(0, 0, SCREEN_WIDTH, HEADER_H)
    pygame.draw.rect(surf, UI_SURFACE, band)
    pygame.draw.line(
        surf, UI_NEON_MAGENTA, (0, HEADER_H - 1), (SCREEN_WIDTH, HEADER_H - 1), 2
    )
    # Generous top padding; clear title↔subtitle gap when both present
    title_center_y = 44 if subtitle else HEADER_H // 2
    title_rect = draw_title_glow(surf, title, (SCREEN_WIDTH // 2, title_center_y))
    if subtitle:
        small = get_small_font()
        sub = small.render(subtitle, True, UI_NEON_MAGENTA)
        # midtop keeps subtitle horizontally centered under the title
        surf.blit(sub, sub.get_rect(midtop=(SCREEN_WIDTH // 2, title_rect.bottom + 16)))


def draw_footer_band(surf: pygame.Surface) -> pygame.Rect:
    """Bottom shell band background; returns the footer rect."""
    band = pygame.Rect(0, SCREEN_HEIGHT - FOOTER_H, SCREEN_WIDTH, FOOTER_H)
    pygame.draw.rect(surf, UI_SURFACE, band)
    pygame.draw.line(
        surf,
        UI_NEON_CYAN,
        (0, band.top),
        (SCREEN_WIDTH, band.top),
        1,
    )
    return band


def draw_system_line(
    surf: pygame.Surface,
    text: str = "BUBBLE TROUBLE SYSTEM V2.5",
    *,
    y: int | None = None,
) -> None:
    small = get_small_font()
    line = small.render(text, True, UI_MUTED)
    yy = y if y is not None else SCREEN_HEIGHT - 10
    surf.blit(line, line.get_rect(midbottom=(SCREEN_WIDTH // 2, yy)))


def draw_volume_segments(
    surf: pygame.Surface,
    rect: pygame.Rect,
    value: int,
    *,
    max_value: int = 10,
    fill_color: tuple[int, int, int] = UI_NEON_CYAN,
) -> None:
    """Draw a 10-segment volume bar (filled left→right)."""
    gap = 4
    empty = (17, 17, 26)
    border = (34, 34, 48)
    n = max(1, max_value)
    seg_w = max(4, (rect.width - gap * (n - 1)) // n)
    used = n * seg_w + (n - 1) * gap
    x = rect.left + max(0, (rect.width - used) // 2)
    filled = max(0, min(n, int(value)))
    for i in range(n):
        seg = pygame.Rect(x, rect.top, seg_w, rect.height)
        color = fill_color if i < filled else empty
        pygame.draw.rect(surf, color, seg)
        pygame.draw.rect(surf, border, seg, width=1)
        x += seg_w + gap


def draw_card(
    surf: pygame.Surface,
    rect: pygame.Rect,
    *,
    selected: bool = False,
    radius: int = 6,
) -> None:
    """Dark card with gold selection border or muted border."""
    fill = pygame.Surface(rect.size, flags=pygame.SRCALPHA)
    bg = (*UI_SURFACE_RAISED, 230) if selected else (*UI_SURFACE, 210)
    fill.fill(bg)
    surf.blit(fill, rect.topleft)
    border = UI_NEON_GOLD if selected else UI_IDLE_BORDER
    pygame.draw.rect(surf, border, rect, width=2, border_radius=radius)
    if selected:
        inner = rect.inflate(-6, -6)
        pygame.draw.rect(surf, UI_NEON_GOLD, inner, width=1, border_radius=max(2, radius - 2))


def draw_panel(
    surf: pygame.Surface,
    rect: pygame.Rect,
    *,
    accent: tuple[int, int, int] = UI_NEON_CYAN,
    fill: tuple[int, int, int] = UI_SURFACE,
    radius: int = 8,
) -> None:
    """Framed panel used for overlays and HUD strips."""
    pygame.draw.rect(surf, fill, rect, border_radius=radius)
    pygame.draw.rect(surf, accent, rect, width=2, border_radius=radius)
    # Magenta corner ticks
    tick = 10
    pygame.draw.line(surf, UI_NEON_MAGENTA, (rect.left, rect.top + tick), (rect.left, rect.top), 2)
    pygame.draw.line(surf, UI_NEON_MAGENTA, (rect.left, rect.top), (rect.left + tick, rect.top), 2)
    pygame.draw.line(
        surf, UI_NEON_MAGENTA, (rect.right - 1, rect.top + tick), (rect.right - 1, rect.top), 2
    )
    pygame.draw.line(
        surf, UI_NEON_MAGENTA, (rect.right - tick, rect.top), (rect.right - 1, rect.top), 2
    )


def draw_keycap(
    surf: pygame.Surface,
    label: str,
    midleft: tuple[int, int],
    *,
    font: pygame.font.Font | None = None,
) -> int:
    """Draw a small keycap pill; returns total width consumed."""
    f = font or get_small_font()
    text = f.render(label, True, UI_FG)
    pad_x, pad_y = 6, 3
    w = text.get_width() + pad_x * 2
    h = max(18, text.get_height() + pad_y * 2)
    rect = pygame.Rect(0, 0, w, h)
    rect.midleft = midleft
    pygame.draw.rect(surf, UI_SURFACE_RAISED, rect, border_radius=4)
    pygame.draw.rect(surf, UI_NEON_CYAN, rect, width=1, border_radius=4)
    surf.blit(text, text.get_rect(center=rect.center))
    return w


def draw_hint_row(
    surf: pygame.Surface,
    hints: list[tuple[list[str], str]],
    *,
    center_y: int,
    font: pygame.font.Font | None = None,
) -> None:
    """Footer hints: [(keys, label), ...] as keycaps + English labels."""
    f = font or get_small_font()
    gap_inner = 4
    gap_group = 16
    sep_w = 8

    # Measure
    widths: list[int] = []
    for keys, label in hints:
        kw = 0
        for i, k in enumerate(keys):
            tw = f.size(k)[0] + 12
            kw += tw + (gap_inner if i else 0)
        lw = f.size(label)[0]
        widths.append(kw + 6 + lw)

    total = sum(widths) + gap_group * (len(hints) - 1) + sep_w * max(0, len(hints) - 1)
    x = (SCREEN_WIDTH - total) // 2

    for gi, ((keys, label), w) in enumerate(zip(hints, widths)):
        if gi > 0:
            sep = f.render("·", True, UI_MUTED)
            surf.blit(sep, sep.get_rect(center=(x + sep_w // 2, center_y)))
            x += sep_w + 4
        for i, k in enumerate(keys):
            used = draw_keycap(surf, k, (x, center_y), font=f)
            x += used + (gap_inner if i < len(keys) - 1 else 0)
        x += 6
        lab = f.render(label, True, UI_MUTED)
        surf.blit(lab, lab.get_rect(midleft=(x, center_y)))
        x += lab.get_width() + gap_group


def draw_dim_overlay(surf: pygame.Surface) -> None:
    dim = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.SRCALPHA)
    dim.fill(UI_OVERLAY)
    surf.blit(dim, (0, 0))


def draw_overlay_panel(
    surf: pygame.Surface,
    *,
    title: str,
    title_color: tuple[int, int, int] = UI_NEON_CYAN,
    lines: list[tuple[str, tuple[int, int, int]]] | None = None,
    center_y: int | None = None,
    font: pygame.font.Font | None = None,
    big_font: pygame.font.Font | None = None,
) -> None:
    """Centered end-state / dialog panel with cyberpunk chrome."""
    f = font or (_font or load_ui_fonts()[0])
    bf = big_font or (_big_font or load_ui_fonts()[1])
    lines = lines or []
    cy = center_y if center_y is not None else SCREEN_HEIGHT // 2

    title_surf = bf.render(title, True, title_color)
    line_surfs = [f.render(text, True, color) for text, color in lines]
    content_h = title_surf.get_height() + 16 + sum(s.get_height() + 8 for s in line_surfs)
    content_w = max(
        title_surf.get_width(),
        *(s.get_width() for s in line_surfs),
        280,
    )
    panel = pygame.Rect(0, 0, content_w + 48, content_h + 40)
    panel.center = (SCREEN_WIDTH // 2, cy)
    draw_panel(surf, panel)

    y = panel.top + 20
    surf.blit(title_surf, title_surf.get_rect(midtop=(panel.centerx, y)))
    y += title_surf.get_height() + 16
    for s in line_surfs:
        surf.blit(s, s.get_rect(midtop=(panel.centerx, y)))
        y += s.get_height() + 8


def selection_color(selected: bool) -> tuple[int, int, int]:
    return UI_NEON_GOLD if selected else UI_IDLE


def arrow_color(selected: bool) -> tuple[int, int, int]:
    return UI_NEON_CYAN if selected else UI_IDLE
