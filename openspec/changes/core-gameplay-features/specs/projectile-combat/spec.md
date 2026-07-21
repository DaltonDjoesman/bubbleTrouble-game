## ADDED Requirements

### Requirement: Upward projectiles
Bullets SHALL use Craftpix bullet sprites, travel upward, and despawn when leaving the top of the screen.

#### Scenario: Bullet rises and despawns
- **WHEN** a bullet is spawned
- **THEN** it moves upward each frame and is removed when its rect leaves the top of the screen

### Requirement: Multiple shots with a cap
The game SHALL allow multiple simultaneous bullets up to a configured maximum (default 2).

#### Scenario: At capacity
- **WHEN** the maximum number of active bullets already exists
- **THEN** pressing Space does not spawn an additional bullet

#### Scenario: Slot frees
- **WHEN** an active bullet despawns or hits a ball and the count falls below the maximum
- **THEN** the player can fire again

### Requirement: Bullet hits ball
A bullet that collides with a ball SHALL be removed and trigger the ball-system hit resolution.

#### Scenario: Collision
- **WHEN** a bullet rect intersects a ball rect
- **THEN** the bullet is destroyed and the ball is processed for split or removal
