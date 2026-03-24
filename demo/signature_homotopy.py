from matplotlib import pyplot as plt

from seaweed_algebra import Meander
from seaweed_algebra.visual import plot_meander

# Create the Meander 17|3 by 10|4|6
m = Meander([17, 3], [10, 4, 6])

# Compute the signature, this returns a list of moves that constitutes the signature.
moves = m.signature()

# Calculate the Homotopy type, H(c_1, ..., c_h), this returns a list of c values.
homotopy = m.homotopy()

# Print our results.
homotopy_type = f"H({','.join(map(str, homotopy))})"
print(f"\nThe signature of {m} is: {''.join(m.value for m in moves)}")
print(f"\nThe homotopy type of {m} is: {homotopy_type}")

# Display the plots
_, ax_dict = plt.subplot_mosaic("AA.B", figsize=(10, 3))

plot_meander(m, ax=ax_dict["A"])
ax_dict["A"].set_title(
    rf"Meander of type $\frac{{{str(m).split(' / ')[0]}}}{{{str(m).split(' / ')[1]}}}$"
)

m_homotopy = Meander(homotopy, homotopy)
plot_meander(m_homotopy, ax=ax_dict["B"], arc_scale=0.5)
ax_dict["B"].set_title(homotopy_type)

plt.show()
