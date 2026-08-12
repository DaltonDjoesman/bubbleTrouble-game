## Purpose

Main menu entry flow: Play/Quit, mode and level selection (including Survival), High Scores, keyboard navigation, and audio settings before a match.

## Requirements

### Requirement: Main menu on launch
The game SHALL show a main menu before a match starts, with Play and Quit actions.

#### Scenario: Boot to menu
- **WHEN** the game launches
- **THEN** the main menu is shown and a match does not start until Play is confirmed

#### Scenario: Quit
- **WHEN** the player selects Quit from the menu
- **THEN** the application exits

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

### Requirement: High Scores entry on menu
The main menu SHALL expose a High Scores action that opens the High Scores view (1P/2P boards) defined by the high-scores capability.

#### Scenario: Open High Scores
- **WHEN** the player selects High Scores from the menu
- **THEN** the High Scores view is shown

### Requirement: Keyboard navigation
The menu SHALL be operable with keyboard (navigate + confirm).

#### Scenario: Confirm Play
- **WHEN** the player highlights Play and confirms
- **THEN** the app transitions into a match with the selected mode and level

### Requirement: Audio section in menu
The main menu SHALL expose controls to adjust music and SFX volumes.

#### Scenario: Adjust from menu
- **WHEN** the player is on the main menu audio controls
- **THEN** they can increase or decrease music and SFX volumes separately

### Requirement: Functional two-player menu option
Selecting 2 players and Play SHALL start a co-op match (not a silent fallback to 1P).

#### Scenario: 2P Play
- **WHEN** mode is 2P and the player confirms Play
- **THEN** a co-op match starts with two players

### Requirement: Cyberpunk menu presentation
Main menu screens (root, options, level select, high scores) SHALL render using the shared cyberpunk UI chrome (dark shell, neon branding, gold selection, English labels) while preserving existing navigation actions and flows.

#### Scenario: Root looks themed
- **WHEN** the root menu is shown
- **THEN** items remain Play (or equivalent English play label), Mode, High Scores, Options, and Quit, presented with cyberpunk chrome and gold highlight on the selected item

#### Scenario: Level select chrome only
- **WHEN** the player opens level select from Play
- **THEN** Campaign/Survival selection and starting a level still work as before, with restyled chrome only

### Requirement: English menu copy
User-facing menu labels and footer hints SHALL be in English.

#### Scenario: English hints
- **WHEN** a menu footer is shown
- **THEN** hint labels are English (for example Navigate, Confirm, Back)
