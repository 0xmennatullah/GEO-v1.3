# GEO Matrix Transformation Visualizer v2.1

A Python-based GUI application designed to demonstrate 2D and 3D linear transformations using Manim animations, providing step-by-step visualizations of how matrices transform vector spaces and points.

---

## Overview

This project serves as an educational tool for students and educators in linear algebra, offering an interactive interface to explore matrix transformations. Built with **Tkinter** for the GUI and **Manim** for animations, it supports both 2D and 3D transformations with enhanced visualization features.

---

## Key Features

- 🖥️ **Intuitive Tkinter Interface**: Easily input 2x2 or 3x3 matrices.
- 🧮 **Matrix Support**: Visualize transformations for various matrix types (e.g., scaling, rotation).
- 📊 **Basis Vector Animation**: Dynamically shows transformations of basis vectors (î, ĵ, k̂).
- 🔄 **Step-by-Step Visualization**: Displays intermediate steps for custom point and basis vector transformations.
- 🎥 **Automatic Video Generation**: Renders and plays animation videos automatically.

---

## Installation

### Prerequisites

Ensure the following are installed before running the application:

1. **Python 3.8+**
   - Verify with: `python --version`

2. **FFmpeg** (for video rendering)
   - Windows (PowerShell as Admin): `winget install Gyan.FFmpeg`
   - Mac: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`

3. **LaTeX Distribution**
   - Windows: `winget install ChristianSchenk.MiKTeX` followed by `mpm --update-db` and `mpm --update`
   - Mac: `brew install --cask mactex`
   - Linux (Debian/Ubuntu): `sudo apt install texlive-full`

4. **Manim Dependencies**
   - Install with: `pip install manim numpy tkinter`
   - Verify Manim: `manim --version`

### Setup Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/0xmennatullah/GEO-v2.1.git
   cd GEO-v2.1
   ```

2. Run the setup script:
   ```bash
   ./setup_environment.bat  # Windows
   ./setup_environment.sh  # Mac/Linux
   ```

3. Install dependencies:
   ```bash
   pip install manim numpy
   ```

4. Launch the application:
   ```bash
   python main_gui.py
   ```

---

## Usage

1. Start the application:
   ```bash
   python main_gui.py
   ```

2. Interact with the GUI:
   - Enter a 2x2 or 3x3 matrix.
   - Input a point (2D or 3D, matching matrix dimensions).
   - Click "Calculate & Visualize" to generate and play the animation.

---

## What's New in v2.1

- **Custom Point Transformations**: Tracks user-defined points through each transformation step.
- **Step-by-Step Animation**: Visualizes point transformation by Matrix A, then Matrix B.
- **Improved Error Handling**: Provides clear error messages for invalid inputs or missing dependencies.
- **Enhanced 3D Visualization**: Offers better camera angles for depth perception.
- **Educational Focus**: Highlights both point and basis vector transformations for learning.

---

## Documentation

For a detailed understanding of the project, refer to the included documentation:

- **Project Report**: `GEO_Visualizer_Report.pdf` contains comprehensive information, including:
  - A detailed project description.
  - Screenshots of the GUI and animations.
  - Code snippets and setup instructions.

---

## Troubleshooting

- **Encoding Errors**: Ensure UTF-8 encoding is used on your system.
- **Manim Not Found**: Verify with `manim --version`.
- **Blank Videos**: Try `manim render --clean` first.
- **Rendering Errors**: Ensure point dimensions match matrix dimensions (2D for 2x2, 3D for 3x3).
- **LaTeX Errors**: Confirm MiKTeX is installed with "Install packages on-the-fly" enabled.

---

## How It Works

1. Accepts user-input matrices and points via the Tkinter interface.
2. Computes intermediate and final transformations.
3. Generates a Manim script to visualize:
   - Initial coordinate system and original point.
   - Point transformation by Matrix A.
   - Subsequent transformation by Matrix B.
   - Final result.
   - Basis vector transformations for educational insight.
4. Renders and displays the animation.

---

## Code Structure

```
GEO-v2.1/
├── main_gui.py              # Main application logic
├── matrix_visualization.py  # Generated Manim animation script
├── check_environment.py     # Dependency verification script
├── setup_environment.bat    # Windows setup script
├── setup_environment.sh     # Mac/Linux setup script
├── manim.cfg                # Manim rendering configuration
├── GEO_Visualizer_Report.pdf # Project documentation and report
├── .gitignore               # Excludes media/ and cache files
└── README.md                # This file
```

---

## License

MIT License - See [LICENSE](LICENSE) for details.
