from __future__ import annotations

from pathlib import Path

import pygame

from consts import (
    PLAYER_FRAME_SIZE,
    PLAYER_IDLE_FRAMES,
    PLAYER_RUN_FRAMES,
    PLAYER_SCALE,
    screenHeight,
    screenWidth,
)


class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.idle_sprites = self._load_strip_frames(PLAYER_IDLE_FRAMES)
        self.run_sprites = self._load_strip_frames(PLAYER_RUN_FRAMES)
        self.facing_right = True
        self.index = 0.0
        self.index_speed = 0.15
        self.vel_x = 8
        self.image = self.idle_sprites[0]
        # (x, y) is midbottom — feet near arena floor
        self.rect = self.image.get_rect(midbottom=(x, min(y, screenHeight - 4)))

    @staticmethod
    def _load_strip_frames(paths: list[Path]) -> list[pygame.Surface]:
        """Cut each Craftpix strip into 48×48 cells, then scale."""
        frames: list[pygame.Surface] = []
        cell = PLAYER_FRAME_SIZE
        out_size = (cell * PLAYER_SCALE, cell * PLAYER_SCALE)
        for path in paths:
            surface = pygame.image.load(path).convert_alpha()
            w, h = surface.get_size()
            for col in range(w // cell):
                cut = pygame.Surface((cell, cell), flags=pygame.SRCALPHA)
                cut.blit(surface, (0, 0), pygame.Rect(col * cell, 0, cell, min(cell, h)))
                frames.append(pygame.transform.scale(cut, out_size))
        if not frames:
            raise ValueError(f"No frames loaded from {paths}")
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
        midbottom = self.rect.midbottom
        self.image = frame
        self.rect = self.image.get_rect(midbottom=midbottom)
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
