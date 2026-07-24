"""Level definitions, loader, and arena solid helpers."""
from __future__ import annotations

from dataclasses import dataclass

import pygame

from consts import screenHeight, screenWidth

DEFAULT_LEVEL = 1
MAX_LEVEL = 5


@dataclass(frozen=True)
class BallSpawn:
    tier: str
    x: float
    y: float
    vel: tuple[float, float]


@dataclass(frozen=True)
class Solid:
    x: int
    y: int
    w: int
    h: int

    def as_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.w, self.h)


@dataclass(frozen=True)
class LevelTheme:
    """Per-level neon palette so arenas read as distinct places."""

    bg_top: tuple[int, int, int]
    bg_bottom: tuple[int, int, int]
    platform_fill: tuple[int, int, int]
    platform_edge: tuple[int, int, int]
    obstacle_fill: tuple[int, int, int]
    obstacle_edge: tuple[int, int, int]
    floor_a: tuple[int, int, int]
    floor_b: tuple[int, int, int]


@dataclass(frozen=True)
class Level:
    id: int
    name: str
    blurb: str
    balls: tuple[BallSpawn, ...]
    platforms: tuple[Solid, ...]
    obstacles: tuple[Solid, ...]
    theme: LevelTheme
    player_x: int = screenWidth // 2

    def solid_rects(self) -> list[pygame.Rect]:
        return [s.as_rect() for s in self.platforms] + [
            s.as_rect() for s in self.obstacles
        ]


def _level(
    level_id: int,
    name: str,
    blurb: str,
    theme: LevelTheme,
    balls: list[BallSpawn],
    platforms: list[Solid] | None = None,
    obstacles: list[Solid] | None = None,
    player_x: int | None = None,
) -> Level:
    return Level(
        id=level_id,
        name=name,
        blurb=blurb,
        theme=theme,
        balls=tuple(balls),
        platforms=tuple(platforms or ()),
        obstacles=tuple(obstacles or ()),
        player_x=screenWidth // 2 if player_x is None else player_x,
    )


# --- Themes -------------------------------------------------------------------

_THEME_OPEN = LevelTheme(
    bg_top=(10, 14, 28),
    bg_bottom=(18, 28, 48),
    platform_fill=(30, 90, 140),
    platform_edge=(80, 220, 255),
    obstacle_fill=(80, 40, 100),
    obstacle_edge=(200, 120, 255),
    floor_a=(80, 220, 255),
    floor_b=(120, 160, 255),
)
_THEME_SHELVES = LevelTheme(
    bg_top=(14, 10, 32),
    bg_bottom=(32, 14, 48),
    platform_fill=(40, 70, 150),
    platform_edge=(100, 180, 255),
    obstacle_fill=(90, 30, 110),
    obstacle_edge=(220, 100, 255),
    floor_a=(100, 180, 255),
    floor_b=(180, 100, 255),
)
_THEME_CORRIDOR = LevelTheme(
    bg_top=(18, 8, 24),
    bg_bottom=(40, 12, 36),
    platform_fill=(50, 80, 120),
    platform_edge=(255, 180, 80),
    obstacle_fill=(110, 25, 70),
    obstacle_edge=(255, 70, 160),
    floor_a=(255, 180, 80),
    floor_b=(255, 70, 160),
)
_THEME_HIGH = LevelTheme(
    bg_top=(8, 16, 28),
    bg_bottom=(12, 36, 40),
    platform_fill=(20, 100, 90),
    platform_edge=(60, 255, 200),
    obstacle_fill=(30, 70, 90),
    obstacle_edge=(80, 220, 255),
    floor_a=(60, 255, 200),
    floor_b=(80, 220, 255),
)
_THEME_DENSE = LevelTheme(
    bg_top=(16, 6, 28),
    bg_bottom=(48, 10, 40),
    platform_fill=(70, 40, 110),
    platform_edge=(255, 90, 200),
    obstacle_fill=(120, 20, 80),
    obstacle_edge=(255, 60, 140),
    floor_a=(255, 90, 200),
    floor_b=(255, 200, 80),
)


# --- Authored pack (each level has a clear identity) -------------------------

_LEVELS: dict[int, Level] = {
    # 1 — Wide open tutor: one island, few mediums
    1: _level(
        1,
        "Open Floor",
        "Arena aberta · aprende a mirar",
        _THEME_OPEN,
        balls=[
            BallSpawn("M", screenWidth // 3, 180, (2.0, 0.0)),
            BallSpawn("M", 2 * screenWidth // 3, 140, (-2.0, 0.0)),
        ],
        platforms=[
            Solid(270, 430, 260, 16),
        ],
    ),
    # 2 — Two side shelves, open pit in the middle
    2: _level(
        2,
        "Twin Shelves",
        "Duas prateleiras · centro livre",
        _THEME_SHELVES,
        balls=[
            BallSpawn("L", 160, 100, (2.3, 0.0)),
            BallSpawn("M", 640, 90, (-2.3, 0.0)),
        ],
        platforms=[
            Solid(40, 340, 220, 16),
            Solid(540, 340, 220, 16),
            Solid(300, 480, 200, 16),
        ],
    ),
    # 3 — Central pillar splits lanes; play around it
    3: _level(
        3,
        "Corridor",
        "Pilar central · duas pistas",
        _THEME_CORRIDOR,
        balls=[
            BallSpawn("L", 120, 90, (2.6, 0.0)),
            BallSpawn("L", 680, 90, (-2.6, 0.0)),
            BallSpawn("M", screenWidth // 2, 140, (2.2, 0.0)),
        ],
        platforms=[
            Solid(40, 280, 200, 16),
            Solid(560, 280, 200, 16),
            Solid(40, 440, 240, 16),
            Solid(520, 440, 240, 16),
        ],
        obstacles=[
            Solid(378, 200, 44, 200),
        ],
        player_x=200,
    ),
    # 4 — Stair climb on the left, drop shaft on the right
    4: _level(
        4,
        "High Ground",
        "Escada à esquerda · queda à direita",
        _THEME_HIGH,
        balls=[
            BallSpawn("L", 180, 70, (2.8, 0.0)),
            BallSpawn("L", 620, 70, (-2.8, 0.0)),
            BallSpawn("M", 400, 120, (2.2, 0.0)),
            BallSpawn("S", 500, 160, (-2.0, 0.0)),
        ],
        platforms=[
            Solid(40, 480, 140, 16),
            Solid(100, 400, 140, 16),
            Solid(160, 320, 140, 16),
            Solid(220, 240, 140, 16),
            Solid(520, 360, 200, 16),
            Solid(560, 480, 180, 16),
        ],
        obstacles=[
            Solid(380, 280, 36, 90),
        ],
        player_x=110,
    ),
    # 5 — Dense staggered shelves + flanking bounce walls
    5: _level(
        5,
        "Dense Arena",
        "Caos total · muitas ricochetes",
        _THEME_DENSE,
        balls=[
            BallSpawn("L", 100, 55, (3.0, 0.0)),
            BallSpawn("L", 700, 55, (-3.0, 0.0)),
            BallSpawn("L", 400, 70, (2.7, 0.0)),
            BallSpawn("M", 250, 120, (-2.5, 0.0)),
            BallSpawn("M", 550, 120, (2.5, 0.0)),
        ],
        platforms=[
            Solid(50, 170, 130, 16),
            Solid(620, 170, 130, 16),
            Solid(180, 270, 130, 16),
            Solid(490, 290, 130, 16),
            Solid(50, 380, 150, 16),
            Solid(600, 400, 150, 16),
            Solid(200, 490, 130, 16),
            Solid(470, 490, 130, 16),
        ],
        obstacles=[
            Solid(310, 190, 30, 60),
            Solid(460, 320, 30, 60),
            Solid(385, 420, 30, 50),
        ],
    ),
}


def get_level(level_id: int) -> Level:
    """Return a level by id, clamping to the authored pack."""
    clamped = max(DEFAULT_LEVEL, min(int(level_id), MAX_LEVEL))
    return _LEVELS[clamped]


def list_levels() -> list[Level]:
    """All levels in id order (for menu / tooling)."""
    return [_LEVELS[i] for i in range(DEFAULT_LEVEL, MAX_LEVEL + 1)]


def build_arena_background(theme: LevelTheme) -> pygame.Surface:
    """Vertical gradient + scanlines + themed floor accent."""
    surf = pygame.Surface((screenWidth, screenHeight))
    for y in range(screenHeight):
        t = y / max(1, screenHeight - 1)
        r = int(theme.bg_top[0] + (theme.bg_bottom[0] - theme.bg_top[0]) * t)
        g = int(theme.bg_top[1] + (theme.bg_bottom[1] - theme.bg_top[1]) * t)
        b = int(theme.bg_top[2] + (theme.bg_bottom[2] - theme.bg_top[2]) * t)
        pygame.draw.line(surf, (r, g, b), (0, y), (screenWidth, y))
    for y in range(2, screenHeight, 4):
        pygame.draw.line(surf, (0, 0, 0), (0, y), (screenWidth, y))
    pygame.draw.line(
        surf, theme.floor_a, (0, screenHeight - 3), (screenWidth, screenHeight - 3), 2
    )
    pygame.draw.line(
        surf, theme.floor_b, (0, screenHeight - 6), (screenWidth, screenHeight - 6), 1
    )
    return surf


def draw_arena_geometry(screen: pygame.Surface, level: Level) -> None:
    """Draw platforms and obstacles with the level theme colors."""
    theme = level.theme

    for solid in level.platforms:
        rect = solid.as_rect()
        pygame.draw.rect(screen, theme.platform_fill, rect, border_radius=3)
        pygame.draw.rect(screen, theme.platform_edge, rect, width=2, border_radius=3)
        pygame.draw.line(
            screen,
            theme.platform_edge,
            (rect.left + 2, rect.top + 1),
            (rect.right - 3, rect.top + 1),
            2,
        )

    for solid in level.obstacles:
        rect = solid.as_rect()
        pygame.draw.rect(screen, theme.obstacle_fill, rect, border_radius=2)
        pygame.draw.rect(screen, theme.obstacle_edge, rect, width=2, border_radius=2)
        mid_x = rect.centerx
        pygame.draw.line(
            screen,
            theme.obstacle_edge,
            (mid_x, rect.top + 4),
            (mid_x, rect.bottom - 4),
            1,
        )
