## ADDED Requirements

### Requirement: Gameplay notes document
The project SHALL include gameplay notes (e.g. `docs/gameplay.md`) describing the MVP rules.

#### Scenario: Core loop documented
- **WHEN** a reader opens the gameplay notes
- **THEN** they can learn movement, shooting (multiple bullets, not a classic rope harpoon), ball split, lives, win, and game over

### Requirement: Explicit non-goals
Gameplay notes SHALL list what is out of scope for the current MVP (including no level progression yet).

#### Scenario: No levels called out
- **WHEN** a reader checks scope in the gameplay notes
- **THEN** multi-level progression is listed as not in the current MVP

### Requirement: Alignment with product decisions
Gameplay notes SHALL reflect cyberpunk presentation intent and bullet-based combat rather than a classic Bubble Trouble harpoon.

#### Scenario: Combat model stated
- **WHEN** a reader reads the combat section
- **THEN** combat is described as upward (or configured) projectile shots using Craftpix bullet sprites
