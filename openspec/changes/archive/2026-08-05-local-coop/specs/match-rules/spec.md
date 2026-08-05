## MODIFIED Requirements

### Requirement: Co-op win and lose
In co-op, clearing all balls on the final level wins (non-final levels advance). Game over when the shared time barrier empties or when no co-op players remain alive in the level.

#### Scenario: Co-op clear final
- **WHEN** two players are in co-op and the last ball of the final level is destroyed
- **THEN** the match enters the won state

#### Scenario: Co-op all down
- **WHEN** the last living co-op player is hit by a ball
- **THEN** the match enters game over

#### Scenario: Co-op time out
- **WHEN** shared remaining time reaches zero
- **THEN** the match enters game over
