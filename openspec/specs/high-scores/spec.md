## Purpose

Local persistence and menu presentation of the top five Survival run times, with separate 1P and 2P boards switchable like tabs.

## Requirements

### Requirement: Persist top five per mode
The game SHALL store at most five Survival high-score entries per mode board (`1p` and `2p`), each with a three-letter name and elapsed time. Entries SHALL be ordered best time first. Scores SHALL persist across application restarts on the local machine.

#### Scenario: Relaunch remembers boards
- **WHEN** the player saves a qualifying Survival entry, quits, and relaunches
- **THEN** that entry still appears on the correct mode board in ranked order

#### Scenario: Sixth place discarded
- **WHEN** a new qualifying entry is inserted into a full board of five
- **THEN** only the best five times remain stored for that board

### Requirement: High Scores menu with mode tabs
The main menu flow SHALL provide a High Scores view that shows one mode board at a time and lets the player switch between 1P and 2P boards (tab-like selection).

#### Scenario: View 1P board
- **WHEN** the player opens High Scores and selects the 1P tab
- **THEN** up to five 1P Survival entries are listed (rank, name, time)

#### Scenario: Switch to 2P board
- **WHEN** the player switches to the 2P tab on High Scores
- **THEN** the 2P Survival board is shown instead of the 1P board

#### Scenario: Empty board
- **WHEN** a mode board has no entries
- **THEN** the High Scores view for that tab shows an empty-state indication rather than crashing
