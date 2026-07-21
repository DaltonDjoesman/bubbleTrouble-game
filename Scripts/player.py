from __future__ import annotations

from pathlib import Path

import pygame

from consts import (
    PLAYER_IDLE_FRAMES,
    PLAYER_RUN_FRAMES,
    PLAYER_SCALE,
    screenWidth,
)


class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.idle_sprites = self._load_frame_list(PLAYER_IDLE_FRAMES)
        self.run_sprites = self._load_frame_list(PLAYER_RUN_FRAMES)
        self.facing_right = True
        self.index = 0.0
        self.index_speed = 0.12
        self.vel_x = 8
        self.image = self.idle_sprites[0]
        self.rect = self.image.get_rect(center=(x, y))

    @staticmethod
    def _load_frame_list(paths: list[Path]) -> list[pygame.Surface]:
        frames: list[pygame.Surface] = []
        for path in paths:
            surface = pygame.image.load(path).convert_alpha()
            # cut (full frame) → blit onto transparent surface → scale
            w, h = surface.get_size()
            cut = pygame.Surface((w, h), flags=pygame.SRCALPHA)
            cut.blit(surface, (0, 0), pygame.Rect(0, 0, w, h))
            scaled = pygame.transform.scale(
                cut, (int(w * PLAYER_SCALE), int(h * PLAYER_SCALE))
            )
            frames.append(scaled)
        return frames

    def _current_frames(self, moving: bool) -> list[pygame.Surface]:
        return self.run_sprites if moving else self.idle_sprites

    def _animate(self, moving: bool) -> None:
        frames = self._current_frames(moving)
        if self.index >= len(frames):
            self.index = 0.0
        frame = frames[int(self.index)]
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)
        center = self.rect.center
        self.image = frame
        self.rect = self.image.get_rect(center=center)
        self.index += self.index_speed

    def update(self) -> None:
        dx = 0
        keys = pygame.key.get_pressed()
        moving = False

        if keys[pygame.K_d]:
            dx += self.vel_x
            self.facing_right = True
            moving = True
        elif keys[pygame.K_a]:
            dx -= self.vel_x
            self.facing_right = False
            moving = True

        if self.rect.left + dx < 0 or self.rect.right + dx > screenWidth:
            dx = 0

        self.rect.x += dx
        if not moving:
            self.index = 0.0
        self._animate(moving)
