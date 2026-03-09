import math
from typing import Literal

from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import PathPatch
from matplotlib.path import Path


class Meander:
    def __init__(self, top_blocks: list[int], bottom_blocks: list[int]):
        if sum(top_blocks) != sum(bottom_blocks):
            raise ValueError("The sum of the top and bottom blocks must be equal.")

        self.n = sum(top_blocks)

        self.top_blocks = top_blocks
        self.bottom_blocks = bottom_blocks

    @classmethod
    def from_seaweed(cls, seaweed):
        return cls(seaweed.top_blocks, seaweed.bottom_blocks)

    def _plot_bezier_curve(
        self,
        ax: Axes,
        left: int,
        right: int,
        depth: int,
        scale: int,
        orientation: Literal["top", "bottom"],
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
        scale: int = 1,
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
                    ax, left, right, num_arcs - arc_offset, scale, orientation
                )
                size -= 2
                arc_offset += 1
            start_offset += block

    def draw_matplotlib(self, ax=None, size: int = 5, arc_scale: int = 1) -> Axes:

        n = self.n

        if ax is None:
            fig, ax = plt.subplots(figsize=(size, size))

        # Set the aspect ratio to be square.
        ax.set_aspect("equal")
        # Remove the default matplotlib border.
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        # Remove the axes.
        ax.set_axis_off()

        # Draw a line of verticies, these are on the x-axis spaced 1 unit apart from 1-n.
        ax.plot([x for x in range(n)], [0 for y in range(n)], "k.", markersize=5)

        # Draw the arcs
        self._plot_arcs(ax, self.top_blocks, "top", arc_scale)
        self._plot_arcs(ax, self.bottom_blocks, "bottom", arc_scale)

        return ax
