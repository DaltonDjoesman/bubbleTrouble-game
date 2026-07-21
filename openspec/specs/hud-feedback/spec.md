## Purpose

On-screen HUD for lives and clear win / game over messaging with restart guidance.

## Requirements

### Requirement: Lives display
While playing, the HUD SHALL show the current remaining lives.

#### Scenario: Lives visible
- **WHEN** the match is in the playing state
- **THEN** the current life count is visible on screen

### Requirement: End-state messaging
Win and game over states SHALL show clear on-screen text including how to restart.

#### Scenario: Game over message
- **WHEN** the match enters game over
- **THEN** a game over message and restart hint are displayed

#### Scenario: Win message
- **WHEN** the match enters the won state
- **THEN** a win message and restart hint are displayed
