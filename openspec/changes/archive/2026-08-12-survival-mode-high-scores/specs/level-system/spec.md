## MODIFIED Requirements

### Requirement: Level definitions
The game SHALL define five authored campaign levels plus a final selectable Survival level, each with an id and display name. Campaign levels SHALL include initial balls, `time_seconds`, barriers, and doors (as needed), and SHALL NOT rely on platforms. The Survival level SHALL be identified as Survival mode (endless) rather than a clearable campaign arena with a draining time budget.

#### Scenario: Five levels available
- **WHEN** the player opens level select
- **THEN** five distinct campaign levels can be chosen in addition to Survival

#### Scenario: Level carries time budget
- **WHEN** a campaign level is defined
- **THEN** it includes a positive `time_seconds` used to fill the time barrier at load

#### Scenario: Survival selectable
- **WHEN** the player selects Survival from level select and starts Play
- **THEN** a Survival match loads instead of a normal campaign clear arena

### Requirement: Advance on clear
Clearing all balls on a non-final campaign level SHALL advance to the next campaign level (or prompt to continue into it). Clearing the final campaign level (the last clearable arena before Survival) SHALL show the win end state and SHALL NOT auto-advance into Survival. Advancing between campaign levels SHALL refill time from the next level's `time_seconds` and reset weapon mode to default harpoon.

#### Scenario: Clear level 1
- **WHEN** the player clears all balls on level 1
- **THEN** the game proceeds toward level 2 rather than ending the campaign

#### Scenario: Clear level 5
- **WHEN** the player clears all balls on level 5
- **THEN** the won state is shown and Survival does not start automatically
