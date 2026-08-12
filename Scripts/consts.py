from pathlib import Path

from assets import SPRITE_SCALE

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSETS = PROJECT_ROOT / "assets"

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.3

# Play area sits above a reserved Pang-style bottom status panel
HUD_PANEL_HEIGHT = 80
PLAY_TOP = 0
PLAY_LEFT = 0
PLAY_RIGHT = SCREEN_WIDTH
PLAY_BOTTOM = SCREEN_HEIGHT - HUD_PANEL_HEIGHT
PLAY_HEIGHT = PLAY_BOTTOM - PLAY_TOP
FLOOR_INSET = 4
FLOOR_Y = PLAY_BOTTOM - FLOOR_INSET

# Ceiling spike row (visual + collision band below PLAY_TOP)
SPIKE_BAND_HEIGHT = 16
SPIKE_WIDTH = 14
CEILING_Y = PLAY_TOP + SPIKE_BAND_HEIGHT

MAX_BULLETS = 2  # max active lasers (harpoon / drill)
STICKY_MAX_ON_MAP = 3  # planted/growing stickies kept on the arena
BULLET_COOLDOWN_MS = 150
LASER_GROW_SPEED = 10
# Cropped DragChain vertical link opaque width (~10px); keeps hitbox thin
LASER_WIDTH = 10
# Classic: ~25% slower than the old hard-coded vel_x=8
PLAYER_VEL_X = 6
# Time barrier (survival resource replaces multi-life stock)
TIME_DRAIN_PER_SEC = 1.0
TIME_POWER_SECONDS = 8
POWERUP_DROP_CHANCE = 0.28
POWERUP_SIZE = 24  # native icon size (no downscale)
POWERUP_FALL_MAX = 4.0
# Crawl gap under barriers/doors so the player can cross (pixels above floor)
BARRIER_CRAWL_GAP = 72

# Survival spawn director (endless mode)
SURVIVAL_MAX_BALLS = 12
SURVIVAL_SPAWN_INTERVAL_START_MS = 2800
SURVIVAL_SPAWN_INTERVAL_MIN_MS = 900
SURVIVAL_SPAWN_RAMP_MS = 120_000  # reach min interval over ~2 minutes
SURVIVAL_SPAWN_PAUSE_MS = 4000  # TIME powerup pauses new spawns
SURVIVAL_SPAWN_Y = CEILING_Y + 48
SURVIVAL_SPAWN_SPEED = 2.2
# Size weight milestones: (elapsed_ms, (S, M, L) weights)
SURVIVAL_SIZE_WEIGHTS = (
    (0, (80, 20, 0)),
    (45_000, (50, 40, 10)),
    (90_000, (25, 45, 30)),
    (150_000, (10, 40, 50)),
)

# Ball size tiers: large → medium → small
BALL_SIZES = {
    "L": {"scale": 0.18, "bounce": -14, "next": "M"},
    "M": {"scale": 0.12, "bounce": -12, "next": "S"},
    "S": {"scale": 0.07, "bounce": -10, "next": None},
}

# Neon tint per ball size (cyberpunk palette; applied at load time)
BALL_TINTS = {
    "L": (255, 60, 160),  # magenta
    "M": (60, 220, 255),  # cyan
    "S": (180, 100, 255),  # violet
}

CRAFTPIX = ASSETS / "craftpix"
CYBORG_DIR = CRAFTPIX / "characters" / "cyborg"
BIKER_DIR = CRAFTPIX / "characters" / "biker"
GUNS_DIR = CRAFTPIX / "guns"
SHOOT_EFFECTS_DIR = CRAFTPIX / "shoot_effects"

PLAYER_IDLE_FRAMES = [
    CYBORG_DIR / "Idle1.png",
    CYBORG_DIR / "Idle2.png",
]
PLAYER_RUN_FRAMES = [
    CYBORG_DIR / "Run1.png",
    CYBORG_DIR / "Run2.png",
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
# Growing harpoon shaft — tileable vertical chain link (not Craftpix bullet)
CHAIN_LINK_SPRITE = ASSETS / "chain" / "DragChainLinkVertical.png"
CHAIN_TIP_SPRITE = ASSETS / "chain" / "ChainArrowHead.png"
# Shoot-effect strips are 48×48 cells — load via strip cutter, not whole PNG
SHOOT_EFFECT_FRAMES = [
    SHOOT_EFFECTS_DIR / "4_1.png",
    SHOOT_EFFECTS_DIR / "4_2.png",
]

BALL_SPRITE = ASSETS / "ball.png"

# Powerup pickup sprites — crisp 24×24 pixel icons (native size)
POWERUP_SPRITES = {
    "TIME": ASSETS / "powerups" / "time.png",
    "STICKY": ASSETS / "powerups" / "sticky.png",
    "DRILL": ASSETS / "powerups" / "drill.png",
}

# Time barrier HUD — drawn inside the bottom status panel
TIME_BAR_WIDTH = 520
TIME_BAR_HEIGHT = 18
TIME_BAR_POS = (16, PLAY_BOTTOM + 22)
TIME_BAR_FILL = (220, 40, 70)
TIME_BAR_FILL_LOW = (255, 90, 40)
TIME_BAR_EDGE = (255, 120, 160)
TIME_BAR_BG = (20, 8, 18)

# Bottom panel chrome (Pang-inspired brick strip)
PANEL_BRICK_A = (118, 72, 48)
PANEL_BRICK_B = (92, 54, 36)
PANEL_BRICK_MORTAR = (48, 28, 18)
PANEL_FRAME = (210, 170, 110)
PANEL_FRAME_INNER = (40, 22, 14)

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
