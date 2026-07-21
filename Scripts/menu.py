"""Main menu: Play/Quit, mode, level; audio in Options submenu."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

import pygame

from consts import VOLUME_MAX, screenHeight, screenWidth
from levels import DEFAULT_LEVEL, MAX_LEVEL, get_level

if TYPE_CHECKING:
    from audio import AudioManager

_NEON_CYAN = (80, 240, 255)
_HUD_DIM = (180, 200, 220)
_TITLE = (230, 240, 255)
_SELECTED = (255, 220, 80)
_CARD_BG = (18, 12, 40, 210)
_CARD_BORDER = (90, 70, 140)
_CARD_BORDER_SEL = (255, 220, 80)
_ARROW = (80, 240, 255)
_HINT_DIM = (140, 160, 190)

_CARD_W = 360
_CARD_H = 48
_CARD_GAP = 12

MODES = ("1P", "2P")

Screen = Literal["root", "options"]


@dataclass
class MenuAction:
    """Result of handling a menu key; Game applies side effects."""

    start_game: bool = False
    quit_app: bool = False


class MainMenu:
    """Root: Play / Mode / Level / Options / Quit. Options: Music / SFX / Back."""

    def __init__(
        self,
        font: pygame.font.Font,
        big_font: pygame.font.Font,
        audio: AudioManager | None,
        *,
        mode: str = "1P",
        level: int = DEFAULT_LEVEL,
        max_level: int = MAX_LEVEL,
    ) -> None:
        self.font = font
        self.big_font = big_font
        self.audio = audio
        self.screen: Screen = "root"
        self.selected = 0
        self._root_selected = 0
        self.mode = mode if mode in MODES else "1P"
        self.max_level = max(1, max_level)
        self.level = max(1, min(level, self.max_level))

    def _items(self) -> list[tuple[str, str]]:
        if self.screen == "options":
            music = self.audio.music_volume if self.audio else 0
            sfx = self.audio.sfx_volume if self.audio else 0
            return [
                ("music", f"Music   {music}/{VOLUME_MAX}"),
                ("sfx", f"SFX     {sfx}/{VOLUME_MAX}"),
                ("back", "Back"),
            ]
        return [
            ("play", "Play"),
            ("mode", f"Mode    {self.mode}"),
            ("level", f"Level   {self.level}/{self.max_level}"),
            ("options", "Options"),
            ("quit", "Quit"),
        ]

    def _enter_options(self) -> None:
        self._root_selected = self.selected
        self.screen = "options"
        self.selected = 0
        self._sfx("ui_confirm")

    def _leave_options(self) -> None:
        self.screen = "root"
        self.selected = self._root_selected
        self._sfx("ui_select")

    def handle_keydown(self, key: int) -> MenuAction:
        items = self._items()
        n = len(items)
        action = MenuAction()

        if key == pygame.K_ESCAPE:
            if self.screen == "options":
                self._leave_options()
            return action

        if key in (pygame.K_UP, pygame.K_w):
            self.selected = (self.selected - 1) % n
            self._sfx("ui_select")
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.selected = (self.selected + 1) % n
            self._sfx("ui_select")
        elif key in (pygame.K_LEFT, pygame.K_a):
            self._nudge_field(-1)
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self._nudge_field(+1)
        elif key in (pygame.K_RETURN, pygame.K_SPACE):
            kind = items[self.selected][0]
            if kind == "play":
                self._sfx("ui_confirm")
                action.start_game = True
            elif kind == "quit":
                self._sfx("ui_confirm")
                action.quit_app = True
            elif kind == "options":
                self._enter_options()
            elif kind == "back":
                self._leave_options()
            elif kind in ("mode", "level", "music", "sfx"):
                self._nudge_field(+1)
        return action

    def _nudge_field(self, delta: int) -> None:
        kind = self._items()[self.selected][0]
        if kind == "mode":
            idx = MODES.index(self.mode)
            self.mode = MODES[(idx + delta) % len(MODES)]
            self._sfx("ui_select")
        elif kind == "level":
            self.level = ((self.level - 1 + delta) % self.max_level) + 1
            self._sfx("ui_select")
        elif kind in ("music", "sfx"):
            self._adjust_volume(delta)

    def _adjust_volume(self, delta: int) -> None:
        if self.audio is None:
            return
        kind = self._items()[self.selected][0]
        if kind == "music":
            self.audio.adjust_music_volume(delta)
            self.audio.save_settings()
            self.audio.play_music()
            self._sfx("ui_select")
        elif kind == "sfx":
            self.audio.adjust_sfx_volume(delta)
            self.audio.save_settings()
            self._sfx("ui_select")

    def _sfx(self, name: str) -> None:
        if self.audio is not None:
            self.audio.play_sfx(name)

    @staticmethod
    def _draw_arrow_left(surf: pygame.Surface, cx: int, cy: int, size: int, color: tuple) -> None:
        points = [
            (cx + size // 2, cy - size // 2),
            (cx - size // 2, cy),
            (cx + size // 2, cy + size // 2),
        ]
        pygame.draw.polygon(surf, color, points)

    @staticmethod
    def _draw_arrow_right(surf: pygame.Surface, cx: int, cy: int, size: int, color: tuple) -> None:
        points = [
            (cx - size // 2, cy - size // 2),
            (cx + size // 2, cy),
            (cx - size // 2, cy + size // 2),
        ]
        pygame.draw.polygon(surf, color, points)

    def draw(self, screen: pygame.Surface) -> None:
        title = self.big_font.render("Bubble Trouble", True, _TITLE)
        screen.blit(
            title, title.get_rect(center=(screenWidth // 2, screenHeight // 2 - 160))
        )
        if self.screen == "options":
            subtitle = self.font.render("Options", True, _NEON_CYAN)
            screen.blit(
                subtitle,
                subtitle.get_rect(center=(screenWidth // 2, screenHeight // 2 - 118)),
            )

        items = self._items()
        total_h = len(items) * _CARD_H + (len(items) - 1) * _CARD_GAP
        start_y = screenHeight // 2 - total_h // 2 + 20
        cx = screenWidth // 2

        for i, (kind, label) in enumerate(items):
            selected = i == self.selected
            card_rect = pygame.Rect(0, 0, _CARD_W, _CARD_H)
            card_rect.center = (cx, start_y + i * (_CARD_H + _CARD_GAP) + _CARD_H // 2)

            card = pygame.Surface((_CARD_W, _CARD_H), flags=pygame.SRCALPHA)
            card.fill(_CARD_BG)
            screen.blit(card, card_rect.topleft)
            border = _CARD_BORDER_SEL if selected else _CARD_BORDER
            pygame.draw.rect(screen, border, card_rect, width=2, border_radius=8)
            if selected:
                inner = card_rect.inflate(-6, -6)
                pygame.draw.rect(screen, _NEON_CYAN, inner, width=1, border_radius=6)

            text_color = _SELECTED if selected else _HUD_DIM

            if kind in ("mode", "level", "music", "sfx"):
                if kind == "mode":
                    name, value = "Mode", self.mode
                elif kind == "level":
                    lvl = get_level(self.level)
                    name, value = "Level", f"{self.level}·{lvl.name}"
                elif kind == "music":
                    name = "Music"
                    value = f"{self.audio.music_volume if self.audio else 0}/{VOLUME_MAX}"
                else:
                    name = "SFX"
                    value = f"{self.audio.sfx_volume if self.audio else 0}/{VOLUME_MAX}"

                name_surf = self.font.render(name, True, text_color)
                val_surf = self.font.render(value, True, text_color)
                name_rect = name_surf.get_rect(midleft=(card_rect.left + 28, card_rect.centery))
                screen.blit(name_surf, name_rect)

                cluster_cx = card_rect.right - 100
                cy = card_rect.centery
                arrow_color = _ARROW if selected else _HUD_DIM
                self._draw_arrow_left(screen, cluster_cx - 42, cy, 14, arrow_color)
                val_rect = val_surf.get_rect(center=(cluster_cx, cy))
                screen.blit(val_surf, val_rect)
                self._draw_arrow_right(screen, cluster_cx + 42, cy, 14, arrow_color)
            else:
                text = self.font.render(label, True, text_color)
                screen.blit(text, text.get_rect(center=card_rect.center))

        self._draw_hints(screen)

    def _draw_hints(self, screen: pygame.Surface) -> None:
        """Footer: control legend; Esc appears while in Options."""
        y = screenHeight - 40
        parts: list[tuple[str, str | None]] = [
            ("nav", None),
            ("text", "mover"),
            ("sep", None),
            ("vol", None),
            ("text", "ajustar"),
            ("sep", None),
            ("text", "Enter"),
            ("text_dim", "confirmar"),
        ]
        if self.screen == "options":
            parts.extend(
                [
                    ("sep", None),
                    ("text", "Esc"),
                    ("text_dim", "voltar"),
                ]
            )

        gap = 8
        widths: list[int] = []
        for kind, payload in parts:
            if kind in ("nav", "vol"):
                widths.append(28)
            elif kind == "sep":
                widths.append(10)
            else:
                widths.append(self.font.size(payload or "")[0])
        total_w = sum(widths) + gap * (len(parts) - 1)
        x = (screenWidth - total_w) // 2

        for (kind, payload), w in zip(parts, widths):
            if kind == "nav":
                self._draw_arrow_up(screen, x + 6, y, 10, _NEON_CYAN)
                self._draw_arrow_down(screen, x + 20, y, 10, _NEON_CYAN)
            elif kind == "vol":
                self._draw_arrow_left(screen, x + 6, y, 10, _NEON_CYAN)
                self._draw_arrow_right(screen, x + 20, y, 10, _NEON_CYAN)
            elif kind == "sep":
                dot = self.font.render("·", True, _HINT_DIM)
                screen.blit(dot, dot.get_rect(center=(x + w // 2, y)))
            elif kind == "text":
                surf = self.font.render(payload or "", True, _NEON_CYAN)
                screen.blit(surf, surf.get_rect(midleft=(x, y)))
            elif kind == "text_dim":
                surf = self.font.render(payload or "", True, _HINT_DIM)
                screen.blit(surf, surf.get_rect(midleft=(x, y)))
            x += w + gap

    @staticmethod
    def _draw_arrow_up(surf: pygame.Surface, cx: int, cy: int, size: int, color: tuple) -> None:
        points = [
            (cx, cy - size // 2),
            (cx - size // 2, cy + size // 2),
            (cx + size // 2, cy + size // 2),
        ]
        pygame.draw.polygon(surf, color, points)

    @staticmethod
    def _draw_arrow_down(surf: pygame.Surface, cx: int, cy: int, size: int, color: tuple) -> None:
        points = [
            (cx - size // 2, cy - size // 2),
            (cx + size // 2, cy - size // 2),
            (cx, cy + size // 2),
        ]
        pygame.draw.polygon(surf, color, points)
