# ============================================================
# LaTeX Formulas — centralized constants for all scenes
# Import with: from src.components.formulas import *
# ============================================================

# ── Scene 4: Localization ────────────────────────────────────
# Daugman's Integro-Differential Operator (split for per-part coloring)
FORMULA_DAUGMAN = [
    r"\max_{(r,x_0,y_0)} \Big| G_{\sigma}(r) * \frac{\partial}{\partial r} ",
    r"\oint",
    r" \frac{",
    r"I(x,y)",
    r"}{2\pi r} ds \Big|"
]
# Convenience: joined string version
FORMULA_LOCALIZATION = "".join(FORMULA_DAUGMAN)

# ── Scene 5: Normalization ───────────────────────────────────
# Mapping from Cartesian to normalized polar coordinates
FORMULA_NORMALIZATION = r"I(r,\theta)"

# Rubber Sheet radial mapping
FORMULA_RUBBER_SHEET_OVERVIEW = (
    r"I(x(r,\theta),\ y(r,\theta))",
    r"\ \longrightarrow\ ",
    r"I(r,\theta)",
)
FORMULA_RUBBER_SHEET_X = r"x(r,\theta) = (1-r)\,x_p(\theta) + r\,x_s(\theta)"
FORMULA_RUBBER_SHEET_Y = r"y(r,\theta) = (1-r)\,y_p(\theta) + r\,y_s(\theta)"
FORMULA_POLAR_RANGE    = r"r \in [0,1],\quad \theta \in [0,2\pi]"

# ── Scene 6: Feature Extraction ──────────────────────────────
# 2D Complex Gabor Wavelet G(x,y)
FORMULA_FEATURE_EXTRACTION = r"G(x,y)"

# Gabor components (for multi-part MathTex coloring)
FORMULA_GABOR_GAUSS   = r"\underbrace{\exp\!\left(-\frac{x'^2+\gamma^2 y'^2}{2\sigma^2}\right)}"
FORMULA_GABOR_SIN     = r"\underbrace{\exp\!\left(j\!\left(2\pi\frac{x'}{\lambda}+\phi\right)\right)}"

# ── Scene 7: Encoding / Phase Quantization ───────────────────
# Complex response from feature filter
FORMULA_COMPLEX_RE    = r"\operatorname{Re} = A\cos\phi"
FORMULA_COMPLEX_IM    = r"\operatorname{Im} = A\sin\phi"
FORMULA_COMPLEX_Z     = r"z = \operatorname{Re} + j\operatorname{Im} = A e^{j\phi}"

# Full Daugman encoding formula
FORMULA_DAUGMAN_ENCODING = (
    r"h_{\{Re,Im\}} = ",
    r"\operatorname{sgn}_{\{Re,Im\}}",
    r"\left( \int_{\rho}\int_{\phi} I(\rho,\phi)\,e^{-i\omega(\theta_0-\phi)}"
    r" e^{-\frac{(r_0-\rho)^2}{\alpha^2}} e^{-\frac{(\theta_0-\phi)^2}{\beta^2}}"
    r" \rho\, d\rho\, d\phi \right)",
)

# Bit encoding rules (tuple of (latex, color_key))
FORMULA_BIT_RULES = [
    r"\operatorname{Re}\ge0\;\Rightarrow\;\text{Bit}_1=1",
    r"\operatorname{Re}<0\;\Rightarrow\;\text{Bit}_1=0",
    r"\operatorname{Im}\ge0\;\Rightarrow\;\text{Bit}_2=1",
    r"\operatorname{Im}<0\;\Rightarrow\;\text{Bit}_2=0",
]

# IrisCode representation
FORMULA_IRIS_CODE = r"101101001\dots"

# ── Scene 8: Matching ────────────────────────────────────────
FORMULA_MATCHING = r"HD = \frac{1}{N} \sum A_j \oplus B_j"

# Full masked Hamming Distance
FORMULA_HD_NUMERATOR   = r"|\,(\text{code}_A \oplus \text{code}_B)\cap\text{mask}_A\cap\text{mask}_B\,|"
FORMULA_HD_DENOMINATOR = r"|\,\text{mask}_A \cap \text{mask}_B\,|"

# Normalized Hamming Distance
FORMULA_HD_NORM = r"HD_{norm} = 0.5 - (0.5 - HD)\,\sqrt{\dfrac{n}{911}}"
