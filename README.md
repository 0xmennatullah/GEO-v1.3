# GEO Matrix Transformation Visualizer v2.1

A Python GUI application that demonstrates 2D-3D linear transformations through Manim animations, showing how matrices transform vector spaces and points step-by-step.

## Key Features

- 🖥️ Intuitive Tkinter interface for matrix input
- 🧮 Supports 2x2 and 3x3 matrix transformation visualization
- 📊 Animated transformation of basis vectors (î, ĵ, and k̂)
- 🔄 Shows intermediate transformation steps for both basis vectors and custom points
- 🎥 Automatic video generation and playback

## Installation

1. **First, run setup**:
   ```bash
   ./setup_environment.bat  # Windows
   ./setup_environment.sh  # Mac/Linux
   ```

2. **Install LaTeX**:
   - https://miktex.org/download
   - Click "Download" under the "Basic MiKTeX" section
   - Select "Install missing packages on-the-fly" (IMPORTANT for Manim)
   - Check "Run MiKTeX Console after exiting"
   - Click "Finish"
   - First-Time Setup: When MiKTeX Console opens, go to "Updates" tab, Click "Check for updates" and install any available updates.

3. **Then launch the GUI**:
   ```bash
   python main_gui.py
   ```

## 🛠 Prerequisites

Before running, ensure you have:

1. **FFmpeg** (required for video rendering):
   ```bash
   # Windows (PowerShell as Admin):
   winget install Gyan.FFmpeg
   
   # Mac:
   brew install ffmpeg
   
   # Linux:
   sudo apt install ffmpeg
   ```
   
2. **Python 3.8+**
   Verify with:
   ```bash
   python --version
   ```

3. **LaTeX Distribution**
   ```powershell
   # Windows (Run PowerShell as Administrator)
   winget install ChristianSchenk.MiKTeX
   # Update MiKTeX packages
   mpm --update-db
   mpm --update
   ```
   
4. **Manim Dependencies**
   ```bash
   pip install manim numpy tkinter
   # Verify Manim can find MiKTeX
   manim --version
   ```
   
## Full Dependencies

For complete mathematical rendering:
- **Windows**: MiKTeX (auto-installed by setup script)
- **Mac/Linux**: 
  ```bash
  # Mac
  brew install --cask mactex
  
  # Linux (Debian/Ubuntu)
  sudo apt install texlive-full
  ```

### Setup
```bash
git clone https://github.com/0xmennatullah/GEO-v2.1.git
cd GEO-v2.1
pip install manim numpy
```

## Usage

1. Run the application:
   ```bash
   setup.bat
   python main_gui.py
   ```

2. In the GUI:
   - Enter your matrices (2x2 or 3x3)
   - Enter a point to transform (2D or 3D, matching matrix dimensions)
   - Click "Calculate & Visualize"
   - The animation will automatically play after rendering

## What's New in v2.1

- **Custom Point Transformations**: Now visualizes how your custom-defined point is transformed through each step
- **Step-by-Step Animation**: See your point transform first by Matrix A, then by Matrix B
- **Improved Error Handling**: Comprehensive error messages for common issues
- **Enhanced 3D Visualization**: Better camera angles and clearer transformations
- **Educational Approach**: Shows both point transformation and basis vectors transformation

## 🔧 Troubleshooting

If you encounter:
- **Encoding errors**: Ensure your system uses UTF-8 encoding
- **Manim not found**: Verify with `manim --version`
- **Blank videos**: Try `manim render --clean` first
- **Rendering errors**: Check that your point dimensions match matrix dimensions (2D point for 2x2 matrices, 3D point for 3x3 matrices)
- **LaTeX errors**: Make sure MiKTeX is properly installed with "Install packages on-the-fly" enabled

## How It Works

The application:
1. Takes user-input matrices and a point through a Tkinter interface
2. Computes intermediate and final transformations
3. Generates a Manim script visualizing:
   - Initial coordinate system and original point
   - Transformation of the point by matrix A
   - Subsequent transformation by matrix B
   - Final combined transformation result
   - Transformation of basis vectors as an educational demonstration
4. Renders and displays the animation

## Code Structure

```
GEO-v2.1/
├── main_gui.py              # Main application
├── matrix_visualization.py  # Generated Manim script
├── check_environment.py     # Dependency verifier
├── setup_environment.bat    # Windows setup
├── setup_environment.sh     # Mac/Linux setup
├── manim.cfg                # Render configuration
├── .gitignore               # Ignore media/ and caches
└── README.md                # This file
```

## License

MIT License - See [LICENSE](LICENSE) for details.
