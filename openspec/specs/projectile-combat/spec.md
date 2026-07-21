## Purpose

Growing upward lasers with an active cap and laser–ball hit resolution.

## Requirements

### Requirement: Growing upward laser
Lasers SHALL spawn at the player's fire position, grow upward each frame, and despawn when they reach the top of the screen.

#### Scenario: Laser grows
- **WHEN** a laser is active
- **THEN** its vertical extent increases upward each frame from the spawn baseline

#### Scenario: Laser reaches ceiling
- **WHEN** the laser's top edge reaches or passes the top of the screen
- **THEN** that laser is removed

### Requirement: Multiple lasers with a cap
The game SHALL allow multiple simultaneous lasers up to a configured maximum (default 2).

#### Scenario: At capacity
- **WHEN** the maximum number of active lasers already exists
- **THEN** pressing Space does not spawn an additional laser

#### Scenario: Slot frees
- **WHEN** an active laser despawns or hits a ball and the count falls below the maximum
- **THEN** the player can fire again

### Requirement: Laser hits ball
A laser that collides with a ball SHALL be removed and trigger the ball-system hit resolution.

#### Scenario: Collision
- **WHEN** a laser rect intersects a ball rect
- **THEN** the laser is destroyed and the ball is processed for split or removal
