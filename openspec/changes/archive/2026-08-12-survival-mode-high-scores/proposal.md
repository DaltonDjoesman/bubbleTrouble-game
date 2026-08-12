## Why

The campaign ends after clearing a finite arena pack, with no endless challenge or lasting run record. A final Survival level with an ascending chronometer, escalating ball spawns, and local top-5 leaderboards (1P / 2P) gives replay value and a clear “best run” goal after the story pack.

## What Changes

- Add **Survival** as the last selectable level (after the five campaign arenas).
- In Survival: **no time drain / no time-out loss**; shared **elapsed chronometer** counts up; lose only when the last living player dies (1P one-hit; 2P when both are down).
- **Never win by clearing balls** — empty arena just waits for the next spawn.
- **Continuous ball spawns** with difficulty ramp (faster spawns and/or larger balls) and a concurrent-ball cap.
- On a qualifying run, prompt for a **3-letter name** and save into the matching board (1P or 2P).
- Persist **top 5** times per board locally; show them in a menu High Scores view with **1P / 2P tabs**.
- HUD in Survival shows a **numeric chronometer** (not a draining barrier fill); campaign levels keep the time barrier.
- TIME powerup in Survival **briefly pauses spawns** (does not add barrier seconds).
- Campaign clear of level 5 still ends in **YOU WIN** and does **not** auto-advance into Survival (Survival is entered from level select).

## Capabilities

### New Capabilities
- `survival-mode`: Endless Survival level rules — chronometer, spawn ramp, lose conditions, initials entry, TIME-as-spawn-pause.
- `high-scores`: Local top-5 persistence and menu UI with separate 1P / 2P boards (tab switching).

### Modified Capabilities
- `level-system`: Sixth selectable entry “Survival”; campaign advance/win still keyed to the five clearable arenas.
- `match-rules`: Survival match lifecycle differs from time-barrier campaign (no timer game over; no clear-all win).
- `hud-feedback`: Survival HUD shows elapsed chronometer instead of draining time barrier fill.
- `main-menu`: Access to High Scores (1P/2P tabs) and Survival in level select.
- `powerups`: TIME behavior in Survival pauses spawns rather than adding barrier time.

## Impact

- `Scripts/levels.py` — Survival level definition / flag.
- `Scripts/main.py` — match loop branches, spawn director, chronometer, initials UI, end overlay.
- `Scripts/menu.py` — Survival in select; High Scores screen with tabs.
- New small module or helpers for score load/save (pattern like `settings.json` / `audio.py`).
- `Scripts/powerup.py` / pickup apply path — Survival TIME semantics.
- Specs listed above; no new third-party dependencies.
