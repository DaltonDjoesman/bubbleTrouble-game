## Purpose

Independent music and SFX volume settings with local persistence across launches.

## Requirements

### Requirement: Separate volume controls
The player SHALL be able to set music volume and SFX volume independently from the menu.

#### Scenario: Lower music only
- **WHEN** the player decreases music volume and leaves SFX unchanged
- **THEN** music becomes quieter (or silent at 0) while SFX volume setting remains as before

### Requirement: Persist volumes
Volume settings SHALL persist across application restarts.

#### Scenario: Relaunch remembers volumes
- **WHEN** the player sets volumes, quits, and relaunches
- **THEN** the previous music and SFX volumes are applied
