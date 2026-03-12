import math
from enum import Enum, auto
from typing import Literal, Self

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

    def __eq__(self, other):
        if not isinstance(other, Meander):
            return NotImplemented

        return (
            self.top_blocks == other.top_blocks
            and self.bottom_blocks == other.bottom_blocks
        )

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
        self, ax=None, vertex_spacing: float = 1.0, arc_scale: float = 0.7
    ) -> Axes:

        n = self.n

        top_max = max((math.floor(b / 2) for b in self.top_blocks), default=0)
        bottom_max = max((math.floor(b / 2) for b in self.bottom_blocks), default=0)
        max_height = max(top_max, bottom_max)

        if ax is None:
            _, ax = plt.subplots()

        # ax.set_xlim(-0.5, n + 0.5)
        ax.set_ylim(-max_height, max_height)

        # Set the aspect ratio to be square.
        # ax.set_aspect("equal")
        # Remove the axes.
        ax.set_axis_off()

        # Draw a line of verticies, these are on the x-axis spaced 1 unit apart from 1-n.
        ax.plot([x for x in range(n)], [0 for y in range(n)], "k.", markersize=5)

        # Draw the arcs
        self._plot_arcs(ax, self.top_blocks, "top", arc_scale)
        self._plot_arcs(ax, self.bottom_blocks, "bottom", arc_scale)

        return ax

    def block_elimination(self) -> Self:
        """
        If a_1 = 2b_1 then M(g) -> M' of type (b_1|a_2|...|a_m) / (b_2|b_3|...|b_t)
        """

        a = self.top_blocks.copy()
        b = self.bottom_blocks.copy()

        if a[0] == 2 * b[0]:
            # Change the first element of a to be from b.
            a[0] = b[0]
            # Remove the first element from b.
            b = b[1:]

        return Meander(a, b)

    def rotation_contraction(self) -> Self:
        """
        If b_1 < a_1 < 2b_1, then M(g) -> M' of type (b_1|a_2|...|a_m) / ((2b_1 - a_1)|b_2|...|b_t)
        """

        a = self.top_blocks.copy()
        b = self.bottom_blocks.copy()

        if b[0] < a[0] and a[0] < 2 * b[0]:
            a1 = a[0]
            # Change the first element of a to be from b.
            a[0] = b[0]
            # Change the first element of b to be (2*b1 - a1)
            b[0] = 2 * b[0] - a1

        return Meander(a, b)

    def pure_contraction(self) -> Self:
        """
        If a_1 > 2_b1, then M(g) -> M' of type ((a_1 - 2b_1)|b_1|a_2|...|a_m) / (b_2|b_3|...|b_t)
        """

        a = self.top_blocks.copy()
        b = self.bottom_blocks.copy()

        a1 = a[0]
        b1 = b[0]
        if a1 > 2 * b1:
            # Insert a_1-2b_1 into the start of a.
            # So now a is: a_1-2b_1|a_1|a_2|...|a_m
            a.insert(0, a1 - 2 * b1)
            # Replace a_1 with b_1
            a[1] = b1
            # Remove the first element from b
            b = b[1:]

        return Meander(a, b)

    def flip(self) -> Self:
        """
        If a_1 < b_1, then M(g) -> M' of type (b_1|b_2|...|b_t) / (a_1|...|a_m)
        """

        a = self.top_blocks.copy()
        b = self.bottom_blocks.copy()

        if a[0] < b[0]:
            # Flip the meander.
            return Meander(b, a)

        return self

    def component_deletion(self) -> tuple[Self, int]:
        """
        If a_1 = b_1 = c, then M(g) -> M' of type (a_2|...|a_m) / (b_2|...|b_t)
        """

        a = self.top_blocks.copy()
        b = self.bottom_blocks.copy()

        # If a_1 == b_1, then set c equal to that, else leave it as 0
        c = a[0] if a[0] == b[0] else 0
        # If c != 0 (a_1 == b_1), then return the Meander,
        # with the first element of each block removed,
        # otherwise, return the Meander as is.
        return [Meander(a[1:], b[1:]) if c != 0 else self, c]

    class Move(Enum):
        BLOCK_ELIMINATION = auto()
        ROTATION_CONTRACTION = auto()
        PURE_CONTRACTION = auto()
        FLIP = auto()
        COMPONENT_DELETION = auto()

    def signature(self) -> list[Move]:
        """
        Calculate the signature of this Meander.
        """

        # Is this as simple as looping through Bl, R, P, F, C(c) until we get an empty meander?

        current_meander: Meander = Meander(self.top_blocks, self.bottom_blocks)
        moves: list[Meander.Move] = []

        def perform_move(
            curr: Meander, move_func: callable[..., Meander], move: Meander.Move
        ) -> Meander:
            m = move_func()
            if curr != m:
                moves.append(move)
            return m

        while True:
            current_meander = perform_move(
                current_meander,
                current_meander.block_elimination,
                Meander.Move.BLOCK_ELIMINATION,
            )
            current_meander = perform_move(
                current_meander,
                current_meander.rotation_contraction,
                Meander.Move.ROTATION_CONTRACTION,
            )
            current_meander = perform_move(
                current_meander,
                current_meander.pure_contraction,
                Meander.Move.PURE_CONTRACTION,
            )
            current_meander = perform_move(
                current_meander, current_meander.flip, Meander.Move.FLIP
            )
            current_meander = perform_move(
                current_meander,
                lambda: current_meander.component_deletion()[0],
                Meander.Move.COMPONENT_DELETION,
            )

            if current_meander.n == 0:
                break

        return moves

    def homotopy_type(self) -> list[int]:
        """
        Calculate the homotopy type of this Meander.
        """

        m = Meander(self.top_blocks, self.bottom_blocks)
        moves = self.signature()

        c_vals = []

        for move in moves:
            match move:
                case Meander.Move.BLOCK_ELIMINATION:
                    m = m.block_elimination()
                case Meander.Move.ROTATION_CONTRACTION:
                    m = m.rotation_contraction()
                case Meander.Move.PURE_CONTRACTION:
                    m = m.pure_contraction()
                case Meander.Move.FLIP:
                    m = m.flip()
                case Meander.Move.COMPONENT_DELETION:
                    m, c = m.component_deletion()
                    c_vals.append(c)

        return c_vals
