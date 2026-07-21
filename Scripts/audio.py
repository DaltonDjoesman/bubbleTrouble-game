"""Background music and SFX via pygame.mixer (graceful no-op if unavailable)."""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import pygame

from consts import (
    AUDIO_MUSIC_PATH,
    AUDIO_SFX,
    SETTINGS_PATH,
    VOLUME_DEFAULT,
    VOLUME_MAX,
)

logger = logging.getLogger(__name__)

# Internal mixer scale for a 0..VOLUME_MAX UI step
_VOL_SCALE = 1.0 / VOLUME_MAX


class AudioManager:
    """Owns mixer init, volumes, BGM loop, and named one-shot SFX."""

    def __init__(self) -> None:
        self.available = False
        self.music_volume = VOLUME_DEFAULT
        self.sfx_volume = VOLUME_DEFAULT
        self._sounds: dict[str, pygame.mixer.Sound] = {}
        self._music_loaded = False

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.available = True
        except pygame.error as exc:
            logger.warning("Audio mixer unavailable; running silent: %s", exc)
            self.available = False
            return

        self.load_settings()
        self._load_sfx()
        self._apply_volumes()

    def _load_sfx(self) -> None:
        if not self.available:
            return
        for name, path in AUDIO_SFX.items():
            try:
                self._sounds[name] = pygame.mixer.Sound(str(path))
            except pygame.error as exc:
                logger.warning("Could not load SFX %s (%s): %s", name, path, exc)

    def load_settings(self) -> None:
        path = SETTINGS_PATH
        if not path.is_file():
            return
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning("Could not read settings from %s: %s", path, exc)
            return
        self.music_volume = _clamp_volume(data.get("music_volume", self.music_volume))
        self.sfx_volume = _clamp_volume(data.get("sfx_volume", self.sfx_volume))

    def save_settings(self) -> None:
        payload: dict[str, Any] = {
            "music_volume": self.music_volume,
            "sfx_volume": self.sfx_volume,
        }
        try:
            SETTINGS_PATH.write_text(
                json.dumps(payload, indent=2) + "\n", encoding="utf-8"
            )
        except OSError as exc:
            logger.warning("Could not save settings to %s: %s", SETTINGS_PATH, exc)

    def set_music_volume(self, value: int) -> None:
        self.music_volume = _clamp_volume(value)
        self._apply_volumes()

    def set_sfx_volume(self, value: int) -> None:
        self.sfx_volume = _clamp_volume(value)
        self._apply_volumes()

    def adjust_music_volume(self, delta: int) -> None:
        self.set_music_volume(self.music_volume + delta)

    def adjust_sfx_volume(self, delta: int) -> None:
        self.set_sfx_volume(self.sfx_volume + delta)

    def _apply_volumes(self) -> None:
        if not self.available:
            return
        pygame.mixer.music.set_volume(self.music_volume * _VOL_SCALE)
        sfx_v = self.sfx_volume * _VOL_SCALE
        for sound in self._sounds.values():
            sound.set_volume(sfx_v)

    def play_music(self) -> None:
        if not self.available or self.music_volume <= 0:
            return
        try:
            if not self._music_loaded:
                if not AUDIO_MUSIC_PATH.is_file():
                    logger.warning("Music file missing: %s", AUDIO_MUSIC_PATH)
                    return
                pygame.mixer.music.load(str(AUDIO_MUSIC_PATH))
                self._music_loaded = True
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(self.music_volume * _VOL_SCALE)
        except pygame.error as exc:
            logger.warning("Could not play music: %s", exc)

    def stop_music(self) -> None:
        if not self.available:
            return
        try:
            pygame.mixer.music.stop()
        except pygame.error:
            pass

    def play_sfx(self, name: str) -> None:
        if not self.available or self.sfx_volume <= 0:
            return
        sound = self._sounds.get(name)
        if sound is None:
            return
        try:
            sound.play()
        except pygame.error as exc:
            logger.warning("Could not play SFX %s: %s", name, exc)


def _clamp_volume(value: Any) -> int:
    try:
        n = int(value)
    except (TypeError, ValueError):
        return VOLUME_DEFAULT
    return max(0, min(VOLUME_MAX, n))


# Module-level singleton created after pygame/mixer bootstrap in main.
audio: AudioManager | None = None


def init_audio() -> AudioManager:
    """Create the global AudioManager (call once after pygame.init)."""
    global audio
    audio = AudioManager()
    return audio
