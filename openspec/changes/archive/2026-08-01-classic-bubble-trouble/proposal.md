## Why

The current build drifts from classic Bubble Trouble: jump + platforms + multi-life HUD. We want the original feel — grounded movement, time pressure, one-hit death, power drops, and level variety from balls + vertical barriers/doors.

## What Changes

- **BREAKING**: Remove jump; player stays on the floor and moves slower horizontally
- **BREAKING**: Remove platforms; scrap current 5 platform layouts and redesign around vertical barriers and doors
- **BREAKING**: Remove multi-life system and life HUD/barrier; one hit in single-player ends the match
- Add a **time barrier** (shared countdown bar): full at level start, fixed drain rate, empty = instant lose; levels may set different starting seconds
- Add **powerups** dropped at random on ball kills: TIME (+seconds), STICKY (weapon mode), DRILL (weapon mode); only one weapon at a time; default = current growing harpoon
- STICKY: unlimited fire (cooldown only); at most 3 lines stay on the map (oldest replaced); ball hit resolves + despawns that line
- DRILL: shot passes through all balls on that vertical line (barriers/doors still solid)
- Barriers/doors are solid for balls and lasers; door open rules vary per door (timed cycle and/or open when lane clear)
- Co-op rules (for when `local-coop` lands): hit removes that player only; partner continues; both respawn on next level; shared time bar; both dead or time empty = game over
- Align sibling open changes: `local-coop` and `game-documentation` must be updated to match (not re-applied as-is)

## Capabilities

### New Capabilities

- `powerups`: Random ball-kill drops, pickup, weapon modes (TIME / STICKY / DRILL), one active weapon

### Modified Capabilities

- `player-controls`: No jump; grounded-only; slower horizontal speed
- `match-rules`: One-hit lose (1P); time-bar lose; level time budget; co-op death/revive contract
- `arena-geometry`: Replace platforms with barriers and doors (solid to balls and lasers)
- `ball-system`: Balls bounce on barriers/doors instead of platforms
- `level-system`: Level schema uses barriers/doors + `time_seconds`; redesign five levels
- `projectile-combat`: Default harpoon plus STICKY plant and DRILL pierce behaviors
- `hud-feedback`: Show time barrier instead of lives
- `life-hud-sprites`: Retire multi-life sprite HUD requirement (no longer used in play)

## Impact

- Code: `Scripts/player.py`, `main.py`, `bullet.py`, `levels.py`, `bolinha.py`, `consts.py`; likely new powerup/door helpers; HUD draw path in `Game`
- Content: full rewrite of five authored levels
- Specs: supersedes platform-centric `level-pack` geometry model
- Open changes: pause apply of `local-coop` and `game-documentation` until rebased on these rules
- Out of scope here: writing final README/gameplay docs (update that change’s plan; ship docs after this plays); online/PvP; level editor
