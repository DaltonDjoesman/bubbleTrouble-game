## MODIFIED Requirements

### Requirement: Lives display
While playing, the HUD SHALL show the time barrier (remaining time as a fill bar). The HUD SHALL NOT show a multi-life stock or life-capsule lives display during play.

#### Scenario: Time barrier visible
- **WHEN** the match is in the playing state
- **THEN** a time barrier fill representing remaining time is visible on screen

#### Scenario: No life icons in play
- **WHEN** the match is in the playing state
- **THEN** remaining-lives sprites are not shown as the survival meter
