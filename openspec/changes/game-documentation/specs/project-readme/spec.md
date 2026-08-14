## Purpose

Root README that lets a new reader install, run, and see the shipped game, including full-window screenshots and a GIF.

## ADDED Requirements

### Requirement: Root README with quickstart
The repository SHALL include a README at the project root covering what the game is, requirements, install, how to run, and controls.

#### Scenario: Contributor can run from README
- **WHEN** a reader follows the README install and run steps with a compatible Python environment
- **THEN** they have enough information to launch the game without reading source

### Requirement: Project structure documented
The README (or a linked doc) SHALL describe the main folders: Scripts, assets, audio, docs, openspec.

#### Scenario: Structure section exists
- **WHEN** a reader opens the README
- **THEN** they can identify where code, assets, and OpenSpec planning live

### Requirement: Asset credits
Documentation SHALL credit the Craftpix cyberpunk pack and point to its license file.

#### Scenario: License mentioned
- **WHEN** a reader checks credits in the docs
- **THEN** the Craftpix pack and `License.txt` location are referenced

### Requirement: Shipped feature surface in README
The README SHALL describe the shipped product: five-level campaign, Survival, 1P/2P local co-op, High Scores, and Options/audio, with a link to gameplay notes for rules.

#### Scenario: Modes are discoverable
- **WHEN** a reader opens the README
- **THEN** they can tell the game has a campaign, a Survival mode, local co-op, and a High Scores view without opening source

### Requirement: Full-window game media in README
The README SHALL include screenshots of the main menu, a campaign match in play, a Survival match in play, and the High Scores view, plus one GIF of in-match play.

#### Scenario: Reader sees the shipped screens
- **WHEN** a reader opens the README
- **THEN** they see those four screenshots and one play GIF without leaving the README

### Requirement: Game media captures the entire window
Every screenshot and GIF of the running game SHALL capture the entire game window framebuffer, including HUD, menus, and chrome. Game media MUST NOT crop to the play arena only.

#### Scenario: Match shot includes HUD
- **WHEN** a campaign or Survival screenshot or the play GIF is shown
- **THEN** the image includes the full window (play arena and bottom status panel), not a cropped playfield

#### Scenario: Menu and High Scores shots are full window
- **WHEN** a main-menu or High Scores screenshot is shown
- **THEN** the image is the entire game window, not a cropped panel
