## Context

Uma arena flat. Queremos 5 níveis com plataformas e obstáculos, selecionáveis no menu e com progressão ao vencer.

## Goals / Non-Goals

**Goals:**
- Data-driven levels (lista/dict ou módulos)
- 5 layouts com dificuldade crescente
- Plataformas: chão extra; player anda em cima; bolas bounce no topo
- Obstáculos: blocos sólidos que bolas/player/bullets tratam de forma definida
- Win nível 1–4 → próximo; nível 5 → won final / menu

**Non-Goals:**
- Editor visual
- Ball types especiais (futuro)
- Moving platforms (v1 estático)

## Decisions

1. **Level schema (exemplo):**
   ```
   id, name,
   balls: [{tier, x, y, vel}],
   platforms: [{x, y, w, h}],
   obstacles: [{x, y, w, h}]
   ```
2. **Plataformas:** rect solid; player usa floor collision (pé sobre topo); bolas invertem `vel_y` no topo e laterais como paredes se hit side; bullets destroem-se ou passam — **Decisão: bullets param/desaparecem ao bater obstáculo/plataforma por baixo** (como teto local).
3. **Obstáculos:** iguais a plataformas para física, visual distinto (cor/sprite); podem bloquear passagem do player.
4. **Chão da arena:** continua a ser o bottom screen; plataformas são adicionais.
5. **Progressão:** ao limpar bolas, se `level_id < 5` auto-advance após short beat ou prompt “Enter next”; no 5 mostra YOU WIN.
6. **Conteúdo sugerido:**  
   - L1: open + 1 plataforma baixa, poucas bolas  
   - L2: duas plataformas  
   - L3: corredor com obstáculos  
   - L4: plataformas altas + mais bolas L  
   - L5: layout denso (quase boss-arena sem ball types ainda)

## Risks / Trade-offs

| Risco | Mitigação |
|-------|-----------|
| Physics bugs em corners | Testes manuais por nível; AABB simples |
| Softlock (bola presa) | Evitar geometria que prenda; playtest |
| Menu sem level-pack | ids 1..5; menu lista nomes |

## Migration Plan

1. Level data + loader  
2. Collision helpers platform/obstacle  
3. Author 5 levels  
4. Wire win → next level  
5. Menu level select integration  

## Open Questions

- Timer por nível? **Não no v1**
