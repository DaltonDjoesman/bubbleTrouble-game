## Context

README, `docs/gameplay.md`, `requirements.txt` e `CREDITS.md` já existem, mas o texto ainda cobre só a campanha classic. O produto shipped inclui co-op, Survival, High Scores, spikes no teto, painel HUD de baixo e menus cyberpunk (`openspec/specs/` é a fonte de verdade das regras). Ver proposal.md — Why.

## Goals / Non-Goals

**Goals:**
- README + notas descrevem o jogo shipped, não um slice antigo
- Prints e um GIF mostram a janela inteira
- Um leitor consegue instalar, correr e perceber as regras sem abrir código

**Non-Goals:**
- Alterar gameplay, UI ou resolução
- Documentação de API / tutoriais pygame
- Traduzir para vários idiomas (inglês, alinhado à UI)
- Capturas com chrome do desktop ou crop da arena

## Decisions

1. **Idioma inglês** — UI, README atual e `docs/gameplay.md` já estão em inglês (change `cyberpunk-menu-redesign`). Docs em PT divergiriam do produto. Alternativa rejeitada: rebasear tudo para PT.

2. **Split README vs gameplay** — README: o que é, install/run, controlos, pastas, créditos, media, link para notas. `docs/gameplay.md`: regras alinhadas a `openspec/specs/` (campanha, Survival, co-op, combate, arena, HUD). Alternativa rejeitada: um único README longo.

3. **Fonte das regras** — copiar o comportamento shipped das main specs (`match-rules`, `survival-mode`, `high-scores`, `ceiling-hazards`, `hud-feedback`, `main-menu`, `powerups`, `local-coop`, `player-controls`, `level-system`). Não reintroduzir vidas, jump ou plataformas.

4. **Media em `docs/screens/`**
   - `menu.png` — menu principal
   - `campaign.png` — campanha a correr
   - `survival.png` — Survival a correr
   - `high-scores.png` — vista High Scores
   - `play.gif` — loop curto de campanha
   README embute os cinco. Alternativa rejeitada: só um hero shot.

5. **Captura = framebuffer pygame 800×600** — gravar a superfície de display (`SCREEN_WIDTH` × `SCREEN_HEIGHT`), não um print do gestor de janelas. Assim cada PNG/GIF contém a tela inteira (arena + painel de baixo, ou shell de menu), sem crop. GIF: alguns segundos de play in-match à resolução nativa.

6. **Sem helper de captura no jogo** — capturar na sessão de apply (jogo a correr + save da surface / gravação de frames). Não adicionar modo screenshot permanente ao runtime.

## Risks / Trade-offs

| Risco | Mitigação |
|-------|-----------|
| Docs desatualizadas vs código | Secção de overview no README + apontar a `openspec/specs/` e `openspec/changes/` |
| Print cortado à arena (some o HUD) | Spec + checklist: dimensões 800×600; campanha/Survival mostram o painel de baixo |
| GIF pesado | Loop curto, resolução nativa, um ficheiro só |

## Migration Plan

1. Reescrever README e `docs/gameplay.md` ao produto shipped
2. Capturar os quatro PNGs + `play.gif` a 800×600 e gravar em `docs/screens/`
3. Embutir media no README; confirmar que nenhum media de jogo está cropped
4. Review: um leitor novo instala, corre e percebe campanha vs Survival vs High Scores
