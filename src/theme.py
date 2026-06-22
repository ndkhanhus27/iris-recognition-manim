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

# ==========================================
# 6. GLOBAL TEXT OVERRIDE (LATEX FALLBACK)
# ==========================================
# Override Manim's Text class to use Tex globally, avoiding system font rendering errors.
_OriginalText = Text

class Text(Tex):
    def __init__(self, text, font=None, font_size=36, color=TEXT_COLOR, weight="NORMAL", **kwargs):
        # Scale up font size to match Pango's default visual size
        adjusted_size = int(font_size * 1.25)
        
        s = str(text)
        # Escape special LaTeX characters
        s = s.replace("\\", r"\textbackslash{}")
        s = s.replace("\n", r"\\")
        for ch in ["%", "_", "&", "#", "$", "{", "}"]:
            if ch != "\\": # Handled above
                s = s.replace(ch, "\\" + ch)
        
        # Handle special Unicode characters used in the project
        s = s.replace("°", r"$^\circ$")
        s = s.replace("·", r"$\cdot$")
        s = s.replace("—", r"---")
        s = s.replace("ϕ", r"$\phi$")
        s = s.replace("θ", r"$\theta$")
        s = s.replace("●", r"$\bullet$")
        s = s.replace("≠", r"$\neq$")
        s = s.replace("×", r"$\times$")
        s = s.replace("\u2192", r"$\rightarrow$")
        s = s.replace("\u2265", r"$\ge$")
        s = s.replace("\u2264", r"$\le$")
        s = s.replace("→", r"$\rightarrow$")
        s = s.replace("≥", r"$\ge$")
        s = s.replace("≤", r"$\le$")
        
        # Handle font families
        if font == MONO_FONT or font == "Consolas":
            inner = rf"\texttt{{{s}}}"
        else:
            inner = rf"\textsf{{{s}}}"
            
        if weight == BOLD or weight == "BOLD":
            inner = rf"\textbf{{{inner}}}"
            
        super().__init__(inner, font_size=adjusted_size, color=color, **kwargs)
