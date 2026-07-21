## Purpose

Application screen state machine: menu, playing, and end states with explicit transitions.

## Requirements

### Requirement: Application screen states
The application SHALL support distinct states including at least menu, playing, won, and game_over, and transition between them explicitly.

#### Scenario: Menu to playing
- **WHEN** Play is confirmed on the menu
- **THEN** the state becomes playing and the match runs

#### Scenario: Return to menu from end
- **WHEN** the match is won or over and the player chooses return-to-menu
- **THEN** the state becomes menu
