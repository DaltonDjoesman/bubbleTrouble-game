## Purpose

On-screen HUD for the time barrier and clear win / game over messaging with restart guidance.

## Requirements

### Requirement: Lives display
While playing, the HUD SHALL show the time barrier (remaining time as a fill bar). The HUD SHALL NOT show a multi-life stock or life-capsule lives display during play.

#### Scenario: Time barrier visible
- **WHEN** the match is in the playing state
- **THEN** a time barrier fill representing remaining time is visible on screen

#### Scenario: No life icons in play
- **WHEN** the match is in the playing state
- **THEN** remaining-lives sprites are not shown as the survival meter

### Requirement: End-state messaging
Win and game over states SHALL show clear on-screen text including how to restart.

#### Scenario: Game over message
- **WHEN** the match enters game over
- **THEN** a game over message and restart hint are displayed

#### Scenario: Win message
- **WHEN** the match enters the won state
- **THEN** a win message and restart hint are displayed
