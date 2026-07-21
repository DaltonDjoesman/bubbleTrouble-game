"""Bubble Trouble — core gameplay entry point.

Run from the repository root:
    python Scripts/main.py
"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import pygame

pygame.init()

from bolinha import Ball
from bullet import Bullet
from consts import (
    BOLA_SPRITE,
    BULLET_COOLDOWN_MS,
    DEFAULT_LIVES,
    FPS,
    IFRAME_MS,
    MAX_BULLETS,
    screenHeight,
    screenWidth,
)
from player import Player
from shoot_effect import ShootEffect

# Cyberpunk palette (HUD + arena)
_BG_TOP = (12, 8, 32)
_BG_BOTTOM = (28, 10, 48)
_NEON_CYAN = (80, 240, 255)
_NEON_MAGENTA = (255, 70, 180)
_HUD_DIM = (180, 200, 220)
_OVERLAY = (8, 4, 20, 180)


def _build_arena_background() -> pygame.Surface:
    """Vertical cyberpunk gradient + scanlines + neon floor accent."""
    surf = pygame.Surface((screenWidth, screenHeight))
    for y in range(screenHeight):
        t = y / max(1, screenHeight - 1)
        r = int(_BG_TOP[0] + (_BG_BOTTOM[0] - _BG_TOP[0]) * t)
        g = int(_BG_TOP[1] + (_BG_BOTTOM[1] - _BG_TOP[1]) * t)
        b = int(_BG_TOP[2] + (_BG_BOTTOM[2] - _BG_TOP[2]) * t)
        pygame.draw.line(surf, (r, g, b), (0, y), (screenWidth, y))
    # Subtle scanlines (skip every other band; keep gradient visible)
    for y in range(2, screenHeight, 4):
        pygame.draw.line(surf, (0, 0, 0), (0, y), (screenWidth, y))
    # Neon floor strip
    pygame.draw.line(
        surf, _NEON_CYAN, (0, screenHeight - 3), (screenWidth, screenHeight - 3), 2
    )
    pygame.draw.line(
        surf, _NEON_MAGENTA, (0, screenHeight - 6), (screenWidth, screenHeight - 6), 1
    )
    return surf


class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Bubble Trouble")
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 64)
        self.background = _build_arena_background()

        self.bolas = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.bullets = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()

        self.state = "playing"
        self.lives = DEFAULT_LIVES
        self.iframe_until = 0
        self.fire_cooldown_until = 0

        self._ball_base_image = pygame.image.load(BOLA_SPRITE).convert_alpha()
        self.reset_match()

    def reset_match(self) -> None:
        self.bolas.empty()
        self.bullets.empty()
        self.effects.empty()
        self.player.empty()
        self.lives = DEFAULT_LIVES
        self.iframe_until = 0
        self.fire_cooldown_until = 0
        self.state = "playing"

        self.player.add(Player(screenWidth // 2, screenHeight - 4))
        # Playable arena: one large + one medium ball
        self.bolas.add(
            Ball(self._ball_base_image, "L", screenWidth // 3, screenHeight // 3, (2, 0))
        )
        self.bolas.add(
            Ball(
                self._ball_base_image,
                "M",
                2 * screenWidth // 3,
                screenHeight // 4,
                (-2, 0),
            )
        )

    def _try_fire(self) -> None:
        if self.state != "playing":
            return
        now = pygame.time.get_ticks()
        if now < self.fire_cooldown_until:
            return
        if len(self.bullets) >= MAX_BULLETS:
            return
        p = self.player.sprite
        if p is None:
            return
        # Laser grows upward from the player's top (classic vertical beam)
        self.bullets.add(Bullet(p.rect.centerx, p.rect.top))
        self.effects.add(ShootEffect(p.rect.centerx, p.rect.top))
        self.fire_cooldown_until = now + BULLET_COOLDOWN_MS

    def _handle_bullet_ball_hits(self) -> None:
        # Laser removed on hit; ball split/removed
        hits = pygame.sprite.groupcollide(self.bullets, self.bolas, True, False)
        for _laser, balls in hits.items():
            for ball in balls:
                children = ball.split(self._ball_base_image)
                ball.kill()
                self.bolas.add(*children)

    def _handle_player_ball_hits(self) -> None:
        p = self.player.sprite
        if p is None:
            return
        now = pygame.time.get_ticks()
        if now < self.iframe_until:
            return
        hit = any(p.hitbox.colliderect(ball.rect) for ball in self.bolas)
        if not hit:
            return

        self.lives -= 1
        if self.lives <= 0:
            self.lives = 0
            self.state = "game_over"
            return

        # Stay in place; brief i-frames only
        self.iframe_until = now + IFRAME_MS
        self.bullets.empty()

    def _check_win(self) -> None:
        if self.state == "playing" and len(self.bolas) == 0:
            self.state = "won"

    def _draw_hud(self) -> None:
        # High-contrast lives label (shadow + neon)
        label = f"Lives: {self.lives}"
        shadow = self.font.render(label, True, (0, 0, 0))
        lives_surf = self.font.render(label, True, _NEON_CYAN)
        self.screen.blit(shadow, (12, 12))
        self.screen.blit(lives_surf, (10, 10))

        if self.state in ("won", "game_over"):
            dim = pygame.Surface((screenWidth, screenHeight), flags=pygame.SRCALPHA)
            dim.fill(_OVERLAY)
            self.screen.blit(dim, (0, 0))

        if self.state == "won":
            msg = self.big_font.render("YOU WIN", True, _NEON_CYAN)
            hint = self.font.render("Press R to restart", True, _HUD_DIM)
            self.screen.blit(msg, msg.get_rect(center=(screenWidth // 2, screenHeight // 2 - 20)))
            self.screen.blit(hint, hint.get_rect(center=(screenWidth // 2, screenHeight // 2 + 30)))
        elif self.state == "game_over":
            msg = self.big_font.render("GAME OVER", True, _NEON_MAGENTA)
            hint = self.font.render("Press R to restart", True, _HUD_DIM)
            self.screen.blit(msg, msg.get_rect(center=(screenWidth // 2, screenHeight // 2 - 20)))
            self.screen.blit(hint, hint.get_rect(center=(screenWidth // 2, screenHeight // 2 + 30)))

    def runGame(self) -> None:
        run = True
        while run:
            self.clock.tick(FPS)
            now = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.state == "playing":
                        self._try_fire()
                    elif event.key == pygame.K_r and self.state in ("won", "game_over"):
                        self.reset_match()

            self.screen.blit(self.background, (0, 0))

            if self.state == "playing":
                self.bolas.update()
                self.bullets.update()
                self.effects.update()
                self.player.update()
                self._handle_bullet_ball_hits()
                self._handle_player_ball_hits()
                self._check_win()

            self.bolas.draw(self.screen)
            self.bullets.draw(self.screen)
            self.effects.draw(self.screen)
            # Blink player during i-frames
            if self.player.sprite is not None:
                if self.state != "playing" or now >= self.iframe_until or (now // 100) % 2 == 0:
                    self.player.draw(self.screen)

            self._draw_hud()
            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    Game().runGame()
