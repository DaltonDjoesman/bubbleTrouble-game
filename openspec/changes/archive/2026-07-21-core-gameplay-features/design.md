## Context

Protótipo pygame com `Game`, `Player` e `Ball`, já com um primeiro apply de mecânicas core. Problemas observados: as strips Craftpix Cyborg (ex. Idle 192×48 = 4 frames de 48×48) são carregadas inteiras (vários personagens no ecrã); o tiro é um projétil pontual minúsculo (bullet ~3×3), longe do laser vertical clássico. Personagem cyberpunk e **sem níveis** mantêm-se. Fundação (init, paths, limpeza) já feita; este update corrige loader + modelo de disparo.

## Goals / Non-Goals

**Goals:**
- Um loop jogável numa arena: mover, disparar laser, estourar/dividir bolas, perder vidas, ganhar ao limpar
- Runtime fiável (init, paths, um entry point)
- Player com **um** sprite Cyborg correcto (frames cortados da strip) e lasers legíveis o suficiente para jogar (polish fino em `game-visual-design`)

**Non-Goals:**
- Sistema de níveis / progressão
- Menus elaborados, score/timer de leaderboard
- Áudio, partículas avançadas, polish de HUD / overlay de arma
- Manter Knight como personagem principal
- Projéteis pontuais “bullet hell” como modelo de combate

## Decisions

1. **Arma = laser vertical (estilo clássico)**  
   Space cria um laser ancorado na posição X do disparo que **cresce para cima** cada frame. Permanece activo até colidir com uma bola ou o topo do ecrã, depois é removido. Vários lasers activos permitidos com **limite** (default **2**) para manter desafio. Substitui a decisão anterior de “tiros pontuais, não arpão”.

2. **Representação do laser (MVP)**  
   Usar um PNG de `sprites/.../5 Bullets/` **escalado/alongado** num rect vertical (ou tile/stretch do sprite ao longo da altura actual do laser). Hitbox = `rect` do laser. Gun overlay e shoot effects ficam para `game-visual-design`.

3. **Personagem default + corte de strip**  
   Cyborg. Ficheiros Idle/Run são **strips horizontais**; o loader corta células de **48×48** (Idle: 4 frames/ficheiro; Run: 6 frames/ficheiro), depois scale (`PLAYER_SCALE`), depois `rect = image.get_rect`. Knight deixa de ser referenciado em `consts`.

4. **Split de bolas**  
   Níveis de tamanho (L → M → S). Hit em L/M spawna 2 bolas menores com `vel_x` opostas; S remove. Bounce no chão com impulsão proporcional ao tamanho.

5. **Match rules**  
   3 vidas. Player–bola: −1 vida, i-frames curtos ou reset posições. 0 vidas → game over. 0 bolas → win. Tecla R para restart no ecrã final.

6. **Arquitetura**  
   Sprite groups: `player` (GroupSingle), `bolas`, `bullets` (grupo de lasers activos; nome do grupo pode manter-se). Módulo `bullet.py` (ou equivalente) modela o laser. `Game` orquestra colisões e estados (`playing` / `won` / `game_over`). Paths via `pathlib` relativos à raiz do repo.

7. **Legacy**  
   `boubble_trouble.py` e `teste.py` em `Scripts/legacy/` (já feito).

## Risks / Trade-offs

| Risco | Mitigação |
|-------|-----------|
| Hitbox do player desalinhada / strip inteira | Cortar 48×48 → blit → scale; rect = frame cortado |
| Laser largo demais = trivial | Hitbox estreita + limite de 2 lasers activos |
| Strips multi-frame mal documentadas no pack | Assumir célula 48×48; validar com Idle 192×48 e Run 288×48 |
| Visual “cru” do laser (stretch) | Aceitável no MVP; `game-visual-design` trata apresentação |
| Docs desatualizadas se features mudarem | `game-documentation` aplica por último |

## Migration Plan

1. Runtime + consts/paths + entry (já feito)  
2. **Fix** loader Cyborg: slice 48×48 + idle/run/flip  
3. **Substituir** projétil pontual por laser que cresce; colisão + split  
4. Vidas + win/lose + restart (já feito; revalidar)  
5. Smoke test: um personagem, laser legível, split, die, win, restart

## Open Questions

- Limite de lasers simultâneos: **2** (fechado)
- Tecla de disparo: **SPACE** (fechado)
- Direção: só vertical para cima (fechado)
- Velocidade de crescimento do laser (px/frame): a fixar no apply (ex. ~8–12)
