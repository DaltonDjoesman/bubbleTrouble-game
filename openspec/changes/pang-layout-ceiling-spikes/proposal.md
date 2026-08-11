## Why

The match window still uses the full 800×600 as playfield with a floating top HUD, so it does not read like classic Pang / Bubble Trouble. Players also lack the signature ceiling hazard: balls that rise into the spiked roof should pop and split instead of drifting off-screen.

## What Changes

- Reserve a **bottom status panel** (Pang-style brick / framed strip) so the play arena is smaller than the window.
- Move **time barrier** and **level** into that bottom panel (visual presentation closer to the classic UI; still no multi-life stock or score).
- Add a **ceiling spike / pointed chain hazard** along the top of the play area; balls that touch it are treated like a laser hit (**split** into smaller balls, or remove if smallest).
- Update floor / spawn / bounce / laser-ceiling math so gameplay uses the reduced play rect, not the full window.
- Keep cyberpunk arena art inside the play rect; panel chrome can be Pang-inspired without restoring retired lives HUD.

## Capabilities

### New Capabilities
- `ceiling-hazards`: Spiked / pointed ceiling along the play-area top that destroys/splits balls on contact.

### Modified Capabilities
- `hud-feedback`: Time barrier and level relocate to a reserved bottom Pang-style panel; top overlay HUD removed for those elements.
- `arena-geometry`: Playable region shrinks to leave a bottom UI strip; floor and solid interactions use that region.
- `ball-system`: Balls collide with the ceiling hazard (split/destroy) instead of escaping through the top of the screen.

## Impact

- `Scripts/consts.py` — play-area / HUD / spike layout constants.
- `Scripts/main.py` — HUD draw, match loop, ceiling-hit resolution (reuse ball-hit split path).
- `Scripts/bolinha.py` — top-of-play collision / spike contact.
- `Scripts/player.py`, `Scripts/levels.py`, `Scripts/powerup.py`, `Scripts/bullet.py` — floor Y, spawn, laser ceiling use play-area bounds.
- `Scripts/` background / geometry helpers — draw play rect vs bottom panel; optional procedural spike row.
- Specs: `hud-feedback`, `arena-geometry`, `ball-system`; new `ceiling-hazards`.
- No new runtime dependencies; spikes can be drawn procedurally if no sprite pack is added.
