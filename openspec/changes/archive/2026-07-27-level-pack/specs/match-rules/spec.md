## REMOVED Requirements

### Requirement: No level progression in MVP
**Reason:** Replaced by multi-level progression in `level-system`.

## ADDED Requirements

### Requirement: Multi-level campaign progress
Winning a non-final level SHALL progress the run; winning the final level SHALL complete the run with the won state.

#### Scenario: Mid-campaign clear
- **WHEN** the last ball of a non-final level is destroyed
- **THEN** the match does not permanently end the campaign without offering or performing advance to the next level
