import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from ..seaweed import Seaweed


class SeaweedPlot:
    """Class for plotting Seaweed objects using Matplotlib."""

    def __init__(self, seaweed: Seaweed):
        self.seaweed = seaweed

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

    def plot(self, ax: Axes | None = None, size: int = 5) -> Axes:
        """Renders the graph using Matplotlib."""

        n = self.seaweed.n

        if ax is None:
            _, ax = plt.subplots(figsize=(size, size))

        # Clean up the plot.
        ax.set_axis_off()
        ax.set_aspect("equal")
        ax.invert_yaxis()

        # Draw the outer bounding box.
        ax.plot([0, n, n, 0, 0], [0, 0, n, n, 0], color="black", lw=0.5)

        # Draw diagonal dotted line.
        ax.plot([0, n], [0, n], color="black", linestyle=":", lw=1)

        # Draw the lower staircase.
        x, y = 0, 0
        lower_x, lower_y = [x], [y]
        for block in self.seaweed.top_blocks:
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
        for block in self.seaweed.bottom_blocks:
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
        min_rows = self.seaweed._get_min_row()
        max_rows = self.seaweed._get_max_row()

        for column in range(n):
            for row in range(n):
                if min_rows[row] <= column <= max_rows[row]:
                    self._draw_astrisk(ax, column + 0.5, row + 0.5)

        return ax
