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
class Level:
    id: int
    name: str
    balls: tuple[BallSpawn, ...]
    platforms: tuple[Solid, ...]
    obstacles: tuple[Solid, ...]

    def solid_rects(self) -> list[pygame.Rect]:
        return [s.as_rect() for s in self.platforms] + [
            s.as_rect() for s in self.obstacles
        ]


def _level(
    level_id: int,
    name: str,
    balls: list[BallSpawn],
    platforms: list[Solid] | None = None,
    obstacles: list[Solid] | None = None,
) -> Level:
    return Level(
        id=level_id,
        name=name,
        balls=tuple(balls),
        platforms=tuple(platforms or ()),
        obstacles=tuple(obstacles or ()),
    )


# --- Authored pack (difficulty rising) ---------------------------------------

_LEVELS: dict[int, Level] = {
    1: _level(
        1,
        "Open Floor",
        balls=[
            BallSpawn("M", screenWidth // 3, screenHeight // 3, (2.0, 0.0)),
            BallSpawn("M", 2 * screenWidth // 3, screenHeight // 4, (-2.0, 0.0)),
        ],
        platforms=[
            Solid(280, 420, 240, 18),
        ],
    ),
    2: _level(
        2,
        "Twin Shelves",
        balls=[
            BallSpawn("L", screenWidth // 4, 120, (2.2, 0.0)),
            BallSpawn("M", 3 * screenWidth // 4, 100, (-2.2, 0.0)),
        ],
        platforms=[
            Solid(80, 380, 200, 18),
            Solid(520, 380, 200, 18),
        ],
    ),
    3: _level(
        3,
        "Corridor",
        balls=[
            BallSpawn("L", screenWidth // 2, 100, (2.5, 0.0)),
            BallSpawn("M", 150, 160, (-2.0, 0.0)),
            BallSpawn("M", 650, 160, (2.0, 0.0)),
        ],
        platforms=[
            Solid(40, 320, 160, 18),
            Solid(600, 320, 160, 18),
            Solid(280, 450, 240, 18),
        ],
        obstacles=[
            Solid(370, 250, 60, 100),
        ],
    ),
    4: _level(
        4,
        "High Ground",
        balls=[
            BallSpawn("L", 200, 80, (2.8, 0.0)),
            BallSpawn("L", 600, 80, (-2.8, 0.0)),
            BallSpawn("M", screenWidth // 2, 140, (2.0, 0.0)),
        ],
        platforms=[
            Solid(60, 280, 180, 18),
            Solid(560, 280, 180, 18),
            Solid(260, 400, 280, 18),
            Solid(120, 480, 140, 18),
            Solid(540, 480, 140, 18),
        ],
        obstacles=[
            Solid(380, 180, 40, 80),
        ],
    ),
    5: _level(
        5,
        "Dense Arena",
        balls=[
            BallSpawn("L", 150, 70, (3.0, 0.0)),
            BallSpawn("L", 650, 70, (-3.0, 0.0)),
            BallSpawn("L", screenWidth // 2, 90, (2.4, 0.0)),
            BallSpawn("M", 300, 150, (-2.2, 0.0)),
            BallSpawn("M", 500, 150, (2.2, 0.0)),
        ],
        platforms=[
            Solid(40, 240, 140, 18),
            Solid(620, 240, 140, 18),
            Solid(220, 340, 160, 18),
            Solid(420, 340, 160, 18),
            Solid(100, 460, 200, 18),
            Solid(500, 460, 200, 18),
            Solid(300, 520, 200, 18),
        ],
        obstacles=[
            Solid(300, 200, 50, 90),
            Solid(450, 200, 50, 90),
            Solid(375, 380, 50, 70),
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


def draw_arena_geometry(screen: pygame.Surface, level: Level) -> None:
    """Draw platforms (cyan) and obstacles (magenta) distinctly."""
    platform_fill = (40, 120, 160)
    platform_edge = (80, 240, 255)
    obstacle_fill = (100, 30, 90)
    obstacle_edge = (255, 70, 180)

    for solid in level.platforms:
        rect = solid.as_rect()
        pygame.draw.rect(screen, platform_fill, rect, border_radius=3)
        pygame.draw.rect(screen, platform_edge, rect, width=2, border_radius=3)
        # Top lip highlight
        pygame.draw.line(
            screen, platform_edge, (rect.left + 2, rect.top + 1), (rect.right - 3, rect.top + 1), 2
        )

    for solid in level.obstacles:
        rect = solid.as_rect()
        pygame.draw.rect(screen, obstacle_fill, rect, border_radius=2)
        pygame.draw.rect(screen, obstacle_edge, rect, width=2, border_radius=2)
        # Cross hatch hint so obstacles read as blockers
        mid_x = rect.centerx
        pygame.draw.line(screen, obstacle_edge, (mid_x, rect.top + 4), (mid_x, rect.bottom - 4), 1)
