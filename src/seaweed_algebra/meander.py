import math
from enum import Enum
from typing import Literal, Self

from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import PathPatch
from matplotlib.path import Path


class Meander:
    class Move(Enum):
        BLOCK_ELIMINATION = "Bl"
        ROTATION_CONTRACTION = "R"
        PURE_CONTRACTION = "P"
        FLIP = "F"
        COMPONENT_DELETION = "C"

    def __init__(self, top_blocks: list[int], bottom_blocks: list[int]):
        if sum(top_blocks) != sum(bottom_blocks):
            raise ValueError("The sum of the top and bottom blocks must be equal.")

        self.n = sum(top_blocks)
        self.top_blocks = top_blocks
        self.bottom_blocks = bottom_blocks

    @classmethod
    def from_seaweed(cls, seaweed):
        return cls(seaweed.top_blocks, seaweed.bottom_blocks)

    def __eq__(self, other):
        if not isinstance(other, Meander):
            return NotImplemented

        return (
            self.top_blocks == other.top_blocks
            and self.bottom_blocks == other.bottom_blocks
        )

    # --- Visualization ---

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

    def draw_matplotlib(
        self,
        ax: Axes | None = None,
        vertex_spacing: float = 1.0,
        arc_scale: float = 0.7,
    ) -> Axes:

        top_max = max((math.floor(b / 2) for b in self.top_blocks), default=0)
        bottom_max = max((math.floor(b / 2) for b in self.bottom_blocks), default=0)
        max_height = max(top_max, bottom_max)

        if ax is None:
            _, ax = plt.subplots()

        # Clean up the plot.
        ax.set_axis_off()
        ax.set_ylim(-max_height, max_height)

        # Draw a line of verticies, these are on the x-axis spaced 1 unit apart from 1-n.
        ax.plot(list(range(self.n)), [0] * self.n, "k.", markersize=5)

        # Draw the arcs
        self._plot_arcs(ax, self.top_blocks, "top", arc_scale)
        self._plot_arcs(ax, self.bottom_blocks, "bottom", arc_scale)

        return ax

    # --- Mathematical Operations ---

    def block_elimination(self) -> Self:
        """
        If a_1 = 2b_1 then M(g) -> M' of type (b_1|a_2|...|a_m) / (b_2|b_3|...|b_t)
        """

        a, b = self.top_blocks, self.bottom_blocks

        if a[0] == 2 * b[0]:
            return Meander([b[0]] + a[1:], b[1:])

        return self

    def rotation_contraction(self) -> Self:
        """
        If b_1 < a_1 < 2b_1, then M(g) -> M' of type (b_1|a_2|...|a_m) / ((2b_1 - a_1)|b_2|...|b_t)
        """

        a, b = self.top_blocks, self.bottom_blocks

        if b[0] < a[0] and a[0] < 2 * b[0]:
            return Meander([b[0]] + a[1:], [2 * b[0] - a[0]] + b[1:])

        return self

    def pure_contraction(self) -> Self:
        """
        If a_1 > 2_b1, then M(g) -> M' of type ((a_1 - 2b_1)|b_1|a_2|...|a_m) / (b_2|b_3|...|b_t)
        """

        a, b = self.top_blocks, self.bottom_blocks

        if a[0] > 2 * b[0]:
            return Meander([a[0] - 2 * b[0], b[0]] + a[1:], b[1:])

        return self

    def flip(self) -> Self:
        """
        If a_1 < b_1, then M(g) -> M' of type (b_1|b_2|...|b_t) / (a_1|...|a_m)
        """

        a, b = self.top_blocks, self.bottom_blocks

        if a[0] < b[0]:
            return Meander(b, a)

        return self

    def component_deletion(self) -> tuple[Self, int]:
        """
        If a_1 = b_1 = c, then M(g) -> M' of type (a_2|...|a_m) / (b_2|...|b_t)
        """

        a, b = self.top_blocks, self.bottom_blocks

        if a[0] == b[0]:
            return Meander(a[1:], b[1:]), a[0]

        return self, 0

    # --- Sequences and Properties

    def _wind_down(self):
        """
        Generator which will continuously apply the next valid move until the Meander is the empty Meander.
        """
        curr = self
        while curr.n > 0:
            a1, b1 = curr.top_blocks[0], curr.bottom_blocks[0]

            if a1 == b1:
                curr, c = curr.component_deletion()
                yield Meander.Move.COMPONENT_DELETION, c
            elif a1 < b1:
                curr = curr.flip()
                yield Meander.Move.FLIP, 0
            elif a1 == 2 * b1:
                curr = curr.block_elimination()
                yield Meander.Move.BLOCK_ELIMINATION, 0
            elif b1 < a1 < 2 * b1:
                curr = curr.rotation_contraction()
                yield Meander.Move.ROTATION_CONTRACTION, 0
            elif a1 > 2 * b1:
                curr = curr.pure_contraction()
                yield Meander.Move.PURE_CONTRACTION, 0
            else:
                raise RuntimeError(f"No valid move. a_1={a1}, b_1={b1}")

    def signature(self) -> list[Move]:
        """
        Calculate the signature of this Meander.
        """

        return [move for move, _ in self._wind_down()]

    def homotopy_type(self) -> list[int]:
        """
        Calculate the homotopy type of this Meander.
        """

        return [
            c_val
            for move, c_val in self._wind_down()
            if move == Meander.Move.COMPONENT_DELETION
        ]
