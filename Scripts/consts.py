from pathlib import Path

from assets import SPRITE_SCALE

PROJECT_ROOT = Path(__file__).resolve().parent.parent

screenWidth = 800
screenHeight = 600
FPS = 60
GRAVITY = 0.3

MAX_BULLETS = 2  # max active lasers (harpoon / drill)
STICKY_MAX_ON_MAP = 3  # planted/growing stickies kept on the arena
BULLET_COOLDOWN_MS = 150
LASER_GROW_SPEED = 10
LASER_WIDTH = 6
# Classic: ~25% slower than the old hard-coded vel_x=8
PLAYER_VEL_X = 6
# Time barrier (survival resource replaces multi-life stock)
TIME_DRAIN_PER_SEC = 1.0
TIME_POWER_SECONDS = 8
POWERUP_DROP_CHANCE = 0.28
POWERUP_SIZE = 22
POWERUP_FALL_MAX = 4.0
# Crawl gap under barriers/doors so the player can cross (pixels above floor)
BARRIER_CRAWL_GAP = 72

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
BIKER_DIR = CRAFTPIX / "1 Characters" / "1 Biker"
GUNS_DIR = CRAFTPIX / "2 Guns"
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

# P2 (Biker) — co-op
P2_IDLE_FRAMES = [
    BIKER_DIR / "Idle1.png",
    BIKER_DIR / "Idle2.png",
]
P2_RUN_FRAMES = [
    BIKER_DIR / "Run1.png",
    BIKER_DIR / "Run2.png",
]

# Keymaps: left / right / fire (grounded; no jump)
P1_KEYS = {
    "left": "a",
    "right": "d",
    "fire": "space",
}
P2_KEYS = {
    "left": "left",
    "right": "right",
    "fire": "return",
}

# Co-op spawn offsets from arena center (floor baseline)
P1_SPAWN_X_OFFSET = -120
P2_SPAWN_X_OFFSET = 120

# Compact pistol (set 4) — P1; set 3 for P2 visual distinction
GUN_SPRITE = GUNS_DIR / "4_1.png"
P2_GUN_SPRITE = GUNS_DIR / "3_1.png"
BULLET_SPRITE = BULLETS_DIR / "4_1.png"
# Shoot-effect strips are 48×48 cells — load via strip cutter, not whole PNG
SHOOT_EFFECT_FRAMES = [
    SHOOT_EFFECTS_DIR / "4_1.png",
    SHOOT_EFFECTS_DIR / "4_2.png",
]

BOLA_SPRITE = PROJECT_ROOT / "Assests" / "bola branca.png"

# Time barrier HUD (replaces multi-life capsule display)
TIME_BAR_WIDTH = 220
TIME_BAR_HEIGHT = 18
TIME_BAR_POS = (12, 12)
TIME_BAR_FILL = (220, 40, 70)
TIME_BAR_FILL_LOW = (255, 90, 40)
TIME_BAR_EDGE = (255, 120, 160)
TIME_BAR_BG = (20, 8, 18)

PLAYER_FRAME_SIZE = 48
PLAYER_SCALE = SPRITE_SCALE  # alias — documented scale lives in assets.SPRITE_SCALE
# Shrink opaque bounds a bit so collisions feel fair vs transparent padding
PLAYER_HITBOX_INSET = 0.15
GUN_SCALE = 2  # same pixel scale as the Cyborg frames
# Hand height as fraction of body opaque box (0 = head, 1 = feet)
GUN_HAND_Y_FRAC = 0.48

SHOOT_EFFECT_MS = 100
# Effects are strip cells; keep small (1× after crop) so muzzle flash ≠ whole sheet
SHOOT_EFFECT_SCALE = 1

# Audio (Kenney CC0 — see audio/CREDITS.md)
AUDIO_DIR = PROJECT_ROOT / "audio"
AUDIO_MUSIC_PATH = AUDIO_DIR / "music" / "bgm.ogg"
AUDIO_SFX = {
    "shoot": AUDIO_DIR / "sfx" / "shoot.ogg",
    "ball_pop": AUDIO_DIR / "sfx" / "ball_pop.ogg",
    "player_hit": AUDIO_DIR / "sfx" / "player_hit.ogg",
    "win": AUDIO_DIR / "sfx" / "win.ogg",
    "lose": AUDIO_DIR / "sfx" / "lose.ogg",
    "ui_select": AUDIO_DIR / "sfx" / "ui_select.wav",
    "ui_confirm": AUDIO_DIR / "sfx" / "ui_confirm.wav",
}
VOLUME_MAX = 10
VOLUME_DEFAULT = 7
SETTINGS_PATH = PROJECT_ROOT / "settings.json"
