## ADDED Requirements

### Requirement: Balls collide with arena geometry
Balls SHALL bounce off platforms and obstacles rather than passing through them.

#### Scenario: Ball hits platform top
- **WHEN** a ball collides with the top of a platform
- **THEN** its vertical velocity is reflected upward (bounce impulse)
