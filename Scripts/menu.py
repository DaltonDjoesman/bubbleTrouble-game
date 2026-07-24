"""Main menu: Play → level select; Mode/Options/Quit on root."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

import pygame

from consts import VOLUME_MAX, screenHeight, screenWidth
from levels import DEFAULT_LEVEL, MAX_LEVEL, get_level, list_levels

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

_CARD_W = 400
_CARD_H = 48
_CARD_GAP = 10

MODES = ("1P", "2P")

Screen = Literal["root", "options", "levels"]


@dataclass
class MenuAction:
    """Result of handling a menu key; Game applies side effects."""

    start_game: bool = False
    quit_app: bool = False


class MainMenu:
    """Root: Play / Mode / Options / Quit. Play opens level select."""

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
        if self.screen == "levels":
            items = [
                (f"level:{lvl.id}", f"{lvl.id}  {lvl.name}")
                for lvl in list_levels()
            ]
            items.append(("back", "Back"))
            return items
        return [
            ("play", "Play"),
            ("mode", f"Mode    {self.mode}"),
            ("options", "Options"),
            ("quit", "Quit"),
        ]

    def _enter_options(self) -> None:
        self._root_selected = self.selected
        self.screen = "options"
        self.selected = 0
        self._sfx("ui_confirm")

    def _enter_levels(self) -> None:
        self._root_selected = self.selected
        self.screen = "levels"
        # Highlight last-played / current level
        self.selected = max(0, min(self.level - 1, self.max_level - 1))
        self._sfx("ui_confirm")

    def _leave_submenu(self) -> None:
        self.screen = "root"
        self.selected = self._root_selected
        self._sfx("ui_select")

    def handle_keydown(self, key: int) -> MenuAction:
        items = self._items()
        n = len(items)
        action = MenuAction()

        if key == pygame.K_ESCAPE:
            if self.screen in ("options", "levels"):
                self._leave_submenu()
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
                self._enter_levels()
            elif kind == "quit":
                self._sfx("ui_confirm")
                action.quit_app = True
            elif kind == "options":
                self._enter_options()
            elif kind == "back":
                self._leave_submenu()
            elif kind.startswith("level:"):
                self.level = int(kind.split(":", 1)[1])
                self._sfx("ui_confirm")
                action.start_game = True
            elif kind in ("mode", "music", "sfx"):
                self._nudge_field(+1)
        return action

    def _nudge_field(self, delta: int) -> None:
        kind = self._items()[self.selected][0]
        if kind == "mode":
            idx = MODES.index(self.mode)
            self.mode = MODES[(idx + delta) % len(MODES)]
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
        if self.screen == "levels":
            self._draw_levels_screen(screen)
            self._draw_hints(screen)
            return

        title = self.big_font.render("Bubble Trouble", True, _TITLE)
        screen.blit(
            title, title.get_rect(center=(screenWidth // 2, screenHeight // 2 - 170))
        )

        if self.screen == "options":
            subtitle = self.font.render("Options", True, _NEON_CYAN)
            screen.blit(
                subtitle,
                subtitle.get_rect(center=(screenWidth // 2, screenHeight // 2 - 128)),
            )

        items = self._items()
        total_h = len(items) * _CARD_H + (len(items) - 1) * _CARD_GAP
        start_y = screenHeight // 2 - total_h // 2 + (20 if self.screen == "options" else 12)
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
            arrow_color = _ARROW if selected else _HUD_DIM

            if kind in ("mode", "music", "sfx"):
                if kind == "mode":
                    name, value = "Mode", self.mode
                elif kind == "music":
                    name = "Music"
                    value = f"{self.audio.music_volume if self.audio else 0}/{VOLUME_MAX}"
                else:
                    name = "SFX"
                    value = f"{self.audio.sfx_volume if self.audio else 0}/{VOLUME_MAX}"

                name_surf = self.font.render(name, True, text_color)
                val_surf = self.font.render(value, True, text_color)
                screen.blit(
                    name_surf,
                    name_surf.get_rect(midleft=(card_rect.left + 28, card_rect.centery)),
                )
                cluster_cx = card_rect.right - 88
                cy = card_rect.centery
                self._draw_arrow_left(screen, cluster_cx - 36, cy, 12, arrow_color)
                screen.blit(val_surf, val_surf.get_rect(center=(cluster_cx, cy)))
                self._draw_arrow_right(screen, cluster_cx + 36, cy, 12, arrow_color)
            else:
                text = self.font.render(label, True, text_color)
                screen.blit(text, text.get_rect(center=card_rect.center))

        self._draw_hints(screen)

    def _draw_levels_screen(self, screen: pygame.Surface) -> None:
        """Dedicated level picker: header, spaced list, blurb for selection."""
        header = self.big_font.render("Select Level", True, _TITLE)
        screen.blit(header, header.get_rect(center=(screenWidth // 2, 72)))

        items = self._items()
        level_items = [it for it in items if it[0].startswith("level:")]
        back_item = next(it for it in items if it[0] == "back")

        list_top = 130
        cx = screenWidth // 2
        # Leave room under header; keep Back + blurb above footer
        for i, (kind, _label) in enumerate(level_items):
            selected = i == self.selected
            card_rect = pygame.Rect(0, 0, _CARD_W, _CARD_H)
            card_rect.center = (cx, list_top + i * (_CARD_H + _CARD_GAP) + _CARD_H // 2)
            self._draw_card_chrome(screen, card_rect, selected)

            lvl = get_level(int(kind.split(":", 1)[1]))
            text_color = _SELECTED if selected else _HUD_DIM
            # Number badge
            badge = pygame.Rect(card_rect.left + 14, card_rect.centery - 14, 28, 28)
            pygame.draw.rect(
                screen,
                lvl.theme.platform_edge if selected else _CARD_BORDER,
                badge,
                border_radius=6,
            )
            id_surf = self.font.render(str(lvl.id), True, (12, 8, 24))
            screen.blit(id_surf, id_surf.get_rect(center=badge.center))
            name_surf = self.font.render(lvl.name, True, text_color)
            screen.blit(
                name_surf,
                name_surf.get_rect(midleft=(badge.right + 16, card_rect.centery)),
            )

        back_index = len(level_items)
        back_selected = self.selected == back_index
        back_y = list_top + len(level_items) * (_CARD_H + _CARD_GAP) + 16
        back_rect = pygame.Rect(0, 0, _CARD_W, _CARD_H)
        back_rect.center = (cx, back_y + _CARD_H // 2)
        self._draw_card_chrome(screen, back_rect, back_selected)
        back_color = _SELECTED if back_selected else _HUD_DIM
        back_surf = self.font.render(back_item[1], True, back_color)
        screen.blit(back_surf, back_surf.get_rect(center=back_rect.center))

        # Blurb for highlighted level (not Back)
        if self.selected < len(level_items):
            lvl = get_level(self.selected + 1)
            blurb = self.font.render(lvl.blurb, True, _NEON_CYAN)
            screen.blit(
                blurb,
                blurb.get_rect(center=(screenWidth // 2, back_rect.bottom + 36)),
            )

    @staticmethod
    def _draw_card_chrome(
        screen: pygame.Surface, card_rect: pygame.Rect, selected: bool
    ) -> None:
        card = pygame.Surface(card_rect.size, flags=pygame.SRCALPHA)
        card.fill(_CARD_BG)
        screen.blit(card, card_rect.topleft)
        border = _CARD_BORDER_SEL if selected else _CARD_BORDER
        pygame.draw.rect(screen, border, card_rect, width=2, border_radius=8)
        if selected:
            inner = card_rect.inflate(-6, -6)
            pygame.draw.rect(screen, _NEON_CYAN, inner, width=1, border_radius=6)


    def _draw_hints(self, screen: pygame.Surface) -> None:
        """Footer: control legend; Esc on submenus."""
        y = screenHeight - 40
        parts: list[tuple[str, str | None]] = [
            ("nav", None),
            ("text", "mover"),
            ("sep", None),
        ]
        if self.screen in ("root", "options"):
            parts.extend(
                [
                    ("vol", None),
                    ("text", "ajustar"),
                    ("sep", None),
                ]
            )
        parts.extend(
            [
                ("text", "Enter"),
                ("text_dim", "confirmar"),
            ]
        )
        if self.screen in ("options", "levels"):
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
