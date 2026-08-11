from __future__ import annotations

import pygame

from consts import (
    BALL_SIZES,
    BALL_TINTS,
    FLOOR_Y,
    GRAVITY,
    PLAY_LEFT,
    PLAY_RIGHT,
)


def _tint_surface(base: pygame.Surface, tint: tuple[int, int, int]) -> pygame.Surface:
    """Multiply white-ish ball pixels toward a neon tint (preserves alpha)."""
    out = base.copy()
    tint_layer = pygame.Surface(out.get_size(), flags=pygame.SRCALPHA)
    tint_layer.fill((*tint, 255))
    out.blit(tint_layer, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return out


class Ball(pygame.sprite.Sprite):
    def __init__(
        self,
        base_image: pygame.Surface,
        size: str,
        x: float,
        y: float,
        vel: tuple[float, float],
    ) -> None:
        super().__init__()
        if size not in BALL_SIZES:
            raise ValueError(f"Unknown ball size: {size}")
        self.size = size
        self.bounce_impulse = BALL_SIZES[size]["bounce"]
        scale = BALL_SIZES[size]["scale"]
        tinted = _tint_surface(base_image, BALL_TINTS[size])
        bw, bh = tinted.get_size()
        self.image = pygame.transform.scale(
            tinted, (max(1, int(bw * scale)), max(1, int(bh * scale)))
        )
        self.rect = self.image.get_rect(center=(int(x), int(y)))
        self.vel_x, self.vel_y = float(vel[0]), float(vel[1])

    def update(self, solids: list[pygame.Rect] | None = None) -> None:
        solids = solids or []

        if (
            self.rect.left + self.vel_x <= PLAY_LEFT
            or self.rect.right + self.vel_x >= PLAY_RIGHT
        ):
            self.vel_x *= -1

        self.rect.x += int(self.vel_x)
        for solid in solids:
            if not self.rect.colliderect(solid):
                continue
            if self.vel_x > 0:
                self.rect.right = solid.left
            else:
                self.rect.left = solid.right
            self.vel_x *= -1
            break

        self.vel_y += GRAVITY
        self.rect.y += int(self.vel_y)

        if self.rect.bottom > FLOOR_Y:
            self.rect.bottom = FLOOR_Y
            self.vel_y = self.bounce_impulse

        for solid in solids:
            if not self.rect.colliderect(solid):
                continue
            if self.vel_y >= 0:
                # Land / bounce on top
                self.rect.bottom = solid.top
                self.vel_y = self.bounce_impulse
            else:
                # Hit underside
                self.rect.top = solid.bottom
                self.vel_y = abs(self.vel_y) * 0.35
            break

    def split(
        self,
        base_image: pygame.Surface,
        *,
        spawn_y: float | None = None,
    ) -> list[Ball]:
        """Resolve a hit: spawn two smaller balls, or nothing if already smallest."""
        next_size = BALL_SIZES[self.size]["next"]
        if next_size is None:
            return []
        cx = self.rect.centerx
        cy = float(self.rect.centery if spawn_y is None else spawn_y)
        speed = abs(self.vel_x) if self.vel_x != 0 else 2.0
        return [
            Ball(base_image, next_size, cx - 8, cy, (-speed, self.bounce_impulse * 0.6)),
            Ball(base_image, next_size, cx + 8, cy, (speed, self.bounce_impulse * 0.6)),
        ]
