## ADDED Requirements

### Requirement: Bottom status panel
While playing, the window SHALL reserve a bottom status panel outside the playable arena. The panel SHALL present a Pang-inspired framed strip (brick / stone chrome) and SHALL display the time barrier and the current level indicator.

#### Scenario: Panel reserved below play
- **WHEN** the match is in the playing state
- **THEN** a bottom status panel is visible below the playable arena and gameplay sprites do not use that strip as floor space

#### Scenario: Time and level in panel
- **WHEN** the match is in the playing state
- **THEN** the time barrier fill and a level indicator are shown inside the bottom status panel

## MODIFIED Requirements

### Requirement: Lives display
While playing, the HUD SHALL show the time barrier (remaining time as a fill bar) inside the bottom status panel. The HUD SHALL NOT show a multi-life stock or life-capsule lives display during play. The time barrier and level indicator SHALL NOT be drawn as a floating overlay at the top of the playfield.

#### Scenario: Time barrier visible
- **WHEN** the match is in the playing state
- **THEN** a time barrier fill representing remaining time is visible in the bottom status panel

#### Scenario: No life icons in play
- **WHEN** the match is in the playing state
- **THEN** remaining-lives sprites are not shown as the survival meter

#### Scenario: No top floating time/level HUD
- **WHEN** the match is in the playing state
- **THEN** the time barrier and level text are not drawn as a top-of-playfield overlay
