## Context

Campaign levels 1–5 use a draining time barrier, initial-only ball spawns, and win-on-clear. Persistence today is only audio volumes in `settings.json`. Co-op already removes hit players and game-overs when none remain. See proposal.md for motivation.

## Goals / Non-Goals

**Goals:**
- Survival as selectable final level with ascending shared chronometer and spawn director.
- Qualifying runs → 3-letter initials → top 5 local boards (1P vs 2P).
- Menu High Scores with tab-like board switch.
- Campaign behavior for levels 1–5 unchanged (including win on clear of 5 without forcing Survival).

**Non-Goals:**
- Online / cloud leaderboards.
- Score points besides elapsed time.
- Auto-advance from level 5 into Survival.
- Changing ceiling spikes, weapons, or arena chrome beyond Survival HUD/time semantics.

## Decisions

### 1. Survival as level id 6, not a separate menu mode
- **Choice:** Add level id 6 named “Survival” to level select; `Level` gains a mode flag (e.g. `survival=True`) or equivalent.
- **Why:** Matches “último level”; reuses Play → Select Level flow.
- **Alternatives:** Root-menu “Survival” button — clearer separation but user asked for last level.

### 2. Campaign final vs Survival
- **Choice:** `MAX_CAMPAIGN_LEVEL = 5` for clear→win / advance. Survival is never the target of `_advance_to_next_level`. Selecting Survival starts that mode directly.
- **Why:** Clearing all balls cannot “beat” Survival; auto-advance would strand the campaign win fantasy.

### 3. Chronometer, not inverted barrier
- **Choice:** Float/ms elapsed while `playing`; HUD shows `M:SS` or `M:SS.s`. No drain; TIME powerup does not add to chronometer.
- **Why:** User asked for numeric chronometer; barrier fill would confuse “more time = better.”

### 4. Spawn director with ramp + cap
- **Choice:** Timer-based spawns from the top band of the play area. Interval shrinks over elapsed time; size weights shift Small→Medium→Large. Hard cap on live balls (skip spawn if at cap). Optional brief grace at start with 1–2 small balls.
- **Why:** Continuous pressure without soft-lock; tuning constants in `consts.py`.
- **Alternatives:** Wave clear gates — rejected (user wanted continuous appearance with ramp).

### 5. Lose / end flow
- **Choice:** Same death contract as campaign (1P hit → over; 2P both down → over). On game over in Survival: show elapsed time; if top-5 for the active mode board, enter initials entry (3 A–Z chars), then save and show rank; always offer R retry / M menu.
- **Why:** Aligns with co-op rules; initials only when worth recording.

### 6. High score storage
- **Choice:** JSON file beside settings (e.g. `highscores.json`) with `{ "1p": [{name, time_ms}], "2p": [...] }` sorted best→worst, max 5 each. Load at boot / menu open; save after successful insert.
- **Why:** Mirrors existing settings persistence; no DB.

### 7. Menu High Scores UI
- **Choice:** Menu entry “High Scores”; Left/Right or Tab switches **1P / 2P** boards (tabs). Lists rank, name, time. Esc/back to root.
- **Why:** User asked for tab-like boards.

### 8. TIME powerup in Survival
- **Choice:** Collecting TIME starts a short spawn-pause window; does not change chronometer or weapon.
- **Why:** Barrier seconds are meaningless; pause is a readable survival buff.
- **Alternatives:** Disable TIME drops in Survival — simpler but less fun.

### 9. Board key = match mode at run start
- **Choice:** 1P run → `1p` board; 2P run → `2p` board even if one player dies early (shared chronometer until both down).
- **Why:** Matches “boards separados” and shared timer.

## Risks / Trade-offs

- **[Risk]** Spawn ramp too hard/easy → **Mitigation:** Tunable consts; smoke-test early/mid/late minutes.
- **[Risk]** Initials UI awkward on keyboard → **Mitigation:** Arcade-style Left/Right letter + confirm (and/or type A–Z).
- **[Risk]** File write fail on quit → **Mitigation:** Save immediately after accept initials; ignore corrupt file with empty boards.
- **[Risk]** HUD panel assumes barrier fill → **Mitigation:** Branch draw path on survival flag.

## Migration Plan

- New file for scores; absent file = empty boards.
- No migration of old saves.
- Rollback = remove Survival level + score UI; campaign unchanged.

## Open Questions

- Exact spawn interval curve and max ball count can be tuned in implementation without changing requirements.
- Chronometer display precision (tenths vs whole seconds) is visual polish.
