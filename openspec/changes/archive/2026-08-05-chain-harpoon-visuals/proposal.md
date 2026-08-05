## Why

Default harpoon shots still use a Craftpix bullet tip stretched over a solid-color beam. The DragChain vertical link pack tiles cleanly as a classic Bubble Trouble chain shaft and reads better as a growing harpoon.

## What Changes

- Render growing shots (harpoon / sticky / drill) as a **tiled vertical chain** instead of Craftpix bullet tip + solid fill
- Differentiate weapon modes with **color tints** on the same chain art (natural metal / green sticky / amber drill)
- **BREAKING** (presentation only): shots no longer use Craftpix bullet sprites; muzzle shoot effects may remain Craftpix

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `cyberpunk-presentation`: Projectile art requirement changes from Craftpix bullets to the chain link shaft (shoot effects may stay Craftpix)

## Impact

- `Scripts/bullet.py` rebuild/draw path
- `Scripts/consts.py` chain sprite path and `LASER_WIDTH`
- Asset: `sprites/chain/DragChainLinkVertical.png`
- Spec: `openspec/specs/cyberpunk-presentation`
