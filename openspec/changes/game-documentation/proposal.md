## Why

O projeto não tem README completo nem notas de como se joga alinhadas ao classic. Sem documentação, é difícil correr o jogo e perceber as regras atuais.

## What Changes

- Criar `README.md` com: o que é o jogo, requisitos, instalação, como correr, controlos
- Garantir `requirements.txt` (pygame pinado ou range claro)
- Documentar estrutura de pastas (`Scripts/`, `sprites/`, `Assests/`, `openspec/`)
- Escrever **notas de gameplay** alinhadas a **`classic-bubble-trouble`**:
  - movimento grounded (sem jump), velocidade reduzida
  - barreira de tempo (não vidas); one-hit em 1P
  - barreiras/portas (não plataformas)
  - armas: harpoon default, STICKY, DRILL; drops TIME/STICKY/DRILL
  - cinco níveis com `time_seconds`
- Referenciar assets Craftpix e licença; apontar para OpenSpec changes ativas
- **Defer writing** o README/`docs/gameplay.md` até classic estar jogável (esta change só atualiza o plano agora; escrita no apply após classic)
- **Não inclui:** implementar código de jogo (só docs); wiki externa; manuais longos

## Capabilities

### New Capabilities

- `project-readme`: Documentação de instalação, execução, estrutura e controlos
- `gameplay-notes`: Regras classic (tempo, one-hit, barriers, powers, níveis)

### Modified Capabilities

- (nenhuma)

## Impact

- Ficheiros novos/alterados: `README.md`, `requirements.txt`, `docs/gameplay.md`
- **Depende de:** `classic-bubble-trouble` playable antes da escrita final
- Co-op docs: mencionar contrato 2P quando `local-coop` existir; até lá, notar 2P stub
