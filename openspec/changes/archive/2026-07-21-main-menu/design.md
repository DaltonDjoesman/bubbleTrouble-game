## Context

`Game` só conhece `playing` / `won` / `game_over` e arranca em match. Expansion precisa de menu com Play, Quit, 1P/2P e level select, mais ganchos para volume.

## Goals / Non-Goals

**Goals:**
- Estado `menu` no boot
- Navegação teclado (setas/WASD + Enter, Esc volta)
- Play inicia match com mode + level escolhidos
- Quit fecha o jogo
- Estrutura pronta para volume (UI placeholder ou secção Settings)

**Non-Goals:**
- Implementar 2º player ou 5 níveis completos nesta change
- Mouse-only UI obrigatório
- Online

## Decisions

1. **Estados da app:** `menu` | `playing` | `won` | `game_over` (e opcional `settings` embutido no menu).
2. **Menu fields:**  
   - Mode: `1P` | `2P` (2P guardado em `Game.mode`; se coop ainda não existir, Play em 2P pode mostrar aviso ou correr 1P com flag — preferir **guardar escolha e iniciar; P2 inerte até local-coop**, ou desabilitar Start em 2P com label “Soon”. **Decisão: permitir selecionar 2P; ao Play, se coop não implementado, fallback 1P + mensagem curta. Após local-coop, 2P real.**  
   - Level: índice 1..N (N=1 até level-pack).
3. **Pós-match:** R = retry mesmo nível/mode; M ou Esc = menu.
4. **Módulo:** `menu.py` com draw/update/input; `Game` delega.
5. **Visual:** texto/neon coerente com tema; sem novo art pack obrigatório.

## Risks / Trade-offs

| Risco | Mitigação |
|-------|-----------|
| Acoplar cedo a levels/coop | Menu guarda `selected_mode`, `selected_level`; loaders no-op safe |
| Scope settings | Volume real na change audio; aqui só slot/secção “Audio” se fácil |

## Migration Plan

1. Introduzir estado menu + loop branch  
2. UI Play/Quit/mode/level  
3. Play → `reset_match()` com params  
4. End screens → menu path  

## Open Questions

- Resolvido: teclado-first. Mouse click nice-to-have.
