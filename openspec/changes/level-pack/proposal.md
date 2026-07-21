## Why

O MVP é uma única arena. Para o jogo crescer, precisamos de ~5 níveis distintos com **plataformas e obstáculos**, escolhíveis no menu e com progressão ao limpar.

## What Changes

- Modelo de dados de nível (bolas iniciais, plataformas, obstáculos, bounds)
- **5 níveis** com layouts diferentes (dificuldade crescente)
- Plataformas sólidas: player pode ficar em cima; bolas ricocheteiam conforme regras definidas no design
- Obstáculos: bloqueiam movimento/projéteis ou alteram path (especificado no design)
- Integração com seleção de nível do menu; ao ganhar, avançar para o próximo nível ou voltar ao menu no último
- **BREAKING** (spec): remove a restrição MVP “sem progressão de níveis” em `match-rules`
- **Não inclui:** tipos especiais de bola (change futura de identidade), áudio, 2P, editor de níveis

## Capabilities

### New Capabilities

- `level-system`: Definição, carga e progressão de níveis
- `arena-geometry`: Plataformas e obstáculos com colisão

### Modified Capabilities

- `match-rules`: Permitir progressão multi-nível; win num nível não-final avança em vez de só “won forever”
- `ball-system`: Interação de bolas com plataformas/obstáculos
- `player-controls`: Player colide/anda sobre plataformas
- `main-menu` / level select: listar os 5 níveis (se menu já existir; senão esta change assume ou documenta acoplamento)

## Impact

- Código: novo `levels.py` / dados; colisões em `player.py`, `bolinha.py`, `bullet.py`; `Game` carrega nível por id
- Ordem: preferir após `main-menu`
- Conteúdo: 5 layouts authorados à mão
