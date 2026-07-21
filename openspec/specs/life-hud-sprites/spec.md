## Purpose

Render remaining lives in the HUD using sprites from `sprites/Life/` instead of a numeric text label.

## Requirements

### Requirement: Sprite-based life display
While playing, remaining lives SHALL be shown as life sprites from `sprites/Life/` (capsule bar fill levels mapped to remaining lives).

#### Scenario: Three lives
- **WHEN** the player has 3 lives and the match is playing
- **THEN** the full life bar sprite is visible in the HUD area

#### Scenario: Life lost
- **WHEN** lives decrease from 3 to 2
- **THEN** the HUD shows the reduced-fill life bar for 2 remaining lives
