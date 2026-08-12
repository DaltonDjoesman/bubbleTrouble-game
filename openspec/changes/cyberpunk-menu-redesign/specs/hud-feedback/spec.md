## MODIFIED Requirements

### Requirement: Bottom status panel
While playing, the window SHALL reserve a bottom status panel outside the playable arena. The panel SHALL present cyberpunk UI chrome consistent with the shared non-level visual system (dark framed strip with neon accents) and SHALL display the time barrier and the current level indicator.

#### Scenario: Panel reserved below play
- **WHEN** the match is in the playing state
- **THEN** a bottom status panel is visible below the playable arena and gameplay sprites do not use that strip as floor space

#### Scenario: Time and level in panel
- **WHEN** the match is in the playing state
- **THEN** the time barrier fill and a level indicator are shown inside the bottom status panel

#### Scenario: Cyberpunk panel chrome
- **WHEN** the match is in the playing state
- **THEN** the bottom status panel uses cyberpunk framing rather than Pang-style brick/stone chrome

### Requirement: End-state messaging
Win and game over states SHALL show clear on-screen text including how to restart, presented with cyberpunk overlay chrome consistent with the shared UI visual system.

#### Scenario: Game over message
- **WHEN** the match enters game over
- **THEN** a game over message and restart hint are displayed with cyberpunk overlay treatment

#### Scenario: Win message
- **WHEN** the match enters the won state
- **THEN** a win message and restart hint are displayed with cyberpunk overlay treatment
