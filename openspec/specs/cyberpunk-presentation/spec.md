## Purpose

Cyberpunk visual identity for the player, arena, and projectile feedback using the Craftpix asset pack.

## Requirements

### Requirement: Cyberpunk player presentation
The player SHALL be rendered using the Craftpix Cyborg character frames as the default look.

#### Scenario: Cyborg on screen
- **WHEN** a match is playing
- **THEN** the player sprite is sourced from the Cyborg asset set (not the Knight sheets)

### Requirement: Themed arena background
The play field SHALL not be a flat black fill; it SHALL use a cyberpunk-appropriate background treatment.

#### Scenario: Non-plain background
- **WHEN** the game draws a playing frame
- **THEN** the background presents a gradient, pattern, or image consistent with the cyberpunk theme

### Requirement: Bullet and muzzle feedback
Shots SHALL use Craftpix bullet art and SHOULD show a brief shoot effect when firing.

#### Scenario: Bullet art
- **WHEN** a bullet is visible
- **THEN** it uses a sprite from the Craftpix bullets folder
