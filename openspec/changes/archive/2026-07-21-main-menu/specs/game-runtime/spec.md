## MODIFIED Requirements

### Requirement: Reliable game bootstrap
The game SHALL initialize pygame, resolve asset paths from the project root, and expose a single supported entry point. **On launch it SHALL enter the menu state rather than starting a match immediately.**

#### Scenario: Game starts from project root
- **WHEN** the player runs the supported entry point from the repository root with pygame installed
- **THEN** a window opens and the main menu is shown first
