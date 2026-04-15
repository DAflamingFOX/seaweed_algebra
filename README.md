# Seaweed Algebra

![GitHub Actions - CI](https://img.shields.io/github/actions/workflow/status/daflamingfox/seaweed_algebra/ci.yml?label=CI)
![PyPI - Version](https://img.shields.io/pypi/v/seaweed_algebra)
![PyPI - License](https://img.shields.io/pypi/l/seaweed_algebra)

A Python library for computing, plotting, and other tasks related to seaweed algebra.

## Setup

### Requirements

- [Python](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/) (typically installed alongside python)

### Development Environments

Any Python or Jupyter Notebook development environment will work!

Here are a few recommendations if you need a place to start:

- [Visual Studio Code](https://code.visualstudio.com/) (very popular)
    - Install the [Python Extension.](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
    - If you want to use notebooks, you'll want the [Jupyter Extension](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) as well.
- [Google Colab](https://colab.research.google.com/) (cloud based)
    - Try opening [this demo file](https://colab.research.google.com/github/DAflamingFOX/seaweed_algebra/blob/main/examples/basic_usage.ipynb) in Colab.
- [JupyterLab / Jupyter Notebook](https://jupyter.org/)

### Installation

Running the following command will tell pip to download the most recently published version from the [Python Package Index.](https://pypi.org/project/seaweed-algebra/)

```bash
pip install seaweed-algebra
```

<details>

<summary>Advanced installation information</summary>

If you wish to use a version of the library that is unpublished, you can do so in a few ways:

#### Installing from GitHub

```bash
pip install git+https://github.com/daflamingfox/seaweed_algebra
```

Additionally, you can specify a specific version by appending `@VERSION` to the link, where `@VERSION` can be:
- A specific branch, such as `@main` (the default if no `@VERSION` is provided)
- A specific tag, such as `@v0.0.5`
- A specific commit hash, such as `@c87aad3`

#### Installing from a local copy

If you want to change the source code yourself and test your changes, you can install your local copy of the library like such:

```bash
# This command assumes you are running it from the base project directory.
pip install -e .
```

Using the `-e` flag tells pip to install the package as 'editable,' so that any changes you make to the source code is immediately reflected in the installed version on your machine.
</details>

## Usage

See the [example](examples/README.md) folder for examples and demos for how to use the library.

## License

This work is licensed under the [GNU Lesser General Public License](https://www.gnu.org/licenses/lgpl-3.0.en.html#license-text).