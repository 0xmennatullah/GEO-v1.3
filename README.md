# GEO Matrix Transformation Visualizer v1.3

A Python GUI application that demonstrates 2D linear transformations through Manim animations, showing how matrices transform vector spaces step-by-step.

## Key Features

- 🖥️ Intuitive Tkinter interface for matrix input
- 🧮 Supports 2x2 matrix multiplication visualization
- 📊 Animated transformation of basis vectors (î and ĵ)
- 🔄 Shows intermediate transformation steps
- 🎥 Automatic video generation and playback

## Installation

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

4. **Manim Dependencies**
   ```bash
   pip install manim numpy
   ```

### Setup
   ```bash
   git clone https://github.com/0xmennatullah/GEO-v1.3.git
   cd GEO-v1.3
   pip install manim numpy
   ```

## Usage

1. Run the application:
```bash
python main_gui.py
```

2. In the GUI:
   - Enter your 2x2 matrices (default shows identity and scaling matrices)
   - Click "Calculate & Visualize"
   - The animation will automatically play after rendering


## 🔧 Troubleshooting


FFmpeg not found => Run the installation command for your OS

Invalid LaTeX matrix => Use proper syntax: \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}

Blank videos => Run manim render --clean first
Encoding errors => Ensure files are saved as UTF-8

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
├── main_gui.py # Main application entry point
├── README.md # This documentation
├── .gitignore # Git exclusion rules
└── manim/ # Manim-related files
```

## Customization Options

Modify these in `matrix_visualizer.py`:
- `x_range`/`y_range` in `create_manim_file()` - Change coordinate system bounds
- `.scale()` values - Adjust text/object sizes
- Color codes - Change vector colors (RED/GREEN)

## Troubleshooting

If you encounter:
- **Encoding errors**: Ensure your system uses UTF-8 encoding
- **Manim not found**: Verify with `manim --version`
- **Blank videos**: Try `manim render --clean` first

## License

MIT License - See [LICENSE](LICENSE) for details.

