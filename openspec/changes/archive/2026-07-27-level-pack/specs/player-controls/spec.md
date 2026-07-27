## ADDED Requirements

### Requirement: Player collides with platforms
The player SHALL be supported by platform tops and blocked by obstacle solids horizontally as applicable.

#### Scenario: Walk on platform
- **WHEN** the player moves while standing on a platform
- **THEN** they remain on the platform until walking off an edge or jumping/falling (if jump exists; otherwise walking off falls)
