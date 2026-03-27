import matplotlib.pyplot as plt

from seaweed_algebra import Meander, Seaweed
from seaweed_algebra.visual import plot_meander, plot_seaweed

# Create Meanders and Seaweeds.
m = Meander([17, 3], [10, 4, 6])
cm = m.component()
sw = Seaweed.from_meander(m)

m2 = Meander([7, 10, 6, 5], [7, 3, 4, 3, 1, 2, 2, 2, 1, 3])
cm2 = m2.component()
sw2 = Seaweed.from_meander(m2)

# Create the figure.
fig = plt.figure(figsize=(12, 9), layout="constrained")
fig.suptitle("Distinguishing Meander Paths")

# Create two subfigures
subfigs = fig.subfigures(2, 1)

# Subfigure 1 has meander, component meander, and seaweed 1
subfigs[0].suptitle(str(m))
ax = subfigs[0].subplots(1, 3)
ax[0].set_title("Meander")
ax[1].set_title("Component Meander")
ax[2].set_title("Seaweed")

# Color the cycles differently, and show the meander within the seaweed graph.
plot_meander(m, ax[0], color_cycles=True, arc_scale=0.5)
plot_meander(cm, ax[1], color_cycles=True, arc_scale=0.5)
plot_seaweed(
    sw,
    ax[2],
    nonzero_element=".",
    draw_diagonal=False,
    draw_meander=True,
    color_cycles=True,
)

# Subfigure 2 has the meander, component meander, and seaweed 2
subfigs[1].suptitle(str(m2))
ax = subfigs[1].subplots(1, 3)
ax[0].set_title("Meander")
ax[1].set_title("Component Meander")
ax[2].set_title("Seaweed")

# Color the cycles differently, and show the meander within the seaweed graph.
plot_meander(m2, ax[0], color_cycles=True, arc_scale=0.5)
plot_meander(cm2, ax[1], color_cycles=True, arc_scale=0.5)
plot_seaweed(
    sw2,
    ax[2],
    nonzero_element=".",
    draw_diagonal=False,
    draw_meander=True,
    color_cycles=True,
)

# Show the figure.
plt.show()
