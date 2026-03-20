from functools import partial

from matplotlib import pyplot as plt

from seaweed_algebra import Meander, Seaweed
from seaweed_algebra.latex_utils import export_as_pgf
from seaweed_algebra.visual import plot_meander, plot_seaweed

# Create a few seaweeds and meanders.
sw1 = Seaweed([4, 1], [2, 1, 2])
m1 = Meander([4, 1], [2, 1, 2])

sw2 = Seaweed([17, 3], [10, 4, 6])
m2 = Meander.from_seaweed(sw2)

m3 = Meander([16, 6, 12, 1, 1], [8, 4, 20, 4])
sw3 = Seaweed.from_meander(m3)

# Plot the afformentioned seaweeds and meanders.
f1, (f1_ax1, f1_ax2) = plt.subplots(1, 2, figsize=(7, 3), layout="constrained")

plot_meander(m1, f1_ax1)
plot_seaweed(sw1, f1_ax2)

f1_ax1.set_title("Meander")
f1_ax2.set_title("Seaweed")
f1.suptitle(r"Meander and Seaweed of type $\frac{4|1}{2|1|2}$.")


def generate_fig2():
    f2, (f2_ax1, f2_ax2) = plt.subplots(1, 2, figsize=(7, 3), layout="constrained")
    plot_seaweed(sw2, f2_ax2, nonzero_element=".", draw_diagonal=False)
    plot_meander(m2, ax=f2_ax1)

    f2_ax1.set_title("Meander")
    f2_ax2.set_title("Seaweed")
    f2.suptitle(r"Meander and Seaweed of type $\frac{17|3}{10|4|6}$.")

    return f2


generate_fig2()

# You don't need to provide a MPL Axes object...
plot_meander(m3, arc_scale=0.5)

export_as_pgf(partial(plot_seaweed, sw1), "./graphs/seaweed1.pgf")
export_as_pgf(generate_fig2, "./graphs/fig2")
export_as_pgf(partial(plot_meander, m3, arc_scale=0.5), "./graphs/meander3")

plt.show()
