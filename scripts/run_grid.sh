#!/usr/bin/env bash
set -e

COMPOSE="docker compose"
PROFILE="trainer"

CONFIG="configs/experiment.yaml"
GRID="configs/grid.yaml"

# 1. Поднимаем infra
$COMPOSE up -d minio mlflow

echo " Waiting for MinIO & MLflow..."
sleep 5

# 2. Запускаем grid search
$COMPOSE --profile $PROFILE run --rm trainer \
  python -m ds_git_homework.experiments.train \
  --config $CONFIG \
  --grid $GRID

echo "Grid search finished"
