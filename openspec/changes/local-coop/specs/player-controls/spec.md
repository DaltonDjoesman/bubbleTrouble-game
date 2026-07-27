## ADDED Requirements

### Requirement: Per-player control schemes
The player system SHALL support multiple instances with independent keymaps and facing/animation. All co-op players SHALL stay on the floor baseline (no jump).

#### Scenario: Instantiate P2 scheme
- **WHEN** a second player is spawned for co-op
- **THEN** that instance responds only to the P2 keymap and remains grounded
