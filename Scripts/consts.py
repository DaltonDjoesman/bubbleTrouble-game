from pathlib import Path

from assets import SPRITE_SCALE

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

# Neon tint per ball size (cyberpunk palette; applied at load time)
BALL_TINTS = {
    "L": (255, 60, 160),   # magenta
    "M": (60, 220, 255),   # cyan
    "S": (180, 100, 255),  # violet
}

CRAFTPIX = (
    PROJECT_ROOT
    / "sprites"
    / "craftpix-net-730561-free-guns-for-cyberpunk-characters-pixel-art"
)

CYBORG_DIR = CRAFTPIX / "1 Characters" / "3 Cyborg"
BULLETS_DIR = CRAFTPIX / "5 Bullets"
SHOOT_EFFECTS_DIR = CRAFTPIX / "4 Shoot_effects"

# Explicit frame lists (also discoverable via assets.load_folder_frames)
PLAYER_IDLE_FRAMES = [
    CYBORG_DIR / "Idle1.png",
    CYBORG_DIR / "Idle2.png",
]
PLAYER_RUN_FRAMES = [
    CYBORG_DIR / "Run1.png",
    CYBORG_DIR / "Run2.png",
]
PLAYER_JUMP_FRAMES = [
    CYBORG_DIR / "Jump1.png",
    CYBORG_DIR / "Jump2.png",
]

BULLET_SPRITE = BULLETS_DIR / "4_1.png"
# Brief muzzle flash pair (Craftpix shoot effect set 4)
SHOOT_EFFECT_FRAMES = [
    SHOOT_EFFECTS_DIR / "4_1.png",
    SHOOT_EFFECTS_DIR / "4_2.png",
]

BOLA_SPRITE = PROJECT_ROOT / "Assests" / "bola branca.png"

PLAYER_FRAME_SIZE = 48
PLAYER_SCALE = SPRITE_SCALE  # alias — documented scale lives in assets.SPRITE_SCALE
# Shrink opaque bounds a bit so collisions feel fair vs transparent padding
PLAYER_HITBOX_INSET = 0.15

SHOOT_EFFECT_MS = 120
SHOOT_EFFECT_SCALE = 2
