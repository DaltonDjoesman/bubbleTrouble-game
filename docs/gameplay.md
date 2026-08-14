# Gameplay notes

Shipped rules for this build. Install and run from the [root README](../README.md).

There is no jump, no platforms, and no multi-life stock. Survival is a draining **time barrier** (campaign) or an elapsed **chronometer** (Survival mode).

## Menu flow

The game boots to a cyberpunk main menu. A match starts only after Play.

1. **PLAY GAME** — opens level select. Tabs: **Campaign** (levels 1–5) and **Survival**. Confirm a level to start.
2. **MODE** — 1P or 2P (A/D). 2P starts a real co-op match, not a silent 1P fallback.
3. **HIGH SCORES** — Survival boards. Switch **1P / 2P** tabs (A/D). Empty boards show an empty state.
4. **OPTIONS** — music and SFX volumes, 0–10, saved across launches.
5. **QUIT** — exits.

Esc backs out of Options, level select, and High Scores.

## Campaign vs Survival

| | Campaign | Survival |
|--|----------|----------|
| Goal | Clear all balls on each of five levels; clearing level 5 wins | Last as long as you can |
| Time | Shared **barrier** that **drains**; empty = game over | Shared **chronometer** that **counts up**; time never times you out |
| Win | Final level cleared | None — clearing balls does not win |
| Lose | Barrier empty, or last living player hit | Last living player hit |
| TIME pickup | Adds seconds to the barrier | Briefly **pauses new spawns** (does not add barrier seconds) |
| After a run | R retry / M or Esc menu | Qualifying times prompt for **three initials**, then High Scores |

Starting Play from Survival in level select loads Survival. Clearing campaign level 5 does **not** auto-start Survival.

## Movement

- Players stay on the floor (no jump, no platforms).
- Horizontal move only; crawl under barriers/doors via the gap above the floor.

## HUD (bottom status panel)

While playing, a Pang-style **brick panel** sits under the arena (not a floating overlay at the top of the playfield). It shows:

- **Campaign** — remaining time as a fill bar, plus the level name.
- **Survival** — elapsed chronometer (for example `0:42.3`) plus a Survival level indicator.

Win and game over use cyberpunk overlays with restart hints. Survival game over also shows the finalized elapsed time.

## Time barrier (campaign)

- Shared survival resource (replaces multi-life stock).
- Each campaign level starts full for that level's `time_seconds` budget.
- Drains while playing. Collecting **TIME** refills some seconds (clamped to the level budget) and does **not** change weapon mode.
- Empty time → game over, even if a co-op partner is still alive.

## Survival chronometer

- Elapsed time increases while Survival is playing.
- The match does **not** end because the clock reached a limit.
- **TIME** pauses the spawn director for a few seconds; weapon mode stays the same.
- Balls keep appearing with a ramp (shorter intervals, heavier large-ball weighting). Concurrent balls are capped; spawns wait when the cap is full.
- Clearing the last ball does **not** win — more balls will spawn.

## Balls

- Tiers: large → medium → small.
- A weapon hit (or **ceiling spikes**) splits a non-smallest ball into two smaller ones; the smallest is removed.
- Balls bounce off walls, floor, barriers, and closed doors. The top of the play area is a spike hazard, not an open sky.

## Ceiling spikes

A row of downward spikes runs along the top of the arena on **every** playable level. Contact uses the same split/destroy rules as a weapon hit.

## Combat

Default weapon is a **growing chain harpoon** (up to two active shots per player; sticky mode is not limited by that slot cap).

| Mode | Behavior |
|------|----------|
| Harpoon (default) | Grows upward; first ball hit resolves the shot |
| STICKY | Plants / grows; up to three stickies can stay on the map; a ball hit pops that line |
| DRILL | Pierces through multiple balls until a barrier, closed door, or the ceiling |

Powerups drop from ball kills: **TIME**, **STICKY**, **DRILL**. STICKY and DRILL replace the current weapon mode. A new campaign level (or Survival start) resets to default harpoon.

## Barriers and doors

- **Barriers** — static solids; crawl underneath.
- **Timed doors** — cycle open/closed on a timer.
- **Lane-clear doors** — open when the marked lane has no balls left.

## Campaign levels

Five authored levels with rising density and door complexity. Each has its own `time_seconds` budget. Advancing refills time and resets weapon mode to default harpoon.

| # | Name | Notes | Time |
|---|------|-------|------|
| 1 | Open Floor | No barriers | 40s |
| 2 | Barrier Lanes | Static barriers | 55s |
| 3 | Timed Gates | Timed central door | 70s |
| 4 | Lane Clear | Center-lane door | 85s |
| 5 | Mixed Chaos | Timed + lane-clear | 100s |

Clearing a non-final level advances (short clear beat, then the next arena). Clearing level 5 shows the win overlay.

## Local co-op (2P)

- Shared time barrier (campaign) or shared chronometer (Survival).
- Distinct keys (see README). Each player has their own shot cap.
- A ball hit removes **only** that player from the current level; the partner may continue.
- Advancing to the next campaign level respawns both players.
- If no living players remain (or campaign time empties) → game over.

## High Scores

- Local top five Survival times per mode (`1P` and `2P`), best time first.
- Persisted on disk across launches.
- After a Survival game over, if the run beats 5th place (or the board has fewer than five entries), enter **three letters** (A–Z), then the entry is saved.
- Non-qualifying runs skip the prompt. View boards from the main menu **HIGH SCORES** item.

## End states

- **Win** — clear campaign level 5. (Survival never enters this state from clearing balls.)
- **Game over** — campaign time out, or last living player hit (campaign or Survival).
- **R** — restart the selected level / mode.
- **M** or **Esc** — return to the menu.
