## Purpose

Background music and gameplay/UI sound effects via pygame.mixer, with mute when volume is zero or the device is unavailable.

## Requirements

### Requirement: Background music
The game SHALL play looping background music when audio is available and music volume is above zero.

#### Scenario: Music plays
- **WHEN** the game is running with music volume > 0 and a music file is configured
- **THEN** background music is audible in a loop

### Requirement: Gameplay and UI sound effects
The game SHALL play short SFX for shoot, ball pop/split, player hit, win, lose, and menu UI actions when SFX volume is above zero.

#### Scenario: Shoot SFX
- **WHEN** the player fires and SFX volume > 0
- **THEN** a shoot sound plays

#### Scenario: Mute SFX
- **WHEN** SFX volume is 0
- **THEN** gameplay SFX are not heard
