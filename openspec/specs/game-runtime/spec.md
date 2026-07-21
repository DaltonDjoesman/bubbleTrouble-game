## Purpose

Game bootstrap, asset paths, single entry point, and sprite group orchestration.

## Requirements

### Requirement: Reliable game bootstrap
The game SHALL initialize pygame, resolve asset paths from the project root, and expose a single supported entry point.

#### Scenario: Game starts from project root
- **WHEN** the player runs the supported entry point from the repository root with pygame installed
- **THEN** a window opens at the configured resolution and the main loop runs at the configured FPS without path load errors for required assets

#### Scenario: Single entry point
- **WHEN** a contributor looks for how to launch the game
- **THEN** only one primary module is documented/supported as the live game entry (legacy scripts are not required to run)

### Requirement: Sprite group orchestration
The game runtime SHALL own sprite groups for the player, balls, and bullets and update/draw them each frame while in the playing state.

#### Scenario: Playing frame update
- **WHEN** the match is in the playing state
- **THEN** balls, bullets, and the player are updated and drawn each frame before the display flip
