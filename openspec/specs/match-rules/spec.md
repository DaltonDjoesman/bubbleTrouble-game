## Purpose

Match lifecycle: lives, win/lose states, restart, and multi-level campaign progress.

## Requirements

### Requirement: Lives and player-ball collision
The match SHALL track lives (default 3). Colliding with a ball costs one life.

#### Scenario: Lose a life
- **WHEN** the player collides with a ball while vulnerable and has lives remaining after the hit
- **THEN** lives decrease by one and the match continues with a brief recovery (i-frames and/or position reset)

#### Scenario: Game over
- **WHEN** lives reach zero after a ball collision
- **THEN** the match enters the game over state and playing updates stop

### Requirement: Win by clearing balls
The match SHALL enter the won state when no balls remain.

#### Scenario: Arena cleared
- **WHEN** the last ball is destroyed
- **THEN** the match enters the won state

### Requirement: Restart from end states
From won or game over, the player SHALL be able to restart a fresh match with a single key.

#### Scenario: Restart
- **WHEN** the match is won or over and the player presses the restart key (R)
- **THEN** lives and balls reset to the initial arena setup and play resumes

### Requirement: Return to menu after match
From won or game over, the player SHALL be able to return to the main menu (in addition to any retry control).

#### Scenario: Back to menu
- **WHEN** the match is won or over and the player presses the menu-return key
- **THEN** the main menu is shown

### Requirement: Multi-level campaign progress
Winning a non-final level SHALL progress the run; winning the final level SHALL complete the run with the won state.

#### Scenario: Mid-campaign clear
- **WHEN** the last ball of a non-final level is destroyed
- **THEN** the match does not permanently end the campaign without offering or performing advance to the next level
