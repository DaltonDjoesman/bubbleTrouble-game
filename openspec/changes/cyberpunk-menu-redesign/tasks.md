## 1. UI foundation

- [x] 1.1 Add shared UI token constants (cyan, magenta, gold, surfaces, muted) from the hybrid prototype
- [x] 1.2 Bundle or wire a monospace UI font with safe fallback; load from Game init
- [x] 1.3 Create shared draw helpers for shell bands, cards, gold selection, keycap hints, optional scanline overlay / title glow

## 2. Menu screens

- [ ] 2.1 Restyle root menu (header brand, English labels, gold selection, footer hints)
- [ ] 2.2 Restyle options screen with the same chrome and volume controls
- [ ] 2.3 Restyle level-select chrome (tabs/cards/back) without changing Campaign/Survival flow or start-level behavior
- [ ] 2.4 Restyle high-scores screen (tabs, table, back) with shared chrome

## 3. Match HUD and overlays

- [ ] 3.1 Replace Pang brick bottom status panel with cyberpunk panel chrome; keep time barrier + level indicator
- [ ] 3.2 Restyle game over / win / level clear / initials overlays to cyberpunk chrome; keep R/M (and existing) controls

## 4. Polish and verify

- [ ] 4.1 Visual pass against `designPrototype` tokens (glow/scanlines subtlety, spacing at 800×600)
- [ ] 4.2 Manual smoke: root → options → levels → play level unchanged → end overlay → menu; scores path; 1P/2P mode toggle
- [ ] 4.3 Optional stretch: brief skippable boot splash if foundation work finishes early
