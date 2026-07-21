## Context

Sem áudio no projeto. Utilizador quer música + SFX e volumes separados no menu; não tem ficheiros — há que obter assets free e creditar.

## Goals / Non-Goals

**Goals:**
- mixer: BGM loop + SFX one-shots
- Menu: volume Music 0–10 (ou 0–100) e SFX 0–10, independentes
- Persistência local (ex. `settings.json` na raiz ou `user_settings.json`)
- Créditos no README/docs

**Non-Goals:**
- FMOD/espacial
- Músicas diferentes por nível (uma BGM default chega; swap opcional depois)

## Decisions

1. **Obter assets:** Kenney Interface/Digital Audio, OpenGameArt, ou similares CC0/CC-BY; guardar em `audio/music/` e `audio/sfx/`.
2. **SFX mínimos:** shoot, ball_pop, player_hit, win, lose, ui_select, ui_confirm.
3. **BGM:** uma track loop no menu e in-game (ou menu quiet + in-game — **Decisão: BGM contínua com volume music; crossfade não necessário**).
4. **API:** `AudioManager` set_music_volume, set_sfx_volume, play_sfx(name), play_music().
5. **Menu UI:** duas linhas com ◀ ▶ ou +/- para ajustar; mostrar valor.
6. **Init:** `pygame.mixer.init()` no bootstrap; falha graceful se device indisponível (mute + log).

## Risks / Trade-offs

| Risco | Mitigação |
|-------|-----------|
| Licença | Preferir CC0; documentar BY |
| Atraso a “encontrar” sons | Tasks incluem download + placeholder beep se preciso |
| Menu ainda sem secção | Depende main-menu; adicionar submenu Audio |

## Migration Plan

1. Folder + acquire assets + credits  
2. AudioManager  
3. Hook gameplay/UI events  
4. Menu volume controls + save/load  

## Open Questions

- Formato: OGG preferido (pygame-friendly); WAV ok para SFX curtos
