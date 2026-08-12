## MODIFIED Requirements

### Requirement: One weapon at a time
Collecting STICKY or DRILL SHALL set the player's weapon mode to that power and replace any previous weapon mode. Default mode SHALL be the growing harpoon. Collecting TIME on a campaign level SHALL add seconds to the shared time barrier and SHALL NOT change weapon mode. Collecting TIME during Survival SHALL briefly pause ball spawns and SHALL NOT add time-barrier seconds or change weapon mode.

#### Scenario: Replace weapon
- **WHEN** the player collects DRILL while in STICKY mode
- **THEN** subsequent shots use DRILL rules

#### Scenario: TIME adds seconds
- **WHEN** the player collects a TIME powerup on a campaign level
- **THEN** remaining time increases by the configured amount (clamped) and weapon mode is unchanged

#### Scenario: TIME pauses Survival spawns
- **WHEN** the player collects a TIME powerup during Survival
- **THEN** ball spawns pause for a short configured duration and weapon mode is unchanged
