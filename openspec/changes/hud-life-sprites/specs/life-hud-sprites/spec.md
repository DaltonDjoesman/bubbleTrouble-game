## ADDED Requirements

### Requirement: Sprite-based life icons
While playing, remaining lives SHALL be shown as life/heart sprites from `sprites/Life/`, one icon per remaining life.

#### Scenario: Three lives
- **WHEN** the player has 3 lives and the match is playing
- **THEN** three life icons are visible in the HUD area

#### Scenario: Life lost
- **WHEN** lives decrease from 3 to 2
- **THEN** exactly two life icons remain visible
