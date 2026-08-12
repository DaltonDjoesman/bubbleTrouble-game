## Purpose

Ball physics, size tiers, and split-on-hit behavior for the arena match.

## Requirements

### Requirement: Gravity and wall bounce
Balls SHALL bounce horizontally off the left/right edges of the playable arena and use gravity with a floor bounce impulse at the bottom of the playable arena. Balls SHALL NOT escape through the top of the playable arena without contacting the ceiling spike hazard.

#### Scenario: Wall bounce
- **WHEN** a ball reaches the left or right edge of the playable arena
- **THEN** its horizontal velocity reverses

#### Scenario: Floor bounce
- **WHEN** a ball would pass below the floor of the playable arena
- **THEN** it receives an upward velocity impulse (parametrized by size when sizes exist)

#### Scenario: Top of play is hazardous not open
- **WHEN** a ball reaches the top of the playable arena
- **THEN** it contacts the ceiling spike hazard rather than leaving the playfield through an open top

### Requirement: Size tiers and split
Balls SHALL have size tiers. Hitting a non-smallest ball splits it into two smaller balls; hitting the smallest removes it.

#### Scenario: Split on hit
- **WHEN** a non-smallest ball is hit by a bullet
- **THEN** that ball is removed and two smaller balls spawn near its position with opposite horizontal velocities

#### Scenario: Smallest destroyed
- **WHEN** a smallest-tier ball is hit by a bullet
- **THEN** that ball is removed and no new balls spawn from it

### Requirement: Balls collide with arena geometry
Balls SHALL bounce off barriers and closed doors rather than passing through them. Balls SHALL NOT require platforms.

#### Scenario: Ball hits barrier
- **WHEN** a ball collides with a barrier or closed door
- **THEN** its velocity is reflected according to arena bounce rules and it does not pass through
