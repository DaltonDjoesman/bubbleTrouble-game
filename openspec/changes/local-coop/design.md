## Context

Menu terá 1P/2P; só existe um player. Co-op local same-screen: partilhar arena e limpar bolas juntos.

## Goals / Non-Goals

**Goals:**
- P2 jogável com keymap e sprite distintos
- Mode do menu inicia 1 ou 2 players
- Win/lose co-op claros
- Funciona com níveis/plataformas existentes

**Non-Goals:**
- Online, versus, splitscreen, pad obrigatório (teclado first; pad nice-to-have)

## Decisions

1. **P1:** A/D + Space (Cyborg). **P2:** Left/Right arrows + Return (ou RCTRL) — Biker ou Punk.
2. **Vidas partilhadas** (um pool): qualquer player hit gasta vida; i-frames global ou por player — **i-frames só no player atingido**.
3. **Bullet cap:** **por jogador** (ex. 2 cada) para fairness.
4. **Spawn:** P1 esquerda-centro, P2 direita-centro do chão (ou lados opostos).
5. **Game over:** vidas 0; **Win:** 0 bolas (igual).
6. **1P:** não instancia P2 (performance/clarity).

## Risks / Trade-offs

| Risco | Mitigação |
|-------|-----------|
| Ecrã cheio / friendly fire N/A | Só bolas fazem dano |
| Teclado AZERTY/layout | Documentar keys no menu/docs |
| Refactor Player | Constructor (control_scheme, sprite_set, player_id) |

## Migration Plan

1. Parametrize Player  
2. Game spawns 1–2 from mode  
3. Collisions/HUD (vidas partilhadas; opcional indicador P1/P2)  
4. Menu 2P path  
5. Playtest em nível com plataformas  

## Open Questions

- Dual lives bars? **Não** — um row de hearts basta no co-op v1
