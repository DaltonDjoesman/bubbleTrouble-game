## Purpose

Gameplay notes that describe the shipped campaign, Survival, co-op, combat, and arena rules so a reader can play without reading source.

## ADDED Requirements

### Requirement: Gameplay notes document
The project SHALL include gameplay notes (e.g. `docs/gameplay.md`) describing the shipped rules.

#### Scenario: Core loop documented
- **WHEN** a reader opens the gameplay notes
- **THEN** they can learn grounded movement, campaign time barrier, Survival chronometer, one-hit defeat (1P), co-op hit/revive, shooting (harpoon / STICKY / DRILL), ball split, ceiling spikes, barriers/doors, win, and game over

### Requirement: Explicit scope
Gameplay notes SHALL list current shipped features. Local co-op, Survival, High Scores, and ceiling spikes SHALL be described as current rules, not deferred work.

#### Scenario: Shipped features called out
- **WHEN** a reader checks scope in the gameplay notes
- **THEN** campaign time barrier, Survival, one-hit 1P, co-op, barriers/doors, powerups, five campaign levels, ceiling spikes, and High Scores are described as current rules

### Requirement: Alignment with classic product decisions
Gameplay notes SHALL reflect cyberpunk presentation plus classic Bubble Trouble stakes (time, grounded, powers) rather than multi-life platform gameplay.

#### Scenario: Combat and survival model stated
- **WHEN** a reader reads the combat/survival sections
- **THEN** campaign survival is the time barrier (not lives), Survival uses an elapsed chronometer, and weapons include default harpoon plus STICKY/DRILL pickups

### Requirement: Survival rules documented
Gameplay notes SHALL describe Survival as distinct from campaign: elapsed chronometer, no clear-all win, continuous ramping spawns, lose when the last living player is down, TIME pausing spawns, and qualifying-run initials into High Scores.

#### Scenario: Survival vs campaign is clear
- **WHEN** a reader reads the Survival section
- **THEN** they can tell Survival does not drain a time barrier, does not win by clearing balls, and records elapsed time on High Scores

### Requirement: Ceiling spikes documented
Gameplay notes SHALL describe the spiked ceiling hazard: balls that touch it split or are destroyed using the same size-tier rules as a weapon hit.

#### Scenario: Roof hazard stated
- **WHEN** a reader reads the arena/balls sections
- **THEN** they learn that ceiling spikes pop balls on contact

### Requirement: Menu and High Scores documented
Gameplay notes (or the README they link from) SHALL mention the main-menu flow: Play, 1P/2P mode, campaign and Survival select, High Scores (1P/2P boards), and Options/audio.

#### Scenario: High Scores mentioned
- **WHEN** a reader looks for how Survival times are viewed
- **THEN** they find that High Scores shows separate 1P and 2P boards
