## Purpose

Solid arena geometry: vertical barriers and doors that interact with balls and lasers (crawl gaps for the player).

## Requirements

### Requirement: Barriers
Barriers SHALL be static solid vertical (or block) geometry. Balls bounce on contact. Lasers that hit a barrier SHALL despawn (or stop growth) and SHALL NOT pass through. Barriers intended as lanes SHALL leave a floor crawl gap so the player can move underneath.

#### Scenario: Ball blocked by barrier
- **WHEN** a ball collides with a barrier
- **THEN** the ball bounces and does not pass through

#### Scenario: Laser blocked by barrier
- **WHEN** a laser collides with a barrier
- **THEN** the laser does not continue through the barrier

### Requirement: Doors
Doors SHALL behave as solid barriers while closed and non-solid while open. Each door SHALL use an authored mode: timed open/close cycle, and/or open when its lane is clear of balls.

#### Scenario: Timed door closes
- **WHEN** a timed door's closed phase is active
- **THEN** balls and lasers treat it as solid

#### Scenario: Lane-clear door opens
- **WHEN** a lane-clear door's lane has no remaining balls
- **THEN** the door is open (non-solid)
