## Context

See proposal.md for motivation. Today `MainMenu` in `Scripts/menu.py` owns root/options/levels/scores with functional card chrome and yellow/cyan selection. Match HUD in `Scripts/main.py` uses a Pang-style brick bottom panel and plain end-state text. Match theming already lives under `cyberpunk-presentation` (Craftpix player, arena background, chain harpoons). Visual reference: hybrid of `designPrototype/bubble-trouble-arcade.html` (shell + footer) and `designPrototype/bubble-trouble-arcade-2.html` (tokens, screens, gold selection) — without the physical arcade cabinet (sticks/fire buttons/marquee bezel).

Constraint: keep `SCREEN_WIDTH`/`SCREEN_HEIGHT` at 800×600 unless a later spike proves otherwise; level definitions and in-match gameplay stay untouched.

## Goals / Non-Goals

**Goals:**
- One shared UI token/draw layer reusable by menu screens and match overlays/panel chrome.
- Fidelity to prototype atmosphere (glow, scanlines, neon cyan/magenta title treatment, gold focus) within pygame surfaces.
- Preserve existing menu IA and keybinds; English labels aligned to prototype wording where sensible (`PLAY GAME`, `MODE`, `HIGH SCORES`, `OPTIONS`, `QUIT`, etc.).
- Restyle level-select chrome only; Campaign/Survival structure and starting a level remain as today.

**Non-Goals:**
- Porting the HTML arcade cabinet chrome or the browser mini-game.
- Changing level JSON, ball physics, player controls, or Craftpix match sprites.
- Localization / Portuguese UI.
- Mouse-first navigation (keyboard remains primary; mouse optional if already present).
- Raising resolution as a hard requirement.

## Decisions

1. **Hybrid visual source**  
   Use arcade-2 CSS tokens (`--neon-cyan #00f0ff`, `--neon-magenta #ff0055`, `--neon-gold #ffb700`, dark surfaces `#09090f` / `#111118`, muted `#6e6e80`) plus the three-band shell from arcade-1/screenshots (header brand, content well, footer hints + system line). Skip cabinet side rails and physical controls.  
   *Alternatives considered:* full cabinet port (too cramped at 800×600); screenshots-only empty shell (no content patterns).

2. **Shared `ui_chrome` module (or equivalent helpers)**  
   Centralize colors, panel/card drawing, gold selection border, scanline overlay, key-hint pills, and title glow helpers. `menu.py` and HUD/end overlays in `main.py` call the same primitives so menus and overlays do not drift.  
   *Alternatives considered:* duplicate constants in each file (status quo drift); CSS-like theme file unused by pygame draw path.

3. **Typography**  
   Prefer a bundled monospace font (JetBrains Mono or similar OFL font under `Assests/` / project fonts) loaded once in `Game`; fall back to pygame default only if load fails. Title uses larger weight/size with cyan glow approximation (multi-pass blit / soft shadow).  
   *Alternatives considered:* system font only (inconsistent across machines); bitmap font art (higher asset cost).

4. **Selection = gold**  
   Selected cards/tabs use neon gold border + warm gold label (not the current yellow/cyan mix). Inactive items use muted HUD gray; accents (arrows, tabs idle) stay cyan where the proto does.

5. **Footer control legend**  
   Menu surfaces show English key hints as keycaps + labels (e.g. `W`/`S` Navigate, `ENTER` Confirm, `ESC` Back) and a muted system line (product-appropriate, not “PROTO” unless we keep it as flavor). Hints adapt slightly per screen if needed but stay in the footer band.

6. **HUD / end states**  
   Replace brick panel fill with cyberpunk panel chrome (dark bar, thin cyan/magenta edge accents, same tokens). Keep time barrier + level indicator data and layout roles. Game over / win / level clear / initials overlays use the same panel + gold/magenta emphasis as menu dialogs, without changing restart keys (`R` / `M`) or flow.

7. **Levels untouched**  
   Entering a match from level select does not alter level load, geometry, rules, or playfield art beyond the already-themed arena background. No redesign of mid-match gameplay.

8. **Optional short boot**  
   A brief boot/splash (proto has boot → root) is nice-to-have if cheap (2–3s or skippable); not required for apply if it risks scope. Default: skip dedicated boot state unless leftover time after chrome work.

## Risks / Trade-offs

- [Glow/scanlines cost / noise] → Keep effects subtle; draw scanlines as a cached translucent surface; glow via few offset blits, not per-frame blur.
- [Font licensing / path] → Bundle an OFL mono font in-repo; document path in consts or assets helper.
- [800×600 crowding vs proto 960×740] → Scale spacing down; prioritize title + selected card readability over decorative empty CRT area.
- [HUD brick removal surprises] → Spec delta for `hud-feedback`; keep time/level semantics identical.
- [Scope creep into match HUD redesign of data] → Only chrome; no new HUD metrics.

## Migration Plan

1. Introduce tokens + draw helpers; wire fonts.
2. Restyle menu screens behind existing navigation.
3. Restyle status panel + end overlays.
4. Visual pass against prototype screenshots/HTML; tune colors.
5. Manual smoke: root → options → levels → play → game over → menu; scores path; 1P/2P unchanged.

Rollback: revert UI module + menu/HUD draw changes; gameplay code paths remain independent.

## Open Questions

- Exact system footer string (keep “BUBBLE TROUBLE PROTO SYSTEM V2.5” as flavor vs a shipping “vX” string) — pick during implementation; does not change specs.
- Whether to ship the optional boot splash — defer; tasks treat it as optional stretch.
