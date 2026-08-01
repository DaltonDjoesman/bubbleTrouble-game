## Purpose

Authored multi-level campaign: level definitions with barriers/doors and time budgets, loading into a match, and advance-on-clear progression.

## Requirements

### Requirement: Level definitions
The game SHALL define five authored levels, each with an id, display name, initial balls, `time_seconds`, barriers, and doors (as needed). Levels SHALL NOT rely on platforms.

#### Scenario: Five levels available
- **WHEN** the player opens level select
- **THEN** five distinct levels can be chosen

#### Scenario: Level carries time budget
- **WHEN** a level is defined
- **THEN** it includes a positive `time_seconds` used to fill the time barrier at load

### Requirement: Load level into match
Starting a match with a level id SHALL spawn that level's balls, barriers/doors, and time budget.

#### Scenario: Load level 1
- **WHEN** Play starts with level 1 selected
- **THEN** level 1 balls, geometry, and time barrier appear as defined

### Requirement: Advance on clear
Clearing all balls on a non-final level SHALL advance to the next level (or prompt to continue into it). Clearing the final level SHALL show the win end state. Advancing SHALL refill time from the next level's `time_seconds` and reset weapon mode to default harpoon.

#### Scenario: Clear level 1
- **WHEN** the player clears all balls on level 1
- **THEN** the game proceeds toward level 2 rather than ending the campaign

#### Scenario: Clear level 5
- **WHEN** the player clears all balls on level 5
- **THEN** the won state is shown
