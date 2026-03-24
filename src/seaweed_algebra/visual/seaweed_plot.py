from typing import Literal

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

from seaweed_algebra import Seaweed

from ._visual_util import generate_component_color_map


def _draw_astrisk(ax, x: float, y: float, radius: float = 0.15):
    """Draws a 6-point asterisk using matplotlib coordinates so it is scalable.

    Args:
        ax (_type_): The matplotlib Axes object.
        x (_type_): The x coordinate of the astrisk.
        y (_type_): The y coordinate of the astrisk.
        radius (float, optional): The size of the astrisk. Defaults to 0.15.
    """

    line_width = 1
    capstyle = "round"

    ax.plot(
        [x, x],
        [y - radius, y + radius],
        color="black",
        lw=line_width,
        solid_capstyle=capstyle,
    )

    # dx = radius * math.cos(math.pi / 180 * 30)
    # dy = radius * math.sin(math.pi / 180 * 30)
    dx = radius * 0.866
    dy = radius * 0.5

    ax.plot(
        [x - dx, x + dx],
        [y - dy, y + dy],
        color="black",
        lw=line_width,
        solid_capstyle=capstyle,
    )
    ax.plot(
        [x - dx, x + dx],
        [y + dy, y - dy],
        color="black",
        lw=line_width,
        solid_capstyle=capstyle,
    )


def _draw_dot(ax: Axes, x: float, y: float, size: float = 5):
    ax.plot(x, y, "k.", markersize=size)


def plot_seaweed(
    seaweed: Seaweed,
    ax: Axes | None = None,
    size: int = 5,
    nonzero_element: Literal["*", "."] = "*",
    draw_diagonal: bool = True,
    draw_meander: bool = False,
    color_cycles: bool = False,
) -> Axes:
    """Renders the graph using Matplotlib."""

    n = seaweed.n

    if ax is None:
        _, ax = plt.subplots(figsize=(size, size))

    # Clean up the plot.
    ax.set_axis_off()
    ax.set_aspect("equal")
    ax.invert_yaxis()

    # Draw the outer bounding box.
    ax.plot([0, n, n, 0, 0], [0, 0, n, n, 0], color="black", lw=0.5)

    if draw_diagonal:
        ax.plot([0, n], [0, n], color="black", linestyle=":", lw=1)

    # Draw the lower staircase.
    x, y = 0, 0
    lower_x, lower_y = [x], [y]
    for block in seaweed.top_blocks:
        # Go down.
        y += block
        lower_x.append(x)
        lower_y.append(y)

        # Go right.
        x += block
        lower_x.append(x)
        lower_y.append(y)

    ax.plot(lower_x, lower_y, color="black", lw=2, solid_joinstyle="miter")

    # Draw the upper staircase.
    x, y = 0, 0
    upper_x, upper_y = [x], [y]
    for block in seaweed.bottom_blocks:
        # Go right.
        x += block
        upper_x.append(x)
        upper_y.append(y)

        # Go down.
        y += block
        upper_x.append(x)
        upper_y.append(y)

    ax.plot(upper_x, upper_y, color="black", lw=2, solid_joinstyle="miter")

    # Fill the non-zero area.
    min_rows = seaweed._get_min_row()
    max_rows = seaweed._get_max_row()

    for column in range(n):
        for row in range(n):
            if min_rows[row] <= column <= max_rows[row]:
                x = column + 0.5
                y = row + 0.5
                match nonzero_element:
                    case "*":
                        _draw_astrisk(ax, x, y)
                    case ".":
                        _draw_dot(ax, x, y)

    if draw_meander:
        color_map = generate_component_color_map(
            seaweed.top_blocks, seaweed.bottom_blocks
        )

        def plot_meander(blocks: list[int], is_top: bool):
            start_offset = 0
            for block in blocks:
                size = block - 1
                arc_offset = 0
                while size >= 1:
                    left = start_offset + arc_offset
                    right = start_offset + arc_offset + size

                    # Fetch the color for this specific component
                    arc_color = color_map[left] if color_cycles else "black"

                    if is_top:
                        x = np.array([right - size, left, left + size]) + 0.5
                        y = np.array([left, right, right]) + 0.5
                    else:
                        x = np.array([left + size, right, right - size]) + 0.5
                        y = np.array([right, left, left]) + 0.5

                    ax.plot(
                        x,
                        y,
                        color=arc_color,
                        linewidth=1.5,
                        solid_joinstyle="round",
                    )
                    size -= 2
                    arc_offset += 1
                start_offset += block

        plot_meander(seaweed.top_blocks, True)
        plot_meander(seaweed.bottom_blocks, False)

    return ax
