## Purpose

Match lifecycle: time barrier (campaign), Survival lifecycle branch, one-hit (1P) / co-op death contract, win/lose states, restart, and multi-level campaign progress.

## Requirements

### Requirement: Time barrier
Each campaign level SHALL start with a full time barrier equal to that level's `time_seconds`. Time SHALL drain at a fixed global rate while playing a campaign level. When remaining time reaches zero on a campaign level, the match SHALL enter game over immediately. Survival matches SHALL NOT use this draining time barrier.

#### Scenario: Level starts full
- **WHEN** a campaign level loads into playing state
- **THEN** the time barrier is full for that level's budget

#### Scenario: Time expires
- **WHEN** remaining time reaches zero while balls remain on a campaign level
- **THEN** the match enters game over and playing updates stop

### Requirement: Survival match lifecycle
When the selected level is Survival, the match SHALL use Survival rules (elapsed chronometer, spawn director, no clear-all win, no time-barrier expiry) as defined by the survival-mode capability. Campaign time-barrier drain and win-by-clearing-balls SHALL apply only to campaign levels.

#### Scenario: Survival ignores barrier expiry
- **WHEN** Survival is playing
- **THEN** the match does not enter game over due to a drained time barrier

#### Scenario: Campaign still times out
- **WHEN** a campaign level's remaining time reaches zero while balls remain
- **THEN** the match enters game over as before

### Requirement: One-hit defeat in single-player
In single-player, colliding with a ball while playing SHALL immediately end the match in game over (no multi-life stock, no mid-level continue).

#### Scenario: Ball touch ends run
- **WHEN** the single player collides with a ball while vulnerable in playing state
- **THEN** the match enters game over

### Requirement: Co-op hit and revive contract
When local co-op is active, a ball hit SHALL remove only the hit player from the current level; the other player MAY continue. Advancing to the next level SHALL respawn both players. If no players remain alive in the level, or the shared time barrier empties (campaign), the match SHALL game over.

#### Scenario: Partner continues
- **WHEN** P1 is hit by a ball and P2 is still alive
- **THEN** P1 is removed from play and P2 continues with the shared time barrier

#### Scenario: Both return next level
- **WHEN** the level is cleared while at least one co-op player was alive
- **THEN** both players are present again at the start of the next level

### Requirement: Lives and player-ball collision
The match SHALL NOT use a multi-life stock. Single-player ball collision follows one-hit defeat. Co-op follows the co-op hit and revive contract.

#### Scenario: No life decrement loop
- **WHEN** the single player collides with a ball while playing
- **THEN** the match does not continue on the same level with reduced lives

### Requirement: Win by clearing balls
Clearing all balls on the final campaign level SHALL enter the won state. Clearing a non-final campaign level SHALL advance per multi-level campaign progress (not a permanent campaign win). Clearing all balls during Survival SHALL NOT enter the won or level-clear state.

#### Scenario: Final arena cleared
- **WHEN** the last ball of the final campaign level is destroyed
- **THEN** the match enters the won state

#### Scenario: Survival clear is not a win
- **WHEN** the last ball during Survival is destroyed
- **THEN** the match does not enter won or level clear from that alone

### Requirement: Restart from end states
From won or game over, the player SHALL be able to restart a fresh match with a single key.

#### Scenario: Restart
- **WHEN** the match is won or over and the player presses the restart key (R)
- **THEN** time budget, balls, geometry, weapon mode, and player state reset to the selected level's initial setup and play resumes

### Requirement: Return to menu after match
From won or game over, the player SHALL be able to return to the main menu (in addition to any retry control).

#### Scenario: Back to menu
- **WHEN** the match is won or over and the player presses the menu-return key
- **THEN** the main menu is shown

### Requirement: Multi-level campaign progress
Winning a non-final level SHALL progress the run; winning the final campaign level SHALL complete the run with the won state.

#### Scenario: Mid-campaign clear
- **WHEN** the last ball of a non-final level is destroyed
- **THEN** the match does not permanently end the campaign without offering or performing advance to the next level

### Requirement: Co-op win and lose
In co-op, clearing all balls on the final campaign level wins (non-final levels advance). Game over when the shared time barrier empties (campaign) or when no co-op players remain alive in the level.

#### Scenario: Co-op clear final
- **WHEN** two players are in co-op and the last ball of the final campaign level is destroyed
- **THEN** the match enters the won state

#### Scenario: Co-op all down
- **WHEN** the last living co-op player is hit by a ball
- **THEN** the match enters game over

#### Scenario: Co-op time out
- **WHEN** shared remaining time reaches zero on a campaign level
- **THEN** the match enters game over
