## ADDED Requirements

### Requirement: Gameplay notes document
The project SHALL include gameplay notes (e.g. `docs/gameplay.md`) describing the classic rules.

#### Scenario: Core loop documented
- **WHEN** a reader opens the gameplay notes
- **THEN** they can learn grounded movement, time barrier, one-hit defeat (1P), shooting (harpoon / STICKY / DRILL), ball split, barriers/doors, win, and game over

### Requirement: Explicit scope
Gameplay notes SHALL list current classic features and deferred work (e.g. local co-op implementation).

#### Scenario: Classic features called out
- **WHEN** a reader checks scope in the gameplay notes
- **THEN** time barrier, one-hit 1P, barriers/doors, powerups, and five levels are described as current rules

### Requirement: Alignment with classic product decisions
Gameplay notes SHALL reflect cyberpunk presentation plus classic Bubble Trouble stakes (time, grounded, powers) rather than multi-life platform gameplay.

#### Scenario: Combat and survival model stated
- **WHEN** a reader reads the combat/survival sections
- **THEN** survival is the time barrier (not lives), and weapons include default harpoon plus STICKY/DRILL pickups
