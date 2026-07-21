from __future__ import annotations

import pygame

from assets import load_image, load_strip_frames
from consts import (
    GUN_HAND_Y_FRAC,
    GUN_SCALE,
    GUN_SPRITE,
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
        self.idle_sprites = load_strip_frames(PLAYER_IDLE_FRAMES, scale=PLAYER_SCALE)
        self.run_sprites = load_strip_frames(PLAYER_RUN_FRAMES, scale=PLAYER_SCALE)
        # Left-facing hold looks correct; right-facing uses a horizontal mirror
        self._gun_left = self._load_gun_overlay()
        self._gun_right = pygame.transform.flip(self._gun_left, True, False)
        self.facing_right = True
        self.index = 0.0
        self.index_speed = 0.15
        self.vel_x = 8
        self.muzzle = (x, y)
        self.image = self.idle_sprites[0]
        self.rect = self.image.get_rect(midbottom=(x, min(y, screenHeight - 4)))
        self._compose_with_gun(self.idle_sprites[0])
        self.hitbox = self._compute_hitbox()

    @staticmethod
    def _load_gun_overlay() -> pygame.Surface:
        gun = load_image(GUN_SPRITE, scale=GUN_SCALE)
        # Craftpix guns face right; +90° CCW → barrel up
        return pygame.transform.rotate(gun, 90)

    def _compose_with_gun(self, body: pygame.Surface) -> None:
        """Upward pistol at the leading hand; mirrored when facing right."""
        body_box = body.get_bounding_rect(min_alpha=1)
        gun = self._gun_right if self.facing_right else self._gun_left
        gw = gun.get_width()
        # Leading side (direction of facing), tucked against the outer hand
        if self.facing_right:
            hold_x = body_box.right + gw // 2 - 4
        else:
            hold_x = body_box.left - gw // 2 + 4
        hold_y = body_box.top + int(body_box.height * GUN_HAND_Y_FRAC)
        gun_rect = gun.get_rect(midbottom=(hold_x, hold_y))

        union = body.get_rect().union(gun_rect)
        composed = pygame.Surface(union.size, flags=pygame.SRCALPHA)
        ox, oy = -union.x, -union.y
        composed.blit(body, (ox, oy))
        gun_on = gun_rect.move(ox, oy)
        composed.blit(gun, gun_on)

        midbottom = self.rect.midbottom
        self.image = composed
        self.rect = self.image.get_rect(midbottom=midbottom)
        self._body_local = body_box.move(ox, oy)
        self.muzzle = (self.rect.left + gun_on.centerx, self.rect.top + gun_on.top)

    def _compute_hitbox(self) -> pygame.Rect:
        local = getattr(self, "_body_local", None) or self.image.get_bounding_rect(min_alpha=1)
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
        self.rect = frame.get_rect(midbottom=midbottom)
        self._compose_with_gun(frame)
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
