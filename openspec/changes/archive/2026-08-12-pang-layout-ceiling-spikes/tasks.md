## 1. Play-area bounds

- [x] 1.1 Add play-area / bottom-panel constants in `consts.py` (`HUD_PANEL_HEIGHT`, `PLAY_TOP`, `PLAY_BOTTOM` / related helpers) while keeping window 800×600
- [x] 1.2 Derive `FLOOR_Y` from the play-area bottom and update player / powerup / level spawn call sites that assumed `screenHeight` as floor
- [x] 1.3 Update ball left/right/floor bounce and laser ceiling checks to use play-area bounds (not full window)

## 2. Bottom Pang-style HUD

- [x] 2.1 Draw a reserved bottom status panel (brick/framed Pang-inspired chrome) below the play rect
- [x] 2.2 Move time barrier fill and level indicator into the panel; remove top floating time/level overlay
- [x] 2.3 Relocate weapon-mode hint and co-op “P down” so they do not fight the new panel layout

## 3. Ceiling spikes

- [x] 3.1 Draw a continuous downward spike row along the top of the play area
- [x] 3.2 Detect ball ∩ spike-band collision each update and resolve via existing ball-hit split path (SFX + powerup chance)
- [x] 3.3 Ensure spike contact works on every level during play; avoid same-frame infinite split loops (spawn children below band if needed)

## 4. Presentation & smoke test

- [x] 4.1 Clip or size arena background/geometry so play art fills the play rect and panel stays chrome
- [x] 4.2 Manually smoke-test: floor above panel, time/level in panel, ball hits spikes and splits, lasers stop at play top, barriers/crawl still work
