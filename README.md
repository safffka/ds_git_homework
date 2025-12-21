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
pre-commit run --all-files
```

During development all changes to the `main` branch must be made via Pull Requests.
Commits that break code style or type checks will be blocked by pre-commit hooks.

Running MLflow + MinIO
```bash
docker compose up -d
docker compose --profile trainer run --rm trainer \
  uv run python -m ds_git_homework.experiments.train \
  --config configs/experiment.yaml \
  --grid configs/grid.yaml
```
MinIO UI: http://localhost:9001
MLflow UI: http://localhost:5001
## Experiment tracking

All ML experiments are tracked using **MLflow** and **S3 (MinIO)**.

- Experiment metadata (parameters, metrics) are stored in MLflow
- Trained models and artifacts are stored in S3 (MinIO)
- No datasets or models are committed to Git
## Notes

This section was added in a separate feature branch to demonstrate
a non fast-forward merge.



