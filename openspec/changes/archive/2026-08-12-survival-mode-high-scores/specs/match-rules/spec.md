## ADDED Requirements

### Requirement: Survival match lifecycle
When the selected level is Survival, the match SHALL use Survival rules (elapsed chronometer, spawn director, no clear-all win, no time-barrier expiry) as defined by the survival-mode capability. Campaign time-barrier drain and win-by-clearing-balls SHALL apply only to campaign levels.

#### Scenario: Survival ignores barrier expiry
- **WHEN** Survival is playing
- **THEN** the match does not enter game over due to a drained time barrier

#### Scenario: Campaign still times out
- **WHEN** a campaign level's remaining time reaches zero while balls remain
- **THEN** the match enters game over as before

## MODIFIED Requirements

### Requirement: Time barrier
Each campaign level SHALL start with a full time barrier equal to that level's `time_seconds`. Time SHALL drain at a fixed global rate while playing a campaign level. When remaining time reaches zero on a campaign level, the match SHALL enter game over immediately. Survival matches SHALL NOT use this draining time barrier.

#### Scenario: Level starts full
- **WHEN** a campaign level loads into playing state
- **THEN** the time barrier is full for that level's budget

#### Scenario: Time expires
- **WHEN** remaining time reaches zero while balls remain on a campaign level
- **THEN** the match enters game over and playing updates stop

### Requirement: Win by clearing balls
Clearing all balls on the final campaign level SHALL enter the won state. Clearing a non-final campaign level SHALL advance per multi-level campaign progress (not a permanent campaign win). Clearing all balls during Survival SHALL NOT enter the won or level-clear state.

#### Scenario: Final arena cleared
- **WHEN** the last ball of the final campaign level is destroyed
- **THEN** the match enters the won state

#### Scenario: Survival clear is not a win
- **WHEN** the last ball during Survival is destroyed
- **THEN** the match does not enter won or level clear from that alone
