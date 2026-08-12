## Purpose

Ceiling spike hazard along the top of the play arena that pops balls on contact, matching classic Pang / Bubble Trouble roof behavior.

## Requirements

### Requirement: Spiked play-area ceiling
During play, the top edge of the playable arena SHALL present a continuous row of downward-pointing spikes (or equivalent pointed ceiling hazard) visible to the player.

#### Scenario: Spikes visible in play
- **WHEN** the match is in the playing state
- **THEN** a spiked / pointed hazard is drawn along the top of the play area

### Requirement: Ball hit by ceiling spikes splits or is destroyed
When a ball contacts the ceiling spike hazard, the game SHALL resolve that contact using the same size-tier split rules as a successful laser hit: a non-smallest ball is removed and replaced by two smaller balls; a smallest-tier ball is removed with no children.

#### Scenario: Large or medium ball hits spikes
- **WHEN** a non-smallest ball intersects the ceiling spike hazard
- **THEN** that ball is removed and two smaller balls spawn near its position according to normal split rules

#### Scenario: Smallest ball hits spikes
- **WHEN** a smallest-tier ball intersects the ceiling spike hazard
- **THEN** that ball is removed and no new balls spawn from it

### Requirement: Spikes active every level
The ceiling spike hazard SHALL be active for every playable level during the playing state (not optional per level).

#### Scenario: Spikes on any level
- **WHEN** any authored level is in the playing state
- **THEN** ceiling spike contact can destroy or split balls
