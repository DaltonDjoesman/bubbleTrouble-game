## Context

Shots grow upward as thin beams (`Bullet` in `Scripts/bullet.py`). Today the tip is Craftpix `4_1.png` and the body is a solid fill tinted per weapon mode. A tileable vertical chain link is available at `sprites/chain/DragChainLinkVertical.png`.

## Goals / Non-Goals

**Goals:**
- Tile the vertical chain for the full beam height
- Tint sticky (green) and drill (amber); harpoon stays natural metal
- Keep grow / plant / pierce / solid collision behavior unchanged
- Keep hitbox thin (~8–10px)

**Non-Goals:**
- New sticky-only art, pulse VFX, or horizontal links
- Changing fire caps, cooldowns, or hit rules
- Replacing guns or Craftpix muzzle shoot effects

## Decisions

1. **Single link asset for all modes** — Same `DragChainLinkVertical`; mode = `BLEND_RGBA_MULT` tint. Avoids extra art and matches today’s color-only differentiation.
2. **Crop then use native content width** — Link canvas is 16×16 with ~10px opaque width; crop and set `LASER_WIDTH` to that width so rect matches art without upscaling.
3. **No Craftpix tip** — Top of the tiled shaft is the tip; whole shaft shares the mode tint.
4. **Spec delta on `cyberpunk-presentation`** — Bullet art requirement points at the chain shaft; shoot effects may remain Craftpix.

## Risks / Trade-offs

- [Wider than 6px] → Cropped ~10px; monitor fairness vs balls
- [Tint washes metal detail] → Use multiply with saturated mode colors; harpoon untinted
- [Theme clash cyberpunk vs gold chain] → Accepted for classic BT harpoon readability
