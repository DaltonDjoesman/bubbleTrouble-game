from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

screenWidth = 800
screenHeight = 600
FPS = 60
GRAVITY = 0.3

MAX_BULLETS = 2  # max active lasers
BULLET_COOLDOWN_MS = 150
LASER_GROW_SPEED = 10
LASER_WIDTH = 6
DEFAULT_LIVES = 3
IFRAME_MS = 1500

# Ball size tiers: large → medium → small
BALL_SIZES = {
    "L": {"scale": 0.18, "bounce": -14, "next": "M"},
    "M": {"scale": 0.12, "bounce": -12, "next": "S"},
    "S": {"scale": 0.07, "bounce": -10, "next": None},
}

CRAFTPIX = (
    PROJECT_ROOT
    / "sprites"
    / "craftpix-net-730561-free-guns-for-cyberpunk-characters-pixel-art"
)

PLAYER_IDLE_FRAMES = [
    CRAFTPIX / "1 Characters" / "3 Cyborg" / "Idle1.png",
    CRAFTPIX / "1 Characters" / "3 Cyborg" / "Idle2.png",
]

PLAYER_RUN_FRAMES = [
    CRAFTPIX / "1 Characters" / "3 Cyborg" / "Run1.png",
    CRAFTPIX / "1 Characters" / "3 Cyborg" / "Run2.png",
]

BULLET_SPRITE = CRAFTPIX / "5 Bullets" / "4_1.png"
BOLA_SPRITE = PROJECT_ROOT / "Assests" / "bola branca.png"

PLAYER_FRAME_SIZE = 48
PLAYER_SCALE = 2
