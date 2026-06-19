from manim import *

# ==========================================
# 1. COLOR PALETTE (SCIENCE & BIOMETRICS)
# ==========================================
# Background
BG_COLOR = "#0F172A"  # Deep Slate/Navy (Clean Science look)

# Text colors
TEXT_COLOR = "#F8FAFC"  # Clean White
MUTED_TEXT_COLOR = "#94A3B8"  # Slate Gray

# Primary Accent Colors (Biometric/Tech vibe)
PRIMARY_COLOR = "#00E5FF"    # Cyan (Laser/Scan effect)
SECONDARY_COLOR = "#14B8A6"  # Teal (Biology/Iris)
ACCENT_COLOR = "#8B5CF6"     # Purple (AI/Deep Learning)

# Functional Colors
SUCCESS_COLOR = "#10B981"    # Emerald Green
ERROR_COLOR = "#EF4444"      # Medical Red
WARNING_COLOR = "#F59E0B"    # Amber

# ==========================================
# 2. TYPOGRAPHY
# ==========================================
MAIN_FONT = "Segoe UI" 
MONO_FONT = "Consolas" 

TITLE_FONT_SIZE = 48
BODY_FONT_SIZE = 36
SMALL_FONT_SIZE = 24
SUBTITLE_FONT_SIZE = 20

# ==========================================
# 3. MOBJECT STYLING
# ==========================================
DEFAULT_STROKE_WIDTH = 4
THICK_STROKE_WIDTH = 8
THIN_STROKE_WIDTH = 2

DEFAULT_FILL_OPACITY = 0.5
SOLID_FILL_OPACITY = 1.0
TRANSPARENT_FILL_OPACITY = 0.0

# ==========================================
# 4. ANIMATION CONSTANTS
# ==========================================
FAST_RUN_TIME = 0.5
DEFAULT_RUN_TIME = 1.0
SLOW_RUN_TIME = 2.0

SHORT_WAIT = 0.5
DEFAULT_WAIT = 1.0
LONG_WAIT = 2.0

# ==========================================
# 5. LAYOUT & POSITIONING
# ==========================================
MARGIN_X = 1.0
MARGIN_Y = 1.0

TITLE_POS = UP * 3.2 + LEFT * 6.0
FOOTER_POS = DOWN * 3.5

def setup_theme():
    """Apply global configurations to Manim."""
    config.background_color = BG_COLOR
