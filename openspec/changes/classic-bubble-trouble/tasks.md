## 1. Classic locomotion and match stakes

- [x] 1.1 Remove jump/air control; keep player locked to floor baseline
- [x] 1.2 Reduce horizontal move speed (~25%) via consts and wire through Player
- [x] 1.3 Replace lives with per-level time budget + fixed drain; empty time → game over
- [x] 1.4 Single-player ball hit → immediate game over (remove life decrement / i-frame continue)

## 2. HUD

- [x] 2.1 Draw time barrier fill from remaining time (reuse/adapt red bar look)
- [x] 2.2 Remove life sprite / life-capsule HUD from playing state

## 3. Barriers and doors

- [x] 3.1 Change level schema: barriers + doors + `time_seconds`; drop platforms
- [x] 3.2 Collision: balls and lasers solid vs barriers / closed doors; player crawl under gaps
- [x] 3.3 Implement door modes: timed cycle and lane-clear open
- [x] 3.4 Update draw path for barriers/doors (no platform shelves)

## 4. Weapons and powerups

- [x] 4.1 Add weapon mode state (default harpoon / STICKY / DRILL); reset on level start
- [x] 4.2 STICKY: plant one sticky line that stays until ball hit; keep planted on mode switch
- [x] 4.3 DRILL: pierce all balls on vertical path until barrier/closed door/ceiling
- [x] 4.4 Default harpoon: despawn on first ball or ceiling/barrier as today + solids
- [x] 4.5 Random drops on ball kill; pickup TIME (+seconds), STICKY, DRILL; one weapon at a time

## 5. Redesign five levels

- [x] 5.1 Author L1–L5 around open / barriers / timed doors / lane-clear / mix (no platforms)
- [x] 5.2 Set per-level `time_seconds`; verify advance refills time and resets weapon
- [x] 5.3 Manual smoke: clear each level path, time-out lose, one-hit lose, each power once

## 6. Sibling change alignment

- [ ] 6.1 Update `local-coop` proposal/design/specs/tasks for per-player death, revive next level, shared time (no shared lives)
- [ ] 6.2 Update `game-documentation` proposal/design/specs/tasks for classic rules (time, one-hit, barriers, powers); defer writing README until after playable apply
