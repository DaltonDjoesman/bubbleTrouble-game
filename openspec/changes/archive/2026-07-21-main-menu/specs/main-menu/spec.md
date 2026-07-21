## ADDED Requirements

### Requirement: Main menu on launch
The game SHALL show a main menu before a match starts, with Play and Quit actions.

#### Scenario: Boot to menu
- **WHEN** the game launches
- **THEN** the main menu is shown and a match does not start until Play is confirmed

#### Scenario: Quit
- **WHEN** the player selects Quit from the menu
- **THEN** the application exits

### Requirement: Mode and level selection
The menu SHALL let the player choose 1 or 2 players and select a level.

#### Scenario: Choose mode
- **WHEN** the player changes mode between 1P and 2P on the menu
- **THEN** the selected mode is stored for the next Play action

#### Scenario: Choose level
- **WHEN** the player changes the selected level on the menu
- **THEN** Play starts (or will start) that level id when levels exist

### Requirement: Keyboard navigation
The menu SHALL be operable with keyboard (navigate + confirm).

#### Scenario: Confirm Play
- **WHEN** the player highlights Play and confirms
- **THEN** the app transitions into a match with the selected mode and level
