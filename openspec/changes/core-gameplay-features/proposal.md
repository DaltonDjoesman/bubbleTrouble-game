## Why

O protótipo atual só mostra bolas a saltar e um player a mover-se — falta o loop jogável (atirar, estourar, perder/ganhar). Antes de níveis ou polish visual, precisamos de uma fundação estável e das mecânicas core para o jogo ser jogável de ponta a ponta numa única arena. Após o primeiro apply, o loader do Cyborg trata strips inteiras como um frame (vários personagens no ecrã) e o tiro é um projétil pontual demasiado pequeno — o combate deve alinhar-se ao laser vertical clássico.

## What Changes

- Estabilizar o runtime: `pygame.init()`, paths a partir da raiz do projeto, um único entry point (`Scripts/main.py`), limpar scripts experimentais ou marcá-los como legacy
- Corrigir fundação do player com o pack cyberpunk: **cortar frames** das strips Craftpix (célula 48×48), scale, idle vs run, facing — um único personagem no ecrã
- Disparo = **laser vertical estilo clássico** (não projétil pontual): cresce/sobe a partir do player, permanece activo até colidir com uma bola ou atingir o topo do ecrã; limite de lasers activos simultâneos
- Colisão laser ↔ bola: bola destruída ou dividida em bolas menores; bola mínima some; o laser que acertou é removido
- Colisão player ↔ bola: perda de vida / game over
- Vitória ao limpar todas as bolas da arena (sem sistema de níveis ainda)
- Vidas simples + estados win / game over com restart básico
- **Não inclui:** níveis, menus elaborados, score/timer avançados, plataformas, power-ups; polish visual fino da arma/HUD (fica para `game-visual-design`)

## Capabilities

### New Capabilities

- `game-runtime`: Inicialização, entry point único, constantes/paths, loop e grupos de sprites
- `player-controls`: Movimento A/D, facing, animação idle/run mínima (frames cortados da strip), disparo
- `projectile-combat`: Laser vertical persistente (crescimento para cima), limite de lasers activos, representação visual mínima (sprite Craftpix escalado ou segmento alongado)
- `ball-system`: Física de quique/gravidade, tamanhos, split ao ser atingido
- `match-rules`: Vidas, hit player–bola, vitória ao limpar bolas, game over e restart

### Modified Capabilities

- (nenhuma — ainda não existem specs em `openspec/specs/`)

## Impact

- Código: `Scripts/main.py`, `player.py`, `bolinha.py`, `consts.py`; módulo de tiro (`bullet.py` / laser); possível remoção/arquivo de `boubble_trouble.py` / `teste.py`
- Assets: personagem em `sprites/.../1 Characters/3 Cyborg/` (strips Idle/Run); bullets/laser em `sprites/.../5 Bullets/` (escala/alongamento para leitura; polish fino na change visual)
- Deps: `pygame` em `requirements.txt`
- Dependência de ordem: esta change é pré-requisito lógico de `game-visual-design` e alimenta o conteúdo de `game-documentation`
- Delta pós-apply: reabrir tarefas de player (corte de sheet) e combat (laser) e reaplicar no código
