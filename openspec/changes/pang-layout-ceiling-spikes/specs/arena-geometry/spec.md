## ADDED Requirements

### Requirement: Playable region excludes bottom panel
The playable arena SHALL occupy the window region above the reserved bottom status panel. Player floor, ball floor bounce, lateral walls for balls, barrier/door solids, and projectile ceiling checks SHALL use that playable region (not the full window height).

#### Scenario: Floor above panel
- **WHEN** the player or a ball rests on the arena floor during play
- **THEN** that floor is the bottom of the playable region above the status panel

#### Scenario: Balls stay in play width and play height
- **WHEN** a ball moves during play
- **THEN** horizontal walls are the playable left/right edges and the ball does not enter the bottom status panel as valid play space
