## Purpose

Shared cyberpunk visual chrome for all non-level UI: menu shell, selection states, footer hints, and match overlays/status panel framing, based on the hybrid designPrototype tokens without arcade-cabinet hardware chrome.

## ADDED Requirements

### Requirement: Shared neon UI tokens
Non-level UI SHALL use a consistent cyberpunk token set: dark screen/surface backgrounds, neon cyan primary brand, neon magenta secondary accent, neon gold for selection/focus, and muted text for idle labels.

#### Scenario: Tokens visible on menu
- **WHEN** the main menu root screen is shown
- **THEN** branding uses neon cyan (and magenta subtitle treatment where a subtitle is present) on a dark cyberpunk surface, not flat unthemed gray panels alone

#### Scenario: Gold selection
- **WHEN** a menu item or tab is highlighted
- **THEN** its selection treatment uses neon gold rather than an unrelated default highlight color

### Requirement: Menu shell layout
Menu screens SHALL present a three-band shell: header brand region, central content well, and footer band for control hints (and optional muted system line).

#### Scenario: Shell bands on root
- **WHEN** the root menu is shown
- **THEN** a header brand region, a central list/content area, and a footer hint band are all visible

### Requirement: Keyboard hint footer
Menu screens SHALL show English keyboard hints in the footer band for navigate, confirm, and back where those actions apply.

#### Scenario: Footer hints readable
- **WHEN** the player is on a menu screen that supports keyboard navigation
- **THEN** the footer shows English hints for navigation and confirm (and back when leaving a submenu)

### Requirement: No arcade cabinet chrome
The product UI SHALL NOT draw the prototype’s physical arcade cabinet chrome (side sticks, fire buttons, credit marquee bezel) as required chrome.

#### Scenario: No cabinet controls required
- **WHEN** the main menu is shown
- **THEN** the UI does not require on-screen arcade stick or fire-button widgets to operate

### Requirement: Match overlay chrome alignment
Game over, win, level-clear, and similar full-screen match messages SHALL use the same cyberpunk chrome language (dark panels, neon accents, gold emphasis where focused) as the menus.

#### Scenario: Game over themed
- **WHEN** the match enters game over
- **THEN** the message overlay uses cyberpunk panel/accent treatment consistent with the menu visual system
