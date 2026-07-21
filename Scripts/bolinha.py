from __future__ import annotations

import pygame

from consts import BALL_SIZES, GRAVITY, screenHeight, screenWidth


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
        bw, bh = base_image.get_size()
        self.image = pygame.transform.scale(
            base_image, (max(1, int(bw * scale)), max(1, int(bh * scale)))
        )
        self.rect = self.image.get_rect(center=(int(x), int(y)))
        self.vel_x, self.vel_y = float(vel[0]), float(vel[1])

    def update(self) -> None:
        if self.rect.left + self.vel_x <= 0 or self.rect.right + self.vel_x >= screenWidth:
            self.vel_x *= -1

        self.rect.x += int(self.vel_x)

        self.vel_y += GRAVITY
        if self.rect.bottom + self.vel_y > screenHeight:
            self.vel_y = self.bounce_impulse

        self.rect.y += int(self.vel_y)

    def split(self, base_image: pygame.Surface) -> list[Ball]:
        """Resolve a hit: spawn two smaller balls, or nothing if already smallest."""
        next_size = BALL_SIZES[self.size]["next"]
        if next_size is None:
            return []
        cx, cy = self.rect.center
        speed = abs(self.vel_x) if self.vel_x != 0 else 2.0
        return [
            Ball(base_image, next_size, cx - 8, cy, (-speed, self.bounce_impulse * 0.6)),
            Ball(base_image, next_size, cx + 8, cy, (speed, self.bounce_impulse * 0.6)),
        ]
