## Why

O README e as notas de gameplay já existem, mas ainda descrevem só o slice classic da campanha. Um leitor novo não vê Survival, High Scores, spikes no teto, o painel HUD de baixo nem os menus cyberpunk, e não há prints nem GIF da janela inteira do jogo shipped.

## What Changes

- Rebasear `README.md` e `docs/gameplay.md` ao produto shipped (todas as changes OpenSpec arquivadas: classic, local co-op, layout Pang / ceiling spikes, Survival + high scores, menu cyberpunk, áudio, chain harpoon)
- Capturar e embutir screenshots da janela inteira mais um GIF da janela inteira
- Regra permanente: cada screenshot e GIF do jogo MUST mostrar a janela pygame completa (800×600), incluindo HUD/menus — nunca cortar só à arena
- Manter `requirements.txt`, mapa de pastas e créditos de assets
- **Não inclui:** alterações de gameplay/código; wiki; docs em vários idiomas

## Capabilities

### New Capabilities

- `project-readme`: Instalação, execução, estrutura, controlos, créditos e media full-window no README da raiz
- `gameplay-notes`: Regras shipped (campanha, Survival, co-op, spikes, HUD, menu/high scores)

### Modified Capabilities

- (nenhuma)

## Impact

- `README.md`, `docs/gameplay.md`, `docs/screens/` (PNGs de menu, campanha, Survival e High Scores + um GIF de play)
- `requirements.txt` e `CREDITS.md` continuam as fontes de install/créditos
- Sem mudanças no match loop nem no código de gameplay
