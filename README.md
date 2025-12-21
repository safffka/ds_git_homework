# DS Git Homework

![PyPI version](https://img.shields.io/pypi/v/ds_git_homework.svg)
[![Documentation Status](https://readthedocs.org/projects/ds_git_homework/badge/?version=latest)](https://ds_git_homework.readthedocs.io/en/latest/?version=latest)

Homework for git, linters and tooling

* PyPI package: https://pypi.org/project/ds_git_homework/
* Free software: MIT License
* Documentation: https://ds_git_homework.readthedocs.io.

## Features

* TODO

## Credits

This package was created with [Cookiecutter](https://github.com/audreyfeldroy/cookiecutter) and the [audreyfeldroy/cookiecutter-pypackage](https://github.com/audreyfeldroy/cookiecutter-pypackage) project template.
## Project purpose

This project is created as a homework to practice git workflow,
branching strategies, linters, type checking and pre-commit hooks.
## Usage

This repository demonstrates a basic git workflow with feature branches,
merges and pull requests.

## Development setup

Create a virtual environment and install all development dependencies:

```bash
uv sync
pre-commit install
```

Run code quality checks manually:

```bash
flake8
mypy src tests
pre-commit run --all-files
```

During development all changes to the `main` branch must be made via Pull Requests.
Commits that break code style or type checks will be blocked by pre-commit hooks.


## Notes

This section was added in a separate feature branch to demonstrate
a non fast-forward merge.



