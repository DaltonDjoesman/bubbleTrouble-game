"""Main menu: Play → level select; Mode/High Scores/Options/Quit on root."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

import pygame

from consts import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    UI_FG,
    UI_MUTED,
    UI_NEON_CYAN,
    UI_NEON_GOLD,
    VOLUME_MAX,
)
from highscores import board_key_for_mode, format_time_ms, load_highscores
from levels import (
    DEFAULT_LEVEL,
    MAX_CAMPAIGN_LEVEL,
    MAX_LEVEL,
    SURVIVAL_LEVEL_ID,
    get_level,
    list_levels,
)
from ui_chrome import (
    CONTENT_TOP,
    arrow_color,
    draw_card,
    draw_footer_band,
    draw_header_brand,
    draw_hint_row,
    draw_scanlines,
    draw_screen_bg,
    draw_system_line,
    get_small_font,
    selection_color,
)

if TYPE_CHECKING:
    from audio import AudioManager
    from highscores import ScoreEntry

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
                ("back", "BACK"),
            ]
        if self.screen == "levels":
            return [("back", "BACK")]
        if self.screen == "scores":
            return [("back", "BACK")]
        return [
            ("play", "PLAY GAME"),
            ("mode", f"MODE    {self.mode}"),
            ("scores", "HIGH SCORES"),
            ("options", "OPTIONS"),
            ("quit", "QUIT"),
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
        draw_screen_bg(screen)
        if self.screen == "root":
            draw_header_brand(screen, subtitle="CYBER ARCADE")
        elif self.screen == "options":
            draw_header_brand(screen, subtitle="SYSTEM OPTIONS")
        elif self.screen == "levels":
            draw_header_brand(screen, subtitle="SELECT LEVEL")
        else:
            draw_header_brand(screen, subtitle="HIGH SCORES")

        if self.screen == "levels":
            self._draw_levels_screen(screen)
        elif self.screen == "scores":
            self._draw_scores_screen(screen)
        else:
            self._draw_list_screen(screen)

        self._draw_footer(screen)
        draw_scanlines(screen)

    def _draw_list_screen(self, screen: pygame.Surface) -> None:
        items = self._items()
        total_h = len(items) * _CARD_H + (len(items) - 1) * _CARD_GAP
        start_y = CONTENT_TOP + 36 + (SCREEN_HEIGHT - CONTENT_TOP - 72 - total_h) // 2
        start_y = max(CONTENT_TOP + 40, min(start_y, SCREEN_HEIGHT - 72 - total_h - 20))
        cx = SCREEN_WIDTH // 2

        for i, (kind, label) in enumerate(items):
            selected = i == self.selected
            card_rect = pygame.Rect(0, 0, _CARD_W, _CARD_H)
            card_rect.center = (cx, start_y + i * (_CARD_H + _CARD_GAP) + _CARD_H // 2)
            draw_card(screen, card_rect, selected=selected)

            text_color = selection_color(selected)
            a_color = arrow_color(selected)

            if kind in ("mode", "music", "sfx"):
                if kind == "mode":
                    name, value = "MODE", self.mode
                elif kind == "music":
                    name = "MUSIC"
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
                self._draw_arrow_left(screen, cluster_cx - 36, cy, 12, a_color)
                screen.blit(val_surf, val_surf.get_rect(center=(cluster_cx, cy)))
                self._draw_arrow_right(screen, cluster_cx + 36, cy, 12, a_color)
            else:
                text = self.font.render(label, True, text_color)
                screen.blit(text, text.get_rect(center=card_rect.center))

    def _draw_levels_screen(self, screen: pygame.Surface) -> None:
        """Campaign | Survival tabs; campaign uses a 2-column grid."""
        tab_y = CONTENT_TOP + 28
        tab_labels = ("CAMPAIGN", "SURVIVAL")
        for i, key in enumerate(LEVEL_TABS):
            selected = key == self.level_tab
            tab_rect = pygame.Rect(0, 0, 148, 34)
            tab_rect.center = (SCREEN_WIDTH // 2 - 82 + i * 164, tab_y)
            draw_card(screen, tab_rect, selected=selected, radius=4)
            color = selection_color(selected) if selected else UI_NEON_CYAN
            if not selected:
                color = UI_MUTED
            text = self.font.render(tab_labels[i], True, color)
            screen.blit(text, text.get_rect(center=tab_rect.center))

        cx = SCREEN_WIDTH // 2
        card_h = _LEVEL_CARD_H

        if self.level_tab == "campaign":
            grid_top = tab_y + 36
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
            back_sel = self.selected >= len(self._campaign_levels())
            draw_card(screen, back_rect, selected=back_sel)
            back_surf = self.font.render("BACK", True, selection_color(back_sel))
            screen.blit(back_surf, back_surf.get_rect(center=back_rect.center))

            if self.selected < len(self._campaign_levels()):
                blurb_lvl = self._campaign_levels()[self.selected]
                blurb = get_small_font().render(blurb_lvl.blurb, True, UI_NEON_CYAN)
                screen.blit(blurb, blurb.get_rect(center=(cx, back_rect.bottom + 20)))
        else:
            surv = self._survival_level()
            card_rect = pygame.Rect(0, 0, _CARD_W, card_h + 8)
            card_rect.center = (cx, tab_y + 70)
            self._draw_level_card(screen, card_rect, surv, self.selected == 0, badge="S")

            board_key = board_key_for_mode(self.mode)
            board = self._score_boards.get(board_key, [])
            if board:
                best = self.font.render(
                    f"BEST ({self.mode}): {format_time_ms(board[0].time_ms)}",
                    True,
                    UI_NEON_GOLD,
                )
                screen.blit(best, best.get_rect(center=(cx, card_rect.bottom + 26)))

            blurb = get_small_font().render(surv.blurb, True, UI_NEON_CYAN)
            screen.blit(blurb, blurb.get_rect(center=(cx, card_rect.bottom + 52)))

            back_rect = pygame.Rect(0, 0, _CARD_W, card_h)
            back_rect.center = (cx, card_rect.bottom + 100)
            draw_card(screen, back_rect, selected=self.selected == 1)
            back_surf = self.font.render("BACK", True, selection_color(self.selected == 1))
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
        draw_card(screen, card_rect, selected=selected)
        text_color = selection_color(selected)
        badge_text = badge if badge is not None else str(lvl.id)
        badge_w = 26 if len(badge_text) > 1 else 28
        badge_rect = pygame.Rect(
            card_rect.left + 10,
            card_rect.centery - 12,
            badge_w,
            24,
        )
        badge_fill = UI_NEON_GOLD if selected else UI_NEON_CYAN
        pygame.draw.rect(screen, badge_fill, badge_rect, border_radius=4)
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
        tab_y = CONTENT_TOP + 28
        for i, key in enumerate(SCORE_TABS):
            label = "1P" if key == "1p" else "2P"
            selected = key == self.score_tab
            tab_rect = pygame.Rect(0, 0, 120, 34)
            tab_rect.center = (SCREEN_WIDTH // 2 - 70 + i * 140, tab_y)
            draw_card(screen, tab_rect, selected=selected, radius=4)
            color = selection_color(selected)
            text = self.font.render(label, True, color)
            screen.blit(text, text.get_rect(center=tab_rect.center))

        board = self._score_boards.get(self.score_tab, [])
        list_top = tab_y + 44
        cx = SCREEN_WIDTH // 2
        if not board:
            empty = self.font.render("No scores yet — survive longer!", True, UI_MUTED)
            screen.blit(empty, empty.get_rect(center=(cx, list_top + 40)))
        else:
            for i, entry in enumerate(board):
                row = pygame.Rect(0, 0, _CARD_W, _LEVEL_CARD_H)
                row.center = (
                    cx,
                    list_top + i * (_LEVEL_CARD_H + _LEVEL_CARD_GAP) + _LEVEL_CARD_H // 2,
                )
                draw_card(screen, row, selected=False)
                rank = self.font.render(f"{i + 1}.", True, UI_NEON_CYAN)
                name = self.font.render(entry.name, True, UI_FG)
                time_s = self.font.render(format_time_ms(entry.time_ms), True, UI_NEON_GOLD)
                screen.blit(rank, rank.get_rect(midleft=(row.left + 24, row.centery)))
                screen.blit(name, name.get_rect(midleft=(row.left + 70, row.centery)))
                screen.blit(time_s, time_s.get_rect(midright=(row.right - 24, row.centery)))

        back_y = list_top + 5 * (_LEVEL_CARD_H + _LEVEL_CARD_GAP) + 16
        back_rect = pygame.Rect(0, 0, _CARD_W, _LEVEL_CARD_H)
        back_rect.center = (cx, back_y + _LEVEL_CARD_H // 2)
        draw_card(screen, back_rect, selected=True)
        back_surf = self.font.render("BACK", True, UI_NEON_GOLD)
        screen.blit(back_surf, back_surf.get_rect(center=back_rect.center))

    def _draw_footer(self, screen: pygame.Surface) -> None:
        draw_footer_band(screen)
        if self.screen == "root":
            self._draw_play_controls(screen)
            hints: list[tuple[list[str], str]] = [
                (["W", "S"], "Navigate"),
                (["A", "D"], "Adjust"),
                (["ENTER"], "Confirm"),
            ]
        elif self.screen == "options":
            hints = [
                (["W", "S"], "Navigate"),
                (["A", "D"], "Adjust"),
                (["ENTER"], "Confirm"),
                (["ESC"], "Back"),
            ]
        elif self.screen == "levels":
            hints = [
                (["W", "S"], "Navigate"),
                (["TAB"], "Mode"),
                (["ENTER"], "Confirm"),
                (["ESC"], "Back"),
            ]
        else:
            hints = [
                (["A", "D"], "Tabs"),
                (["ENTER"], "Confirm"),
                (["ESC"], "Back"),
            ]
        hint_y = SCREEN_HEIGHT - 40
        draw_hint_row(screen, hints, center_y=hint_y, font=get_small_font())
        draw_system_line(screen)

    def _draw_play_controls(self, screen: pygame.Surface) -> None:
        """Gameplay key legend above the nav footer."""
        y = SCREEN_HEIGHT - 58
        small = get_small_font()
        if self.mode == "2P":
            line = small.render("P1  A/D + SPACE   ·   P2  ←/→ + ENTER", True, UI_MUTED)
        else:
            line = small.render("A/D move  ·  SPACE fire", True, UI_MUTED)
        screen.blit(line, line.get_rect(center=(SCREEN_WIDTH // 2, y)))
