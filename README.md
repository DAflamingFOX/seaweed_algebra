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

See the `demo/` folder for demo examples for how to use the library.

## License

This work is licensed under the [GNU Lesser General Public License](https://www.gnu.org/licenses/lgpl-3.0.en.html#license-text).