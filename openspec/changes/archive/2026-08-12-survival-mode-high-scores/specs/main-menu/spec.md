## ADDED Requirements

### Requirement: High Scores entry on menu
The main menu SHALL expose a High Scores action that opens the High Scores view (1P/2P boards) defined by the high-scores capability.

#### Scenario: Open High Scores
- **WHEN** the player selects High Scores from the menu
- **THEN** the High Scores view is shown

## MODIFIED Requirements

### Requirement: Mode and level selection
The menu SHALL let the player choose 1 or 2 players and select a level, including the Survival level as the last selectable entry.

#### Scenario: Choose mode
- **WHEN** the player changes mode between 1P and 2P on the menu
- **THEN** the selected mode is stored for the next Play action

#### Scenario: Choose level
- **WHEN** the player changes the selected level on the menu
- **THEN** Play starts (or will start) that level id when levels exist

#### Scenario: Choose Survival
- **WHEN** the player selects Survival in level select and confirms Play
- **THEN** the next match starts in Survival mode
