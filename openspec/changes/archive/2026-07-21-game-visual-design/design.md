## Context

Após (ou em paralelo cuidadoso com) as mecânicas core, o jogo precisa de identidade cyberpunk usando o pack Craftpix já presente. Knight e fundo preto não representam a direção acordada. Esta change não inventa mecânicas — só apresentação, pipeline de assets e HUD.

## Goals / Non-Goals

**Goals:**
- Player, tiros e arena com look cyberpunk coerente
- Sprites escalados e hitboxes alinhadas
- HUD mínimo legível (vidas, win/lose)
- Fundo/atmosfera (gradiente, tile ou imagem simples do pack/promo se existir)

**Non-Goals:**
- Novas regras de jogo, níveis, power-ups
- Soundtrack completa / voice
- Substituir física ou lógica de split

## Decisions

1. **Personagem canónico: Cyborg** (`1 Characters/3 Cyborg/`) — Idle, Run, Jump, Sitdown. Se faltar frame de “shoot”, usar Idle/Run + efeito de `4 Shoot_effects` no momento do disparo.

2. **Arma visual**  
   Opcional no MVP visual: overlay de gun de `2 Guns` alinhado ao player, ou só bullet + muzzle flash. Preferir **bullet + shoot effect** primeiro; gun overlay se o tempo permitir.

3. **Asset loader**  
   Módulo `assets.py` (ou helpers em consts): paths absolutos a partir da raiz; cache de surfaces; escala única documentada (ex. 2×).

4. **Bolas**  
   Manter `bola branca.png` com tint/colorização por tamanho, ou círculos pygame estilizados se a bola destoar demais do tema.

5. **HUD**  
   Texto pygame simples (vidas no canto); ecrãs win/lose centrados. Fonte do pack (`Font.txt` / assets associados) se for fácil; senão SysFont temporário.

6. **Knight**  
   Deixar em `Assests/` sem uso no runtime; não apagar nesta change (pode documentar-se como unused).

## Risks / Trade-offs

| Risco | Mitigação |
|-------|-----------|
| Frames cyberpunk inconsistentes em tamanho | Normalizar escala no loader |
| Acoplar visual à mecânica a meio | Interfaces estáveis: `Player.image/rect`, `Bullet.image` |
| Scope creep em partículas | Limitar a 1 shoot effect + 1 hit flash |

## Migration Plan

1. Introduzir loader + trocar consts para Cyborg/bullets  
2. Fundo + paleta  
3. HUD  
4. Shoot effects / polish leve  
5. Pass visual de win/lose

## Open Questions

- Usar Biker/Punk como skin selecionável? **Não no MVP** — só Cyborg  
- Sons? **Opcional** se houver ficheiros free; senão defer
