## 1. Survival level & match rules

- [x] 1.1 Add Survival as selectable level id 6 with a survival-mode flag; keep campaign win/advance capped at level 5 (no auto-advance into Survival)
- [x] 1.2 Branch match loop: Survival uses elapsed chronometer (no drain / no time-out loss) and never wins on clearing all balls
- [x] 1.3 Finalize shared elapsed time on Survival game over (1P hit or 2P both down)

## 2. Spawn director

- [x] 2.1 Implement continuous ball spawns with difficulty ramp (interval + size weighting) and concurrent-ball cap
- [x] 2.2 Make TIME powerup pause spawns briefly in Survival; keep campaign TIME adding barrier seconds

## 3. HUD & end flow

- [ ] 3.1 Show numeric chronometer (and Survival label) in the bottom panel during Survival instead of draining barrier fill
- [ ] 3.2 On Survival game over, show final time; if top-5 for the run's mode board, prompt for 3-letter initials and save

## 4. High scores persistence & menu

- [ ] 4.1 Persist top 5 entries per `1p` / `2p` board in a local JSON file (load/save, corrupt-safe empty fallback)
- [ ] 4.2 Add High Scores menu view with 1P/2P tab switching listing rank, name, and time
- [ ] 4.3 Smoke-test: campaign 1–5 unchanged; Survival spawn/ramp/chronometer; 1P and 2P boards; initials; relaunch persistence
