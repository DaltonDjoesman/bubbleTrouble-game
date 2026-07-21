## Why

O protótipo atual só mostra bolas a saltar e um player a mover-se — falta o loop jogável (atirar, estourar, perder/ganhar). Antes de níveis ou polish visual, precisamos de uma fundação estável e das mecânicas core para o jogo ser jogável de ponta a ponta numa única arena.

## What Changes

- Estabilizar o runtime: `pygame.init()`, paths a partir da raiz do projeto, um único entry point (`Scripts/main.py`), limpar scripts experimentais ou marcá-los como legacy
- Corrigir fundação do player (spritesheet cut/scale, idle vs run, facing) o suficiente para a mecânica funcionar com o pack cyberpunk
- Substituir o conceito de arpão por **tiros múltiplos** usando as sprites em `sprites/.../5 Bullets/`
- Colisão tiro ↔ bola: bola destruída ou dividida em bolas menores; bola mínima some
- Colisão player ↔ bola: perda de vida / game over
- Vitória ao limpar todas as bolas da arena (sem sistema de níveis ainda)
- Vidas simples + estados win / game over com restart básico
- **Não inclui:** níveis, menus elaborados, score/timer avançados, plataformas, power-ups

## Capabilities

### New Capabilities

- `game-runtime`: Inicialização, entry point único, constantes/paths, loop e grupos de sprites
- `player-controls`: Movimento A/D, facing, animação idle/run mínima, disparo
- `projectile-combat`: Tiros verticais (ou direção definida), limite de tiros ativos, sprites de bullet do pack craftpix
- `ball-system`: Física de quique/gravidade, tamanhos, split ao ser atingido
- `match-rules`: Vidas, hit player–bola, vitória ao limpar bolas, game over e restart

### Modified Capabilities

- (nenhuma — ainda não existem specs em `openspec/specs/`)

## Impact

- Código: `Scripts/main.py`, `player.py`, `bolinha.py`, `consts.py`; novo módulo de tiro (ex. `bullet.py`); possível remoção/arquivo de `boubble_trouble.py` / `teste.py`
- Assets: bullets em `sprites/craftpix-net-730561-free-guns-for-cyberpunk-characters-pixel-art/5 Bullets/`; personagem cyberpunk (migração a partir do Knight)
- Deps: declarar `pygame` em `requirements.txt` (ficheiro novo se ainda não existir nesta change ou na de documentação — mínimo necessário para correr)
- Dependência de ordem: esta change é pré-requisito lógico de `game-visual-design` e alimenta o conteúdo de `game-documentation`
