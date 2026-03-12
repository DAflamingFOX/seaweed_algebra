from matplotlib import pyplot as plt

from seaweed_algebra.meander import Meander

# Create the Meander 17|3 by 10|4|6
m = Meander([17, 3], [10, 4, 6])

# Compute the signature, this returns a list of moves that constitutes the signature.
moves = m.signature()

# Calculate the Homotopy type, H(c_1, ..., c_h), this returns a list of c values.
homotopy = m.homotopy_type()

# Print our results.
meander_name = (
    f"{'|'.join(map(str, m.top_blocks))} by {'|'.join(map(str, m.bottom_blocks))}"
)
homotopy_type = f"H({','.join(map(str, homotopy))})"
print(f"\nThe signature of {meander_name} is:\n{',\n'.join(m.name for m in moves)}")
print(f"\nThe homotopy type of {meander_name} is: {homotopy_type}")


# Display the plots
input("Press Enter to display the plots...\n")

_, ax_dict = plt.subplot_mosaic("AA.B", figsize=(10, 3))

m.draw_matplotlib(ax=ax_dict["A"])
ax_dict["A"].set_title(
    rf"Meander of type $\frac{{{meander_name.split(' by ')[0]}}}{{{meander_name.split(' by ')[1]}}}$"
)

m_homotopy = Meander(homotopy, homotopy)
m_homotopy.draw_matplotlib(ax=ax_dict["B"])
ax_dict["B"].set_title(homotopy_type)

plt.show()
