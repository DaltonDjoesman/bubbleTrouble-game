## MODIFIED Requirements

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
