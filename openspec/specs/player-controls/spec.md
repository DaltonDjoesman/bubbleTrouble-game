## Purpose

Player movement, facing, locomotion animation, spritesheet frame cutting, and fire input.

## Requirements

### Requirement: Horizontal movement
The player SHALL move left and right with A and D keys and remain clamped inside the screen bounds.

#### Scenario: Move right
- **WHEN** the player holds D and is not at the right edge
- **THEN** the player moves right at the configured speed

#### Scenario: Screen clamp
- **WHEN** movement would place the player outside the screen
- **THEN** the player does not leave the playable horizontal bounds

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
