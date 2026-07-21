## ADDED Requirements

### Requirement: Root README with quickstart
The repository SHALL include a README at the project root covering what the game is, requirements, install, how to run, and controls.

#### Scenario: Contributor can run from README
- **WHEN** a reader follows the README install and run steps with a compatible Python environment
- **THEN** they have enough information to launch the game without reading source

### Requirement: Project structure documented
The README (or a linked doc) SHALL describe the main folders: Scripts, sprites, Assests, openspec.

#### Scenario: Structure section exists
- **WHEN** a reader opens the README
- **THEN** they can identify where code, assets, and OpenSpec planning live

### Requirement: Asset credits
Documentation SHALL credit the Craftpix cyberpunk pack and point to its license file.

#### Scenario: License mentioned
- **WHEN** a reader checks credits in the docs
- **THEN** the Craftpix pack and `License.txt` location are referenced
