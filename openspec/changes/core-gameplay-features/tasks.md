## 1. Runtime foundation

- [x] 1.1 Add `requirements.txt` with pygame and ensure `pygame.init()` runs before display creation
- [x] 1.2 Resolve asset paths from project root (`pathlib`) in `consts` / loaders
- [x] 1.3 Keep `Scripts/main.py` as sole entry; move or quarantine `boubble_trouble.py` and `teste.py` as legacy
- [x] 1.4 Wire sprite groups for player, balls, and bullets in `Game`

## 2. Player controls (cyberpunk-ready)

- [x] 2.1 Fix sprite load pipeline (cut → blit → scale; rect from image)
- [x] 2.2 Point player assets at Craftpix Cyborg Idle/Run frames
- [x] 2.3 Idle vs run animation + horizontal flip on A/D
- [x] 2.4 Space to request fire (respect bullet cap from combat module)

## 3. Projectile combat

- [x] 3.1 Create `bullet.py` using a Craftpix bullet sprite; upward motion; despawn off top
- [ ] 3.2 Enforce max active bullets (default 2) and optional short cooldown
- [ ] 3.3 Detect bullet–ball collisions and remove bullet on hit

## 4. Ball system

- [ ] 4.1 Parametrize ball sizes / bounce impulse (replace single magic `-13` where needed)
- [ ] 4.2 Implement split: non-smallest → two smaller with opposite `vel_x`; smallest → remove
- [ ] 4.3 Spawn initial arena balls at largest (or mixed) size for a playable match

## 5. Match rules

- [ ] 5.1 Track lives (default 3); player–ball collision reduces life with i-frames/reset
- [ ] 5.2 Enter game over at 0 lives; enter won when no balls remain
- [ ] 5.3 Restart with R from won/game over (no level progression)
- [ ] 5.4 Manual smoke test: move, shoot, split, die, win, restart
