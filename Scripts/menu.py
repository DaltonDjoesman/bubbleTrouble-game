"""Minimal main menu with audio volume controls."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import pygame

from consts import VOLUME_MAX, screenHeight, screenWidth

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


@dataclass
class MenuAction:
    """Result of handling a menu key; Game applies side effects."""

    start_game: bool = False
    quit_app: bool = False


class MainMenu:
    """Keyboard menu: Play, Music vol, SFX vol, Quit."""

    def __init__(
        self,
        font: pygame.font.Font,
        big_font: pygame.font.Font,
        audio: AudioManager | None,
    ) -> None:
        self.font = font
        self.big_font = big_font
        self.audio = audio
        self.selected = 0

    def _items(self) -> list[tuple[str, str]]:
        music = self.audio.music_volume if self.audio else 0
        sfx = self.audio.sfx_volume if self.audio else 0
        return [
            ("play", "Play"),
            ("music", f"Music   {music}/{VOLUME_MAX}"),
            ("sfx", f"SFX     {sfx}/{VOLUME_MAX}"),
            ("quit", "Quit"),
        ]

    def handle_keydown(self, key: int) -> MenuAction:
        items = self._items()
        n = len(items)
        action = MenuAction()

        if key in (pygame.K_UP, pygame.K_w):
            self.selected = (self.selected - 1) % n
            self._sfx("ui_select")
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.selected = (self.selected + 1) % n
            self._sfx("ui_select")
        elif key in (pygame.K_LEFT, pygame.K_a):
            self._adjust_volume(-1)
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self._adjust_volume(+1)
        elif key in (pygame.K_RETURN, pygame.K_SPACE):
            kind = items[self.selected][0]
            if kind == "play":
                self._sfx("ui_confirm")
                action.start_game = True
            elif kind == "quit":
                self._sfx("ui_confirm")
                action.quit_app = True
            elif kind in ("music", "sfx"):
                self._adjust_volume(+1)
        return action

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
            title, title.get_rect(center=(screenWidth // 2, screenHeight // 2 - 140))
        )

        items = self._items()
        total_h = len(items) * _CARD_H + (len(items) - 1) * _CARD_GAP
        start_y = screenHeight // 2 - total_h // 2 + 20
        cx = screenWidth // 2

        for i, (kind, label) in enumerate(items):
            selected = i == self.selected
            card_rect = pygame.Rect(0, 0, _CARD_W, _CARD_H)
            card_rect.center = (cx, start_y + i * (_CARD_H + _CARD_GAP) + _CARD_H // 2)

            # Card body
            card = pygame.Surface((_CARD_W, _CARD_H), flags=pygame.SRCALPHA)
            card.fill(_CARD_BG)
            screen.blit(card, card_rect.topleft)
            border = _CARD_BORDER_SEL if selected else _CARD_BORDER
            pygame.draw.rect(screen, border, card_rect, width=2, border_radius=8)
            if selected:
                inner = card_rect.inflate(-6, -6)
                pygame.draw.rect(screen, _NEON_CYAN, inner, width=1, border_radius=6)

            text_color = _SELECTED if selected else _HUD_DIM

            if kind in ("music", "sfx"):
                name = "Music" if kind == "music" else "SFX"
                value = (
                    f"{self.audio.music_volume if self.audio else 0}/{VOLUME_MAX}"
                    if kind == "music"
                    else f"{self.audio.sfx_volume if self.audio else 0}/{VOLUME_MAX}"
                )
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
        """Footer: clear control legend with drawn arrows."""
        y = screenHeight - 40
        # (kind, payload) — icon blocks or text labels
        parts: list[tuple[str, str | None]] = [
            ("nav", None),
            ("text", "mover"),
            ("sep", None),
            ("vol", None),
            ("text", "volume"),
            ("sep", None),
            ("text", "Enter"),
            ("text_dim", "confirmar"),
        ]

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
