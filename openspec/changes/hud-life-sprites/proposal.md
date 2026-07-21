## Why

O HUD de vidas ainda é texto neon (`Lives: N`), apesar de já existirem sprites em `sprites/Life/`. Trocar para ícones melhora legibilidade e alinha o UI ao visual cyberpunk sem mexer em mecânicas.

## What Changes

- Substituir (ou complementar) o label de texto de vidas por sprites de coração/vida já no repo (`Heart.png`, `life*.png`)
- Mostrar um ícone por vida restante (ou barra equivalente clara) durante `playing`
- Manter contraste legível sobre o fundo cyberpunk
- **Não inclui:** menu, níveis, áudio, 2P, mudança de regras de vidas

## Capabilities

### New Capabilities

- `life-hud-sprites`: Renderização das vidas com sprites Life/Heart

### Modified Capabilities

- `hud-feedback`: O requisito de display de vidas passa a exigir representação por sprites (não só texto)

## Impact

- Código: `Scripts/main.py` (`_draw_hud`), possível helper em `assets.py` / `consts.py`
- Assets: `sprites/Life/*` (já presentes, passar a ser usados)
- Dependências: nenhuma nova; independente das outras expansion changes
