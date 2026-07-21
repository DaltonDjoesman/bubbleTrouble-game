from __future__ import annotations

import pygame

from assets import load_strip_frames
from consts import (
    PLAYER_HITBOX_INSET,
    PLAYER_IDLE_FRAMES,
    PLAYER_RUN_FRAMES,
    PLAYER_SCALE,
    screenHeight,
    screenWidth,
)


class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        # Rects derive from scaled Craftpix frames (SPRITE_SCALE via PLAYER_SCALE)
        self.idle_sprites = load_strip_frames(PLAYER_IDLE_FRAMES, scale=PLAYER_SCALE)
        self.run_sprites = load_strip_frames(PLAYER_RUN_FRAMES, scale=PLAYER_SCALE)
        self.facing_right = True
        self.index = 0.0
        self.index_speed = 0.15
        self.vel_x = 8
        self.image = self.idle_sprites[0]
        # (x, y) is midbottom — feet near arena floor
        self.rect = self.image.get_rect(midbottom=(x, min(y, screenHeight - 4)))
        self.hitbox = self._compute_hitbox()

    def _compute_hitbox(self) -> pygame.Rect:
        """Tight box around opaque pixels, slightly inset for fair collisions."""
        local = self.image.get_bounding_rect(min_alpha=1)
        if local.width <= 0 or local.height <= 0:
            local = self.image.get_rect()
        box = local.move(self.rect.topleft)
        inset_x = max(1, int(box.width * PLAYER_HITBOX_INSET))
        inset_y = max(1, int(box.height * PLAYER_HITBOX_INSET))
        return box.inflate(-2 * inset_x, -2 * inset_y)

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
        self.hitbox = self._compute_hitbox()
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
