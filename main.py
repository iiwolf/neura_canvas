from pathlib import Path
import plotly.graph_objects as go
from matplotlib import cm
import random
import shutil
import os
import sys
import plotly
from faker import Faker
fake = Faker()
GOLDEN_RATIO = (1 + 5 ** 0.5) / 2

def oriented_area(A, B, C):
    return (B[0] - A[0]) * (C[1] - A[1]) - (B[1] - A[1]) * (C[0] - A[0])

def segments_intersect(A, B, C, D):
    return ((oriented_area(A, B, C) * oriented_area(A, B, D) <= 0) and
            (oriented_area(C, D, A) * oriented_area(C, D, B) <= 0))

def line_length(line):
    return ((line[1][0] - line[0][0]) ** 2 + (line[1][1] - line[0][1]) ** 2) ** 0.5

def generate_koch_snowflake(level, x1, y1, x2, y2):
    if level == 0:
        return [(x1, y1), (x2, y2)]

    # Calculate the length of each segment
    segment_length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 / 3

    # Calculate the angle between the segment and the x-axis
    angle = (2 * random.random() - 1) * 60  # Random angle deviation within -60 to 60 degrees

    # Calculate the coordinates of the midpoints
    x_mid = (x1 + x2) / 2
    y_mid = (y1 + y2) / 2

    # Calculate the coordinates of the outer points
    x_outer = (
        x_mid + segment_length * (2 ** 0.5 / 2) * (1 + random.uniform(-0.1, 0.1))
    )  # Random scaling within 0.9 to 1.1
    y_outer = y_mid + segment_length * (2 ** 0.5 / 2) * (1 + random.uniform(-0.1, 0.1))

    # Generate the lines for the Koch snowflake
    lines = []
    lines.extend(
        generate_koch_snowflake(
            level - 1, x1, y1, x_mid, y_mid
        )
    )
    lines.extend(
        generate_koch_snowflake(
            level - 1, x_mid, y_mid, x_outer * (1 + random.uniform(-0.05, 0.05)), y_outer
        )
    )
    lines.extend(
        generate_koch_snowflake(
            level - 1, x_outer * (1 + random.uniform(-0.05, 0.05)), y_outer, x_mid, y_mid
        )
    )
    lines.extend(
        generate_koch_snowflake(
            level - 1, x_mid, y_mid, x2, y2
        )
    )

    return lines


def generate_random_art(num_lines, x_range, y_range, level, filename="random_art.png"):
    fig = go.Figure(
        layout=go.Layout(
            paper_bgcolor="black",
            plot_bgcolor="black",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        )
    )

    # Generate Koch snowflake lines
    lines = generate_koch_snowflake(level, x_range[0], y_range[0], x_range[1], y_range[1])

    # Shuffle the lines randomly
    random.shuffle(lines)

    # Get color scale
    colorscale = plotly.colors.n_colors(
        "rgb(0, 200, 255)", "rgb(128, 0, 128)", len(lines), colortype="rgb"
    )

    for i, line in enumerate(lines[:num_lines]):
        fig.add_trace(
            go.Scatter(
                x=[line[0][0], line[1][0]],
                y=[line[0][1], line[1][1]],
                mode="lines",
                line=dict(color=colorscale[i], width=2),
            )
        )

    fig.update_layout(
        template="plotly_dark",
        showlegend=False,
        title_text=fake.sentence(nb_words=4),
    )
    fig.write_image(filename, height=1080, width=1920)
    fig.show()

def save_script(filename):

    # Get the full path of the currently running script
    script_path = os.path.abspath(sys.argv[0])
    
    # Use shutil to copy the file
    shutil.copy(script_path, filename)

if __name__ == '__main__':

    iteration = 19
    n_variations = 10
    for variation in range(0, n_variations):
        path = Path(f"NFT_{iteration:06d}") / f"{variation:02d}"
        path.mkdir(parents=True, exist_ok=True)

        # Use the function
        generate_random_art(50, [-10, 10], [-10, 10], 1, filename=path / "image.png")

        # Copy to working image
        shutil.copy(path / "image.png", "working_image.png")

        # Call the function with the filename you want to save the script as
        save_script(path / f'script.py')

