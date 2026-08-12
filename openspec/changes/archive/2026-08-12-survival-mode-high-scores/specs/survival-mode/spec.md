## Purpose

Endless Survival match rules: ascending shared chronometer, continuous ramping ball spawns, lose-on-last-player-down, and post-run initials when the time qualifies for a local top-five board.

## ADDED Requirements

### Requirement: Survival match uses elapsed chronometer
While Survival is in the playing state, the match SHALL track shared elapsed time that increases while play is active. Survival SHALL NOT drain a time barrier and SHALL NOT enter game over because a timer reached zero.

#### Scenario: Time counts up
- **WHEN** Survival is playing
- **THEN** elapsed survival time increases over real play time

#### Scenario: No time-out game over
- **WHEN** Survival has been playing for longer than any campaign time budget
- **THEN** the match does not end solely due to elapsed time

### Requirement: Survival never wins by clearing balls
Clearing all balls during Survival SHALL NOT enter level clear or won. The match SHALL continue until the Survival lose condition is met, with further ball spawns as defined by the spawn ramp.

#### Scenario: Empty arena continues
- **WHEN** the last ball in Survival is destroyed and at least one player remains alive
- **THEN** the match remains in playing state (awaiting further spawns)

### Requirement: Survival lose condition
Survival SHALL end in game over when the last living player is eliminated by a ball hit, using the same one-hit / co-op removal rules as the campaign (1P: immediate; 2P: when no players remain alive).

#### Scenario: Solo death ends run
- **WHEN** the single player collides with a ball while vulnerable in Survival
- **THEN** the match enters game over and the run's elapsed time is finalized

#### Scenario: Co-op ends when both are down
- **WHEN** both co-op players have been removed in Survival
- **THEN** the match enters game over and the shared elapsed time is finalized

### Requirement: Continuous spawn with difficulty ramp
During Survival play, the game SHALL spawn balls over time with increasing difficulty (shorter intervals and/or larger size weighting as elapsed time grows). The game SHALL enforce a maximum number of concurrent balls and SHALL skip or defer spawns while at that cap. Collecting a TIME powerup during Survival SHALL briefly pause new spawns without adding barrier seconds.

#### Scenario: Balls keep appearing
- **WHEN** Survival play continues and concurrent balls are below the cap
- **THEN** new balls appear over time without requiring a level reload

#### Scenario: Cap prevents overflow
- **WHEN** the number of live balls is at the configured maximum
- **THEN** the spawn director does not add another ball until a slot is free

#### Scenario: TIME pauses spawns
- **WHEN** a player collects TIME during Survival
- **THEN** new ball spawns are paused for a short configured duration and weapon mode is unchanged

### Requirement: Qualifying run prompts for three initials
When a Survival run ends and its elapsed time qualifies for the top five of the board matching the match mode (1P or 2P), the game SHALL prompt for a three-letter name before committing the entry. Non-qualifying runs SHALL skip the initials prompt.

#### Scenario: New top-five entry
- **WHEN** a Survival game over time is strictly better than the fifth place on the mode's board (or the board has fewer than five entries)
- **THEN** the player can enter exactly three letters and the entry is saved to that board

#### Scenario: Non-qualifying skips prompt
- **WHEN** a Survival game over time does not qualify for that mode's top five
- **THEN** the initials prompt is not required and the board is unchanged
