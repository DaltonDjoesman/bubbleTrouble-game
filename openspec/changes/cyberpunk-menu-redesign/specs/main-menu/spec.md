## ADDED Requirements

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
