## Context

Repo sem README nem notas de gameplay. Três changes OpenSpec definem features e visual; a documentação deve espelhar as decisões: clone Bubble Trouble com **tiros cyberpunk** (não arpão), **sem níveis** no MVP, pack Craftpix.

## Goals / Non-Goals

**Goals:**
- Qualquer pessoa (incluindo o autor no futuro) consegue instalar e correr o jogo
- Notas de gameplay descrevem regras do MVP e o que vem depois
- Licença/créditos dos assets visíveis

**Non-Goals:**
- Documentação de API estilo Sphinx
- Tutoriais pygame genéricos
- Traduzir para múltiplos idiomas (PT é suficiente; EN opcional no README curto)

## Decisions

1. **README.md na raiz** — quickstart + controlos + estrutura + link para notas  
2. **docs/gameplay.md** — regras detalhadas: movimento, tiros (limite), split, vidas, win/lose, non-goals (níveis, etc.)  
3. **requirements.txt** — `pygame>=2.5` (ou pin da versão testada no ambiente)  
4. **Ordem de escrita** — rascunho cedo; revisão final depois de features (+ visual se já aplicado)  
5. **Idioma** — Português (alinhado ao projeto pessoal)

## Risks / Trade-offs

| Risco | Mitigação |
|-------|-----------|
| Docs desatualizadas vs código | Secção “Estado atual” + apontar para openspec/changes |
| Duplicar info README vs gameplay | README curto; detalhes em docs/gameplay.md |

## Migration Plan

1. `requirements.txt` + secção instalar/correr no README  
2. `docs/gameplay.md` com regras acordadas  
3. Créditos Craftpix + estrutura de pastas  
4. Pass final de sync após apply das outras changes

## Open Questions

- Incluir changelog? **Não** nesta change — commits bastam
