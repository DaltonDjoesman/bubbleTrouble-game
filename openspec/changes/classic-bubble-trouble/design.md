## Context

The game already has multi-level campaigns, growing harpoons, ball split, platforms/obstacles, and a 3-life HUD. Classic Bubble Trouble identity needs grounded play, time pressure, one-hit stakes, power drops, and corridor barriers/doors instead of platforms.

Sibling open changes `local-coop` and `game-documentation` still assume lives/platforms — rebase them after this lands; do not apply them unchanged.

## Goals / Non-Goals

**Goals:**
- Classic locomotion: no jump, slower horizontal move, floor-only
- Time barrier as the survival resource (shared in co-op)
- One-hit game over in single-player
- Barriers + doors as the level-geometry vocabulary; five redesigned levels
- Power trio: TIME / STICKY / DRILL with one weapon mode at a time
- Spec contract for co-op death/revive so `local-coop` can implement against it

**Non-Goals:**
- Shipping final README / gameplay docs in this change (update `game-documentation` plan only if needed; write docs after playable)
- Implementing full 2P code here (rules only; code stays in `local-coop`)
- Level editor, online, PvP, new ball types
- Keeping platform physics “just in case”

## Decisions

1. **Time model**  
   Global fixed drain rate (e.g. 1 unit/sec). Each level declares `time_seconds` as the full-bar budget. TIME power adds a fixed number of seconds (clamp to bar max = level budget or a global cap — prefer clamp to level’s starting budget). Empty bar → instant game over.

2. **One-hit (1P)**  
   Ball–player collision while playing → immediate game over. No i-frames recovery loop. Remove `DEFAULT_LIVES` from match flow and life capsule HUD.

3. **Geometry model**  
   Replace `platforms` / walkable shelves with:
   - **Barriers**: static vertical solids; balls and lasers collide; leave a crawl gap above the floor so the player can cross under.
   - **Doors**: barrier-like solids with open/closed state. While closed, same solidity as barriers. Open rules per instance:
     - `timed`: cycle open↔closed on intervals
     - `lane_clear`: open when no balls remain in that door’s lane/region  
   Player never stands on tops of barriers (no platform standing). Horizontal blocking only when geometry reaches the floor; under-gap barriers do not block the player horizontally at foot level.

4. **Level schema (illustrative)**  
   ```
   id, name, blurb, theme,
   time_seconds,
   balls: [...],
   barriers: [{x, y, w, h}],
   doors: [{x, y, w, h, mode: timed|lane_clear, ...params}],
   player_x
   ```
   Remove `platforms` / treat obstacles as barriers or drop the name.

5. **Weapons**  
   - Default: current growing harpoon (despawn on ceiling or first ball hit). Cap unchanged unless sticky/drill need tighter rules.  
   - STICKY mode: fire plants at most one sticky line; grows then stays; ball hit → resolve ball + remove line. Switching weapon does **not** despawn an already planted sticky.  
   - DRILL mode: one shot pierces every ball whose rect intersects the beam’s vertical path until blocked by closed barrier/door or ceiling; beam does not stop on first ball.  
   Pickup replaces current weapon mode immediately. TIME is not a weapon — applies instantly and leaves mode unchanged.

6. **Drops**  
   On ball kill, random chance to spawn a pickup that falls/floats for collection. Types: TIME, STICKY, DRILL. Tune chance in consts; exact % not sacred in v1.

7. **Co-op contract (for `local-coop`)**  
   Shared time bar. Hit removes only that player from the level; survivor continues. On advance to next level, both players respawn. If no living players remain, or time empties → game over. This change documents the rule in `match-rules`; implementation remains in `local-coop`.

8. **Content sketch for five levels**  
   - L1: open arena, few balls, short time — teach move/shoot/time  
   - L2: static barriers / lanes  
   - L3: timed doors  
   - L4: lane-clear doors  
   - L5: mix of doors + denser balls / longer budget  

9. **Speed**  
   Reduce horizontal speed ~25% from current `vel_x` (tune in playtest; expose as const).

10. **HUD**  
    Reuse the wide red bar visual as the time barrier (fill ∝ remaining time). Remove life sprites from play HUD.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Fixed drain unfair on maze levels | Per-level `time_seconds` |
| Sticky + drill edge cases with barriers | Solid collision shared with default laser |
| Softlocks (door never opens) | Lane-clear needs clear lane definition; playtest; avoid doors that trap last balls outside their lane |
| Sibling changes diverge | Explicit rebase notes for `local-coop` / `game-documentation` |
| Large content rewrite | Author levels after core systems; smoke each mode |

## Migration Plan

1. Player: remove jump/gravity dependence for play; slower speed; floor clamp only  
2. Match: replace lives with time budget + one-hit lose  
3. HUD: time fill bar; strip life icons  
4. Geometry: barriers/doors API; delete platform standing  
5. Projectiles + powerups modules  
6. Author five levels; delete old platform layouts  
7. Update `local-coop` / `game-documentation` artifacts to match (separate apply)

Rollback: revert change branch; platform levels remain in git history.

## Open Questions

- Exact TIME add seconds and drop % — tune during apply/playtest (defaults in consts).  
- Lane region definition for `lane_clear` — decide as AABB/x-range beside each door when implementing.
