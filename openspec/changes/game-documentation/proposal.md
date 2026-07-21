## Why

O projeto não tem README, deps pinadas nem notas de como se joga. Sem documentação, é difícil correr o jogo, onboarding e alinhar o que é “core” vs ideias futuras — especialmente com três streams de trabalho (features, visual, docs).

## What Changes

- Criar `README.md` com: o que é o jogo, requisitos, instalação, como correr, controlos
- Adicionar `requirements.txt` (pygame pinado ou range claro) se ainda não existir após features
- Documentar estrutura de pastas (`Scripts/`, `sprites/`, `Assests/`, `openspec/`)
- Escrever **notas de gameplay**: loop, tiros (não arpão), split de bolas, vidas, win/lose, o que está fora de scope (níveis, etc.)
- Referenciar assets Craftpix e licença; apontar para as changes OpenSpec ativas
- **Não inclui:** implementar código de jogo (só docs); wiki externa; manuais longos

## Capabilities

### New Capabilities

- `project-readme`: Documentação de instalação, execução, estrutura e controlos
- `gameplay-notes`: Regras e intenções de design jogável (MVP sem níveis)

### Modified Capabilities

- (nenhuma)

## Impact

- Ficheiros novos/alterados: `README.md`, `requirements.txt`, eventual `docs/gameplay.md`
- Depende do conteúdo acordado em `core-gameplay-features` e `game-visual-design` (docs devem refletir tiros cyberpunk + arena sem níveis)
- Ideal aplicar **depois** das outras duas estarem estáveis o suficiente para não documentar comportamento obsoleto; pode começar em rascunho cedo e atualizar no fim
