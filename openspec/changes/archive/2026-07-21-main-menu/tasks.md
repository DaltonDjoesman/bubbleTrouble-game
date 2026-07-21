## 1. App flow states

- [x] 1.1 Introduce app states `menu` / `playing` / `won` / `game_over` and boot into `menu`
- [x] 1.2 Branch the main loop so menu and match update/draw separately

## 2. Main menu UI

- [x] 2.1 Create menu module with Play, Quit, mode (1P/2P), and level select fields
- [x] 2.2 Keyboard navigate + confirm; Quit exits the app
- [x] 2.3 Persist selection into `Game` (`selected_mode`, `selected_level`)

## 3. Match entry/exit

- [x] 3.1 Play calls `reset_match` with selected mode/level (level 1 default if pack absent)
- [x] 3.2 From won/game over: retry key + return-to-menu key
- [x] 3.3 Manual smoke: boot→menu→play→die/win→menu→quit
