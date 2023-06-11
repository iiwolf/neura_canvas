from pathlib import Path
import plotly.graph_objects as go
import random
import shutil
import os
import sys

def generate_random_lines(num_lines, x_range, y_range, filename='random_lines.png'):
    fig = go.Figure()

    for _ in range(num_lines):
        # generate random slope and y-intercept
        slope = random.uniform(-10, 10)
        y_intercept = random.uniform(-10, 10)

        # generate x and y values for the line
        x_values = [random.uniform(x_range[0], x_range[1]) for _ in range(100)]
        y_values = [slope * x + y_intercept for x in x_values]

        fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines'))
    
    fig.write_image(filename)
    fig.show()


def save_script(filename):

    # Get the full path of the currently running script
    script_path = os.path.abspath(sys.argv[0])
    
    # Use shutil to copy the file
    shutil.copy(script_path, filename)

if __name__ == '__main__':

    iteration = 1
    path = Path(f"NFT_{iteration:06d}")
    path.mkdir(parents=True)

    # Use the function
    generate_random_lines(5, [-10, 10], [-10, 10], filename=path / "image.png")

    # Call the function with the filename you want to save the script as
    save_script(path / f'script.py')