## Purpose

Growing upward lasers with weapon modes (default harpoon, STICKY, DRILL), active caps, and laser–ball hit resolution.

## Requirements

### Requirement: Growing upward laser
In default harpoon mode, lasers SHALL spawn at the player's fire position, grow upward each frame, and despawn when they reach the top of the screen or hit solid barrier/door geometry (unless weapon-specific rules say otherwise).

#### Scenario: Laser grows
- **WHEN** a default laser is active
- **THEN** its vertical extent increases upward each frame from the spawn baseline

#### Scenario: Laser reaches ceiling
- **WHEN** the default laser's top edge reaches or passes the top of the screen
- **THEN** that laser is removed

### Requirement: Multiple lasers with a cap
For harpoon and DRILL modes, the game SHALL allow multiple simultaneous lasers up to a configured maximum (default 2). STICKY mode is not limited by this slot cap (see STICKY weapon behavior).

#### Scenario: At capacity
- **WHEN** the maximum number of active non-sticky lasers already exists
- **THEN** pressing Space does not spawn an additional harpoon/drill laser

#### Scenario: Slot frees
- **WHEN** an active laser despawns or hits a ball and the count falls below the maximum
- **THEN** the player can fire again

### Requirement: Laser hits ball
In default harpoon mode, a laser that collides with a ball SHALL be removed and trigger ball-system hit resolution. STICKY and DRILL follow their weapon-specific requirements instead of this despawn-on-first-hit rule where they conflict.

#### Scenario: Default collision
- **WHEN** a default harpoon laser rect intersects a ball rect
- **THEN** the laser is destroyed and the ball is processed for split or removal

### Requirement: STICKY weapon behavior
While STICKY mode is active, the player SHALL be able to fire without an active-laser slot limit (normal fire cooldown still applies). After growing into place, each sticky laser SHALL remain until a ball collides with it. On that collision, the ball SHALL be resolved (split/remove) and that sticky laser SHALL despawn. At most three sticky lasers SHALL remain on the map; firing beyond that SHALL remove the oldest sticky. Changing weapon mode SHALL NOT remove already planted sticky lasers.

#### Scenario: Sticky stays
- **WHEN** a sticky laser has finished growing and no ball has hit it
- **THEN** it remains in place as a solid vertical hazard for balls

#### Scenario: Ball hits sticky
- **WHEN** a ball intersects a planted sticky laser
- **THEN** the ball is processed for split or removal and the sticky laser is removed

#### Scenario: Unlimited sticky fire with map cap
- **WHEN** sticky mode is active and the player fires repeatedly
- **THEN** shots are not blocked by the harpoon/drill laser cap, and at most three sticky lasers remain on the map (oldest culled)

### Requirement: DRILL weapon behavior
While DRILL mode is active, a fired laser SHALL pass through balls along its vertical path, resolving each ball it intersects, until blocked by a barrier, closed door, or the ceiling.

#### Scenario: Drill pierces multiple balls
- **WHEN** a drill laser's path intersects two balls with no barrier between them
- **THEN** both balls are processed for split or removal

#### Scenario: Drill stopped by barrier
- **WHEN** a drill laser reaches a barrier or closed door
- **THEN** it does not affect balls beyond that solid

### Requirement: Per-player bullet cap
Each player SHALL have their own active-bullet cap (default 2 each) in co-op.

#### Scenario: P1 at cap does not block P2
- **WHEN** player 1 has reached their bullet cap and player 2 has not
- **THEN** player 2 can still fire
