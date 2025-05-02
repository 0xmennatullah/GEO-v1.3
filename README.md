# Matrix Transformation Visualizer (2×2)

This Python project provides an intuitive GUI to input and multiply 2×2 matrices, and generates a geometric visualization using [Manim](https://www.manim.community/).

## 🔧 Features
- Input two 2×2 matrices.
- View the calculated result.
- Watch an animated Manim scene showing:
  - The original basis vectors.
  - Step-by-step application of each matrix as a transformation.
  - Final combined transformation (B × A).

## 🖥️ How to Run

1. **Install dependencies**  
   Make sure you have [Manim](https://docs.manim.community/en/stable/installation.html) installed and working. You can also install other requirements:
   ```bash
   pip install numpy tk
Run the app

2. **Run the app**
python main_gui.py

3. **Enter Matrices**
Enter two 2×2 matrices (space-separated values, one row per line) and click Calculate.

4. **View Animation**
Manim will render the transformation and open the video automatically.

## 📂 Project Structure

GEO V1.2/
├── main_gui.py                 # Main GUI and logic
├── manim/                      # (Optional) Any custom Manim assets
├── media/                      # Auto-generated Manim video output
├── matrix_visualization.py     # Auto-generated Manim script (ignored)
├── .gitignore
└── README.md                   # You're reading it now


## ⚠️ Notes
- Only 2×2 matrices are currently supported for geometric visualization.

- You can extend this to 3D or higher-order matrices with more Manim work.