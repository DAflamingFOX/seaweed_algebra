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
    patch = PathPatch(path, facecolor="none", edgecolor=color, lw=1.5, zorder=2)
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

        while size >= 1:
            left = start_offset + arc_offset
            right = start_offset + arc_offset + size

            arc_color = color_map.get(left, "black") if color_map else "black"
            _plot_bezier_curve(
                ax,
                left,
                right,
                right - left,
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
    show_indices: bool = False,
    node_size: float = 14,
    font_size: float = 8,
) -> Axes:
    """Plots the stored Meander object onto a Matplotlib axis.

    Args:
        meander: The Meander instance to plot.
        ax: Optional Matplotlib Axes object.
        arc_scale: Scaling factor for the arc heights.
        color_cycles: If True, colors connected components/cycles distinctly.
        show_indices: If True, draws small circles containing index numbers instead of dots.
        node_size: Size of the node circles when show_indices is True.
        font_size: Font size of the index labels inside the circles.
    """

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

    # Draw a line of vertices, these are on the x-axis spaced 1 unit apart from 0 to n-1.
    for i in range(n):
        c = color_map.get(i, "black") if color_cycles else "black"
        if show_indices:
            ax.plot(
                i,
                0,
                marker="o",
                color=c,
                markerfacecolor="white",
                markeredgecolor=c,
                markeredgewidth=1.2,
                markersize=node_size,
                zorder=3,
            )
            ax.text(
                i,
                0,
                str(i + 1),
                ha="center",
                va="center_baseline",
                fontsize=font_size,
                fontname='serif',
                color="black",
                zorder=4,
            )
        else:
            ax.plot(
                i,
                0,
                marker=".",
                color=c,
                markersize=5,
                zorder=3,
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
