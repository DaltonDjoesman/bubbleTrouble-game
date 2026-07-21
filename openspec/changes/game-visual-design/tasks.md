## 1. Sprite pipeline

- [x] 1.1 Add asset loader helper for folder frame lists + documented scale factor
- [x] 1.2 Ensure player/bullet rects derive from scaled images
- [x] 1.3 Centralize Craftpix paths in consts (Cyborg, bullets, shoot effects)

## 2. Cyberpunk presentation

- [x] 2.1 Replace Knight usage with Cyborg Idle/Run (and Jump if used)
- [x] 2.2 Apply bullet sprite choice consistently; add brief shoot effect on fire
- [x] 2.3 Replace flat black background with cyberpunk gradient/pattern/image
- [x] 2.4 Optionally tint or restyle balls so they fit the theme

## 3. HUD feedback

- [x] 3.1 Draw lives on screen during play
- [x] 3.2 Win and game over overlays with restart hint
- [x] 3.3 Visual pass: readable contrast, no overlapping critical sprites

## 4. Cleanup check

- [ ] 4.1 Confirm Knight sheets are unused at runtime (leave files; no dead imports)
- [ ] 4.2 Manual visual smoke test alongside core gameplay loop
