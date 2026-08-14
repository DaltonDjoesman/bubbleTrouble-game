# Bubble Trouble

A cyberpunk-styled take on classic Bubble Trouble, built with Python and pygame.

Pop bouncing balls with growing chain harpoons. Play a **five-level campaign** against a draining time barrier, or **Survival** against a rising chronometer. Solo or **local co-op**, with **High Scores** and **Options** for music and SFX.

## Requirements

- Python 3.10+
- pygame 2.5+

## Install

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

From the repository root:

```bash
python Scripts/main.py
```

The game opens on the main menu (800×600). A match does not start until you confirm Play and pick a level.

## Modes

| Mode | What it is |
|------|------------|
| **Campaign** | Five authored levels. Clear every ball before the shared time barrier empties. Clearing level 5 wins. |
| **Survival** | Endless. Time counts **up**. Balls keep spawning with a difficulty ramp. Last player down ends the run. Qualifying times go to High Scores. |
| **1P / 2P** | Toggle on the menu. 2P is same-screen co-op with distinct keyboards. |
| **High Scores** | Top five Survival times, separate 1P and 2P boards (tab between them). |
| **Options** | Independent music and SFX volume (persisted locally). |

Rules in detail: [docs/gameplay.md](docs/gameplay.md).

## Screenshots

Full 800×600 window (arena plus bottom status panel, or the menu shell — not a cropped playfield).

![Main menu](docs/screens/menu.png)

![Campaign match](docs/screens/campaign.png)

![Survival match](docs/screens/survival.png)

![High Scores](docs/screens/high-scores.png)

![In-match campaign loop](docs/screens/play.gif)

## Controls

| Player | Move | Fire |
|--------|------|------|
| P1 | A / D | Space |
| P2 | Left / Right arrows | Enter |

Movement is grounded (no jump). Crawl under barriers and doors through the gap above the floor.

| Context | Keys |
|---------|------|
| Menu | W/S navigate, A/D adjust (mode or volume), Enter/Space confirm, Esc back |
| Level select | W/S (and A/D on the campaign grid), Tab switches Campaign / Survival |
| High Scores | A/D (or Left/Right) switch 1P / 2P boards |
| In match | Esc returns to the menu |
| Win / game over | R restart, M or Esc return to menu |

## Project layout

```
Scripts/     Game code (entry: Scripts/main.py)
assets/      Art — ball, Craftpix characters/guns, chain, powerups, fonts
audio/       Music and SFX (Kenney CC0)
docs/        Gameplay notes and screenshots
openspec/    Specs and change history
```

## Credits

Third-party art and audio are listed in [CREDITS.md](CREDITS.md). Character and gun sprites are from the Craftpix cyberpunk pack; see [assets/craftpix/License.txt](assets/craftpix/License.txt).
