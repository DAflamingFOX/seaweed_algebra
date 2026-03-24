import math
from typing import Literal

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import PathPatch
from matplotlib.path import Path

from seaweed_algebra import Meander

from ._visual_util import generate_component_color_map


def _plot_bezier_curve(
    ax: Axes,
    left: int,
    right: int,
    depth: int,
    orientation: Literal["top", "bottom"],
    scale: float = 0.7,
    color: str = "black",
):
    width = right - left
    center = left + width / 2

    control_y = depth * scale

    if orientation == "bottom":
        control_y = -control_y

    verts = [(left, 0), (center, control_y), (right, 0)]

    # Tell MPL how to draw the path.
    codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3]

    path = Path(verts, codes)
    patch = PathPatch(path, facecolor="none", edgecolor=color, lw=1.5)
    ax.add_patch(patch)


def _plot_arcs(
    ax: Axes,
    partitions: list[int],
    orientation: Literal["top", "bottom"],
    arc_scale: float = 0.7,
    color_map: dict[int, str] | None = None,
):
    start_offset = 0
    for block in partitions:
        size = block - 1
        arc_offset = 0
        num_arcs = math.floor(block / 2)

        while size >= 1:
            left = start_offset + arc_offset
            right = start_offset + arc_offset + size

            arc_color = color_map.get(left, "black") if color_map else "black"
            _plot_bezier_curve(
                ax,
                left,
                right,
                num_arcs - arc_offset,
                orientation,
                arc_scale,
                arc_color,
            )

            size -= 2
            arc_offset += 1
        start_offset += block


def plot_meander(
    meander: Meander,
    ax: Axes | None = None,
    arc_scale: float = 0.7,
    color_cycles: bool = False,
) -> Axes:
    """Plots the stored Meander object onto a Matplotlib axis."""

    top_blocks = meander.top_blocks
    btm_blocks = meander.bottom_blocks
    n = meander.n

    top_max = max((math.floor(b / 2) for b in top_blocks), default=0)
    bottom_max = max((math.floor(b / 2) for b in btm_blocks), default=0)
    max_height = max(top_max, bottom_max)

    if ax is None:
        _, ax = plt.subplots()

    # Clean up the plot.
    ax.set_axis_off()
    ax.set_ylim(-max_height, max_height)

    color_map = generate_component_color_map(top_blocks, btm_blocks)

    # Draw a line of verticies, these are on the x-axis spaced 1 unit apart from 1-n.
    for i in range(n):
        ax.plot(
            i,
            0,
            marker=".",
            color=color_map.get(i, "black") if color_cycles else "black",
            markersize=5,
        )

    # Draw the arcs
    _plot_arcs(
        ax,
        top_blocks,
        "top",
        arc_scale,
        color_map=color_map if color_cycles else None,
    )
    _plot_arcs(
        ax,
        btm_blocks,
        "bottom",
        arc_scale,
        color_map=color_map if color_cycles else None,
    )

    return ax
