from __future__ import annotations

import pygame

from assets import load_image
from consts import BULLET_SPRITE, LASER_GROW_SPEED, LASER_WIDTH


class Bullet(pygame.sprite.Sprite):
    """Growing upward laser (classic Bubble Trouble style).

    Modes:
      harpoon — despawn on first ball or solid/ceiling
      sticky  — grow then stay until a ball hits
      drill   — pierce balls; stop on solid/ceiling
    """

    def __init__(
        self,
        x: int,
        base_y: int,
        mode: str = "harpoon",
        *,
        owner_id: int = 1,
    ) -> None:
        super().__init__()
        tip = load_image(BULLET_SPRITE)
        tw, th = tip.get_size()
        tip_w = LASER_WIDTH
        tip_h = max(2, int(th * (LASER_WIDTH / max(1, tw))))
        self._tip = pygame.transform.scale(tip, (tip_w, tip_h))
        self._beam_color = self._tip.get_at((tip_w // 2, tip_h // 2))
        if mode == "sticky":
            self._beam_color = (80, 255, 140, 255)
        elif mode == "drill":
            self._beam_color = (255, 200, 60, 255)

        self.x = x
        self.base_y = base_y
        self.owner_id = owner_id
        self.mode = mode if mode in ("harpoon", "sticky", "drill") else "harpoon"
        self.top = base_y - 1  # start with 1px height, grow upward
        self.planted = False  # sticky: finished growing, waiting for ball
        self.spawned_at = pygame.time.get_ticks()
        self._rebuild()

    def _rebuild(self) -> None:
        height = max(1, self.base_y - self.top)
        image = pygame.Surface((LASER_WIDTH, height), flags=pygame.SRCALPHA)
        if height > self._tip.get_height():
            body_h = height - self._tip.get_height()
            body = pygame.Surface((LASER_WIDTH, body_h), flags=pygame.SRCALPHA)
            body.fill(self._beam_color)
            image.blit(body, (0, self._tip.get_height()))
        image.blit(self._tip, (0, 0))
        self.image = image
        self.rect = self.image.get_rect(midbottom=(self.x, self.base_y))

    def update(self, solids: list[pygame.Rect] | None = None) -> None:
        # Sticky stays put once planted
        if self.mode == "sticky" and self.planted:
            return

        self.top -= LASER_GROW_SPEED
        hit_ceiling = self.top <= 0
        if hit_ceiling:
            self.top = 0
            self._rebuild()
            if self.mode == "sticky":
                self.planted = True
                return
            self.kill()
            return

        self._rebuild()
        for solid in solids or []:
            if self.rect.colliderect(solid):
                # Snap top to solid bottom so the beam doesn't overlap
                self.top = solid.bottom
                self._rebuild()
                if self.mode == "sticky":
                    self.planted = True
                    return
                self.kill()
                return
