## Why

Não há áudio. SFX + música de fundo aumentam feedback e atmosfera; o menu deve permitir controlar o volume de **música** e de **efeitos** em separado. Ainda não existem ficheiros de áudio no repo — esta change inclui obtê-los (assets free/CC) e integrá-los.

## What Changes

- Adicionar pasta de áudio (ex. `audio/` ou `Assests/audio/`) com música de fundo + SFX (tiro, pop/split, hit, win, game over, UI click)
- Música em loop durante menu e/ou match; SFX nos eventos de gameplay/UI
- No menu: controlos de volume para **música** e **efeitos** (sliders ou steps), com persistência simples (ex. ficheiro local ou defaults em consts)
- Mute/respeitar volumes 0
- Documentar créditos/licenças dos ficheiros de áudio
- **Não inclui:** voice acting, equalizer avançado, níveis novos, 2P

## Capabilities

### New Capabilities

- `game-audio`: Reprodução de música e SFX via pygame.mixer
- `audio-settings`: Volumes separados música/SFX no menu + persistência

### Modified Capabilities

- `main-menu`: Secção/opções de volume no menu
- `hud-feedback` / match flow: eventos disparam SFX (win/lose/hit) — requisito de áudio, não visual

## Impact

- Código: `audio.py`, hooks em `Game`/`menu`, deps pygame.mixer
- Assets: novos ficheiros de áudio (Kenney / OpenGameArt / similares, licença permissiva)
- Ordem: após `main-menu` (UI de volume)
- Sistema: mixer init no bootstrap
