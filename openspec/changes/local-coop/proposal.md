## Why

O menu vai oferecer 1P/2P, mas só existe um Cyborg. Modo **co-op local** (mesmo ecrã, limpar bolas juntos) é a forma natural de multiplayer para este género e diferencia o projeto.

## What Changes

- Segundo jogador no mesmo ecrã com controlos próprios (proposta: setas + Enter/Ctrl para disparar)
- Personagem distinto do pack Craftpix (ex. Biker ou Punk) para P2
- Vidas: partilhadas **ou** por jogador — decisão no design (proposta default: **vidas partilhadas** para simplicidade co-op)
- Win = limpar todas as bolas; game over = vidas a 0 (qualquer hit conta)
- Menu “2 jogadores” inicia match co-op; 1 jogador mantém comportamento atual
- Compatível com níveis/plataformas quando `level-pack` existir
- **Não inclui:** online multiplayer, versus PvP, splitscreen, tipos especiais de bola

## Capabilities

### New Capabilities

- `local-coop`: Dois jogadores locais, input, spawn, regras co-op

### Modified Capabilities

- `player-controls`: Suportar instâncias P1/P2 com keymaps distintos
- `projectile-combat`: Tiros atribuídos a cada jogador (cap por jogador ou global — design)
- `match-rules`: Modo co-op e condição de derrota/vitória partilhada
- `main-menu`: Opção 2 jogadores funcional (não stub)

## Impact

- Código: `Player` parametrizado (id, keys, sprites); `Game` gere 1–2 players; colisões player–bola para ambos
- Assets: segundo character set Craftpix
- Ordem: preferir após `main-menu` e idealmente após `level-pack` para testar co-op nos níveis
