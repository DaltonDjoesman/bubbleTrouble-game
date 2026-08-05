## Why

O menu oferece 1P/2P, mas só existe um Cyborg. Modo **co-op local** (mesmo ecrã, limpar bolas juntos) é a forma natural de multiplayer para este género.

## What Changes

- Segundo jogador no mesmo ecrã com controlos próprios (proposta: setas + Enter/Ctrl para disparar)
- Personagem distinto do pack Craftpix (ex. Biker ou Punk) para P2
- **Regras alinhadas a `classic-bubble-trouble`** (não vidas partilhadas):
  - Barreira de **tempo partilhada** (mesmo drain / mesmo `time_seconds`)
  - Hit numa bola **remove só esse jogador** do nível; o parceiro continua
  - Ao avançar de nível, **ambos respawnam**
  - Game over se **ninguém vivo** no nível **ou** tempo a 0
- Win = limpar todas as bolas do nível final (campanha multi-nível)
- Menu “2 jogadores” inicia match co-op; 1 jogador mantém classic 1P (one-hit)
- Compatível com barreiras/portas e powerups do classic
- **Não inclui:** online multiplayer, versus PvP, splitscreen, tipos especiais de bola

## Capabilities

### New Capabilities

- `local-coop`: Dois jogadores locais, input, spawn, regras co-op (morte por jogador + revive no próximo nível)

### Modified Capabilities

- `player-controls`: Suportar instâncias P1/P2 com keymaps distintos (grounded, sem jump)
- `projectile-combat`: Tiros atribuídos a cada jogador (cap por jogador); modes STICKY/DRILL partilhados ou por jogador — design
- `match-rules`: Modo co-op com tempo partilhado e morte individual
- `main-menu`: Opção 2 jogadores funcional (não stub)

## Impact

- Código: `Player` parametrizado (id, keys, sprites); `Game` gere 1–2 players; colisões player–bola por jogador; HUD de tempo (sem vidas)
- Assets: segundo character set Craftpix
- **Depende de:** `classic-bubble-trouble` aplicado (tempo, one-hit 1P, barriers/doors, powers)
- Ordem: aplicar **depois** de classic; não re-aplicar o plano antigo de vidas/plataformas
