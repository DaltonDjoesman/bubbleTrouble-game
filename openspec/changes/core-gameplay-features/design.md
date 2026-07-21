## Context

Protótipo pygame (~300 LOC) com `Game`, `Player` e `Ball`. Sem tiro funcional, sem split, sem win/lose no path modular. Assets cyberpunk (personagens + bullets) já no repo. Decisão de produto: tiros múltiplos (não arpão), personagem cyberpunk, **sem níveis** nesta change. Fundação (init, paths, limpeza) entra aqui.

## Goals / Non-Goals

**Goals:**
- Um loop jogável numa arena: mover, disparar, estourar/dividir bolas, perder vidas, ganhar ao limpar
- Runtime fiável (init, paths, um entry point)
- Player e bullets usáveis com sprites cyberpunk (qualidade visual fina fica para `game-visual-design`)

**Non-Goals:**
- Sistema de níveis / progressão
- Menus elaborados, score/timer de leaderboard
- Áudio, partículas avançadas, polish de HUD
- Manter Knight como personagem principal

## Decisions

1. **Arma = tiros, não arpão**  
   Space (ou tecla definida) dispara um projétil que sobe (como o clássico, mas sem corda). Vários tiros ativos permitidos com **limite** (ex. 1–3) para manter desafio.

2. **Sprites de bullet**  
   Usar PNGs em `sprites/.../5 Bullets/` (escolher 1 estilo default, ex. `1.png` ou par `_1/_2` se for animação). Escala pequena e hitbox apertada.

3. **Personagem default**  
   Cyborg (ou Biker — fixar Cyborg como default por ter Idle/Run/Jump claros). Knight deixa de ser referenciado em `consts`.

4. **Split de bolas**  
   Níveis de tamanho (ex. L → M → S). Hit em L/M spawna 2 bolas menores com `vel_x` opostas; S remove. Bounce no chão com impulsão proporcional ao tamanho (em vez de `-13` mágico único, pelo menos parametrizado).

5. **Match rules**  
   3 vidas. Player–bola: −1 vida, i-frames curtos ou reset posições. 0 vidas → game over. 0 bolas → win. Tecla para restart no ecrã final.

6. **Arquitetura**  
   Manter sprites groups: `player` (GroupSingle), `bolas`, `bullets`. Novo `bullet.py`. `Game` orquestra colisões e estados (`playing` / `won` / `game_over`). Paths via `pathlib` relativos à raiz do repo.

7. **Legacy**  
   `boubble_trouble.py` e `teste.py`: mover para `Scripts/legacy/` ou apagar após confirmar que nada depende deles.

## Risks / Trade-offs

| Risco | Mitigação |
|-------|-----------|
| Hitbox do player desalinhada (bug atual de scale) | Corrigir cut→blit→scale; rect = image.get_rect |
| Muitos tiros = trivial | Limite de tiros ativos + cooldown leve |
| Pack cyberpunk é frames soltos, não sheet | Loader por lista de ficheiros, não só grid sheet |
| Visual “cru” após features | Aceitável; `game-visual-design` trata apresentação |
| Docs desatualizadas se features mudarem | `game-documentation` aplica por último |

## Migration Plan

1. Fix runtime + consts/paths + limpar entry  
2. Player cyberpunk mínimo (idle/run/flip) + disparo  
3. Bullet + colisão com bola + split  
4. Vidas + win/lose + restart  
5. Smoke test manual (correr `python Scripts/main.py` da raiz)

## Open Questions

- Limite exato de tiros simultâneos (proposta: **2**)
- Tecla de disparo (proposta: **SPACE**)
- Direção do tiro: só vertical para cima (clássico) vs também diagonal — **MVP: só para cima**
