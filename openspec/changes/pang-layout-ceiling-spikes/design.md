## Context

Window is fixed at 800×600; the full surface is the playfield. HUD time bar and level text overlay the top of the arena. Balls bounce on left/right walls, floor, and solids, but have **no** top-of-screen clamp—they can leave through y=0. Laser “ceiling” is currently `top <= 0` on the window. Bottom UI strip does not exist. See proposal.md for motivation.

## Goals / Non-Goals

**Goals:**
- Introduce a single **play rect** (above a reserved bottom panel) used by floor, spawns, ball walls, laser ceiling, and spike row.
- Pang-inspired **bottom panel** chrome with time fill + level label (and optional weapon-mode hint).
- Ceiling spikes that resolve ball contact through the **same split path** as laser hits.
- Keep cyberpunk playfield art inside the play rect.

**Non-Goals:**
- Restoring multi-life stock or score displays.
- Per-level toggle for spikes (always on during play).
- New external asset packs (procedural spikes / brick panel is fine).
- Changing weapon modes, powerups, or match win/lose rules beyond geometry.

## Decisions

### 1. Single play-area constants
- **Choice:** Add `PLAY_TOP`, `PLAY_BOTTOM` / `PLAY_HEIGHT`, and `HUD_PANEL_HEIGHT` in `consts.py`. Derive `FLOOR_Y` from `PLAY_BOTTOM` (thin floor inset as today). Window size stays 800×600.
- **Why:** One source of truth avoids HUD / physics / laser drift.
- **Alternatives:** Shrink only visually and keep physics on full window — rejected (balls could enter the panel). Separate left/right borders — out of scope; user asked for bottom panel + ceiling spikes.

### 2. Bottom panel layout (Pang-like, not full clone)
- **Choice:** Reserved strip (~72–96px) with brick/stone-style fill and frame. Wide time bar across most of the width; centered “LEVEL N” (and name if space). Weapon mode (sticky/drill) as small text under or beside the bar. Co-op “P down” stays in play area bottom-left or moves into panel edge.
- **Why:** Matches the reference look for time + level without bringing back lives/score (time barrier remains the survival meter).
- **Alternatives:** Full Pang HUD with fake lives/score — rejected (conflicts with match-rules / hud-feedback). Overlay-only HUD at bottom without reserving space — rejected (user wants smaller arena).

### 3. Ceiling spikes as a thin collision band
- **Choice:** Draw a row of downward spikes along `PLAY_TOP`. Collision = ball rect intersects a short band below the play top (or spike AABB). On hit, call the same `_resolve_ball_hit` / `split` path used for lasers (SFX + optional powerup spawn).
- **Why:** User confirmed split-on-hit; reusing the hit pipeline keeps behavior consistent.
- **Alternatives:** Instant destroy without split — rejected. Bounce off ceiling — not classic Pang roof. Separate spike sprite sheet — optional later; procedural triangles/gray spikes are enough for v1.

### 4. Laser ceiling aligns with play top (under spikes)
- **Choice:** Harpoon/sticky/drill “hit ceiling” uses play-top / spike underside, not window y=0.
- **Why:** Sticky plants and laser despawn must stay inside the arena.

### 5. Split children and immediate re-hit
- **Choice:** After a ceiling split, children spawn with existing split offsets/velocities. If a child still overlaps the spike band on the next update, it can be hit again (same as overlapping a laser)—acceptable. Prefer spawning children slightly below the spike band when the parent died to ceiling if easy.
- **Why:** Avoids infinite same-frame loops; one hit per update pass is enough.

### 6. Drawing order
- Background clipped or drawn only in play rect → geometry → sprites → spike row → bottom panel + HUD → pause/end overlays.
- **Why:** Spikes read as part of the roof; panel never covers balls incorrectly.

## Risks / Trade-offs

- **[Risk]** Existing levels authored for full 600 height feel tighter → **Mitigation:** Keep panel modest (~80px); smoke-test all levels; adjust barrier heights only if crawl gaps break.
- **[Risk]** Ceiling splits cascade and clear large balls “too easily” → **Mitigation:** Spikes are a classic risk/reward; tune band height thin so only near-roof contact counts.
- **[Risk]** Procedural brick panel clashes with cyberpunk arena → **Mitigation:** Panel is clearly “chrome”; playfield keeps theme gradient.
- **[Risk]** Missed call sites still use `screenHeight` as floor → **Mitigation:** Centralize `FLOOR_Y` / play bounds; grep for `screenHeight` in gameplay code during implementation.

## Migration Plan

- Land as a single gameplay change; no save-format migration.
- Rollback = revert the change branch; window layout returns to full-bleed playfield.

## Open Questions

- Exact panel height and spike art polish can be tuned during implementation without changing requirements.
- Whether to show a decorative torch / plate around “LEVEL N” is visual-only and optional.
