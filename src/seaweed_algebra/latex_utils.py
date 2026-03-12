from typing import Callable, Literal

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure


def export_as_pgf(
    plot_mpl: Callable[[], Figure | Axes],
    filename: str,
    texsystem: Literal["pdflatex", "lualatex", "xelatex"] = "pdflatex",
) -> None:
    if not filename.endswith(".pgf"):
        filename += ".pgf"

    pgf_config = {"pgf.texsystem": texsystem}

    with plt.rc_context(pgf_config):
        # Create a fresh figure using the supplied callable.
        x = plot_mpl()

        fig = x if isinstance(x, Figure) else x.get_figure()

        fig.savefig(filename, bbox_inches="tight", transparent=True)

        plt.close(fig)
