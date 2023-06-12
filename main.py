from pathlib import Path
import plotly.graph_objects as go
import random
import shutil
import os
import sys
import plotly
from faker import Faker
from tqdm import tqdm

fake = Faker()
GOLDEN_RATIO = (1 + 5 ** 0.5) / 2


def generate_random_colors(num_colors):
    colors = []
    for _ in range(num_colors):
        # Generate random RGB values between 0 and 255
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)

        # Create the color string in the format "rgb(r, g, b)"
        color = f"rgb({red}, {green}, {blue})"

        colors.append(color)

    return colors


def line_length(line):
    return ((line[1][0] - line[0][0]) ** 2 + (line[1][1] - line[0][1]) ** 2) ** 0.5


def oriented_area(A, B, C):
    return (B[0] - A[0]) * (C[1] - A[1]) - (B[1] - A[1]) * (C[0] - A[0])


def segments_intersect(A, B, C, D):
    return (
        (oriented_area(A, B, C) * oriented_area(A, B, D) <= 0)
        and (oriented_area(C, D, A) * oriented_area(C, D, B) <= 0)
    )
def generate_random_point(x_range, y_range):
    return (random.uniform(x_range[0], x_range[1]), random.uniform(y_range[0], y_range[1]))

def generate_random_line(x_range, y_range, line_length):
    p1 = generate_random_point(x_range, y_range)
    p2 = (p1[0], p1[1] + line_length)
    return (p1,p2)

def generate_random_lines(num_lines, x_range, y_range, filename="random_lines.png"):
    fig = go.Figure(
        layout=go.Layout(
            paper_bgcolor="black",
            plot_bgcolor="black",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        )
    )

    # Generate a random line length
    starting_line_length = 1

    # List of line segments represented as tuple of two points
    lines = [generate_random_line(x_range, y_range, starting_line_length)]

    # Get color scale
    colorscale = generate_random_colors(1000)
    color_idx = -1
    direction = False
    pbar = tqdm(total=num_lines)
    max_attempts = 2
    attempt = 0
    new_color = [False]
    nc = False
    line_length = starting_line_length

    while len(lines) < num_lines:
        attempt += 1
        # Choose randomly between a vertical and a horizontal line
        if direction:
            # Vertical line: x-coordinates are equal, y-coordinates vary
            x1 = x2 = lines[-1][1][0]
            y1, y2 = lines[-1][1][1], lines[-1][1][1] + line_length * (1 if random.random() < 0.5 else -1)
        else:
            # Horizontal line: y-coordinates are equal, x-coordinates vary
            y1 = y2 = lines[-1][1][1]
            x1, x2 = lines[-1][1][0], lines[-1][1][0] + line_length * (1 if random.random() < 0.5 else -1)


        if attempt >= max_attempts:
            new_line = generate_random_line(x_range, y_range, line_length)
            nc = True
        else:
            new_line = (lines[-1][1], (x2, y2))
            line_length *= 0.9
            nc = False
        
        # Check if the new line intersects with any existing line
        if not any(
            segments_intersect(line[0], line[1], new_line[0], new_line[1])
            for line in lines[:-1]
        ):
            direction = not direction
            lines.append(new_line)
            pbar.update(1)
            attempt = 0
            new_color.append(nc)
            line_length = starting_line_length

    for i, line in enumerate(lines):

        if new_color[i]:
            color_idx = color_idx + 1

        fig.add_trace(
            go.Scatter(
                x=[line[0][0], line[1][0]],
                y=[line[0][1], line[1][1]],
                mode="lines",
                line=dict(color=colorscale[color_idx], width=2),
            )
        )

    fig.update_layout(
        template="plotly_dark", showlegend=False, title_text=fake.sentence(nb_words=4)
    )
    fig.write_image(filename, height=1080, width=1920)
    fig.show()


def save_script(filename):
    # Get the full path of the currently running script
    script_path = os.path.abspath(sys.argv[0])

    # Use shutil to copy the file
    shutil.copy(script_path, filename)


if __name__ == "__main__":

    iteration = 34
    n_variations = 1
    for variation in range(0, n_variations):
        path = Path(f"NFT_{iteration:06d}") / f"{variation:02d}"
        path.mkdir(parents=True, exist_ok=True)

        # Use the function
        generate_random_lines(1000, [-10, 10], [-10, 10], filename=path / "image.png")

        # Copy to working image
        shutil.copy(path / "image.png", "working_image.png")

        # Call the function with the filename you want to save the script as
        save_script(path / f"script.py")
