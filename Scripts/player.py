from __future__ import annotations

from pathlib import Path
from typing import Mapping

import pygame

from assets import load_image, load_strip_frames
from consts import (
    GUN_HAND_Y_FRAC,
    GUN_SCALE,
    GUN_SPRITE,
    P1_KEYS,
    PLAYER_HITBOX_INSET,
    PLAYER_IDLE_FRAMES,
    PLAYER_RUN_FRAMES,
    PLAYER_SCALE,
    PLAYER_VEL_X,
    screenHeight,
    screenWidth,
)

FLOOR_Y = screenHeight - 4

# pygame.key.get_pressed() indices for named keys
_KEY_NAME_TO_CODE: dict[str, int] = {
    "a": pygame.K_a,
    "d": pygame.K_d,
    "space": pygame.K_SPACE,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "return": pygame.K_RETURN,
    "rctrl": pygame.K_RCTRL,
}


def resolve_key(name: str) -> int:
    """Map a keymap string to a pygame key constant."""
    code = _KEY_NAME_TO_CODE.get(name.lower())
    if code is None:
        raise KeyError(f"Unknown key name: {name!r}")
    return code


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        x: int,
        y: int,
        *,
        player_id: int = 1,
        keymap: Mapping[str, str] | None = None,
        idle_frames: list[Path] | None = None,
        run_frames: list[Path] | None = None,
        gun_sprite: Path | None = None,
    ) -> None:
        super().__init__()
        self.player_id = player_id
        self.keymap = dict(keymap if keymap is not None else P1_KEYS)
        self._key_left = resolve_key(self.keymap["left"])
        self._key_right = resolve_key(self.keymap["right"])
        self._key_fire = resolve_key(self.keymap["fire"])

        idle_paths = idle_frames if idle_frames is not None else PLAYER_IDLE_FRAMES
        run_paths = run_frames if run_frames is not None else PLAYER_RUN_FRAMES
        self.idle_sprites = load_strip_frames(idle_paths, scale=PLAYER_SCALE)
        self.run_sprites = load_strip_frames(run_paths, scale=PLAYER_SCALE)
        # Left-facing hold looks correct; right-facing uses a horizontal mirror
        self._gun_left = self._load_gun_overlay(gun_sprite if gun_sprite is not None else GUN_SPRITE)
        self._gun_right = pygame.transform.flip(self._gun_left, True, False)
        self.facing_right = True
        self.index = 0.0
        self.index_speed = 0.15
        self.vel_x = PLAYER_VEL_X
        self.weapon_mode = "harpoon"
        self.alive = True
        self.muzzle = (x, y)
        self.image = self.idle_sprites[0]
        self.rect = self.image.get_rect(midbottom=(x, min(y, FLOOR_Y)))
        self._compose_with_gun(self.idle_sprites[0])
        self.hitbox = self._compute_hitbox()

    @property
    def fire_key(self) -> int:
        return self._key_fire

    @staticmethod
    def _load_gun_overlay(gun_path: Path) -> pygame.Surface:
        gun = load_image(gun_path, scale=GUN_SCALE)
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

    def _body_box(self) -> pygame.Rect:
        """Solid collider from body hitbox — ignores gun overhang in self.rect (~96px)."""
        hb = self.hitbox
        w = max(16, hb.width)
        h = max(24, hb.height)
        return pygame.Rect(
            self.rect.centerx - w // 2,
            self.rect.bottom - h,
            w,
            h,
        )

    def _apply_body_box(self, box: pygame.Rect) -> None:
        """Keep sprite feet locked to the body collider after resolution."""
        self.rect.midbottom = (box.centerx, box.bottom)

    def _clamp_body_to_screen(self, box: pygame.Rect) -> pygame.Rect:
        if box.left < 0:
            box.x = 0
        if box.right > screenWidth:
            box.x = screenWidth - box.width
        return box

    def _resolve_horizontal(self, solids: list[pygame.Rect]) -> None:
        """Block against floor-reaching solids; crawl gaps under barriers stay passable."""
        box = self._body_box()
        for solid in solids:
            if not box.colliderect(solid):
                continue
            if box.centerx < solid.centerx:
                box.right = solid.left
            else:
                box.left = solid.right
        box = self._clamp_body_to_screen(box)
        self._apply_body_box(box)

    def update(self, solids: list[pygame.Rect] | None = None) -> None:
        if not self.alive:
            return
        solids = solids or []
        dx = 0
        keys = pygame.key.get_pressed()
        moving = False

        if keys[self._key_right]:
            dx += self.vel_x
            self.facing_right = True
            moving = True
        elif keys[self._key_left]:
            dx -= self.vel_x
            self.facing_right = False
            moving = True

        # Screen bounds use body collider — not visual rect (gun overhang ~96px)
        box = self._body_box()
        if box.left + dx < 0:
            dx = -box.left
        elif box.right + dx > screenWidth:
            dx = screenWidth - box.right

        self.rect.x += dx
        self._resolve_horizontal(solids)

        # Classic: locked to floor baseline (no jump / platform standing)
        self.rect.bottom = FLOOR_Y

        if not moving:
            self.index = 0.0
        self._animate(moving)
        self.rect.bottom = FLOOR_Y
        self.hitbox = self._compute_hitbox()
