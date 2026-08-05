## Context

Menu tem 1P/2P; só existe um player. Co-op local same-screen: partilhar arena e limpar bolas juntos.

**Rebase:** `classic-bubble-trouble` removeu vidas/plataformas/jump. Este change implementa contra o contrato classic: tempo partilhado, morte por jogador, revive no próximo nível.

## Goals / Non-Goals

**Goals:**
- P2 jogável com keymap e sprite distintos
- Mode do menu inicia 1 ou 2 players
- Win/lose co-op claros (tempo partilhado; morte individual)
- Funciona com níveis de barreiras/portas e powerups

**Non-Goals:**
- Online, versus, splitscreen, pad obrigatório (teclado first; pad nice-to-have)
- Reintroduzir multi-life stock ou plataformas

## Decisions

1. **P1:** A/D + Space (Cyborg). **P2:** Left/Right arrows + Return (ou RCTRL) — Biker ou Punk. Sem jump.
2. **Tempo partilhado:** uma barreira de tempo; drain global; TIME power afeta o pool partilhado.
3. **Hit:** remove só o jogador atingido do nível (sem i-frames de continue). Parceiro continua.
4. **Revive:** ao avançar de nível, ambos respawnam vivos com arma default.
5. **Game over:** nenhum jogador vivo no nível **ou** tempo a 0. **Win:** 0 bolas no nível final.
6. **Bullet cap:** **por jogador** (ex. 2 cada). Weapon mode: **por jogador** (cada um pode ter STICKY/DRILL próprio); sticky plantado não some ao mudar mode.
7. **Spawn:** P1 esquerda-centro, P2 direita-centro do chão.
8. **1P:** não instancia P2; one-hit game over (já no classic).

## Risks / Trade-offs

| Risco | Mitigação |
|-------|-----------|
| Softlock se P1 morre e bola atrás de porta | Playtest; lane-clear / crawl gaps |
| Teclado AZERTY/layout | Documentar keys no menu/docs |
| Refactor Player | Constructor (control_scheme, sprite_set, player_id) |

## Migration Plan

1. Parametrize Player (grounded)  
2. Game spawns 1–2 from mode  
3. Per-player death + shared time; HUD tempo (sem hearts)  
4. Menu 2P path real  
5. Playtest em níveis com barriers/doors  

## Open Questions

- Indicador visual “P2 down”? **Sim** — hint curto no HUD quando um está fora do nível
