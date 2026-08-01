## ADDED Requirements

### Requirement: Grounded movement only
The player SHALL remain on the arena floor during play. Jump input SHALL NOT lift the player. Vertical play position SHALL stay at the floor baseline (no platform standing).

#### Scenario: No jump
- **WHEN** the player presses a former jump control (if still bound) or any key other than move/fire/menu during play
- **THEN** the player does not leave the floor via a jump impulse

#### Scenario: Always on floor
- **WHEN** the match is playing
- **THEN** the player's feet stay on the floor baseline

### Requirement: Slower horizontal speed
The player's configured horizontal move speed SHALL be lower than the pre-classic tune (approximately 25% slower, exact value in consts).

#### Scenario: Move feels slower
- **WHEN** the player holds D on an open floor
- **THEN** they translate horizontally at the reduced configured speed

## MODIFIED Requirements

### Requirement: Horizontal movement
The player SHALL move left and right with A and D keys, remain clamped inside the horizontal play bounds, and be blocked by solid barrier/door geometry at player height (crawl gaps under barriers remain passable).

#### Scenario: Move right
- **WHEN** the player holds D and is not at the right edge or blocked by a solid
- **THEN** the player moves right at the configured speed

#### Scenario: Screen clamp
- **WHEN** movement would place the player outside the screen
- **THEN** the player does not leave the playable horizontal bounds

#### Scenario: Pass under barrier gap
- **WHEN** a barrier leaves a gap above the floor and the player walks through that gap
- **THEN** the player can cross to the other side

## REMOVED Requirements

### Requirement: Player collides with platforms
**Reason**: Platforms are removed; classic levels use barriers/doors only.
**Migration**: Use barrier/door collision and floor-only locomotion from this change.
