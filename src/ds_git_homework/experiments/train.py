from __future__ import annotations

import argparse
import os
import pickle
from pathlib import Path
from typing import Any, cast
import yaml
import mlflow
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from ds_git_homework.s3.client import make_s3_client, S3Config
from ds_git_homework.s3.io import download_file
from itertools import product


def _load_env_s3_config() -> S3Config:
    endpoint_url = os.environ["S3_ENDPOINT_URL"]
    access_key = os.environ["AWS_ACCESS_KEY_ID"]
    secret_key = os.environ["AWS_SECRET_ACCESS_KEY"]
    return S3Config(
        endpoint_url=endpoint_url,
        access_key=access_key,
        secret_key=secret_key,
    )


def _load_yaml_config(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError(f"Config {path} must be a YAML mapping")

    return cast(dict[str, Any], data)


def _iterate_param_grid(param_grid: dict[str, list[Any]]) -> list[dict[str, Any]]:
    keys = list(param_grid.keys())
    values = list(param_grid.values())

    combos = []
    for combo in product(*values):
        combos.append(dict(zip(keys, combo)))

    return combos


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to experiment YAML config")
    parser.add_argument("--grid", required=True)
    args = parser.parse_args()

    cfg_path = Path(args.config)
    cfg = _load_yaml_config(cfg_path)

    experiment_name: str = cfg["experiment_name"]

    # MLflow tracking
    tracking_uri = os.environ.get("MLFLOW_TRACKING_URI", "http://localhost:5001")
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)

    # S3
    s3 = _load_env_s3_config()
    s3_client = make_s3_client(s3)

    bucket: str = cfg["s3"]["bucket"]
    processed_key: str = cfg["s3"]["processed_key"]

    # Download dataset
    local_processed = Path("data/processed") / Path(processed_key).name
    local_processed.parent.mkdir(parents=True, exist_ok=True)

    download_file(
        s3_client=s3_client,
        bucket=bucket,
        key=processed_key,
        dst=local_processed,
    )

    df = pd.read_csv(local_processed)

    target_col: str = cfg["target_col"]
    features: list[str] = cfg["features"]

    # Minimal preprocessing
    if "Sex" in df.columns:
        df["Sex"] = df["Sex"].map({"male": 0, "female": 1}).astype(float)

    X = df[features].copy()
    y = df[target_col].astype(int)

    split_cfg = cfg["split"]
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=float(split_cfg["test_size"]),
        random_state=int(split_cfg["random_state"]),
        stratify=y,
    )

    # Grid search
    model_cfg = cfg["model"]
    grid_cfg = _load_yaml_config(Path(args.grid))
    param_grid: dict[str, list[Any]] = grid_cfg["param_grid"]
    param_combinations = _iterate_param_grid(param_grid)

    for params in param_combinations:
        run_name = "_".join(f"{k}={v}" for k, v in params.items())

        with mlflow.start_run(run_name=run_name):
            mlflow.log_param("model_type", model_cfg["type"])
            mlflow.log_params(params)
            mlflow.log_param("features", ",".join(features))
            mlflow.log_param("target_col", target_col)
            mlflow.log_param("test_size", split_cfg["test_size"])
            mlflow.log_param("random_state", split_cfg["random_state"])
            mlflow.log_param("stratify", True)
            model = DecisionTreeClassifier(
                **params,
                random_state=split_cfg["random_state"],
            )
            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)

            acc = float(accuracy_score(y_test, y_pred))
            f1 = float(f1_score(y_test, y_pred))

            mlflow.log_metric("accuracy", acc)
            mlflow.log_metric("f1", f1)

            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(X_test)[:, 1]
                auc = float(roc_auc_score(y_test, proba))
                mlflow.log_metric("roc_auc", auc)

            active_run = mlflow.active_run()
            if active_run is None:
                raise RuntimeError("MLflow run is not active")

            run_id = active_run.info.run_id

            # Save model locally
            local_model_dir = Path("data/models") / experiment_name / run_id
            local_model_dir.mkdir(parents=True, exist_ok=True)
            local_model_path = local_model_dir / "model.pkl"

            with local_model_path.open("wb") as f:
                pickle.dump(model, f)

            mlflow.log_artifact(str(local_model_path), artifact_path="model_pickle")

            print(f"Finished run: {run_name}")


if __name__ == "__main__":
    main()
