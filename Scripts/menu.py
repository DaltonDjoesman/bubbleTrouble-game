"""Minimal main menu with audio volume controls."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import pygame

from consts import VOLUME_MAX, screenHeight, screenWidth

if TYPE_CHECKING:
    from audio import AudioManager

_NEON_CYAN = (80, 240, 255)
_NEON_MAGENTA = (255, 70, 180)
_HUD_DIM = (180, 200, 220)
_TITLE = (230, 240, 255)
_SELECTED = (255, 220, 80)


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
            ("music", f"Music  ◀ {music}/{VOLUME_MAX} ▶"),
            ("sfx", f"SFX    ◀ {sfx}/{VOLUME_MAX} ▶"),
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
                # Enter on volume row bumps +1 (same as Right)
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

    def draw(self, screen: pygame.Surface) -> None:
        title = self.big_font.render("Bubble Trouble", True, _TITLE)
        screen.blit(
            title, title.get_rect(center=(screenWidth // 2, screenHeight // 2 - 140))
        )
        subtitle = self.font.render("Audio / Start", True, _NEON_MAGENTA)
        screen.blit(
            subtitle,
            subtitle.get_rect(center=(screenWidth // 2, screenHeight // 2 - 90)),
        )

        items = self._items()
        base_y = screenHeight // 2 - 30
        for i, (_kind, label) in enumerate(items):
            color = _SELECTED if i == self.selected else _HUD_DIM
            prefix = "▸ " if i == self.selected else "  "
            text = self.font.render(prefix + label, True, color)
            screen.blit(
                text, text.get_rect(center=(screenWidth // 2, base_y + i * 40))
            )

        hint = self.font.render(
            "↑↓ navigate   ←→ volume   Enter confirm", True, _NEON_CYAN
        )
        screen.blit(
            hint, hint.get_rect(center=(screenWidth // 2, screenHeight - 40))
        )
