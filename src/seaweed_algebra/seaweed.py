import matplotlib.pyplot as plt
from matplotlib.axes import Axes

import seaweed_algebra


class Seaweed:
    def __init__(self, top_blocks: list[int], bottom_blocks: list[int]):
        """
        Initialize the matrix representation of a seaweed algebra.

        Args:
            top_blocks (list[int]): A list of integers for the horizontal partitions.
            bottom_blocks (list[int]): A list of integers for the vertical partiton.
        """

        # Check that the sum of top == bot because the matrix must be square.
        if sum(top_blocks) != sum(bottom_blocks):
            raise ValueError("The sum of the top and bottom blocks must be equal.")

        self.n = sum(top_blocks)

        self.top_blocks = top_blocks
        self.bottom_blocks = bottom_blocks

    @classmethod
    def from_meander(cls, meander: seaweed_algebra.Meander):
        return cls(meander.top_blocks, meander.bottom_blocks)

    def _get_max_row(self) -> list[int]:
        """Get the index of the right-most non-zero element in the row, for all rows.

        Returns:
            list[int]: right-most non-zero column index in each i-th row.
        """
        rows = []
        offset = 0
        for block in self.bottom_blocks:
            for _ in range(block):
                rows.append(offset + block - 1)
            offset += block
        return rows

    def _get_min_row(self) -> list[int]:
        """Get the index of the left-most non-zero element in the row, for all rows.

        Returns:
            list[int]: left-most non-zero column index in each i-th row.
        """
        rows = []
        offset = 0
        for block in self.top_blocks:
            for _ in range(block):
                rows.append(offset)
            offset += block
        return rows

    def _draw_astrisk(self, ax, x: float, y: float, radius: float = 0.15):
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

    def draw_matplotlib(self, ax=None, size: int = 5) -> Axes:
        """Renders the graph using Matplotlib."""

        n = self.n

        if ax is None:
            _, ax = plt.subplots(figsize=(size, size))

        # Set the aspect ratio to be square.
        ax.set_aspect("equal")
        # Invert y because matrix origin is upper left.
        ax.invert_yaxis()
        # Remove the default matplotlib border.
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        # Remove the axes.
        ax.set_axis_off()

        # Draw the outer bounding box.
        ax.plot([0, n, n, 0, 0], [0, 0, n, n, 0], color="black", lw=0.5)

        # Draw diagonal dotted line.
        ax.plot([0, n], [0, n], color="black", linestyle=":", lw=1)

        # Draw the lower staircase.
        x, y = 0, 0
        lower_x, lower_y = [x], [y]
        for block in self.top_blocks:
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
        for block in self.bottom_blocks:
            # Go right.
            x += block
            upper_x.append(x)
            upper_y.append(y)

            # Go down.
            y += block
            upper_x.append(x)
            upper_y.append(y)

        ax.plot(upper_x, upper_y, color="black", lw=2, solid_joinstyle="miter")

        # Fill the valid area with stars.
        min_rows = self._get_min_row()
        max_rows = self._get_max_row()

        for column in range(n):
            for row in range(n):
                if min_rows[row] <= column <= max_rows[row]:
                    self._draw_astrisk(ax, column + 0.5, row + 0.5)

        return ax
