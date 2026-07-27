## ADDED Requirements

### Requirement: Level definitions
The game SHALL define five authored levels, each with an id, display name, initial balls, platforms, and obstacles.

#### Scenario: Five levels available
- **WHEN** the player opens level select
- **THEN** five distinct levels can be chosen

### Requirement: Load level into match
Starting a match with a level id SHALL spawn that level's balls and geometry.

#### Scenario: Load level 1
- **WHEN** Play starts with level 1 selected
- **THEN** level 1 balls and platforms/obstacles appear as defined

### Requirement: Advance on clear
Clearing all balls on a non-final level SHALL advance to the next level (or prompt to continue into it). Clearing the final level SHALL show the win end state.

#### Scenario: Clear level 1
- **WHEN** the player clears all balls on level 1
- **THEN** the game proceeds toward level 2 rather than ending the campaign

#### Scenario: Clear level 5
- **WHEN** the player clears all balls on level 5
- **THEN** the won state is shown
