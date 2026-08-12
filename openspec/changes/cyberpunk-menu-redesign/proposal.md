## Why

The in-match look already leans cyberpunk, but menus, overlays, and HUD chrome still feel like a flat placeholder UI. We now have a concrete visual contract in `designPrototype/` (hybrid of the clean shell + arcade-2 tokens) and want the whole non-level surface to match it before more content piles onto the old chrome.

## What Changes

- Redesign all pre-match menu surfaces (root, options, level select chrome, high scores) to the hybrid cyberpunk shell: dark panels, neon cyan/magenta branding, gold selection, scanline/glow atmosphere, English copy, keyboard-hint footer — without the full physical arcade cabinet chrome from arcade-2.
- Restyle match overlays and HUD framing (game over, win/clear, bottom status panel chrome) to the same visual language.
- Keep match gameplay and level definitions unchanged: when the player confirms Play and enters a level, arena geometry, rules, sprites, and level progression behave as they do today.
- Align selection highlight to prototype gold (`#ffb700` / neon gold).
- Prefer maximum visual fidelity within pygame at the current resolution (800×600), including mono typography where practical.
- Copy stays English (proto mixed PT/EN; product UI is English).

## Capabilities

### New Capabilities

- `cyberpunk-ui-chrome`: Shared non-level UI visual system (tokens, shell layout, selection states, footer hints, overlay chrome) derived from `designPrototype/`.

### Modified Capabilities

- `main-menu`: Menu screens MUST present the cyberpunk shell and English labels; navigation and actions stay the same, including level-select structure (Campaign/Survival) with restyled chrome only.
- `hud-feedback`: Bottom status panel and end-state messaging MUST use the cyberpunk UI chrome instead of Pang brick / plain text overlays; in-play time/level data and no-lives rules stay.
- `cyberpunk-presentation`: Clarify that arena/player/projectile theming remains for match content; shared neon palette MAY align with UI tokens without changing level art packs or playfield geometry.

## Impact

- Primary code: `Scripts/menu.py`, HUD/draw paths used during play and end states (likely `Scripts/game.py` / related draw helpers), possibly shared color/font constants (`Scripts/consts.py` or a small UI module).
- Assets: optional bundled monospace font if system/default fonts cannot match JetBrains Mono closely enough; no change to level JSON or Craftpix gameplay sprites required.
- Specs: new `cyberpunk-ui-chrome`; deltas for `main-menu`, `hud-feedback`, `cyberpunk-presentation`.
- Out of scope: level definitions, ball physics, player controls during play, changing resolution unless required for fidelity (default: keep 800×600).
