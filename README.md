# GEO Matrix Transformation Visualizer v1.3

A Python GUI application that demonstrates 2D linear transformations through Manim animations, showing how matrices transform vector spaces step-by-step.

## Key Features

- 🖥️ Intuitive Tkinter interface for matrix input
- 🧮 Supports 2x2 matrix multiplication visualization
- 📊 Animated transformation of basis vectors (î and ĵ)
- 🔄 Shows intermediate transformation steps
- 🎥 Automatic video generation and playback

## Installation

1. **First, run setup**:
   ```bash
   ./setup_environment.bat  # Windows
   ./setup_environment.sh  # Mac/Linux

2. **Install LaTex**:
   - https://miktex.org/download
   - Click "Download" under the "Basic MiKTeX" section
   - Select "Install missing packages on-the-fly" (IMPORTANT for Manim)
   - Check "Run MiKTeX Console after exiting"
   - Click "Finish"
   - First-Time Setup: When MiKTeX Console opens, go to "Updates" tab, Click "Check for updates" and install any available updates.

3. **Then launch the GUI**:
   ```bash
   python main_gui.py

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
3. **MiKTeX**
   ```powershell
   # Run PowerShell as Administr
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

### Setup
   ```bash
   git clone https://github.com/0xmennatullah/GEO-v1.3.git
   cd GEO-v1.3
   pip install manim numpy
   ```

## Usage

1. Run the application:
```bash
setup.bat
python main_gui.py
```

2. In the GUI:
   - Enter your 2x2 matrices (default shows identity and scaling matrices)
   - Click "Calculate & Visualize"
   - The animation will automatically play after rendering


## 🔧 Troubleshooting
If you encounter:
- **Encoding errors**: Ensure your system uses UTF-8 encoding
- **Manim not found**: Verify with `manim --version`
- **Blank videos**: Try `manim render --clean` first

## How It Works

The application:
1. Takes user-input matrices through a Tkinter interface
2. Computes the matrix product B×A
3. Generates a Manim script visualizing:
   - Initial basis vectors
   - Transformation by matrix A
   - Subsequent transformation by matrix B
   - Final combined transformation
4. Renders and displays the animation

## Code Structure

```
GEO-v1.3/
├── main_gui.py              # Main application
├── check_environment.py     # Dependency verifier
├── setup_environment.bat    # Windows setup
├── manim.cfg                # Render configuration
├── .gitignore               # Ignore media/ and caches
└── README.md                # This file
```

## License

MIT License - See [LICENSE](LICENSE) for details.

