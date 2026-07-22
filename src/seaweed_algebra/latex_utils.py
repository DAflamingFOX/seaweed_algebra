import os
from typing import Callable, Literal

import matplotlib.pyplot as plt


def export_as_pgf(
    plot_mpl: Callable,
    filename: str,
    texsystem: Literal["pdflatex", "lualatex", "xelatex"] = "pdflatex",
) -> None:
    """Export any Matplotlib Figure or Axes as a pgf plot file.

    Args:
        plot_mpl (Callable[[], Figure  |  Axes]): Function which generates a Matplotlib Figure or Axes object to be converted.
        filename (str): The filename (and path) of the output file.
        texsystem (Literal[&quot;pdflatex&quot;, &quot;lualatex&quot;, &quot;xelatex&quot;], optional): The TeX system to support. Defaults to "pdflatex".
    """
    # Append the pgf file extension if it wasn't provided.
    if not filename.endswith(".pgf"):
        filename += ".pgf"

    # Create parent directory if it doesn't exist.
    path = filename.rsplit("/", maxsplit=1)[0]
    os.makedirs(path, exist_ok=True)

    with plt.rc_context({"pgf.texsystem": texsystem}):
        # Create a fresh figure using the supplied callable.
        plot_mpl()

        plt.savefig(filename, bbox_inches="tight", transparent=True)

        plt.close()
