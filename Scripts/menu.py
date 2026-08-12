"""Main menu: Play → level select; Mode/High Scores/Options/Quit on root."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

import pygame

from consts import VOLUME_MAX, SCREEN_HEIGHT, SCREEN_WIDTH
from highscores import board_key_for_mode, format_time_ms, load_highscores
from levels import (
    DEFAULT_LEVEL,
    MAX_CAMPAIGN_LEVEL,
    MAX_LEVEL,
    SURVIVAL_LEVEL_ID,
    get_level,
    list_levels,
)

if TYPE_CHECKING:
    from audio import AudioManager
    from highscores import ScoreEntry

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
_LEVEL_CARD_H = 42
_LEVEL_CARD_GAP = 6
_GRID_CARD_W = 188
_GRID_COL_GAP = 12

MODES = ("1P", "2P")
SCORE_TABS = ("1p", "2p")
LEVEL_TABS = ("campaign", "survival")

# Campaign grid navigation (indices 0–4 = levels, 5 = back)
_CAMPAIGN_NAV: dict[int, dict[str, int]] = {
    0: {"down": 2, "right": 1},
    1: {"down": 3, "left": 0},
    2: {"up": 0, "down": 4, "right": 3},
    3: {"up": 1, "down": 5, "left": 2},
    4: {"up": 2, "down": 5},
    5: {"up": 4},
}

Screen = Literal["root", "options", "levels", "scores"]


@dataclass
class MenuAction:
    """Result of handling a menu key; Game applies side effects."""

    start_game: bool = False
    quit_app: bool = False


class MainMenu:
    """Root: Play / Mode / High Scores / Options / Quit. Play opens level select."""

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
        self.score_tab = "1p"
        self.level_tab = "campaign"
        self._score_boards: dict[str, list[ScoreEntry]] = load_highscores()

    def _campaign_levels(self) -> list:
        return [lvl for lvl in list_levels() if not lvl.survival]

    def _survival_level(self):
        return get_level(SURVIVAL_LEVEL_ID)

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
            return [("back", "Back")]
        if self.screen == "scores":
            return [("back", "Back")]
        return [
            ("play", "Play"),
            ("mode", f"Mode    {self.mode}"),
            ("scores", "High Scores"),
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
        self._score_boards = load_highscores()
        if self.level == SURVIVAL_LEVEL_ID:
            self.level_tab = "survival"
            self.selected = 0
        else:
            self.level_tab = "campaign"
            self.selected = max(0, min(self.level - 1, MAX_CAMPAIGN_LEVEL - 1))
        self._sfx("ui_confirm")

    def _switch_level_tab(self, delta: int) -> None:
        idx = LEVEL_TABS.index(self.level_tab)
        self.level_tab = LEVEL_TABS[(idx + delta) % len(LEVEL_TABS)]
        if self.level_tab == "campaign":
            if 1 <= self.level <= MAX_CAMPAIGN_LEVEL:
                self.selected = self.level - 1
            else:
                self.selected = 0
        else:
            self.selected = 0
        self._sfx("ui_select")

    def _move_level_selection(self, direction: str) -> None:
        if self.level_tab == "survival":
            if direction == "up":
                self.selected = 0
            elif direction == "down":
                self.selected = 1
            elif direction in ("left", "right"):
                return
        else:
            nxt = _CAMPAIGN_NAV.get(self.selected, {}).get(direction)
            if nxt is not None:
                self.selected = nxt
        self._sfx("ui_select")

    def _confirm_level_selection(self, action: MenuAction) -> None:
        if self.level_tab == "campaign":
            if self.selected >= len(self._campaign_levels()):
                self._leave_submenu()
                return
            self.level = self._campaign_levels()[self.selected].id
        else:
            if self.selected != 0:
                self._leave_submenu()
                return
            self.level = SURVIVAL_LEVEL_ID
        self._sfx("ui_confirm")
        action.start_game = True

    def _enter_scores(self) -> None:
        self._root_selected = self.selected
        self.screen = "scores"
        self.selected = 0
        self.score_tab = "1p" if self.mode == "1P" else "2p"
        self._score_boards = load_highscores()
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
            if self.screen in ("options", "levels", "scores"):
                self._leave_submenu()
            return action

        if self.screen == "scores":
            if key in (pygame.K_LEFT, pygame.K_a, pygame.K_TAB):
                self._switch_score_tab(-1 if key != pygame.K_TAB else +1)
                return action
            if key in (pygame.K_RIGHT, pygame.K_d):
                self._switch_score_tab(+1)
                return action
            if key in (pygame.K_RETURN, pygame.K_SPACE):
                self._leave_submenu()
            return action

        if self.screen == "levels":
            if key == pygame.K_TAB:
                self._switch_level_tab(+1)
                return action
            if self.level_tab == "survival" and key == pygame.K_LEFT:
                self._switch_level_tab(-1)
                return action
            if self.level_tab == "campaign" and key == pygame.K_RIGHT and self.selected in (1, 3):
                self._switch_level_tab(+1)
                return action
            if self.level_tab == "campaign":
                if key == pygame.K_LEFT:
                    self._move_level_selection("left")
                    return action
                if key == pygame.K_RIGHT:
                    self._move_level_selection("right")
                    return action
            if key in (pygame.K_UP, pygame.K_w):
                self._move_level_selection("up")
                return action
            if key in (pygame.K_DOWN, pygame.K_s):
                self._move_level_selection("down")
                return action
            if key in (pygame.K_RETURN, pygame.K_SPACE):
                self._confirm_level_selection(action)
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
            elif kind == "scores":
                self._enter_scores()
            elif kind == "back":
                self._leave_submenu()
            elif kind in ("mode", "music", "sfx"):
                self._nudge_field(+1)
        return action

    def _switch_score_tab(self, delta: int) -> None:
        idx = SCORE_TABS.index(self.score_tab)
        self.score_tab = SCORE_TABS[(idx + delta) % len(SCORE_TABS)]
        self._sfx("ui_select")

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
        if self.screen == "scores":
            self._draw_scores_screen(screen)
            self._draw_hints(screen)
            return

        title = self.big_font.render("Bubble Trouble", True, _TITLE)
        screen.blit(
            title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 170))
        )

        if self.screen == "options":
            subtitle = self.font.render("Options", True, _NEON_CYAN)
            screen.blit(
                subtitle,
                subtitle.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 128)),
            )

        items = self._items()
        total_h = len(items) * _CARD_H + (len(items) - 1) * _CARD_GAP
        start_y = SCREEN_HEIGHT // 2 - total_h // 2 + (20 if self.screen == "options" else 12)
        cx = SCREEN_WIDTH // 2

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
        """Campaign | Survival tabs; campaign uses a 2-column grid."""
        header = self.big_font.render("Select Level", True, _TITLE)
        screen.blit(header, header.get_rect(center=(SCREEN_WIDTH // 2, 48)))

        tab_y = 92
        tab_labels = ("Campaign", "Survival")
        for i, key in enumerate(LEVEL_TABS):
            selected = key == self.level_tab
            tab_rect = pygame.Rect(0, 0, 140, 34)
            tab_rect.center = (SCREEN_WIDTH // 2 - 78 + i * 156, tab_y)
            self._draw_card_chrome(screen, tab_rect, selected)
            color = _SELECTED if selected else _HUD_DIM
            text = self.font.render(tab_labels[i], True, color)
            screen.blit(text, text.get_rect(center=tab_rect.center))

        cx = SCREEN_WIDTH // 2
        card_h = _LEVEL_CARD_H
        blurb_y = 0

        if self.level_tab == "campaign":
            grid_top = 138
            col_step = _GRID_CARD_W + _GRID_COL_GAP
            left_x = cx - col_step // 2
            right_x = cx + col_step // 2
            row_step = card_h + _LEVEL_CARD_GAP

            for i, lvl in enumerate(self._campaign_levels()):
                row, col = divmod(i, 2)
                card_x = left_x if col == 0 else right_x
                card_y = grid_top + row * row_step
                card_rect = pygame.Rect(0, 0, _GRID_CARD_W, card_h)
                card_rect.center = (card_x, card_y + card_h // 2)
                self._draw_level_card(screen, card_rect, lvl, i == self.selected)

            back_y = grid_top + 3 * row_step + 4
            back_rect = pygame.Rect(0, 0, _CARD_W, card_h)
            back_rect.center = (cx, back_y + card_h // 2)
            self._draw_card_chrome(screen, back_rect, self.selected >= len(self._campaign_levels()))
            back_color = _SELECTED if self.selected >= len(self._campaign_levels()) else _HUD_DIM
            back_surf = self.font.render("Back", True, back_color)
            screen.blit(back_surf, back_surf.get_rect(center=back_rect.center))
            blurb_y = back_rect.bottom + 22

            if self.selected < len(self._campaign_levels()):
                blurb_lvl = self._campaign_levels()[self.selected]
                blurb = self.font.render(blurb_lvl.blurb, True, _NEON_CYAN)
                screen.blit(blurb, blurb.get_rect(center=(cx, blurb_y)))
        else:
            surv = self._survival_level()
            card_rect = pygame.Rect(0, 0, _CARD_W, card_h + 8)
            card_rect.center = (cx, 168)
            self._draw_level_card(screen, card_rect, surv, self.selected == 0, badge="S")

            board_key = board_key_for_mode(self.mode)
            board = self._score_boards.get(board_key, [])
            if board:
                best = self.font.render(
                    f"Best ({self.mode}): {format_time_ms(board[0].time_ms)}",
                    True,
                    _SELECTED,
                )
                screen.blit(best, best.get_rect(center=(cx, card_rect.bottom + 28)))

            blurb = self.font.render(surv.blurb, True, _NEON_CYAN)
            screen.blit(blurb, blurb.get_rect(center=(cx, card_rect.bottom + 58)))

            back_rect = pygame.Rect(0, 0, _CARD_W, card_h)
            back_rect.center = (cx, card_rect.bottom + 108)
            self._draw_card_chrome(screen, back_rect, self.selected == 1)
            back_color = _SELECTED if self.selected == 1 else _HUD_DIM
            back_surf = self.font.render("Back", True, back_color)
            screen.blit(back_surf, back_surf.get_rect(center=back_rect.center))

    def _draw_level_card(
        self,
        screen: pygame.Surface,
        card_rect: pygame.Rect,
        lvl,
        selected: bool,
        *,
        badge: str | None = None,
    ) -> None:
        self._draw_card_chrome(screen, card_rect, selected)
        text_color = _SELECTED if selected else _HUD_DIM
        badge_text = badge if badge is not None else str(lvl.id)
        badge_w = 26 if len(badge_text) > 1 else 28
        badge_rect = pygame.Rect(
            card_rect.left + 10,
            card_rect.centery - 12,
            badge_w,
            24,
        )
        pygame.draw.rect(
            screen,
            lvl.theme.barrier_edge if selected else _CARD_BORDER,
            badge_rect,
            border_radius=6,
        )
        id_surf = self.font.render(badge_text, True, (12, 8, 24))
        screen.blit(id_surf, id_surf.get_rect(center=badge_rect.center))
        name_surf = self.font.render(lvl.name, True, text_color)
        max_name_w = card_rect.width - badge_rect.width - 28
        if name_surf.get_width() > max_name_w:
            name = lvl.name
            while len(name) > 3 and self.font.size(name + "…")[0] > max_name_w:
                name = name[:-1]
            name_surf = self.font.render(name + "…", True, text_color)
        screen.blit(
            name_surf,
            name_surf.get_rect(midleft=(badge_rect.right + 10, card_rect.centery)),
        )

    def _draw_scores_screen(self, screen: pygame.Surface) -> None:
        header = self.big_font.render("High Scores", True, _TITLE)
        screen.blit(header, header.get_rect(center=(SCREEN_WIDTH // 2, 56)))

        tab_y = 110
        for i, key in enumerate(SCORE_TABS):
            label = "1P" if key == "1p" else "2P"
            selected = key == self.score_tab
            tab_rect = pygame.Rect(0, 0, 120, 36)
            tab_rect.center = (SCREEN_WIDTH // 2 - 70 + i * 140, tab_y)
            self._draw_card_chrome(screen, tab_rect, selected)
            color = _SELECTED if selected else _HUD_DIM
            text = self.font.render(label, True, color)
            screen.blit(text, text.get_rect(center=tab_rect.center))

        board = self._score_boards.get(self.score_tab, [])
        list_top = 170
        cx = SCREEN_WIDTH // 2
        if not board:
            empty = self.font.render("No scores yet — survive longer!", True, _HINT_DIM)
            screen.blit(empty, empty.get_rect(center=(cx, list_top + 40)))
        else:
            for i, entry in enumerate(board):
                row = pygame.Rect(0, 0, _CARD_W, _LEVEL_CARD_H)
                row.center = (
                    cx,
                    list_top + i * (_LEVEL_CARD_H + _LEVEL_CARD_GAP) + _LEVEL_CARD_H // 2,
                )
                self._draw_card_chrome(screen, row, False)
                rank = self.font.render(f"{i + 1}.", True, _NEON_CYAN)
                name = self.font.render(entry.name, True, _TITLE)
                time_s = self.font.render(format_time_ms(entry.time_ms), True, _SELECTED)
                screen.blit(rank, rank.get_rect(midleft=(row.left + 24, row.centery)))
                screen.blit(name, name.get_rect(midleft=(row.left + 70, row.centery)))
                screen.blit(time_s, time_s.get_rect(midright=(row.right - 24, row.centery)))

        back_y = list_top + 5 * (_LEVEL_CARD_H + _LEVEL_CARD_GAP) + 24
        back_rect = pygame.Rect(0, 0, _CARD_W, _LEVEL_CARD_H)
        back_rect.center = (cx, back_y + _LEVEL_CARD_H // 2)
        self._draw_card_chrome(screen, back_rect, True)
        back_surf = self.font.render("Back", True, _SELECTED)
        screen.blit(back_surf, back_surf.get_rect(center=back_rect.center))

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
        """Footer: control legend; Esc on submenus; co-op keys on root."""
        if self.screen == "root":
            self._draw_play_controls(screen)

        y = SCREEN_HEIGHT - 40
        parts: list[tuple[str, str | None]] = [
            ("nav", None),
            ("text", "move"),
            ("sep", None),
        ]
        if self.screen in ("root", "options"):
            parts.extend(
                [
                    ("vol", None),
                    ("text", "adjust"),
                    ("sep", None),
                ]
            )
        if self.screen == "scores":
            parts.extend(
                [
                    ("vol", None),
                    ("text", "tabs"),
                    ("sep", None),
                ]
            )
        if self.screen == "levels":
            parts.extend(
                [
                    ("text", "Tab"),
                    ("text_dim", "mode"),
                    ("sep", None),
                ]
            )
        parts.extend(
            [
                ("text", "Enter"),
                ("text_dim", "confirm"),
            ]
        )
        if self.screen in ("options", "levels", "scores"):
            parts.extend(
                [
                    ("sep", None),
                    ("text", "Esc"),
                    ("text_dim", "back"),
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
        x = (SCREEN_WIDTH - total_w) // 2

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

    def _draw_play_controls(self, screen: pygame.Surface) -> None:
        """Gameplay key legend above the nav footer (drawn arrows, not Unicode)."""
        y = SCREEN_HEIGHT - 68
        if self.mode == "2P":
            p1 = self.font.render("P1  A/D + Space", True, _HINT_DIM)
            sep = self.font.render("·", True, _HINT_DIM)
            p2_pre = self.font.render("P2", True, _HINT_DIM)
            p2_post = self.font.render("+ Enter", True, _HINT_DIM)
            arrow_cluster = 28
            gap = 10
            total = (
                p1.get_width()
                + gap
                + sep.get_width()
                + gap
                + p2_pre.get_width()
                + 8
                + arrow_cluster
                + 8
                + p2_post.get_width()
            )
            x = (SCREEN_WIDTH - total) // 2
            screen.blit(p1, p1.get_rect(midleft=(x, y)))
            x += p1.get_width() + gap
            screen.blit(sep, sep.get_rect(center=(x + sep.get_width() // 2, y)))
            x += sep.get_width() + gap
            screen.blit(p2_pre, p2_pre.get_rect(midleft=(x, y)))
            x += p2_pre.get_width() + 8
            self._draw_arrow_left(screen, x + 6, y, 10, _NEON_CYAN)
            self._draw_arrow_right(screen, x + 20, y, 10, _NEON_CYAN)
            x += arrow_cluster + 8
            screen.blit(p2_post, p2_post.get_rect(midleft=(x, y)))
        else:
            line = self.font.render("A/D move  ·  Space fire", True, _HINT_DIM)
            screen.blit(line, line.get_rect(center=(SCREEN_WIDTH // 2, y)))

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
