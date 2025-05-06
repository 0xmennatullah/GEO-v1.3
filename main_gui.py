import tkinter as tk
from tkinter import messagebox, ttk
import numpy as np
import subprocess
import os
import platform
import sys
import shutil

def verify_setup():
    """Check if setup was completed"""
    required = {
        "FFmpeg": ["ffmpeg", "-version"],
        "LaTeX": ["latex", "--version"],
        "Manim": ["manim", "--version"]
    }
    
    missing = []
    for name, cmd in required.items():
        try:
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except:
            missing.append(name)
    
    if missing:
        messagebox.showerror(
            "Setup Required",
            f"Run setup_environment.bat first!\nMissing: {', '.join(missing)}"
        )
        sys.exit(1)

if __name__ == "__main__":
    verify_setup() 

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except:
        return False
    
def open_video_file(filepath):
    """Open the video file using the default viewer"""
    try:
        # Convert path to raw string and handle spaces
        raw_path = filepath.replace(' ', '%20') if platform.system() == 'Windows' else filepath
        if platform.system() == 'Windows':
            os.startfile(raw_path)
        elif platform.system() == 'Darwin':
            subprocess.run(['open', raw_path])
        else:
            subprocess.run(['xdg-open', raw_path])
    except Exception as e:
        messagebox.showerror("Playback Error", 
            f"Could not open video:\n{str(e)}\n"
            f"Try manually opening:\n{filepath}")

def run_manim_visualization():
    """Run the Manim visualization with comprehensive error handling"""
    try:
        # 1. Clean previous renders
        media_dir = os.path.join(os.getcwd(), "media")
        if os.path.exists(media_dir):
            shutil.rmtree(media_dir)
        
        # 2. Verify LaTeX is available
        try:
            subprocess.run(["pdflatex", "--version"], 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE, 
                         check=True)
        except:
            messagebox.showwarning(
                "LaTeX Not Found",
                "For best results, install LaTeX:\n"
                "Windows: https://miktex.org/download\n"
                "Mac: brew install --cask mactex\n"
                "Linux: sudo apt install texlive-latex-extra"
            )

        # 3. Run Manim with detailed error capture
        command = [
            sys.executable,
            "-m", "manim",
            "-ql",  # Medium quality
            "--progress_bar=none",
            "--disable_caching",
            "matrix_visualization.py",
            "MatrixMultiplicationScene"
        ]
        
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=60  # 1 minute timeout
        )

        # 4. Handle specific error cases
        if result.returncode != 0:
            error_msg = result.stderr.strip()
            
            # LaTeX-specific errors
            if "LaTeX Error" in error_msg:
                latex_error = error_msg.split("! LaTeX Error")[-1].split("\n")[0]
                raise RuntimeError(
                    f"LaTeX rendering failed:\n{latex_error}\n\n"
                    "Install MiKTeX (Windows) or TeX Live (Linux/Mac)"
                )
            
            # General Manim errors
            elif "Error" in error_msg:
                raise RuntimeError(error_msg.split("Error")[-1].strip())
            
            else:
                raise RuntimeError(f"Manim failed: {error_msg}")

        # 5. Find and open the generated video
        video_file = None
        for root, _, files in os.walk(media_dir):
            for file in files:
                if (file.startswith("MatrixMultiplicationScene") and 
                    file.endswith(".mp4")):
                    video_file = os.path.join(root, file)
                    break

        if not video_file:
            raise FileNotFoundError(
                "Video file not found in:\n" 
                f"{media_dir}\n\n"
                "Possible causes:\n"
                "1. Rendering failed silently\n"
                "2. Incorrect output directory"
            )

        # 6. Platform-specific video opening
        try:
            if platform.system() == 'Windows':
                os.startfile(video_file)
            elif platform.system() == 'Darwin':
                subprocess.run(['open', video_file])
            else:
                subprocess.run(['xdg-open', video_file])
            return True
            
        except Exception as e:
            messagebox.showinfo(
                "Visualization Ready",
                f"Video rendered but couldn't auto-play:\n{video_file}"
            )
            return True

    except subprocess.TimeoutExpired:
        messagebox.showerror(
            "Timeout Error",
            "Rendering took too long (over 1 minute)\n"
            "Try simpler matrices or lower quality (-ql)"
        )
        return False

    except Exception as e:
        error_msg = str(e)
        
        # Special handling for common errors
        if "No such file or directory" in error_msg:
            error_msg += "\n\nTry: pip install --upgrade manim"
        elif "Unknown projection" in error_msg:
            error_msg += "\n\nUpdate Manim: pip install manim --upgrade"
            
        messagebox.showerror(
            "Rendering Failed",
            f"{error_msg}\n\n"
            "Troubleshooting:\n"
            "1. Delete 'media' folder and retry\n"
            "2. Check matrices for invalid values\n"
            "3. Update Manim: pip install --upgrade manim"
        )
        return False
    
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
    elements = []
    for row in matrix:
        # Format numbers and handle potential rounding errors
        elements.append(" & ".join([f"{x:.2f}".rstrip('0').rstrip('.') if '.' in f"{x:.2f}" else f"{x}" for x in row]))
    return r"\begin{bmatrix} " + r" \\ ".join(elements) + r" \end{bmatrix}"

def create_manim_file(matrix1, matrix2, point):
    """Create a Manim script file for matrix visualization"""
    matrix1_latex = matrix_to_latex_str(matrix1)
    matrix2_latex = matrix_to_latex_str(matrix2)
    result_matrix = np.dot(matrix2, matrix1)
    result_latex = matrix_to_latex_str(result_matrix)
    
    # Ensure the point has the right dimension for visualization
    rows, cols = matrix1.shape
    if len(point) != cols:
        raise ValueError(f"Point dimension ({len(point)}) must match matrix column count ({cols})")

    script_content = f"""# -*- coding: utf-8 -*-
from manim import *
import numpy as np

class MatrixMultiplicationScene(ThreeDScene):
    def construct(self):
        # Define matrices
        matrix1 = np.array({matrix1.tolist()})
        matrix2 = np.array({matrix2.tolist()})
        result = np.dot(matrix2, matrix1)
        
        # Define point vector
        input_point = np.array({point.tolist()})
        mid_point = matrix1 @ input_point  # Point after first transformation
        transformed_point = result @ input_point  # Point after both transformations
        
        # Create coordinate system first
        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-5, 5, 1],
            x_length=6,
            y_length=6,
            z_length=6
        )
        
        # Animate creation of the axes
        self.play(Create(axes), run_time=2)
        self.wait(1)
        
        # Create vectors for our point in different stages - handle both 2D and 3D carefully
        if len(input_point) == 2:
            # For 2D points, add a zero for the z-coordinate
            original_vec = Arrow(axes.c2p(0, 0, 0), axes.c2p(input_point[0], input_point[1], 0), buff=0, color=BLUE)
            mid_vec = Arrow(axes.c2p(0, 0, 0), axes.c2p(mid_point[0], mid_point[1], 0), buff=0, color=GREEN)
            transformed_vec = Arrow(axes.c2p(0, 0, 0), axes.c2p(transformed_point[0], transformed_point[1], 0), buff=0, color=YELLOW)
        else:
            # For 3D points use the full coordinates
            original_vec = Arrow(axes.c2p(0, 0, 0), axes.c2p(input_point[0], input_point[1], input_point[2]), buff=0, color=BLUE)
            mid_vec = Arrow(axes.c2p(0, 0, 0), axes.c2p(mid_point[0], mid_point[1], mid_point[2]), buff=0, color=GREEN)
            transformed_vec = Arrow(axes.c2p(0, 0, 0), axes.c2p(transformed_point[0], transformed_point[1], transformed_point[2]), buff=0, color=YELLOW)

        point_label = Tex("Original Point").scale(0.5).next_to(original_vec.get_end(), RIGHT)
        
        # Display matrices
        matrix1_tex = MathTex(r"A = {matrix1_latex}").scale(0.8).to_corner(UL)
        matrix2_tex = MathTex(r"B = {matrix2_latex}").scale(0.8).next_to(matrix1_tex, DOWN, buff=1)
        equals_tex = MathTex(r"B \\times A =").scale(0.8).next_to(matrix2_tex, DOWN, buff=1)
        result_tex = MathTex(r"{result_latex}").scale(0.8).next_to(equals_tex, RIGHT)

        # Show matrices on the side
        self.play(Write(matrix1_tex), Write(matrix2_tex))
        self.wait(1)
        
        # Initially set camera angle for good view
        self.move_camera(phi=45 * DEGREES, theta=-125 * DEGREES, run_time=1.5)
        
        # Step 1: Show original point
        self.play(GrowArrow(original_vec), Write(point_label))
        self.wait(1)
        
        # Step 2: Apply first transformation (matrix A)
        title1 = Tex("Transformation by Matrix $A$").scale(0.7).to_edge(UP)
        self.play(Write(title1))
        
        mid_label = Tex("After Matrix A").scale(0.5)
        mid_label.next_to(mid_vec.get_end(), RIGHT)
        
        # Transform original point to mid-point (after matrix A)
        self.play(
            Transform(original_vec, mid_vec), 
            Transform(point_label, mid_label)
        )
        self.wait(1)
        
        # Step 3: Apply second transformation (matrix B)
        title2 = Tex("Transformation by Matrix $B$").scale(0.7).to_edge(UP)
        self.play(FadeOut(title1), Write(title2))
        
        final_label = Tex("Final Point").scale(0.5)
        final_label.next_to(transformed_vec.get_end(), RIGHT)
        
        # Transform mid-point to final point (after matrix B)
        self.play(
            Transform(original_vec, transformed_vec),
            Transform(point_label, final_label)
        )
        self.wait(1)
        
        # Step 4: Show the combined transformation result
        title3 = Tex("Combined Transformation ($B \\times A$)").scale(0.7).to_edge(UP)
        self.play(FadeOut(title2), Write(title3))
        self.play(Write(equals_tex), Write(result_tex))
        self.wait(1)
        
        # Optional: Also show basis vectors transformation for educational purposes
        if matrix1.shape == (3, 3):
            # Create basis vectors for 3D
            i_hat = Arrow(axes.c2p(0, 0, 0), axes.c2p(1, 0, 0), buff=0, color=RED)
            j_hat = Arrow(axes.c2p(0, 0, 0), axes.c2p(0, 1, 0), buff=0, color=GREEN)
            k_hat = Arrow(axes.c2p(0, 0, 0), axes.c2p(0, 0, 1), buff=0, color=BLUE)
            
            basis_title = Tex("Basis Vectors Transformation").scale(0.7).to_edge(UP)
            self.play(FadeOut(title3), Write(basis_title))
            
            # Show basis vectors
            self.play(GrowArrow(i_hat), GrowArrow(j_hat), GrowArrow(k_hat))
            self.wait(1)
            
            # First transformation on basis vectors
            basis_title1 = Tex("Basis Vectors under Matrix $A$").scale(0.7).to_edge(UP)
            self.play(FadeOut(basis_title), Write(basis_title1))
            
            # Map basis vectors through matrix A
            new_i = Arrow(axes.c2p(0, 0, 0), axes.c2p(*matrix1[:, 0]), buff=0, color=RED)
            new_j = Arrow(axes.c2p(0, 0, 0), axes.c2p(*matrix1[:, 1]), buff=0, color=GREEN)
            new_k = Arrow(axes.c2p(0, 0, 0), axes.c2p(*matrix1[:, 2]), buff=0, color=BLUE)
            
            self.play(Transform(i_hat, new_i), Transform(j_hat, new_j), Transform(k_hat, new_k))
            self.wait(1)
            
            # Second transformation on basis vectors
            basis_title2 = Tex("Basis Vectors under $B \\times A$").scale(0.7).to_edge(UP)
            self.play(FadeOut(basis_title1), Write(basis_title2))
            
            # Map basis vectors through combined transformation
            i_transformed = np.dot(matrix2, matrix1[:, 0])
            j_transformed = np.dot(matrix2, matrix1[:, 1])
            k_transformed = np.dot(matrix2, matrix1[:, 2])
            
            final_i = Arrow(axes.c2p(0, 0, 0), axes.c2p(*i_transformed), buff=0, color=RED)
            final_j = Arrow(axes.c2p(0, 0, 0), axes.c2p(*j_transformed), buff=0, color=GREEN)
            final_k = Arrow(axes.c2p(0, 0, 0), axes.c2p(*k_transformed), buff=0, color=BLUE)
            
            self.play(Transform(i_hat, final_i), Transform(j_hat, final_j), Transform(k_hat, final_k))
            self.wait(1)
        
        else:
            # 2D logic
            # Create basis vectors for 2D (adding z=0 explicitly)
            i_hat = Arrow(axes.c2p(0, 0, 0), axes.c2p(1, 0, 0), buff=0, color=RED)
            j_hat = Arrow(axes.c2p(0, 0, 0), axes.c2p(0, 1, 0), buff=0, color=GREEN)
            
            basis_title = Tex("Basis Vectors Transformation").scale(0.7).to_edge(UP)
            self.play(FadeOut(title3), Write(basis_title))
            
            # Show basis vectors
            self.play(GrowArrow(i_hat), GrowArrow(j_hat))
            self.wait(1)
            
            # First transformation on basis vectors
            basis_title1 = Tex("Basis Vectors under Matrix $A$").scale(0.7).to_edge(UP)
            self.play(FadeOut(basis_title), Write(basis_title1))
            
            # Map basis vectors through matrix A (2D)
            new_i = Arrow(axes.c2p(0, 0, 0), axes.c2p(matrix1[0, 0], matrix1[1, 0], 0), buff=0, color=RED)
            new_j = Arrow(axes.c2p(0, 0, 0), axes.c2p(matrix1[0, 1], matrix1[1, 1], 0), buff=0, color=GREEN)
            
            self.play(Transform(i_hat, new_i), Transform(j_hat, new_j))
            self.wait(1)
            
            # Second transformation on basis vectors
            basis_title2 = Tex("Basis Vectors under $B \\times A$").scale(0.7).to_edge(UP)
            self.play(FadeOut(basis_title1), Write(basis_title2))
            
            # Map basis vectors through combined transformation (2D)
            i_transformed = np.dot(matrix2, np.array([matrix1[0, 0], matrix1[1, 0]]))
            j_transformed = np.dot(matrix2, np.array([matrix1[0, 1], matrix1[1, 1]]))
            
            final_i = Arrow(axes.c2p(0, 0, 0), axes.c2p(i_transformed[0], i_transformed[1], 0), buff=0, color=RED)
            final_j = Arrow(axes.c2p(0, 0, 0), axes.c2p(j_transformed[0], j_transformed[1], 0), buff=0, color=GREEN)
            
            self.play(Transform(i_hat, final_i), Transform(j_hat, final_j))
            self.wait(1)
        
        self.wait(2)
"""
    with open("matrix_visualization.py", "w", encoding="utf-8") as f:
        f.write(script_content)    
        """Create a Manim script file for matrix visualization"""
    matrix1_latex = matrix_to_latex_str(matrix1)
    matrix2_latex = matrix_to_latex_str(matrix2)
    result_matrix = np.dot(matrix2, matrix1)
    result_latex = matrix_to_latex_str(result_matrix)

    script_content = f"""# -*- coding: utf-8 -*-
from manim import *
import numpy as np

class MatrixMultiplicationScene(ThreeDScene):
    def construct(self):
        # Define matrices
        matrix1 = np.array({matrix1.tolist()})
        matrix2 = np.array({matrix2.tolist()})
        result = np.dot(matrix2, matrix1)
        
        # Define point vector
        input_point = np.array({point.tolist()})
        transformed_point = result @ input_point
        
        # Create coordinate system first
        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-5, 5, 1],
            x_length=6,
            y_length=6,
            z_length=6
        )
        
        # Animate creation of the axes
        self.play(Create(axes), run_time=2)
        self.wait(1)
        
        # Create vectors after axes is defined
        original_vec = Arrow(axes.c2p(0, 0, 0), axes.c2p(*input_point), buff=0, color=BLUE)
        transformed_vec = Arrow(axes.c2p(0, 0, 0), axes.c2p(*transformed_point), buff=0, color=YELLOW)

        point_label = Tex("Original Point").scale(0.5).next_to(original_vec.get_end(), RIGHT)
        transformed_label = Tex("Transformed Point").scale(0.5).next_to(transformed_vec.get_end(), RIGHT)

        self.play(GrowArrow(original_vec), Write(point_label))
        self.wait(1)
        self.play(GrowArrow(transformed_vec), Write(transformed_label))
        self.wait(2)
        
        # Display matrices
        matrix1_tex = MathTex(r"A = {matrix1_latex}").scale(0.8).to_corner(UL)
        matrix2_tex = MathTex(r"B = {matrix2_latex}").scale(0.8).next_to(matrix1_tex, DOWN, buff=1)
        equals_tex = MathTex(r"B \\times A =").scale(0.8).next_to(matrix2_tex, DOWN, buff=1)
        result_tex = MathTex(r"{result_latex}").scale(0.8).next_to(equals_tex, RIGHT)

        # Show matrices
        self.play(Write(matrix1_tex), Write(matrix2_tex))
        self.wait(1)
        self.play(Write(equals_tex), Write(result_tex))
        self.wait(1)
        
        self.move_camera(phi=45 * DEGREES, theta=-125 * DEGREES, run_time=1.5)
        self.wait(2)
        
        if matrix1.shape == (3, 3):
            # 3D transformation logic
             
            i_hat = Arrow(axes.c2p(0, 0, 0), axes.c2p(1, 0, 0), buff=0, color=RED)
            j_hat = Arrow(axes.c2p(0, 0, 0), axes.c2p(0, 1, 0), buff=0, color=GREEN)
            k_hat = Arrow(axes.c2p(0, 0, 0), axes.c2p(0, 0, 1), buff=0, color=BLUE)

            self.play(GrowArrow(i_hat), GrowArrow(j_hat), GrowArrow(k_hat))
            self.wait(1)

            # First transformation (matrix1)
            title1 = Tex("Transformation by Matrix $A$").scale(0.5).to_edge(UP)
            self.play(Write(title1))

            new_i = Arrow(axes.c2p(0, 0, 0), axes.c2p(*matrix1[:, 0]), buff=0, color=RED)
            new_j = Arrow(axes.c2p(0, 0, 0), axes.c2p(*matrix1[:, 1]), buff=0, color=GREEN)
            new_k = Arrow(axes.c2p(0, 0, 0), axes.c2p(*matrix1[:, 2]), buff=0, color=BLUE)

            self.play(Transform(i_hat, new_i), Transform(j_hat, new_j), Transform(k_hat, new_k))
            self.wait(1)

            # Second transformation (matrix2)
            title2 = Tex("Transformation by Matrix $B$").scale(0.5).to_edge(UP)
            self.play(FadeOut(title1), Write(title2))

            i_transformed = np.dot(matrix2, matrix1[:, 0])
            j_transformed = np.dot(matrix2, matrix1[:, 1])
            k_transformed = np.dot(matrix2, matrix1[:, 2])

            final_i = Arrow(axes.c2p(0, 0, 0), axes.c2p(*i_transformed), buff=0, color=RED)
            final_j = Arrow(axes.c2p(0, 0, 0), axes.c2p(*j_transformed), buff=0, color=GREEN)
            final_k = Arrow(axes.c2p(0, 0, 0), axes.c2p(*k_transformed), buff=0, color=BLUE)

            self.play(Transform(i_hat, final_i), Transform(j_hat, final_j), Transform(k_hat, final_k))

        else:
            # 2D logic

            # Unit vectors
            i_hat = Arrow(axes.c2p(0, 0), axes.c2p(1, 0), buff=0, color=RED)
            j_hat = Arrow(axes.c2p(0, 0), axes.c2p(0, 1), buff=0, color=GREEN)

            self.play(GrowArrow(i_hat), GrowArrow(j_hat))
            self.wait(1)

            # First transformation
            title1 = Tex("Transformation by Matrix $A$").scale(0.5).to_edge(UP)
            self.play(Write(title1))

            new_i = Arrow(axes.c2p(0, 0), axes.c2p(matrix1[0, 0], matrix1[1, 0]), buff=0, color=RED)
            new_j = Arrow(axes.c2p(0, 0), axes.c2p(matrix1[0, 1], matrix1[1, 1]), buff=0, color=GREEN)

            self.play(Transform(i_hat, new_i), Transform(j_hat, new_j))
            self.wait(1)

            # Second transformation
            title2 = Tex("Transformation by Matrix $B$").scale(0.5).to_edge(UP)
            self.play(FadeOut(title1), Write(title2))

            i_transformed = np.dot(matrix2, np.array([matrix1[0, 0], matrix1[1, 0]]))
            j_transformed = np.dot(matrix2, np.array([matrix1[0, 1], matrix1[1, 1]]))

            final_i = Arrow(axes.c2p(0, 0), axes.c2p(i_transformed[0], i_transformed[1]), buff=0, color=RED)
            final_j = Arrow(axes.c2p(0, 0), axes.c2p(j_transformed[0], j_transformed[1]), buff=0, color=GREEN)

            self.play(Transform(i_hat, final_i), Transform(j_hat, final_j))
            self.wait(1)

            # Combined transformation
            title3 = Tex("Combined Transformation ($B \\times A$)").scale(0.5).to_edge(UP)
            self.play(FadeOut(title2), Write(title3))

            combined_tex = MathTex(r"B \\times A = {result_latex}").scale(0.6).next_to(title3, DOWN)
            self.play(Write(combined_tex))
            self.wait(2)
"""
    with open("matrix_visualization.py", "w", encoding="utf-8") as f:
        f.write(script_content)

# GUI Setup
root = tk.Tk()
root.title("Matrix Transformation Visualizer")

style = ttk.Style()
style.configure("TFrame", padding=10)
style.configure("TButton", padding=6)

main_frame = ttk.Frame(root)
main_frame.pack(padx=10, pady=10)

# Matrix Dimensions
dim_frame = ttk.Frame(main_frame)
dim_frame.pack(fill=tk.X, pady=5)

ttk.Label(dim_frame, text="Matrix Dimensions:").pack(side=tk.LEFT)
rows_var = tk.StringVar(value="3")
ttk.Entry(dim_frame, width=3, textvariable=rows_var).pack(side=tk.LEFT, padx=5)
ttk.Label(dim_frame, text="x").pack(side=tk.LEFT)
cols_var = tk.StringVar(value="3")
ttk.Entry(dim_frame, width=3, textvariable=cols_var).pack(side=tk.LEFT)

# Function to update the point entry based on matrix size
def update_matrix_size(*args):
    try:
        # Ensure that the values for rows and columns are valid integers
        rows_str = rows_var.get().strip()  # Strip any surrounding spaces
        cols_str = cols_var.get().strip()  # Strip any surrounding spaces

        # Check if both rows and columns are valid numbers
        if rows_str.isdigit() and cols_str.isdigit():
            rows = int(rows_str)
            cols = int(cols_str)

            if rows == 2 and cols == 2:
                point_label.config(text="2D Point (x y):")
                point_entry.delete(0, tk.END)
                point_entry.insert(0, "1 1")  # Default 2D point
            elif rows == 3 and cols == 3:
                point_label.config(text="3D Point (x y z):")
                point_entry.delete(0, tk.END)
                point_entry.insert(0, "1 1 1")  # Default 3D point
            else:
                # Handle the case where rows and cols are not 2 or 3
                messagebox.showwarning("Warning", "Only 2x2 and 3x3 matrices are supported.")
        else:
            # If rows or columns are invalid, do nothing or show a warning
            messagebox.showerror("Invalid Input", "Matrix dimensions must be numbers.")
    except Exception as e:
        print(f"Error updating matrix size: {e}")
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# Matrix Inputs
matrix_frame = ttk.Frame(main_frame)
matrix_frame.pack(fill=tk.BOTH, expand=True, pady=10)

point_label = ttk.Label(matrix_frame, text="3D Point (x y z):")
point_label.grid(row=2, column=0, sticky="w")
point_entry = tk.Entry(matrix_frame, width=20)
point_entry.grid(row=3, column=0, padx=5, pady=5)
point_entry.insert(0, "1 1 1")  # Default point for 3x3 matrices

# Trace the changes in the matrix dimensions and update point input accordingly
rows_var.trace_add("write", update_matrix_size)
cols_var.trace_add("write", update_matrix_size)

ttk.Label(matrix_frame, text="Matrix A:").grid(row=0, column=0, sticky="w")
matrix1_text = tk.Text(matrix_frame, width=25, height=6)
matrix1_text.grid(row=1, column=0, padx=5, pady=5)
matrix1_text.insert("1.0", "1 0 0\n0 1 0\n0 0 1")  # Default identity matrix

ttk.Label(matrix_frame, text="Matrix B:").grid(row=0, column=1, sticky="w")
matrix2_text = tk.Text(matrix_frame, width=25, height=6)
matrix2_text.grid(row=1, column=1, padx=5, pady=5)
matrix2_text.insert("1.0", "2 0 0\n0 2 0\n0 0 2")  # Default scaling matrix

# Result
result_frame = ttk.Frame(main_frame)
result_frame.pack(fill=tk.X, pady=10)

ttk.Label(result_frame, text="Result (B × A):").pack(anchor="w")
result_text = tk.Text(result_frame, width=40, height=4)
result_text.pack(fill=tk.X)

# Buttons
button_frame = ttk.Frame(main_frame)
button_frame.pack(fill=tk.X, pady=10)

# Function to handle matrix calculation
def calculate_matrices():
    try:
        # Get matrix dimensions
        rows = int(rows_var.get())
        cols = int(cols_var.get())

        # Ensure valid matrix dimensions
        if not ((rows == 2 and cols == 2) or (rows == 3 and cols == 3)):
            messagebox.showwarning("Warning", "Only 2x2 and 3x3 matrices are supported.")
            return

        # Get and validate point
        point_str = point_entry.get()
        point = np.array([float(num) for num in point_str.strip().split()])
        if point.shape != (cols,):
            raise ValueError(f"Please enter a valid point with {cols} values.")

        # Parse matrices
        matrix1_str = matrix1_text.get("1.0", "end-1c")
        matrix2_str = matrix2_text.get("1.0", "end-1c")
        matrix1 = parse_matrix(matrix1_str, rows, cols)
        matrix2 = parse_matrix(matrix2_str, rows, cols)
        result = np.dot(matrix2, matrix1)

        result_text.delete("1.0", "end")
        result_text.insert("1.0", np.array2string(result, precision=2, separator=' '))

        # Visualization
        create_manim_file(matrix1, matrix2, point)

        status_label.config(text="Generating visualization...")
        root.update()

        if run_manim_visualization():
            status_label.config(text="Visualization complete!")
        else:
            status_label.config(text="Visualization failed")

    except Exception as e:
        messagebox.showerror("Error", str(e))

ttk.Button(
    button_frame, 
    text="Calculate & Visualize", 
    command=calculate_matrices
).pack(side=tk.LEFT)

status_label = ttk.Label(main_frame, text="Ready")
status_label.pack(fill=tk.X)

root.mainloop()