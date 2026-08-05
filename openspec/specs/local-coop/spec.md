## Purpose

Local same-screen co-op: two players share the arena and time barrier, with per-player death and revive on level advance.

## Requirements

### Requirement: Two-player co-op match
When mode is 2P, the match SHALL spawn two local players who share the goal of clearing all balls and share the time barrier.

#### Scenario: Start co-op
- **WHEN** the player starts Play with 2P selected
- **THEN** two player characters appear in the arena with distinct controls

### Requirement: Per-player death and revive
A ball hit SHALL remove only the hit player from the current level. The other player MAY continue. Advancing to the next level SHALL respawn both players. If no living players remain, the match SHALL game over.

#### Scenario: Partner continues
- **WHEN** P1 is hit by a ball and P2 is still alive
- **THEN** P1 is removed from play and P2 continues with the shared time barrier

#### Scenario: Both return next level
- **WHEN** the level is cleared while at least one co-op player was alive
- **THEN** both players are present again at the start of the next level

### Requirement: Shared time barrier
Co-op SHALL use one shared time barrier (same drain and TIME pickups). Empty time SHALL game over regardless of living players.

#### Scenario: Time expires in co-op
- **WHEN** remaining time reaches zero while at least one player is alive
- **THEN** the match enters game over

### Requirement: Distinct control schemes
Player 1 and player 2 SHALL use different keyboard bindings. Movement SHALL remain grounded (no jump).

#### Scenario: Both can move and shoot
- **WHEN** a co-op match is playing
- **THEN** P1 can move/shoot with their keys and P2 with theirs without sharing the same keys
