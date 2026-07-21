## Why

Com as mecânicas core a chegar (tiros, bolas, win/lose), o jogo ainda parece um protótipo: fundo preto, sprites Knight inconsistentes, sem HUD nem identidade visual. O pack Craftpix cyberpunk já está no repo e foi escolhido como direção estética — falta aplicá-lo de ponta a ponta.

## What Changes

- Migrar/apresentar o player com personagens cyberpunk (`1 Characters`: Biker / Punk / Cyborg — escolha default a fixar no design)
- Integrar visualmente armas/mãos/efeitos de disparo do pack (`2 Guns`, `3 Hands`, `4 Shoot_effects`) quando fizer sentido sem bloquear a mecânica
- Pipeline de sprites consistente: escala, hitbox alinhada ao visual, flip de facing
- Arena/fundo com atmosfera cyberpunk (não fundo preto plano)
- HUD mínimo: vidas e feedback de win/game over legível
- Coerência visual das bolas com o tema (recolor / substituto se a bola branca destoar)
- **Não inclui:** novas mecânicas de gameplay, níveis, áudio completo (SFX opcional leve se couber sem atrapalhar)

## Capabilities

### New Capabilities

- `cyberpunk-presentation`: Tema visual, personagem, armas/efeitos, fundo da arena
- `sprite-pipeline`: Carregamento, corte, escala e hitboxes consistentes para sheets/frames do pack
- `hud-feedback`: Vidas, mensagens win/lose, feedback visual de hit/disparo

### Modified Capabilities

- (nenhuma ainda em `openspec/specs/`; após arquivar `core-gameplay-features`, eventuais deltas em `player-controls` / `projectile-combat` ficam para sync futuro se o visual alterar requisitos)

## Impact

- Código: `player.py`, `consts.py`, `main.py`, possível `ui.py` / `assets.py`
- Assets: pack sob `sprites/craftpix-net-730561-free-guns-for-cyberpunk-characters-pixel-art/`; Knight em `Assests/` deixa de ser o visual principal
- Ordem: aplicar **depois** (ou em paralelo cuidadoso) de `core-gameplay-features`, para não misturar refactor visual com mecânica incompleta
- Licença: respeitar `License.txt` do pack Craftpix na documentação
