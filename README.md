# opinionated-mixins

[![PyPI - Version](https://img.shields.io/pypi/v/opinionated-mixins.svg)](https://pypi.org/project/opinionated-mixins)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/opinionated-mixins.svg)](https://pypi.org/project/opinionated-mixins)

Opinionated set of mixins. Implemented in Pydantic, SQLAlchemy, MongoEngine, ODMantic, etc.

-----

**Table of Contents**

- [opinionated-mixins](#opinionated-mixins)
  - [Installation](#installation)
  - [License](#license)
  - [Tasks](#tasks)

## Installation

```console
pip install opinionated-mixins
```

## Tasks

The commands below can also be executed using the [xc task runner](https://xcfile.dev/), which combines the usage instructions with the actual commands. Simply run `xc`, it will popup an interactive menu with all available tasks.

### `setup`

Setup the development environment.

```bash
brew install uv
```

### `install`

Install the dependencies.

run: once

```bash
uv sync --all-groups
uv run pre-commit install
```

### `upgrade`

Requires: Install

Upgrade the dependencies.

```bash
uv lock --upgrade
uv run pre-commit autoupdate
```

### `lint`

Requires: Install

Run the linter.

```bash
uv run ruff check .
uv run vulture src
```

### `lint-fix`

Requires: Install

Run the linter and fix the issues.

```bash
uv run ruff check . --fix
```

### `format`

Requires: Install

Run the formatter.

```bash
uv run ruff format .
```

### `pre-commit`

Requires: Install

Run the formatter.

```bash
uv run pre-commit run --all-files
```

### `test`

Requires: Install

Run the tests.

```bash
uv run pytest
```

### `ci`

Requires: install, lint-fix, format, test

Run the tests.

```bash
echo "Running CI..."
```

### `clean`

Requires: Install

Clean the pests.

```bash
rm -rf build/
rm -rf dist/
rm -rf *.egg-info
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type d -name ".mypy_cache" -exec rm -rf {} +
find . -type d -name ".pytest_cache" -exec rm -rf {} +
find . -type d -name ".ruff_cache" -exec rm -rf {} +
find . -type f -name "*.py[cod]" -delete
find . -type f -name ".coverage" -delete
```

## License

`opinionated-mixins` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
