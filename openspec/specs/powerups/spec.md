## Purpose

Random powerup drops on ball hits and weapon modes (TIME / STICKY / DRILL) with one active weapon at a time.

## Requirements

### Requirement: Random power drops
When a ball is destroyed or split by a weapon hit, the game MAY spawn a powerup pickup at random. Pickup types SHALL include TIME, STICKY, and DRILL.

#### Scenario: Drop can appear
- **WHEN** a ball is hit and the random drop roll succeeds
- **THEN** a powerup pickup of one of the supported types appears near the hit

### Requirement: One weapon at a time
Collecting STICKY or DRILL SHALL set the player's weapon mode to that power and replace any previous weapon mode. Default mode SHALL be the growing harpoon. Collecting TIME SHALL add seconds to the shared time barrier and SHALL NOT change weapon mode.

#### Scenario: Replace weapon
- **WHEN** the player collects DRILL while in STICKY mode
- **THEN** subsequent shots use DRILL rules

#### Scenario: TIME adds seconds
- **WHEN** the player collects a TIME powerup
- **THEN** remaining time increases by the configured amount (clamped) and weapon mode is unchanged

### Requirement: Default weapon is growing harpoon
Until the player collects STICKY or DRILL, shots SHALL use the default growing harpoon behavior from projectile-combat.

#### Scenario: Fresh level default
- **WHEN** a level starts
- **THEN** the player weapon mode is the default growing harpoon
