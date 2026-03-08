# Seaweed Algebra
<!--
![PyPI - Version](https://img.shields.io/pypi/v/seaweed_algebra)
![PyPI - License](https://img.shields.io/pypi/l/seaweed_algebra)
-->
[![CI Tests & Build](https://github.com/DAflamingFOX/seaweed_algebra/actions/workflows/tests.yml/badge.svg)](https://github.com/DAflamingFOX/seaweed_algebra/actions/workflows/tests.yml)

A Python library for dealing with seaweed algebra.

## Installation
<!--

The package is only going to be on pypi if we're publishing it, for now, the namespace is simply reserved with an example project.

### Release version

The Seaweed Algebra package is available directly from [pypi.](https://pypi.org/project/seaweed-algebra/)

You can install it via:
```bash
pip install seaweed-algebra
```

-->
### Install from GitHub

To install the library directly from GitHub simply run the following:

```bash
pip install git+https://github.com/daflamingfox/seaweed_algebra
```

Additionally, you can specify a specific version by appending `@VERSION` to the link, where `@VERSION` can be:
- A specific branch, such as `@main` (the default if no `@VERSION` is provided)
- A specific tag, such as `@v0.0.5`
- A specific commit hash, such as `@c87aad3`

### Local Development

To develop locally, you can use the `-e` flag in `pip` which will create install the package as 'editable', meaning, if you update the source files, then the package is automatically rebuilt for you.

To be more direct:

1. Clone this repository using:

    ```bash
    git clone https://github.com/daflamingfox/seaweed_algebra
    ```
2. Open the project directory using:

    ```bash
    cd seaweed_algebra
    ```
3. Install the project as an editable package using:

    ```bash
    pip install -e .
    ```

Now, any changes you make to the library will immediately be represented in your installed version.

## Usage

### Create a Seaweed object

```python
from seaweed_algebra import Seaweed

top_blocks = [4,1]
bottom_blocks = [2,1,2]

# Create a Seaweed object directly from blocks...
sw = Seaweed(top_blocks, bottom_blocks)

# Or if you already have a Meander object...
sw = Seaweed.from_meander(meander)
```

### Create a Meander object

```python
from seaweed_algebra import Meander

top_blocks = [4,1]
bottom_blocks = [2,1,2]

# Create a Meander object directly from blocks...
m = Meander(top_blocks, bottom_blocks)

# Or if you already have a Seaweed object...
m = Meander.from_seaweed(seaweed)
```

### Generate matplotlib

![Demo mpl](/assets/demo_mpl_4_1_by_2_1_2.png)

```python
import matplotlib.pyplot as plt

from seaweed_algebra import Meander, Seaweed

# Create a Seaweed and Meander object.
sw = Seaweed([4, 1], [2, 1, 2])
m = Meander.from_seaweed(sw)

# Create a 1x2 figure
fig, (ax1, ax2) = plt.subplots(1, 2)

# Generate each plot
sw.draw_matplotlib(ax=ax1)
m.draw_matplotlib(ax=ax2, arc_scale=0.5)

# Add some descriptors to the figure.
ax1.set_title(r"Seaweed")
ax2.set_title(r"Meander")
fig.suptitle(r"Seaweed and Meander of type $\frac{4|1}{2|1|2}$.")
fig.tight_layout()

# Show the generate figure.
plt.show()
```

### Export matplotlib as pgfplots for LaTeX

```python
from seaweed_algebra import Meander, Seaweed
from seaweed_algebra.latex_utils import export_as_pgf

# Create the Seaweed object.
sw = Seaweed([4, 1], [2, 1, 2])

# Provide a matplotlib plotting function, and the desired output file.
# The file can then be used in your .tex source using \usepackage{pgf}.
export_as_pgf(sw.draw_matplotlib, "./output/seaweed.pgf")
```

## License

This work is licensed under the [GNU Lesser General Public License](https://www.gnu.org/licenses/lgpl-3.0.en.html#license-text).