## ADDED Requirements

### Requirement: Platforms
Platforms SHALL be solid surfaces. The player can stand on them. Balls bounce when colliding with them according to arena physics rules.

#### Scenario: Player stands on platform
- **WHEN** the player falls onto a platform top
- **THEN** the player rests on that platform instead of falling through

### Requirement: Obstacles
Obstacles SHALL block the player and interact with balls and bullets as solid geometry (bullets despawn on impact with solid arena geometry).

#### Scenario: Bullet hits obstacle
- **WHEN** a bullet collides with an obstacle or platform underside/solid
- **THEN** the bullet is removed
