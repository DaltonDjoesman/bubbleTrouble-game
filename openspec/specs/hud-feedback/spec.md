## Purpose

On-screen HUD for the time barrier / Survival chronometer and clear win / game over messaging with restart guidance. During play, time and level live in a reserved Pang-style bottom status panel.

## Requirements

### Requirement: Bottom status panel
While playing, the window SHALL reserve a bottom status panel outside the playable arena. The panel SHALL present a Pang-inspired framed strip (brick / stone chrome) and SHALL display the time meter (campaign barrier or Survival chronometer) and the current level indicator.

#### Scenario: Panel reserved below play
- **WHEN** the match is in the playing state
- **THEN** a bottom status panel is visible below the playable arena and gameplay sprites do not use that strip as floor space

#### Scenario: Time and level in panel
- **WHEN** the match is in the playing state
- **THEN** the time meter and a level indicator are shown inside the bottom status panel

### Requirement: Lives display
While playing a campaign level, the HUD SHALL show the time barrier (remaining time as a fill bar) inside the bottom status panel. While playing Survival, the HUD SHALL show the elapsed chronometer instead of that draining fill. The HUD SHALL NOT show a multi-life stock or life-capsule lives display during play. The time meter and level indicator SHALL NOT be drawn as a floating overlay at the top of the playfield.

#### Scenario: Time barrier visible
- **WHEN** a campaign level is in the playing state
- **THEN** a time barrier fill representing remaining time is visible in the bottom status panel

#### Scenario: No life icons in play
- **WHEN** the match is in the playing state
- **THEN** remaining-lives sprites are not shown as the survival meter

#### Scenario: No top floating time/level HUD
- **WHEN** the match is in the playing state
- **THEN** the time meter and level text are not drawn as a top-of-playfield overlay

### Requirement: Survival chronometer in status panel
While Survival is playing, the bottom status panel SHALL show a numeric elapsed chronometer (and the Survival level indicator) instead of a draining time-barrier fill bar.

#### Scenario: Chronometer visible in Survival
- **WHEN** Survival is in the playing state
- **THEN** an elapsed-time chronometer is visible in the bottom status panel and a draining time-barrier fill is not shown as the survival meter

#### Scenario: Survival end shows final time
- **WHEN** Survival enters game over
- **THEN** the finalized elapsed time is shown in the end-state messaging

### Requirement: End-state messaging
Win and game over states SHALL show clear on-screen text including how to restart.

#### Scenario: Game over message
- **WHEN** the match enters game over
- **THEN** a game over message and restart hint are displayed

#### Scenario: Win message
- **WHEN** the match enters the won state
- **THEN** a win message and restart hint are displayed
