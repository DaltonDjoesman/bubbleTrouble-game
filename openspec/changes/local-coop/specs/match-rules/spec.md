## ADDED Requirements

### Requirement: Co-op win and lose
In co-op, clearing all balls wins; shared lives reaching zero is game over.

#### Scenario: Co-op clear
- **WHEN** two players are active and the last ball is destroyed
- **THEN** the match enters the won state

#### Scenario: Co-op wipe
- **WHEN** shared lives reach zero after a hit
- **THEN** the match enters game over
