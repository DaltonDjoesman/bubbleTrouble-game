"""Level definitions, loader, barriers/doors, and arena helpers."""
from __future__ import annotations

from dataclasses import dataclass

import pygame

from consts import BARRIER_CRAWL_GAP, screenHeight, screenWidth

DEFAULT_LEVEL = 1
MAX_LEVEL = 5
FLOOR_Y = screenHeight - 4


@dataclass(frozen=True)
class BallSpawn:
    tier: str
    x: float
    y: float
    vel: tuple[float, float]


@dataclass(frozen=True)
class Solid:
    """Static barrier block (balls/lasers solid; crawl gap for player)."""

    x: int
    y: int
    w: int
    h: int

    def as_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.w, self.h)


@dataclass(frozen=True)
class DoorDef:
    """Door template. Closed = solid like a barrier; open = non-solid."""

    x: int
    y: int
    w: int
    h: int
    mode: str  # "timed" | "lane_clear"
    open_ms: int = 2000
    closed_ms: int = 2000
    # lane_clear: balls whose centerx is in [lane_left, lane_right] keep door closed
    lane_left: int | None = None
    lane_right: int | None = None
    start_open: bool = False

    def as_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def lane_bounds(self) -> tuple[int, int]:
        left = self.lane_left if self.lane_left is not None else max(0, self.x - 120)
        right = self.lane_right if self.lane_right is not None else min(screenWidth, self.x + self.w + 120)
        return left, right


class DoorRuntime:
    """Mutable open/closed state for one door instance during a match."""

    def __init__(self, defn: DoorDef) -> None:
        self.defn = defn
        self.is_open = defn.start_open
        self._phase_ends_at = 0

    def reset(self, now_ms: int) -> None:
        self.is_open = self.defn.start_open
        if self.defn.mode == "timed":
            duration = self.defn.open_ms if self.is_open else self.defn.closed_ms
            self._phase_ends_at = now_ms + duration
        else:
            self._phase_ends_at = 0

    def update(self, now_ms: int, balls: pygame.sprite.Group) -> None:
        if self.defn.mode == "timed":
            if now_ms >= self._phase_ends_at:
                self.is_open = not self.is_open
                duration = self.defn.open_ms if self.is_open else self.defn.closed_ms
                self._phase_ends_at = now_ms + duration
        elif self.defn.mode == "lane_clear":
            left, right = self.defn.lane_bounds()
            any_in_lane = any(left <= b.rect.centerx <= right for b in balls)
            self.is_open = not any_in_lane

    def solid_rect(self) -> pygame.Rect | None:
        if self.is_open:
            return None
        return self.defn.as_rect()


@dataclass(frozen=True)
class LevelTheme:
    """Per-level neon palette so arenas read as distinct places."""

    bg_top: tuple[int, int, int]
    bg_bottom: tuple[int, int, int]
    barrier_fill: tuple[int, int, int]
    barrier_edge: tuple[int, int, int]
    door_fill: tuple[int, int, int]
    door_edge: tuple[int, int, int]
    door_open_edge: tuple[int, int, int]
    floor_a: tuple[int, int, int]
    floor_b: tuple[int, int, int]


@dataclass(frozen=True)
class Level:
    id: int
    name: str
    blurb: str
    balls: tuple[BallSpawn, ...]
    barriers: tuple[Solid, ...]
    doors: tuple[DoorDef, ...]
    theme: LevelTheme
    time_seconds: int = 60
    player_x: int = screenWidth // 2

    def barrier_rects(self) -> list[pygame.Rect]:
        return [b.as_rect() for b in self.barriers]

    def make_doors(self) -> list[DoorRuntime]:
        return [DoorRuntime(d) for d in self.doors]


def vertical_barrier(x: int, top: int = 40, width: int = 28) -> Solid:
    """Barrier from `top` down to crawl-gap above the floor."""
    bottom = FLOOR_Y - BARRIER_CRAWL_GAP
    return Solid(x, top, width, max(20, bottom - top))


def _level(
    level_id: int,
    name: str,
    blurb: str,
    theme: LevelTheme,
    balls: list[BallSpawn],
    barriers: list[Solid] | None = None,
    doors: list[DoorDef] | None = None,
    time_seconds: int = 60,
    player_x: int | None = None,
) -> Level:
    return Level(
        id=level_id,
        name=name,
        blurb=blurb,
        theme=theme,
        balls=tuple(balls),
        barriers=tuple(barriers or ()),
        doors=tuple(doors or ()),
        time_seconds=max(1, int(time_seconds)),
        player_x=screenWidth // 2 if player_x is None else player_x,
    )


# --- Themes -------------------------------------------------------------------

_THEME_OPEN = LevelTheme(
    bg_top=(10, 14, 28),
    bg_bottom=(18, 28, 48),
    barrier_fill=(30, 90, 140),
    barrier_edge=(80, 220, 255),
    door_fill=(80, 40, 100),
    door_edge=(200, 120, 255),
    door_open_edge=(80, 255, 180),
    floor_a=(80, 220, 255),
    floor_b=(120, 160, 255),
)
_THEME_LANES = LevelTheme(
    bg_top=(14, 10, 32),
    bg_bottom=(32, 14, 48),
    barrier_fill=(40, 70, 150),
    barrier_edge=(100, 180, 255),
    door_fill=(90, 30, 110),
    door_edge=(220, 100, 255),
    door_open_edge=(100, 255, 200),
    floor_a=(100, 180, 255),
    floor_b=(180, 100, 255),
)
_THEME_TIMED = LevelTheme(
    bg_top=(18, 8, 24),
    bg_bottom=(40, 12, 36),
    barrier_fill=(50, 80, 120),
    barrier_edge=(255, 180, 80),
    door_fill=(110, 25, 70),
    door_edge=(255, 70, 160),
    door_open_edge=(255, 220, 100),
    floor_a=(255, 180, 80),
    floor_b=(255, 70, 160),
)
_THEME_CLEAR = LevelTheme(
    bg_top=(8, 16, 28),
    bg_bottom=(12, 36, 40),
    barrier_fill=(20, 100, 90),
    barrier_edge=(60, 255, 200),
    door_fill=(30, 70, 90),
    door_edge=(80, 220, 255),
    door_open_edge=(180, 255, 120),
    floor_a=(60, 255, 200),
    floor_b=(80, 220, 255),
)
_THEME_MIX = LevelTheme(
    bg_top=(16, 6, 28),
    bg_bottom=(48, 10, 40),
    barrier_fill=(70, 40, 110),
    barrier_edge=(255, 90, 200),
    door_fill=(120, 20, 80),
    door_edge=(255, 60, 140),
    door_open_edge=(255, 200, 80),
    floor_a=(255, 90, 200),
    floor_b=(255, 200, 80),
)


# Interim pack — section 5 rewrites identities around barriers/doors.
# Platforms removed; obstacles become crawl-gap barriers.
_LEVELS: dict[int, Level] = {
    1: _level(
        1,
        "Open Floor",
        "Arena aberta · aprende a mirar",
        _THEME_OPEN,
        balls=[
            BallSpawn("M", screenWidth // 3, 180, (2.0, 0.0)),
            BallSpawn("M", 2 * screenWidth // 3, 140, (-2.0, 0.0)),
        ],
        time_seconds=45,
    ),
    2: _level(
        2,
        "Twin Lanes",
        "Barreiras estáticas · pistas",
        _THEME_LANES,
        balls=[
            BallSpawn("L", 160, 100, (2.3, 0.0)),
            BallSpawn("M", 640, 90, (-2.3, 0.0)),
        ],
        barriers=[
            vertical_barrier(280),
            vertical_barrier(500),
        ],
        time_seconds=55,
    ),
    3: _level(
        3,
        "Timed Gates",
        "Portas a tempo · atravessa no open",
        _THEME_TIMED,
        balls=[
            BallSpawn("L", 120, 90, (2.6, 0.0)),
            BallSpawn("L", 680, 90, (-2.6, 0.0)),
            BallSpawn("M", screenWidth // 2, 140, (2.2, 0.0)),
        ],
        barriers=[
            vertical_barrier(200, top=80, width=24),
            vertical_barrier(576, top=80, width=24),
        ],
        doors=[
            DoorDef(
                388,
                40,
                28,
                FLOOR_Y - BARRIER_CRAWL_GAP - 40,
                mode="timed",
                open_ms=1800,
                closed_ms=2200,
                start_open=True,
            ),
        ],
        time_seconds=70,
        player_x=200,
    ),
    4: _level(
        4,
        "Lane Clear",
        "Limpa a pista · a porta abre",
        _THEME_CLEAR,
        balls=[
            BallSpawn("L", 180, 70, (2.8, 0.0)),
            BallSpawn("L", 620, 70, (-2.8, 0.0)),
            BallSpawn("M", 400, 120, (2.2, 0.0)),
            BallSpawn("S", 500, 160, (-2.0, 0.0)),
        ],
        barriers=[
            vertical_barrier(120, width=24),
            vertical_barrier(656, width=24),
        ],
        doors=[
            DoorDef(
                386,
                40,
                28,
                FLOOR_Y - BARRIER_CRAWL_GAP - 40,
                mode="lane_clear",
                lane_left=260,
                lane_right=540,
            ),
        ],
        time_seconds=80,
        player_x=110,
    ),
    5: _level(
        5,
        "Mixed Chaos",
        "Barreiras + portas · densas bolas",
        _THEME_MIX,
        balls=[
            BallSpawn("L", 100, 55, (3.0, 0.0)),
            BallSpawn("L", 700, 55, (-3.0, 0.0)),
            BallSpawn("L", 400, 70, (2.7, 0.0)),
            BallSpawn("M", 250, 120, (-2.5, 0.0)),
            BallSpawn("M", 550, 120, (2.5, 0.0)),
        ],
        barriers=[
            vertical_barrier(160, width=24),
            vertical_barrier(616, width=24),
        ],
        doors=[
            DoorDef(
                300,
                40,
                26,
                FLOOR_Y - BARRIER_CRAWL_GAP - 40,
                mode="timed",
                open_ms=1500,
                closed_ms=2000,
                start_open=False,
            ),
            DoorDef(
                474,
                40,
                26,
                FLOOR_Y - BARRIER_CRAWL_GAP - 40,
                mode="lane_clear",
                lane_left=400,
                lane_right=620,
            ),
        ],
        time_seconds=90,
    ),
}


def get_level(level_id: int) -> Level:
    """Return a level by id, clamping to the authored pack."""
    clamped = max(DEFAULT_LEVEL, min(int(level_id), MAX_LEVEL))
    return _LEVELS[clamped]


def list_levels() -> list[Level]:
    """All levels in id order (for menu / tooling)."""
    return [_LEVELS[i] for i in range(DEFAULT_LEVEL, MAX_LEVEL + 1)]


def collect_solids(
    level: Level,
    doors: list[DoorRuntime] | None = None,
) -> list[pygame.Rect]:
    """Barrier + closed-door rects for ball/laser/player collision."""
    solids = level.barrier_rects()
    for door in doors or []:
        rect = door.solid_rect()
        if rect is not None:
            solids.append(rect)
    return solids


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


def draw_arena_geometry(
    screen: pygame.Surface,
    level: Level,
    doors: list[DoorRuntime] | None = None,
) -> None:
    """Draw barriers and doors (no platform shelves)."""
    theme = level.theme

    for solid in level.barriers:
        rect = solid.as_rect()
        pygame.draw.rect(screen, theme.barrier_fill, rect, border_radius=2)
        pygame.draw.rect(screen, theme.barrier_edge, rect, width=2, border_radius=2)
        mid_x = rect.centerx
        pygame.draw.line(
            screen,
            theme.barrier_edge,
            (mid_x, rect.top + 4),
            (mid_x, rect.bottom - 4),
            1,
        )

    runtime = list(doors or [])
    for i, defn in enumerate(level.doors):
        rect = defn.as_rect()
        is_open = runtime[i].is_open if i < len(runtime) else False
        if is_open:
            # Ghost outline when open
            pygame.draw.rect(screen, theme.door_open_edge, rect, width=2, border_radius=2)
            for y in range(rect.top + 6, rect.bottom - 4, 10):
                pygame.draw.line(
                    screen,
                    theme.door_open_edge,
                    (rect.left + 4, y),
                    (rect.right - 5, y),
                    1,
                )
        else:
            pygame.draw.rect(screen, theme.door_fill, rect, border_radius=2)
            pygame.draw.rect(screen, theme.door_edge, rect, width=2, border_radius=2)
            mid_x = rect.centerx
            pygame.draw.line(
                screen,
                theme.door_edge,
                (mid_x, rect.top + 4),
                (mid_x, rect.bottom - 4),
                2,
            )
