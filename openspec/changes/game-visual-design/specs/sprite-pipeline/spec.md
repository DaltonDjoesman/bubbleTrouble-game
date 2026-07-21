## ADDED Requirements

### Requirement: Consistent load and scale
Asset loading SHALL apply a documented scale and produce surfaces whose rects match the visible sprite bounds used for gameplay.

#### Scenario: Rect matches image
- **WHEN** a player or bullet sprite is created from Craftpix frames
- **THEN** its collision rect is derived from the scaled image (not an unrelated hardcoded size)

### Requirement: Frame lists for loose PNGs
The pipeline SHALL support loading ordered frame lists from folders (Idle/Run/etc.), not only grid spritesheets.

#### Scenario: Load Cyborg run frames
- **WHEN** run animation frames are requested for Cyborg
- **THEN** the loader returns the available Run frame images in a stable order
