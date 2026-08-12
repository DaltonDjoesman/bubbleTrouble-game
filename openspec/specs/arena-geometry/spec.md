## Purpose

Solid arena geometry: vertical barriers and doors that interact with balls and lasers (crawl gaps for the player). The playable region sits above a reserved bottom status panel.

## Requirements

### Requirement: Playable region excludes bottom panel
The playable arena SHALL occupy the window region above the reserved bottom status panel. Player floor, ball floor bounce, lateral walls for balls, barrier/door solids, and projectile ceiling checks SHALL use that playable region (not the full window height).

#### Scenario: Floor above panel
- **WHEN** the player or a ball rests on the arena floor during play
- **THEN** that floor is the bottom of the playable region above the status panel

#### Scenario: Balls stay in play width and play height
- **WHEN** a ball moves during play
- **THEN** horizontal walls are the playable left/right edges and the ball does not enter the bottom status panel as valid play space

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
