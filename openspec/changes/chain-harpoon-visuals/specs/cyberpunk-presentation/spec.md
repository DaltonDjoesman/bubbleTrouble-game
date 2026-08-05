## MODIFIED Requirements

### Requirement: Bullet and muzzle feedback
Shots SHALL use a tiled vertical chain-link shaft for the growing projectile body. Weapon modes MAY tint the same chain art (default metal, sticky green, drill amber). Shots SHOULD show a brief shoot effect when firing (Craftpix shoot effects remain allowed).

#### Scenario: Chain shaft art
- **WHEN** a projectile is visible
- **THEN** it is drawn from the vertical chain link sprite tiled along its height (not from the Craftpix bullets folder)

#### Scenario: Mode tint
- **WHEN** the player fires in sticky or drill mode
- **THEN** the chain shaft uses a distinct color tint for that mode while sharing the same link art as default harpoon
