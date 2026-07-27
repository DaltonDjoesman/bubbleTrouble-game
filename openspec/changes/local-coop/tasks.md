## 1. Player parametrization

- [ ] 1.1 Refactor `Player` to accept player id, keymap, and sprite set (grounded; no jump)
- [ ] 1.2 Add P2 sprites (Biker or Punk) and P2 keys (arrows + fire)

## 2. Co-op match rules (classic contract)

- [ ] 2.1 Spawn 1 or 2 players from menu mode; shared time barrier (no shared lives)
- [ ] 2.2 Per-player bullet cap; both can hit balls; hit removes only that player from the level
- [ ] 2.3 On level advance, respawn both players; game over if no living players or time empty; win on final clear

## 3. Menu and polish

- [ ] 3.1 Menu 2P Play starts real co-op (no 1P fallback)
- [ ] 3.2 Playtest co-op on a barrier/door level; document controls in overlay/menu hint
- [ ] 3.3 Manual smoke: 1P one-hit/time still works; 2P both move/shoot; one dies partner continues; both revive next level
