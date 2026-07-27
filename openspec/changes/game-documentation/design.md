## Context

Repo precisa de README e notas de gameplay. O comportamento canónico é o de **`classic-bubble-trouble`**: grounded, time barrier, one-hit 1P, barriers/doors, powerups, five levels.

**Defer:** não escrever README/gameplay nesta fase de planeamento rebase — aplicar docs **depois** do classic estar jogável para não documentar regras obsoletas (vidas/plataformas/jump).

## Goals / Non-Goals

**Goals:**
- Qualquer pessoa consegue instalar e correr o jogo
- Notas descrevem regras classic e o que vem depois (co-op)
- Licença/créditos dos assets visíveis

**Non-Goals:**
- Documentação de API estilo Sphinx
- Tutoriais pygame genéricos
- Traduzir para múltiplos idiomas (PT é suficiente; EN opcional no README curto)

## Decisions

1. **README.md na raiz** — quickstart + controlos + estrutura + link para notas  
2. **docs/gameplay.md** — regras: grounded move, shoot (harpoon/STICKY/DRILL), split, time barrier, one-hit, barriers/doors, levels, powerups  
3. **requirements.txt** — `pygame>=2.5` (ou pin da versão testada)  
4. **Ordem de escrita** — **após** classic apply; sync de novo após `local-coop` se necessário  
5. **Idioma** — Português (alinhado ao projeto pessoal)

## Risks / Trade-offs

| Risco | Mitigação |
|-------|-----------|
| Docs desatualizadas vs código | Secção “Estado atual” + openspec/changes |
| Documentar vidas/plataformas por engano | Checklist: tempo, one-hit, barriers, powers |

## Migration Plan

1. Esperar classic playable  
2. `requirements.txt` + README instalar/correr  
3. `docs/gameplay.md` com regras classic  
4. Créditos Craftpix + estrutura  
5. Pass final após local-coop se já aplicado  

## Open Questions

- Incluir changelog? **Não** nesta change — commits bastam
