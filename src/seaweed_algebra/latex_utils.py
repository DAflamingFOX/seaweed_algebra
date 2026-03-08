from typing import Callable, Literal

from matplotlib.axes import Axes
import matplotlib.pyplot as plt


def export_as_pgf(
    plot_mpl: Callable[[], Axes],
    filename: str,
    texsystem: Literal["pdflatex", "lualatex", "xelatex"] = "pdflatex",
) -> None:
    if not filename.endswith(".pgf"):
        filename += ".pgf"

    pgf_config = {"pgf.texsystem": texsystem}

    with plt.rc_context(pgf_config):
        # Create a fresh figure using the supplied callable.
        ax = plot_mpl()
        fig = ax.get_figure()

        fig.savefig(filename, bbox_inches="tight", transparent=True)

        plt.close(fig)
