## Context

HUD de vidas é texto. Sprites `sprites/Life/` (Heart, life1–6) já estão no repo e não são usados. Change pequena e isolada.

## Goals / Non-Goals

**Goals:**
- Vidas representadas por ícones sprite
- Visual claro com 0–3 (ou DEFAULT_LIVES) ícones

**Non-Goals:**
- Animação elaborada de perda de vida (flash curto ok)
- Potions/Stars HUD
- Menu/áudio

## Decisions

1. **Representação:** N ícones cheios = N vidas; ao perder vida, remove-se um ícone (ou troca para empty se houver asset — senão simplesmente deixa de desenhar).
2. **Asset default:** `Heart.png` / `Heart1.png` ou `life.png`–`lifeN` — preferir **Heart** para “vida restante”; escalar via `assets.load` existente.
3. **Posição:** canto superior esquerdo (onde está o texto hoje); remover o label `Lives: N` ou mantê-lo só em debug off.
4. **Sem mudar** `DEFAULT_LIVES` nem regras de hit.

## Risks / Trade-offs

| Risco | Mitigação |
|-------|-----------|
| Ícones grandes demais | Scale documentado (ex. 0.5×) |
| Pouco contraste | Outline/shadow atrás dos hearts |

## Migration Plan

1. Load heart sprite in consts/assets  
2. Replace `_draw_hud` lives text with icon row  
3. Manual check at 3/2/1/0 lives
