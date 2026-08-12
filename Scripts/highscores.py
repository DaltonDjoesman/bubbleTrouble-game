"""Local Survival high-score boards (1P / 2P), JSON persistence."""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Any

from consts import HIGHSCORE_MAX_ENTRIES, HIGHSCORE_NAME_LEN, HIGHSCORES_PATH

logger = logging.getLogger(__name__)

BOARD_KEYS = ("1p", "2p")


@dataclass(frozen=True)
class ScoreEntry:
    name: str
    time_ms: int


def empty_boards() -> dict[str, list[ScoreEntry]]:
    return {key: [] for key in BOARD_KEYS}


def board_key_for_mode(mode: str) -> str:
    return "2p" if mode == "2P" else "1p"


def format_time_ms(time_ms: int) -> str:
    """Format elapsed ms as M:SS.t (tenths)."""
    ms = max(0, int(time_ms))
    total_s = ms // 1000
    tenths = (ms % 1000) // 100
    minutes = total_s // 60
    seconds = total_s % 60
    return f"{minutes}:{seconds:02d}.{tenths}"


def _normalize_name(name: str) -> str:
    letters = [c for c in str(name).upper() if "A" <= c <= "Z"]
    while len(letters) < HIGHSCORE_NAME_LEN:
        letters.append("A")
    return "".join(letters[:HIGHSCORE_NAME_LEN])


def _parse_entry(raw: Any) -> ScoreEntry | None:
    if not isinstance(raw, dict):
        return None
    try:
        time_ms = int(raw.get("time_ms", -1))
    except (TypeError, ValueError):
        return None
    if time_ms < 0:
        return None
    name = _normalize_name(str(raw.get("name", "AAA")))
    return ScoreEntry(name=name, time_ms=time_ms)


def _sort_board(entries: list[ScoreEntry]) -> list[ScoreEntry]:
    # Best (longest) Survival time first.
    return sorted(entries, key=lambda e: e.time_ms, reverse=True)[:HIGHSCORE_MAX_ENTRIES]


def load_highscores(path=HIGHSCORES_PATH) -> dict[str, list[ScoreEntry]]:
    """Load boards from disk; corrupt/missing → empty boards."""
    boards = empty_boards()
    if not path.is_file():
        return boards
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        logger.warning("Could not read high scores from %s: %s", path, exc)
        return boards
    if not isinstance(data, dict):
        return boards
    for key in BOARD_KEYS:
        raw_list = data.get(key, [])
        if not isinstance(raw_list, list):
            continue
        parsed: list[ScoreEntry] = []
        for raw in raw_list:
            entry = _parse_entry(raw)
            if entry is not None:
                parsed.append(entry)
        boards[key] = _sort_board(parsed)
    return boards


def save_highscores(
    boards: dict[str, list[ScoreEntry]],
    path=HIGHSCORES_PATH,
) -> None:
    payload: dict[str, Any] = {}
    for key in BOARD_KEYS:
        entries = _sort_board(list(boards.get(key, [])))
        payload[key] = [{"name": e.name, "time_ms": e.time_ms} for e in entries]
    try:
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    except OSError as exc:
        logger.warning("Could not save high scores to %s: %s", path, exc)


def qualifies(boards: dict[str, list[ScoreEntry]], board_key: str, time_ms: int) -> bool:
    """True if time_ms earns a slot on the board (strictly better than 5th, or room)."""
    if board_key not in BOARD_KEYS or time_ms <= 0:
        return False
    board = boards.get(board_key, [])
    if len(board) < HIGHSCORE_MAX_ENTRIES:
        return True
    return time_ms > board[-1].time_ms


def insert_score(
    boards: dict[str, list[ScoreEntry]],
    board_key: str,
    name: str,
    time_ms: int,
) -> int:
    """Insert a qualifying entry; returns 1-based rank (0 if not inserted)."""
    if board_key not in BOARD_KEYS or time_ms <= 0:
        return 0
    if not qualifies(boards, board_key, time_ms):
        return 0
    entry = ScoreEntry(name=_normalize_name(name), time_ms=int(time_ms))
    board = list(boards.get(board_key, []))
    board.append(entry)
    board = _sort_board(board)
    boards[board_key] = board
    save_highscores(boards)
    for i, e in enumerate(board):
        if e.name == entry.name and e.time_ms == entry.time_ms:
            return i + 1
    return 0
