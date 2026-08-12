"""Level definitions, loader, barriers/doors, and arena helpers."""
from __future__ import annotations

from dataclasses import dataclass

import pygame

from consts import (
    BARRIER_CRAWL_GAP,
    CEILING_Y,
    FLOOR_Y,
    PLAY_BOTTOM,
    PLAY_HEIGHT,
    PLAY_TOP,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)

DEFAULT_LEVEL = 1
# Campaign arenas that can be cleared / auto-advanced (Survival is separate).
MAX_CAMPAIGN_LEVEL = 5
# Last selectable entry (includes Survival).
MAX_LEVEL = 6
SURVIVAL_LEVEL_ID = 6


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
        right = self.lane_right if self.lane_right is not None else min(SCREEN_WIDTH, self.x + self.w + 120)
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
    player_x: int = SCREEN_WIDTH // 2
    survival: bool = False

    def barrier_rects(self) -> list[pygame.Rect]:
        return [b.as_rect() for b in self.barriers]

    def make_doors(self) -> list[DoorRuntime]:
        return [DoorRuntime(d) for d in self.doors]


def vertical_barrier(x: int, top: int | None = None, width: int = 28) -> Solid:
    """Barrier from below the spike band down to crawl-gap above the floor."""
    if top is None:
        top = CEILING_Y + 8
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
    survival: bool = False,
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
        player_x=SCREEN_WIDTH // 2 if player_x is None else player_x,
        survival=survival,
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
_THEME_SURVIVAL = LevelTheme(
    bg_top=(22, 4, 18),
    bg_bottom=(56, 8, 28),
    barrier_fill=(90, 30, 50),
    barrier_edge=(255, 80, 120),
    door_fill=(100, 20, 50),
    door_edge=(255, 100, 140),
    door_open_edge=(255, 200, 100),
    floor_a=(255, 80, 120),
    floor_b=(255, 160, 80),
)


# Classic five: open → barriers → timed → lane-clear → mix
_LEVELS: dict[int, Level] = {
    # L1 — Open tutor: move, shoot, watch the time bar
    1: _level(
        1,
        "Open Floor",
        "No barriers · learn aiming and the timer",
        _THEME_OPEN,
        balls=[
            BallSpawn("M", 220, 160, (2.0, 0.0)),
            BallSpawn("M", 580, 120, (-2.0, 0.0)),
        ],
        time_seconds=40,
        player_x=SCREEN_WIDTH // 2,
    ),
    # L2 — Static vertical barriers create lanes; crawl underneath
    2: _level(
        2,
        "Barrier Lanes",
        "Static barriers · crawl underneath",
        _THEME_LANES,
        balls=[
            BallSpawn("L", 140, 90, (2.2, 0.0)),
            BallSpawn("M", 400, 110, (-2.4, 0.0)),
            BallSpawn("L", 660, 90, (-2.2, 0.0)),
        ],
        barriers=[
            vertical_barrier(260, top=36, width=26),
            vertical_barrier(514, top=36, width=26),
        ],
        time_seconds=55,
        player_x=SCREEN_WIDTH // 2,
    ),
    # L3 — Timed central door cycles open/closed
    3: _level(
        3,
        "Timed Gates",
        "Timed door · cross while open",
        _THEME_TIMED,
        balls=[
            BallSpawn("L", 100, 80, (2.5, 0.0)),
            BallSpawn("L", 700, 80, (-2.5, 0.0)),
            BallSpawn("M", 400, 130, (2.0, 0.0)),
        ],
        barriers=[
            vertical_barrier(180, top=60, width=24),
            vertical_barrier(596, top=60, width=24),
        ],
        doors=[
            DoorDef(
                386,
                36,
                28,
                FLOOR_Y - BARRIER_CRAWL_GAP - 36,
                mode="timed",
                open_ms=2000,
                closed_ms=2000,
                start_open=True,
            ),
        ],
        time_seconds=70,
        player_x=120,
    ),
    # L4 — Clear the center lane to open the door
    4: _level(
        4,
        "Lane Clear",
        "Clear the center lane · door opens",
        _THEME_CLEAR,
        balls=[
            BallSpawn("L", 360, 70, (2.4, 0.0)),
            BallSpawn("M", 420, 110, (-2.2, 0.0)),
            BallSpawn("S", 300, 150, (2.0, 0.0)),
            BallSpawn("L", 680, 80, (-2.6, 0.0)),
        ],
        barriers=[
            vertical_barrier(200, top=40, width=24),
            vertical_barrier(576, top=40, width=24),
        ],
        doors=[
            DoorDef(
                386,
                36,
                28,
                FLOOR_Y - BARRIER_CRAWL_GAP - 36,
                mode="lane_clear",
                lane_left=230,
                lane_right=560,
            ),
        ],
        time_seconds=85,
        player_x=100,
    ),
    # L5 — Mix timed + lane-clear + denser balls
    5: _level(
        5,
        "Mixed Chaos",
        "Mixed doors · dense balls · more time",
        _THEME_MIX,
        balls=[
            BallSpawn("L", 90, 55, (2.8, 0.0)),
            BallSpawn("L", 710, 55, (-2.8, 0.0)),
            BallSpawn("L", 400, 70, (2.5, 0.0)),
            BallSpawn("M", 240, 120, (-2.3, 0.0)),
            BallSpawn("M", 560, 120, (2.3, 0.0)),
            BallSpawn("S", 480, 160, (-2.0, 0.0)),
        ],
        barriers=[
            vertical_barrier(140, top=40, width=24),
            vertical_barrier(636, top=40, width=24),
        ],
        doors=[
            DoorDef(
                290,
                36,
                26,
                FLOOR_Y - BARRIER_CRAWL_GAP - 36,
                mode="timed",
                open_ms=1600,
                closed_ms=1800,
                start_open=False,
            ),
            DoorDef(
                484,
                36,
                26,
                FLOOR_Y - BARRIER_CRAWL_GAP - 36,
                mode="lane_clear",
                lane_left=320,
                lane_right=630,
            ),
        ],
        time_seconds=100,
        player_x=SCREEN_WIDTH // 2,
    ),
    # L6 — Endless Survival (no drain, no clear-all win)
    6: _level(
        SURVIVAL_LEVEL_ID,
        "Survival",
        "Endless · chronometer · best time wins",
        _THEME_SURVIVAL,
        balls=[
            BallSpawn("S", 280, 140, (2.0, 0.0)),
            BallSpawn("S", 520, 120, (-2.0, 0.0)),
        ],
        time_seconds=1,
        player_x=SCREEN_WIDTH // 2,
        survival=True,
    ),
}


def get_level(level_id: int) -> Level:
    """Return a level by id, clamping to the authored pack (campaign + Survival)."""
    clamped = max(DEFAULT_LEVEL, min(int(level_id), MAX_LEVEL))
    return _LEVELS[clamped]


def list_levels() -> list[Level]:
    """All selectable levels in id order (campaign then Survival)."""
    return [_LEVELS[i] for i in range(DEFAULT_LEVEL, MAX_LEVEL + 1)]


def is_survival_level(level: Level | int) -> bool:
    """True when the level (or id) is Survival mode."""
    if isinstance(level, Level):
        return level.survival
    return get_level(level).survival


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


def build_arena_background(
    theme: LevelTheme,
    *,
    fill_window: bool = False,
) -> pygame.Surface:
    """Cyberpunk gradient + scanlines + floor accent.

    During play (`fill_window=False`), art fills only the play rect so the
    bottom status panel stays chrome. Menu uses `fill_window=True` for a
    full-bleed backdrop.
    """
    surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    if fill_window:
        top, bottom = 0, SCREEN_HEIGHT
        height = SCREEN_HEIGHT
        surf.fill(theme.bg_bottom)
    else:
        top, bottom = PLAY_TOP, PLAY_BOTTOM
        height = PLAY_HEIGHT
        # Reserved bottom panel stays chrome (drawn each frame)
        surf.fill((28, 16, 12))

    for y in range(top, bottom):
        t = (y - top) / max(1, height - 1)
        r = int(theme.bg_top[0] + (theme.bg_bottom[0] - theme.bg_top[0]) * t)
        g = int(theme.bg_top[1] + (theme.bg_bottom[1] - theme.bg_top[1]) * t)
        b = int(theme.bg_top[2] + (theme.bg_bottom[2] - theme.bg_top[2]) * t)
        pygame.draw.line(surf, (r, g, b), (0, y), (SCREEN_WIDTH, y))
    for y in range(top + 2, bottom, 4):
        pygame.draw.line(surf, (0, 0, 0), (0, y), (SCREEN_WIDTH, y))

    # Menu full-bleed: subtle floor accent. In-play the brick HUD edge is the floor seam.
    if fill_window:
        floor_y = SCREEN_HEIGHT
        pygame.draw.line(
            surf, theme.floor_a, (0, floor_y - 2), (SCREEN_WIDTH, floor_y - 2), 2
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
