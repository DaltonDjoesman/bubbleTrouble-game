## Why

O jogo arranca direto na partida. Para níveis, modo 1P/2P e opções de áudio, é preciso um menu inicial e uma máquina de estados de ecrã clara (menu → jogo → fim).

## What Changes

- Ecrã de menu principal ao arrancar (em vez de match imediato)
- Opções: **Play**, **Quit**, escolha **1 jogador / 2 jogadores**, e **seleção de nível**
- Fluxo de estados: `menu` → `playing` → `won` / `game_over` → voltar ao menu ou retry
- Hooks para volume (preenchidos pela change `audio-and-volume`) e para 2P (ativado por `local-coop`)
- Enquanto 2P ou níveis extra ainda não existirem: UI presente; 2P pode mostrar “em breve” ou iniciar 1P até `local-coop`; níveis listam o que `level-pack` definir (mínimo nível 1)
- **Não inclui:** implementar física de plataformas, SFX/música, segundo jogador jogável, tipos especiais de bola

## Capabilities

### New Capabilities

- `main-menu`: Ecrã inicial, navegação, Play/Quit, mode select, level select
- `app-flow`: Estados de aplicação (menu / playing / end) e transições

### Modified Capabilities

- `game-runtime`: O bootstrap passa a abrir no menu, não direto em match
- `match-rules`: Após win/game over, deve ser possível regressar ao menu (além de restart in-place se mantido)

## Impact

- Código: `Scripts/main.py` (refactor de estados), possível `menu.py`
- Depende logicamente: base para `level-pack`, `audio-and-volume`, `local-coop`
- Docs: controlos de menu a refletir depois em `game-documentation`
