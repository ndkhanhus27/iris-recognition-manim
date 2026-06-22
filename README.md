# Iris Recognition Animation (Manim)

A visual, step-by-step animation explaining how Iris Recognition works, built with [Manim](https://github.com/3b1b/manim).

**Nguyen Duy Khanh — 23120051**  
**CSC14006 — Pattern Recognition**  
**Faculty of Information Technology**  
**University of Science, VNU-HCM**

---

## 📖 Overview

This project provides an intuitive and educational video about the complete iris recognition pipeline. It breaks down complex concepts into easy-to-understand visual animations, covering everything from the basic anatomy of the eye to classical algorithms (like Daugman's method) and modern Deep Learning approaches.

## 📂 Project Structure

```text
iris-recognition-manim/
│
├── main.py              # The interactive CLI tool to render and combine videos
├── src/
│   ├── components/      # Shared utilities, math formulas, and base scenes
│   ├── scenes/          # The 11 animation scenes (from Scene 0 to 10)
│   └── theme.py         # Global colors and fonts
│
├── assets/              # Images and voice-over audio files
├── media/               # Output folder for rendered videos
└── requirements.txt
```

## 🎬 Scenes Overview

The animation is divided into 11 scenes, taking you from the basics to advanced concepts:

- **Scene 0**: Title
- **Scene 1**: Introduction to Biometrics
- **Scene 2**: Anatomy of the Iris
- **Scene 3**: System Overview
- **Scene 4**: Iris Localization
- **Scene 5**: Normalization (Rubber Sheet Model)
- **Scene 6**: Feature Extraction (2D Gabor Wavelets)
- **Scene 7**: Encoding (Generating the IrisCode)
- **Scene 8**: Matching (Hamming Distance)
- **Scene 9**: Evaluation Metrics
- **Scene 10**: Modern Deep Learning Methods

---

## 🚀 How to Run & Render

Instead of manually typing long Manim commands, this project comes with a convenient, interactive **`main.py`** script that handles everything for you—including rendering and merging the videos into a single final presentation!

### 1. Prerequisites
Make sure you have Python 3.10+ installed, along with [Manim](https://docs.manim.community/) and FFmpeg.  
Activate your virtual environment (if you use one).

### 2. Run the Interactive Menu
Open your terminal at the root of the project and run:

```bash
python main.py
```

### 3. Follow the Prompts
The script will open a clean, interactive menu where you can:
1. **Choose the video quality**:
   - `[1]` 480p (Fast preview)
   - `[2]` 720p
   - `[3]` 1080p (Standard Full HD)
   - `[4]` 4K (Ultra HD)
2. **Choose an action**:
   - Render a specific scene (e.g., type `2` for Scene 2).
   - Type `A` to render all 11 scenes sequentially.
   - Type `AC` to render everything and **automatically combine** them into one final `.mp4` video.
   - Type `C` to combine previously rendered scenes.

*(Note: The `main.py` script will automatically install `imageio-ffmpeg` if it's missing to help with video concatenation).*

