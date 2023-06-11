from pathlib import Path
import plotly.graph_objects as go
import random
import shutil
import os
import sys

def line_length(line):
    return ((line[1][0] - line[0][0]) ** 2 + (line[1][1] - line[0][1]) ** 2) ** 0.5

def oriented_area(A, B, C):
    return (B[0] - A[0]) * (C[1] - A[1]) - (B[1] - A[1]) * (C[0] - A[0])

def segments_intersect(A, B, C, D):
    return ((oriented_area(A, B, C) * oriented_area(A, B, D) <= 0) and
            (oriented_area(C, D, A) * oriented_area(C, D, B) <= 0))

def generate_random_lines(num_lines, x_range, y_range, filename='random_lines.png'):
    fig = go.Figure()

    # List of line segments represented as tuple of two points
    lines = []

    while len(lines) < num_lines:
        # Generate two random points for each line
        x1, x2 = random.uniform(x_range[0], x_range[1]), random.uniform(x_range[0], x_range[1])
        y1, y2 = random.uniform(y_range[0], y_range[1]), random.uniform(y_range[0], y_range[1])
        new_line = ((x1, y1), (x2, y2))

        # Check if the new line intersects with any existing line
        if not any(segments_intersect(line[0], line[1], new_line[0], new_line[1]) for line in lines):
            lines.append(new_line)

    for line in lines:
        fig.add_trace(go.Scatter(x=[line[0][0], line[1][0]], y=[line[0][1], line[1][1]], mode='lines'))

    fig.write_image(filename)
    fig.show()

def save_script(filename):

    # Get the full path of the currently running script
    script_path = os.path.abspath(sys.argv[0])
    
    # Use shutil to copy the file
    shutil.copy(script_path, filename)

if __name__ == '__main__':

    iteration = 4
    path = Path(f"NFT_{iteration:06d}")
    path.mkdir(exist_ok=True)

    # Use the function
    generate_random_lines(50, [-10, 10], [-10, 10], filename=path / "image.png")

    # Call the function with the filename you want to save the script as
    save_script(path / f'script.py')