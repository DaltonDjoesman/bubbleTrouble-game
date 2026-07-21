## ADDED Requirements

### Requirement: Gravity and wall bounce
Balls SHALL bounce horizontally off left/right walls and use gravity with a floor bounce impulse.

#### Scenario: Wall bounce
- **WHEN** a ball reaches the left or right edge
- **THEN** its horizontal velocity reverses

#### Scenario: Floor bounce
- **WHEN** a ball would pass below the floor
- **THEN** it receives an upward velocity impulse (parametrized by size when sizes exist)

### Requirement: Size tiers and split
Balls SHALL have size tiers. Hitting a non-smallest ball splits it into two smaller balls; hitting the smallest removes it.

#### Scenario: Split on hit
- **WHEN** a non-smallest ball is hit by a bullet
- **THEN** that ball is removed and two smaller balls spawn near its position with opposite horizontal velocities

#### Scenario: Smallest destroyed
- **WHEN** a smallest-tier ball is hit by a bullet
- **THEN** that ball is removed and no new balls spawn from it
