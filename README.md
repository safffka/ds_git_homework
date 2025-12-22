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

## Model serving

The trained model is served via a FastAPI application.

How the model is selected

At startup, the API service:

Connects to MLflow

Downloads the corresponding model artifact from S3 (MinIO)

Loads the model into memory for inference

The model is not bundled into the image and is always resolved dynamically.

Run API service
```bash
docker compose up -d --build
```
API endpoints

Swagger UI: http://localhost:8000/docs

Prediction endpoint: POST /predict

request:
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"Pclass":3,"Sex":"male","Age":22,"SibSp":1,"Parch":0,"Fare":7.25}'
```



## Load testing

Load testing is implemented as a standalone script.

Endpoint: /predict

Requests per test: 500

Concurrency levels tested: 1, 2, 5, 10, 20, 50

Metrics collected: average latency and latency quantiles

Run load test
```bash
docker compose run --rm api \
  uv run python scripts/load_test.py \
  --url http://api:8000/predict \
  --output results/load_test.csv
```
## Load test results (latency in seconds)

| N (concurrency) | avg (s) | q25 (s) | q50 (s) | q90 (s) | q95 (s) | q99 (s) |
|-----------------|---------|---------|---------|---------|---------|---------|
| 1               | 0.0023  | 0.0015  | 0.0015  | 0.0032  | 0.0056  | 0.0125  |
| 2               | 0.0033  | 0.0024  | 0.0028  | 0.0048  | 0.0065  | 0.0106  |
| 5               | 0.0088  | 0.0047  | 0.0062  | 0.0135  | 0.0180  | 0.0466  |
| 10              | 0.0121  | 0.0080  | 0.0109  | 0.0198  | 0.0224  | 0.0263  |
| 20              | 0.0407  | 0.0157  | 0.0276  | 0.0840  | 0.1322  | 0.1830  |
| 50              | 0.0871  | 0.0609  | 0.0816  | 0.1627  | 0.1956  | 0.2099  |



Hardware information

Load testing was performed inside a Linux Docker container.

Architecture:        aarch64
CPU(s):              4
Vendor ID:           Apple
Thread(s) per core:  1
Core(s) per cluster: 4
