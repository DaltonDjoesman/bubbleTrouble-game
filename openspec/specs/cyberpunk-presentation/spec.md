## Purpose

Cyberpunk visual identity for the player, arena, and projectile feedback using the Craftpix asset pack (player/guns/effects) plus chain-link harpoon shafts.

## Requirements

### Requirement: Cyberpunk player presentation
The player SHALL be rendered using the Craftpix Cyborg character frames as the default look.

#### Scenario: Cyborg on screen
- **WHEN** a match is playing
- **THEN** the player sprite is sourced from the Cyborg asset set (not the Knight sheets)

### Requirement: Themed arena background
The play field SHALL not be a flat black fill; it SHALL use a cyberpunk-appropriate background treatment.

#### Scenario: Non-plain background
- **WHEN** the game draws a playing frame
- **THEN** the background presents a gradient, pattern, or image consistent with the cyberpunk theme

### Requirement: Bullet and muzzle feedback
Shots SHALL use a tiled vertical chain-link shaft for the growing projectile body. Weapon modes MAY tint the same chain art (default metal, sticky green, drill amber). Shots SHOULD show a brief shoot effect when firing (Craftpix shoot effects remain allowed).

#### Scenario: Chain shaft art
- **WHEN** a projectile is visible
- **THEN** it is drawn from the vertical chain link sprite tiled along its height (not from the Craftpix bullets folder)

#### Scenario: Mode tint
- **WHEN** the player fires in sticky or drill mode
- **THEN** the chain shaft uses a distinct color tint for that mode while sharing the same link art as default harpoon
