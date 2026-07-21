## 1. Acquire audio assets

- [x] 1.1 Create `audio/music` and `audio/sfx` folders
- [x] 1.2 Obtain permissive-license BGM + SFX (shoot, pop, hit, win, lose, UI); add credit notes
- [x] 1.3 Prefer OGG/WAV compatible with pygame.mixer

## 2. Audio manager

- [ ] 2.1 Init mixer in bootstrap; implement play_music / play_sfx / set volumes
- [ ] 2.2 Hook SFX to shoot, ball hit/split, player hit, win, lose, menu navigate/confirm
- [ ] 2.3 Graceful no-op if mixer/device unavailable

## 3. Menu volumes + persistence

- [ ] 3.1 Menu controls for music volume and SFX volume (independent)
- [ ] 3.2 Save/load volumes (e.g. `settings.json`)
- [ ] 3.3 Manual check: mute each channel, relaunch persistence
