## 1. Level data and loader

- [ ] 1.1 Define level schema (balls, platforms, obstacles) and loader API
- [ ] 1.2 Author 5 levels with increasing difficulty and distinct layouts

## 2. Arena geometry collisions

- [ ] 2.1 Implement platform solids: player stands on tops
- [ ] 2.2 Balls bounce on platforms/obstacles; bullets despawn on solid hits
- [ ] 2.3 Draw platforms/obstacles distinctly in-game

## 3. Progression and menu wire-up

- [ ] 3.1 `reset_match(level_id)` spawns that level's content
- [ ] 3.2 Clear non-final level → advance; clear level 5 → won
- [ ] 3.3 Menu level select lists all 5 levels
- [ ] 3.4 Playtest each level for softlocks and collision bugs
