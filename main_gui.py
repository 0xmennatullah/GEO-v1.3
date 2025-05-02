import tkinter as tk
from tkinter import messagebox, ttk
import numpy as np
import subprocess
import os
import platform

# Environment check
from check_environment import verify_environment
if not verify_environment():
    sys.exit(1)
    
def parse_matrix(matrix_str, rows, cols):
    """Parse input text to create a numpy matrix"""
    try:
        matrix = []
        lines = [line.strip() for line in matrix_str.strip().split('\n') if line.strip()]
        
        if len(lines) != rows:
            raise ValueError(f"Expected {rows} rows, got {len(lines)}")
            
        for line in lines:
            elements = [float(num) for num in line.split()]
            if len(elements) != cols:
                raise ValueError(f"Expected {cols} columns in each row, got {len(elements)}")
            matrix.append(elements)
            
        return np.array(matrix)
    except Exception as e:
        raise ValueError(f"Error parsing matrix: {e}")

def matrix_to_latex_str(matrix):
    """Convert numpy matrix to valid LaTeX"""
    rows, cols = matrix.shape
    elements = [" & ".join([f"{x:.2f}" for x in row]) for row in matrix]
    return r"\begin{bmatrix} " + r" \\ ".join(elements) + r" \end{bmatrix}"

def create_manim_file(matrix1, matrix2):
    """Create a Manim script file for matrix visualization"""
    matrix1_latex = matrix_to_latex_str(matrix1)
    matrix2_latex = matrix_to_latex_str(matrix2)
    result_matrix = np.dot(matrix2, matrix1)
    result_latex = matrix_to_latex_str(result_matrix)

    script_content = f"""from manim import *
import numpy as np

class MatrixMultiplicationScene(Scene):
    def construct(self):
        matrix1 = np.array({matrix1.tolist()})
        matrix2 = np.array({matrix2.tolist()})
        result = np.dot(matrix2, matrix1)

        matrix1_tex = MathTex(r"A = {matrix1_latex}").scale(0.8).to_corner(UL)
        matrix2_tex = MathTex(r"B = {matrix2_latex}").scale(0.8).next_to(matrix1_tex, DOWN, buff=1)
        equals_tex = MathTex(r"A \\times B =").scale(0.8).next_to(matrix2_tex, DOWN, buff=1)
        result_tex = MathTex(r"{result_latex}").scale(0.8).next_to(equals_tex, RIGHT)

        self.play(Write(matrix1_tex), Write(matrix2_tex))
        self.wait(1)
        self.play(Write(equals_tex), Write(result_tex))
        self.wait(1)

        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            axis_config={{"color": BLUE}}
        ).scale(0.6).to_edge(RIGHT)

        self.play(Create(axes))

        i_hat = Arrow(axes.c2p(0, 0), axes.c2p(1, 0), buff=0, color=RED)
        j_hat = Arrow(axes.c2p(0, 0), axes.c2p(0, 1), buff=0, color=GREEN)

        self.play(GrowArrow(i_hat), GrowArrow(j_hat))
        self.wait(1)

        title1 = Tex("Transformation by Matrix $A$").scale(0.5).to_edge(UP)
        self.play(Write(title1))

        new_i = Arrow(axes.c2p(0, 0), axes.c2p(matrix1[0, 0], matrix1[1, 0]), buff=0, color=RED)
        new_j = Arrow(axes.c2p(0, 0), axes.c2p(matrix1[0, 1], matrix1[1, 1]), buff=0, color=GREEN)

        self.play(Transform(i_hat, new_i), Transform(j_hat, new_j))
        self.wait(1)

        title2 = Tex("Transformation by Matrix $B$").scale(0.5).to_edge(UP)
        self.play(FadeOut(title1), Write(title2))

        i_transformed = np.dot(matrix2, np.array([matrix1[0, 0], matrix1[1, 0]]))
        j_transformed = np.dot(matrix2, np.array([matrix1[0, 1], matrix1[1, 1]]))

        final_i = Arrow(axes.c2p(0, 0), axes.c2p(i_transformed[0], i_transformed[1]), buff=0, color=RED)
        final_j = Arrow(axes.c2p(0, 0), axes.c2p(j_transformed[0], j_transformed[1]), buff=0, color=GREEN)

        self.play(Transform(i_hat, final_i), Transform(j_hat, final_j))
        self.wait(1)

        title3 = Tex("Combined Transformation ($B \\times A$)").scale(0.5).to_edge(UP)
        self.play(FadeOut(title2), Write(title3))

        combined_tex = MathTex(r"B \\times A = {result_latex}").scale(0.6).next_to(title3, DOWN)
        self.play(Write(combined_tex))
        self.wait(2)
"""
    with open("matrix_visualization.py", "w", encoding="utf-8") as f:
        f.write(script_content)

def open_video_file(filepath):
    """Open the video file using the default viewer"""
    try:
        if platform.system() == 'Windows':
            os.startfile(filepath)
        elif platform.system() == 'Darwin':
            subprocess.run(['open', filepath])
        else:
            subprocess.run(['xdg-open', filepath])
    except Exception as e:
        messagebox.showerror("Error", f"Could not open video file: {str(e)}")

def run_manim_visualization():
    """Run the Manim visualization and show the output"""
    try:
        media_dir = os.path.join(os.getcwd(), "media")
        if os.path.exists(media_dir):
            for root, dirs, files in os.walk(media_dir):
                for file in files:
                    if file.endswith(".mp4"):
                        os.remove(os.path.join(root, file))

        command = ["manim", "-ql", "matrix_visualization.py", "MatrixMultiplicationScene"]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            raise Exception(f"Manim error: {stderr}")

        for root, dirs, files in os.walk(media_dir):
            for file in files:
                if file.startswith("MatrixMultiplicationScene") and file.endswith(".mp4"):
                    open_video_file(os.path.join(root, file))
                    return True

        raise Exception("Could not find generated video file")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate visualization: {str(e)}")
        return False

def calculate_matrices():
    """Calculate matrix product and show visualization"""
    try:
        rows = int(rows_var.get())
        cols = int(cols_var.get())

        if rows != 2 or cols != 2:
            messagebox.showwarning("Only 2x2 matrices supported", "For visualization, please use 2x2 matrices.")
            return

        matrix1_str = matrix1_text.get("1.0", "end-1c")
        matrix2_str = matrix2_text.get("1.0", "end-1c")

        matrix1 = parse_matrix(matrix1_str, rows, cols)
        matrix2 = parse_matrix(matrix2_str, rows, cols)
        result = np.dot(matrix2, matrix1)

        result_text.delete("1.0", "end")
        result_text.insert("1.0", np.array2string(result, precision=2, separator=' '))

        create_manim_file(matrix1, matrix2)

        status_label.config(text="Running Manim...")
        root.update()

        if run_manim_visualization():
            status_label.config(text="Visualization completed.")
        else:
            status_label.config(text="Failed to create visualization.")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI SETUP
root = tk.Tk()
root.title("Matrix Multiplication Visualizer")

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0)

ttk.Label(frame, text="Matrix Dimensions (rows x cols):").grid(row=0, column=0, sticky="w")
rows_var = tk.StringVar(value="2")
cols_var = tk.StringVar(value="2")
ttk.Entry(frame, width=5, textvariable=rows_var).grid(row=0, column=1)
ttk.Label(frame, text="x").grid(row=0, column=2)
ttk.Entry(frame, width=5, textvariable=cols_var).grid(row=0, column=3)

ttk.Label(frame, text="Matrix A (row by row):").grid(row=1, column=0, columnspan=4, sticky="w")
matrix1_text = tk.Text(frame, width=30, height=4)
matrix1_text.grid(row=2, column=0, columnspan=4, pady=5)

ttk.Label(frame, text="Matrix B (row by row):").grid(row=3, column=0, columnspan=4, sticky="w")
matrix2_text = tk.Text(frame, width=30, height=4)
matrix2_text.grid(row=4, column=0, columnspan=4, pady=5)

ttk.Label(frame, text="Result (B × A):").grid(row=5, column=0, columnspan=4, sticky="w")
result_text = tk.Text(frame, width=30, height=4)
result_text.grid(row=6, column=0, columnspan=4, pady=5)

ttk.Button(frame, text="Calculate and Visualize", command=calculate_matrices).grid(row=7, column=0, columnspan=4, pady=10)

status_label = ttk.Label(frame, text="")
status_label.grid(row=8, column=0, columnspan=4)

root.mainloop()
