import math
from typing import Literal

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import PathPatch
from matplotlib.path import Path

from ..meander import Meander


class MeanderPlot:
    """Class for plotting Meander objects using Matplotlib."""

    def __init__(self, meander: Meander):
        self.meander = meander

    def _plot_bezier_curve(
        self,
        ax: Axes,
        left: int,
        right: int,
        depth: int,
        orientation: Literal["top", "bottom"],
        scale: float = 0.7,
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
        patch = PathPatch(path, facecolor="none", edgecolor="black")
        ax.add_patch(patch)

    def _plot_arcs(
        self,
        ax: Axes,
        partitions: list[int],
        orientation: Literal["top", "bottom"],
        arc_scale: float = 0.7,
    ):
        start_offset = 0
        for block in partitions:
            size = block - 1
            arc_offset = 0
            num_arcs = math.floor(block / 2)
            while size >= 1:
                left = start_offset + arc_offset
                right = start_offset + arc_offset + size
                self._plot_bezier_curve(
                    ax, left, right, num_arcs - arc_offset, orientation, arc_scale
                )
                size -= 2
                arc_offset += 1
            start_offset += block

    def plot(
        self,
        ax: Axes | None = None,
        arc_scale: float = 0.7,
    ) -> Axes:
        """Plots the stored Meander object onto a Matplotlib axis."""

        top_blocks = self.meander.top_blocks
        bottom_blocks = self.meander.bottom_blocks
        n = self.meander.n

        top_max = max((math.floor(b / 2) for b in top_blocks), default=0)
        bottom_max = max((math.floor(b / 2) for b in bottom_blocks), default=0)
        max_height = max(top_max, bottom_max)

        if ax is None:
            _, ax = plt.subplots()

        # Clean up the plot.
        ax.set_axis_off()
        ax.set_ylim(-max_height, max_height)

        # Draw a line of verticies, these are on the x-axis spaced 1 unit apart from 1-n.
        ax.plot(list(range(n)), [0] * n, "k.", markersize=5)

        # Draw the arcs
        self._plot_arcs(ax, top_blocks, "top", arc_scale)
        self._plot_arcs(ax, bottom_blocks, "bottom", arc_scale)

        return ax
