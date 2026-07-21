## ADDED Requirements

### Requirement: Two-player co-op match
When mode is 2P, the match SHALL spawn two local players who share the goal of clearing all balls.

#### Scenario: Start co-op
- **WHEN** the player starts Play with 2P selected
- **THEN** two player characters appear in the arena with distinct controls

### Requirement: Shared lives pool
Co-op SHALL use a shared lives pool; a ball hit on either player spends from that pool.

#### Scenario: P2 hit costs life
- **WHEN** player 2 collides with a ball while vulnerable
- **THEN** shared lives decrease by one

### Requirement: Distinct control schemes
Player 1 and player 2 SHALL use different keyboard bindings.

#### Scenario: Both can move and shoot
- **WHEN** a co-op match is playing
- **THEN** P1 can move/shoot with their keys and P2 with theirs without sharing the same keys
