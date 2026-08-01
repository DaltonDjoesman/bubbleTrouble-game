## MODIFIED Requirements

### Requirement: Balls collide with arena geometry
Balls SHALL bounce off barriers and closed doors rather than passing through them. Balls SHALL NOT require platforms.

#### Scenario: Ball hits barrier
- **WHEN** a ball collides with a barrier or closed door
- **THEN** its velocity is reflected according to arena bounce rules and it does not pass through
