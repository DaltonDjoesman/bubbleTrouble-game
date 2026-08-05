"""Bubble Trouble — core gameplay entry point.

Run from the repository root:
    python Scripts/main.py
"""
from __future__ import annotations

import logging
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import pygame

pygame.init()

from audio import init_audio
from bolinha import Ball
from bullet import Bullet
from consts import (
    BOLA_SPRITE,
    BULLET_COOLDOWN_MS,
    FPS,
    MAX_BULLETS,
    P1_KEYS,
    P1_SPAWN_X_OFFSET,
    P2_IDLE_FRAMES,
    P2_KEYS,
    P2_RUN_FRAMES,
    P2_SPAWN_X_OFFSET,
    P2_GUN_SPRITE,
    PLAYER_IDLE_FRAMES,
    PLAYER_RUN_FRAMES,
    STICKY_MAX_ON_MAP,
    TIME_BAR_BG,
    TIME_BAR_EDGE,
    TIME_BAR_FILL,
    TIME_BAR_FILL_LOW,
    TIME_BAR_HEIGHT,
    TIME_BAR_POS,
    TIME_BAR_WIDTH,
    TIME_DRAIN_PER_SEC,
    TIME_POWER_SECONDS,
    screenHeight,
    screenWidth,
)
from levels import (
    DEFAULT_LEVEL,
    MAX_LEVEL,
    DoorRuntime,
    Level,
    build_arena_background,
    collect_solids,
    draw_arena_geometry,
    get_level,
)
from menu import MainMenu
from player import FLOOR_Y, Player
from powerup import Powerup, maybe_spawn_powerup
from shoot_effect import ShootEffect

logging.basicConfig(level=logging.WARNING)

# Cyberpunk palette (HUD)
_NEON_CYAN = (80, 240, 255)
_NEON_MAGENTA = (255, 70, 180)
_HUD_DIM = (180, 200, 220)
_OVERLAY = (8, 4, 20, 180)

LEVEL_CLEAR_AUTO_MS = 1800


class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Bubble Trouble")
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 64)
        self.current_level: Level = get_level(DEFAULT_LEVEL)
        self.background = build_arena_background(self.current_level.theme)
        self._menu_background = build_arena_background(get_level(DEFAULT_LEVEL).theme)

        self.audio = init_audio()
        self.selected_mode = "1P"
        self.selected_level = DEFAULT_LEVEL
        self.menu = MainMenu(
            self.font,
            self.big_font,
            self.audio,
            mode=self.selected_mode,
            level=self.selected_level,
            max_level=MAX_LEVEL,
        )

        self.bolas = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

        self.state = "menu"
        self.time_max = float(self.current_level.time_seconds)
        self.time_remaining = self.time_max
        self._fire_cooldown_until: dict[int, int] = {}
        self._end_sfx_played = False
        self._notice: str | None = None
        self._notice_until = 0
        self._level_clear_at = 0
        self._doors: list[DoorRuntime] = []
        self._solids: list[pygame.Rect] = []

        self._ball_base_image = pygame.image.load(BOLA_SPRITE).convert_alpha()
        self.audio.play_music()

    def _sync_selection_from_menu(self) -> None:
        self.selected_mode = self.menu.mode
        self.selected_level = self.menu.level

    def _show_notice(self, text: str, duration_ms: int = 2200) -> None:
        self._notice = text
        self._notice_until = pygame.time.get_ticks() + duration_ms

    def _refill_time(self) -> None:
        self.time_max = float(self.current_level.time_seconds)
        self.time_remaining = self.time_max

    def add_time(self, seconds: float) -> None:
        """TIME powerup: add seconds, clamped to this level's budget."""
        self.time_remaining = min(self.time_max, self.time_remaining + seconds)

    def _living_players(self) -> list[Player]:
        return [p for p in self.players if getattr(p, "alive", True)]

    def _spawn_players(self) -> None:
        """Spawn P1 (and P2 in co-op) on the floor baseline."""
        base_x = self.current_level.player_x
        coop = self.selected_mode == "2P"
        p1_x = base_x + P1_SPAWN_X_OFFSET if coop else base_x
        p1 = Player(
            p1_x,
            FLOOR_Y,
            player_id=1,
            keymap=P1_KEYS,
            idle_frames=PLAYER_IDLE_FRAMES,
            run_frames=PLAYER_RUN_FRAMES,
        )
        p1.weapon_mode = "harpoon"
        self.players.add(p1)
        if coop:
            p2 = Player(
                base_x + P2_SPAWN_X_OFFSET,
                FLOOR_Y,
                player_id=2,
                keymap=P2_KEYS,
                idle_frames=P2_IDLE_FRAMES,
                run_frames=P2_RUN_FRAMES,
                gun_sprite=P2_GUN_SPRITE,
            )
            p2.weapon_mode = "harpoon"
            self.players.add(p2)

    def reset_match(
        self,
        mode: str | None = None,
        level_id: int | None = None,
    ) -> None:
        if mode is not None:
            self.selected_mode = mode if mode in ("1P", "2P") else "1P"
        if level_id is not None:
            self.selected_level = max(DEFAULT_LEVEL, min(level_id, MAX_LEVEL))

        self.bolas.empty()
        self.bullets.empty()
        self.effects.empty()
        self.powerups.empty()
        self.players.empty()
        self._fire_cooldown_until = {}
        self.state = "playing"
        self._end_sfx_played = False
        self._level_clear_at = 0

        self.current_level = get_level(self.selected_level)
        self.background = build_arena_background(self.current_level.theme)
        now = pygame.time.get_ticks()
        self._doors = self.current_level.make_doors()
        for door in self._doors:
            door.reset(now)
        self._solids = collect_solids(self.current_level, self._doors)
        self._refill_time()
        self._spawn_players()
        if self.selected_mode == "2P":
            self._show_notice("P1 A/D Space · P2 arrows Enter", 2800)
        for spawn in self.current_level.balls:
            self.bolas.add(
                Ball(
                    self._ball_base_image,
                    spawn.tier,
                    spawn.x,
                    spawn.y,
                    spawn.vel,
                )
            )

    def _advance_to_next_level(self) -> None:
        next_id = self.selected_level + 1
        if next_id > MAX_LEVEL:
            self.state = "won"
            return
        self.selected_level = next_id
        self.menu.level = next_id
        self.reset_match(mode=self.selected_mode, level_id=next_id)

    def _try_fire(self, player: Player) -> None:
        if self.state != "playing" or not getattr(player, "alive", True):
            return
        now = pygame.time.get_ticks()
        pid = player.player_id
        if now < self._fire_cooldown_until.get(pid, 0):
            return

        mode = getattr(player, "weapon_mode", "harpoon")
        if mode == "sticky":
            # Unlimited fire rate (cooldown only); map keeps at most STICKY_MAX_ON_MAP
            pass
        else:
            # Planted stickies do not consume harpoon/drill slots; cap is per-player
            active = sum(
                1
                for b in self.bullets
                if getattr(b, "owner_id", None) == pid
                and getattr(b, "mode", "") != "sticky"
            )
            if active >= MAX_BULLETS:
                return

        mx, my = player.muzzle
        self.bullets.add(Bullet(mx, my, mode=mode, owner_id=pid))
        if mode == "sticky":
            self._cull_extra_stickies()
        self.effects.add(ShootEffect(mx, my))
        self._fire_cooldown_until[pid] = now + BULLET_COOLDOWN_MS
        self.audio.play_sfx("shoot")

    def _cull_extra_stickies(self) -> None:
        """Keep only the newest STICKY_MAX_ON_MAP sticky lasers on the map."""
        stickies = sorted(
            (b for b in self.bullets if getattr(b, "mode", "") == "sticky"),
            key=lambda b: getattr(b, "spawned_at", 0),
        )
        overflow = len(stickies) - STICKY_MAX_ON_MAP
        for old in stickies[: max(0, overflow)]:
            old.kill()

    def _resolve_ball_hit(self, ball: Ball) -> None:
        cx, cy = ball.rect.center
        children = ball.split(self._ball_base_image)
        ball.kill()
        self.bolas.add(*children)
        self.audio.play_sfx("ball_pop")
        drop = maybe_spawn_powerup(cx, cy)
        if drop is not None:
            self.powerups.add(drop)

    def _apply_powerup(self, power: Powerup, player: Player) -> None:
        if power.kind == "TIME":
            self.add_time(TIME_POWER_SECONDS)
            self._show_notice(f"+{TIME_POWER_SECONDS}s", 1200)
            return
        if power.kind == "STICKY":
            player.weapon_mode = "sticky"
            self._show_notice(f"P{player.player_id} STICKY", 1200)
        elif power.kind == "DRILL":
            player.weapon_mode = "drill"
            self._show_notice(f"P{player.player_id} DRILL", 1200)

    def _handle_powerup_pickups(self) -> None:
        for player in self._living_players():
            for power in list(self.powerups):
                if player.hitbox.colliderect(power.rect):
                    self._apply_powerup(power, player)
                    power.kill()

    def _handle_bullet_ball_hits(self) -> None:
        # Default/STICKY/DRILL diverge on whether the laser despawns on first hit
        for laser in list(self.bullets):
            mode = getattr(laser, "mode", "harpoon")
            hit_balls = [b for b in self.bolas if laser.rect.colliderect(b.rect)]
            if not hit_balls:
                continue
            if mode == "drill":
                for ball in hit_balls:
                    self._resolve_ball_hit(ball)
                # Drill continues until solid/ceiling (handled in Bullet.update)
                continue
            # harpoon + sticky: first ball resolves and laser dies
            self._resolve_ball_hit(hit_balls[0])
            laser.kill()

    def _remove_player_from_level(self, player: Player) -> None:
        """Co-op: pull one player out of the current level; 1P → game over."""
        player.alive = False
        player.kill()
        self.audio.play_sfx("player_hit")
        if self.selected_mode == "1P" or not self._living_players():
            self.state = "game_over"
        else:
            self._show_notice(f"P{player.player_id} down", 1800)

    def _handle_player_ball_hits(self) -> None:
        for player in list(self._living_players()):
            if any(player.hitbox.colliderect(ball.rect) for ball in self.bolas):
                self._remove_player_from_level(player)

    def _drain_time(self) -> None:
        if self.state != "playing":
            return
        self.time_remaining -= TIME_DRAIN_PER_SEC / FPS
        if self.time_remaining <= 0:
            self.time_remaining = 0.0
            self.state = "game_over"

    def _check_win(self) -> None:
        if self.state != "playing" or len(self.bolas) != 0:
            return
        if self.selected_level < MAX_LEVEL:
            self.state = "level_clear"
            self._level_clear_at = pygame.time.get_ticks()
            self._end_sfx_played = False
        else:
            self.state = "won"

    def _play_end_sfx_once(self) -> None:
        if self._end_sfx_played:
            return
        if self.state in ("won", "level_clear"):
            self.audio.play_sfx("win")
            self._end_sfx_played = True
        elif self.state == "game_over":
            self.audio.play_sfx("lose")
            self._end_sfx_played = True

    def _draw_time_barrier(self) -> None:
        x, y = TIME_BAR_POS
        outer = pygame.Rect(x, y, TIME_BAR_WIDTH, TIME_BAR_HEIGHT)
        pygame.draw.rect(self.screen, TIME_BAR_BG, outer, border_radius=4)
        ratio = 0.0 if self.time_max <= 0 else max(0.0, min(1.0, self.time_remaining / self.time_max))
        fill_w = int((TIME_BAR_WIDTH - 4) * ratio)
        if fill_w > 0:
            fill_color = TIME_BAR_FILL_LOW if ratio <= 0.25 else TIME_BAR_FILL
            fill = pygame.Rect(x + 2, y + 2, fill_w, TIME_BAR_HEIGHT - 4)
            pygame.draw.rect(self.screen, fill_color, fill, border_radius=3)
        pygame.draw.rect(self.screen, TIME_BAR_EDGE, outer, width=2, border_radius=4)

    def _draw_hud(self) -> None:
        if self.state in ("playing", "level_clear", "won", "game_over"):
            self._draw_time_barrier()
            label = self.font.render(
                f"Lv {self.current_level.id}: {self.current_level.name}",
                True,
                _HUD_DIM,
            )
            self.screen.blit(label, (screenWidth - label.get_width() - 12, 12))
            living = self._living_players()
            weapon_y = TIME_BAR_POS[1] + TIME_BAR_HEIGHT + 6
            for p in sorted(living, key=lambda pl: pl.player_id):
                mode = getattr(p, "weapon_mode", "harpoon").upper()
                if mode == "HARPOON":
                    continue
                prefix = f"P{p.player_id} " if self.selected_mode == "2P" else ""
                wlabel = self.font.render(f"{prefix}{mode}", True, _NEON_CYAN)
                self.screen.blit(wlabel, (TIME_BAR_POS[0], weapon_y))
                weapon_y += 22
            if self.selected_mode == "2P" and self.state == "playing":
                down_ids = [
                    pid
                    for pid in (1, 2)
                    if not any(p.player_id == pid for p in living)
                ]
                if down_ids:
                    hint = self.font.render(
                        " · ".join(f"P{pid} down" for pid in down_ids),
                        True,
                        _NEON_MAGENTA,
                    )
                    self.screen.blit(
                        hint,
                        (TIME_BAR_POS[0], screenHeight - 36),
                    )

        if self.state in ("won", "game_over", "level_clear"):
            dim = pygame.Surface((screenWidth, screenHeight), flags=pygame.SRCALPHA)
            dim.fill(_OVERLAY)
            self.screen.blit(dim, (0, 0))

        if self.state == "level_clear":
            msg = self.big_font.render("LEVEL CLEAR", True, _NEON_CYAN)
            hint = self.font.render(
                f"Enter -> Level {self.selected_level + 1} · M menu",
                True,
                _HUD_DIM,
            )
            self.screen.blit(
                msg, msg.get_rect(center=(screenWidth // 2, screenHeight // 2 - 20))
            )
            self.screen.blit(
                hint, hint.get_rect(center=(screenWidth // 2, screenHeight // 2 + 30))
            )
        elif self.state == "won":
            msg = self.big_font.render("YOU WIN", True, _NEON_CYAN)
            hint = self.font.render("R retry · M menu", True, _HUD_DIM)
            self.screen.blit(msg, msg.get_rect(center=(screenWidth // 2, screenHeight // 2 - 20)))
            self.screen.blit(hint, hint.get_rect(center=(screenWidth // 2, screenHeight // 2 + 30)))
        elif self.state == "game_over":
            msg = self.big_font.render("GAME OVER", True, _NEON_MAGENTA)
            hint = self.font.render("R retry · M menu", True, _HUD_DIM)
            self.screen.blit(msg, msg.get_rect(center=(screenWidth // 2, screenHeight // 2 - 20)))
            self.screen.blit(hint, hint.get_rect(center=(screenWidth // 2, screenHeight // 2 + 30)))

    def _go_menu(self) -> None:
        self.state = "menu"
        self.bolas.empty()
        self.bullets.empty()
        self.effects.empty()
        self.powerups.empty()
        self.players.empty()
        self._end_sfx_played = False
        self._notice = None
        self.menu.mode = self.selected_mode
        self.menu.level = self.selected_level
        self.menu.screen = "root"
        self.menu.selected = 0
        self.audio.play_music()

    def _draw_notice(self, now: int) -> None:
        if self._notice is None or now >= self._notice_until:
            self._notice = None
            return
        hint = self.font.render(self._notice, True, _NEON_CYAN)
        self.screen.blit(
            hint, hint.get_rect(center=(screenWidth // 2, screenHeight - 48))
        )

    def runGame(self) -> None:
        run = True
        while run:
            self.clock.tick(FPS)
            now = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if self.state == "menu":
                        result = self.menu.handle_keydown(event.key)
                        if result.quit_app:
                            run = False
                        elif result.start_game:
                            self._sync_selection_from_menu()
                            self.reset_match(
                                mode=self.selected_mode,
                                level_id=self.selected_level,
                            )
                    elif self.state == "playing":
                        for player in self._living_players():
                            if event.key == player.fire_key:
                                self._try_fire(player)
                                break
                    elif (
                        event.key in (pygame.K_RETURN, pygame.K_SPACE)
                        and self.state == "level_clear"
                    ):
                        self._advance_to_next_level()
                    elif event.key == pygame.K_r and self.state in ("won", "game_over"):
                        self.reset_match(
                            mode=self.selected_mode,
                            level_id=self.selected_level,
                        )
                    elif event.key == pygame.K_m and self.state in (
                        "won",
                        "game_over",
                        "level_clear",
                    ):
                        self._go_menu()
                    elif event.key == pygame.K_ESCAPE and self.state in (
                        "won",
                        "game_over",
                        "level_clear",
                        "playing",
                    ):
                        self._go_menu()

            # Auto-advance after a short beat on mid-campaign clears
            if (
                self.state == "level_clear"
                and self._level_clear_at
                and now - self._level_clear_at >= LEVEL_CLEAR_AUTO_MS
            ):
                self._advance_to_next_level()

            self.screen.blit(
                self._menu_background if self.state == "menu" else self.background,
                (0, 0),
            )

            if self.state == "menu":
                self.menu.draw(self.screen)
            else:
                draw_arena_geometry(self.screen, self.current_level, self._doors)

                if self.state == "playing":
                    self._drain_time()
                    for door in self._doors:
                        door.update(now, self.bolas)
                    self._solids = collect_solids(self.current_level, self._doors)
                    self.bolas.update(self._solids)
                    self.bullets.update(self._solids)
                    self.effects.update()
                    self.powerups.update()
                    self.players.update(self._solids)
                    self._handle_bullet_ball_hits()
                    self._handle_powerup_pickups()
                    self._handle_player_ball_hits()
                    self._check_win()

                self._play_end_sfx_once()

                self.bolas.draw(self.screen)
                self.bullets.draw(self.screen)
                self.effects.draw(self.screen)
                self.powerups.draw(self.screen)
                self.players.draw(self.screen)

                self._draw_hud()
                self._draw_notice(now)

            pygame.display.update()

        self.audio.save_settings()
        pygame.quit()


if __name__ == "__main__":
    Game().runGame()
