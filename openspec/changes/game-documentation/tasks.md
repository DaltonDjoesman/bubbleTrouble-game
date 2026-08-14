## 1. Dependencies and README

- [x] 1.1 Ensure `requirements.txt` exists with pygame version guidance
- [x] 1.2 Write root `README.md`: overview, install, run, controls (A/D move, Space fire; no jump), folder map
- [x] 1.3 Add Craftpix credit + link to pack `License.txt`

## 2. Gameplay notes (classic rules)

- [x] 2.1 Create `docs/gameplay.md` with classic loop: grounded move, time barrier, one-hit 1P, ball split, win/lose
- [x] 2.2 Document combat: default growing harpoon + STICKY / DRILL modes and TIME/STICKY/DRILL drops
- [x] 2.3 Document barriers/doors (timed + lane-clear), five levels + `time_seconds`; note platforms/lives removed
- [x] 2.4 Link README ↔ gameplay notes; mention local co-op as shipped

## 3. Sync pass

- [x] 3.1 Docs written to match shipped classic + co-op behavior
- [x] 3.2 Quick review: a new reader can install, run, and understand classic rules from docs alone

## 4. Rebase docs to shipped game

- [x] 4.1 Rewrite README overview: campaign (5 levels), Survival, 1P/2P, High Scores, Options/audio; keep install/run/controls/credits
- [x] 4.2 Rewrite `docs/gameplay.md` from main specs: campaign vs Survival, co-op, spikes, HUD panel, TIME dual behavior, High Scores/initials, menu flow
- [x] 4.3 Confirm folder map uses `assets/` (not `Assests/`) and links README ↔ gameplay notes

## 5. Full-window screenshots and GIF

- [ ] 5.1 Capture `docs/screens/menu.png`, `campaign.png`, `survival.png`, and `high-scores.png` from the pygame framebuffer at 800×600 (entire window, no crop)
- [ ] 5.2 Capture `docs/screens/play.gif` as a short in-match campaign loop at native 800×600 (entire window, including bottom status panel)
- [ ] 5.3 Embed the four PNGs and the GIF in README; verify each image is full-window (campaign/Survival/GIF show the HUD panel)
