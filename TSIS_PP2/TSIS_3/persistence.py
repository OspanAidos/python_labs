"""
persistence.py — Save / load leaderboard and settings to JSON files.
"""

import json
import os
from datetime import datetime

LEADERBOARD_FILE = "leaderboard.json"
SETTINGS_FILE    = "settings.json"

# ─────────────────────────────────────────────
#  Default settings
# ─────────────────────────────────────────────
DEFAULT_SETTINGS = {
    "sound":       True,
    "car_color":   [220, 60, 60],   # RGB list
    "difficulty":  "normal",        # "easy" | "normal" | "hard"
}

DIFFICULTY_PARAMS = {
    "easy":   {"spawn_rate": 0.012, "enemy_speed": 4, "scale": 0.6},
    "normal": {"spawn_rate": 0.020, "enemy_speed": 6, "scale": 1.0},
    "hard":   {"spawn_rate": 0.030, "enemy_speed": 9, "scale": 1.5},
}


# ─────────────────────────────────────────────
#  Settings
# ─────────────────────────────────────────────
def load_settings() -> dict:
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            # merge with defaults so missing keys are filled in
            merged = DEFAULT_SETTINGS.copy()
            merged.update(data)
            return merged
        except (json.JSONDecodeError, OSError):
            pass
    return DEFAULT_SETTINGS.copy()


def save_settings(settings: dict) -> None:
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)


# ─────────────────────────────────────────────
#  Leaderboard
# ─────────────────────────────────────────────
def load_leaderboard() -> list:
    """Return list of dicts: {name, score, distance, coins, date}."""
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                return data
        except (json.JSONDecodeError, OSError):
            pass
    return []


def save_score(name: str, score: int, distance: int, coins: int) -> None:
    board = load_leaderboard()
    entry = {
        "name":     name,
        "score":    score,
        "distance": distance,
        "coins":    coins,
        "date":     datetime.now().strftime("%Y-%m-%d"),
    }
    board.append(entry)
    board.sort(key=lambda e: e["score"], reverse=True)
    board = board[:10]  # keep top 10
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(board, f, indent=2)