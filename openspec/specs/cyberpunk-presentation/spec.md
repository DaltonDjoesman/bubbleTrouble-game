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
Shots SHALL use a tiled vertical chain-link shaft for the growing projectile body, topped by an arrow/harpoon head sprite. The default (harpoon) shaft SHALL be a light gray steel tint. Sticky and drill modes SHALL tint the chain shaft (green / amber) while the arrow head SHALL remain gray in every mode. Shots SHOULD show a brief shoot effect when firing (Craftpix shoot effects remain allowed).

#### Scenario: Chain shaft art
- **WHEN** a projectile is visible
- **THEN** it is drawn from the vertical chain link sprite tiled along its height (not from the Craftpix bullets folder)

#### Scenario: Mode tint
- **WHEN** the player fires in sticky or drill mode
- **THEN** the chain shaft uses a distinct color tint for that mode while sharing the same link art as default harpoon

#### Scenario: Arrow head tip
- **WHEN** a projectile is visible
- **THEN** an arrow/harpoon head sprite is drawn at the top of the chain and remains gray regardless of weapon mode

#### Scenario: Default shaft color
- **WHEN** the player fires in default harpoon mode
- **THEN** the chain shaft uses a light gray steel tint

### Requirement: UI palette alignment
Match presentation MAY share the same neon cyan / magenta / gold accents used by non-level UI chrome, but SHALL NOT require changing level geometry, Craftpix player sheets, or harpoon art rules defined elsewhere in this capability.

#### Scenario: Match art unchanged
- **WHEN** a match is playing after the UI chrome redesign
- **THEN** the player continues to use the Cyborg asset set and projectile chain/arrow rules remain as specified for match presentation
