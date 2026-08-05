## Purpose

Player movement, facing, locomotion animation, spritesheet frame cutting, and fire input. Classic play is grounded (no jump).

## Requirements

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

### Requirement: Spritesheet frame cut
Player Idle/Run Craftpix strips SHALL be sliced into individual 48×48 frames before scaling and animation so only one character is drawn.

#### Scenario: Single character on screen
- **WHEN** the player idle or run animation is displayed
- **THEN** exactly one Cyborg frame (one 48×48 cell, scaled) is drawn — not the full horizontal strip

### Requirement: Facing and locomotion animation
The player SHALL face the last horizontal move direction and play idle when standing still and run while moving.

#### Scenario: Idle when stopped
- **WHEN** neither A nor D is pressed
- **THEN** the idle animation plays (not the run loop)

#### Scenario: Facing flips
- **WHEN** the player moves left then right
- **THEN** the sprite faces the corresponding direction

### Requirement: Fire input
The player SHALL be able to fire a laser with the Space key subject to projectile combat limits.

#### Scenario: Space fires
- **WHEN** the player presses Space while allowed to shoot
- **THEN** a laser is spawned from the player's position

### Requirement: Per-player control schemes
The player system SHALL support multiple instances with independent keymaps and facing/animation. All co-op players SHALL stay on the floor baseline (no jump).

#### Scenario: Instantiate P2 scheme
- **WHEN** a second player is spawned for co-op
- **THEN** that instance responds only to the P2 keymap and remains grounded
