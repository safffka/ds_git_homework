from __future__ import annotations

import os
import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Tuple

from mlflow.tracking import MlflowClient

from ds_git_homework.s3.client import S3Config, make_s3_client
from ds_git_homework.s3.io import download_file


# -------------------------
# Models
# -------------------------

@dataclass(frozen=True)
class ModelRef:
    experiment_name: str
    run_id: str
    artifact_uri: str


# -------------------------
# MLflow helpers
# -------------------------

def get_best_run_id(
    experiment_name: str,
    metric_name: str,
) -> str:
    client = MlflowClient()

    experiment = client.get_experiment_by_name(experiment_name)
    if experiment is None:
        raise RuntimeError(f"Experiment '{experiment_name}' not found")

    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=[f"metrics.{metric_name} DESC"],
        max_results=1,
    )

    if not runs:
        raise RuntimeError("No runs found in experiment")
    run_id = runs[0].info.run_id
    assert isinstance(run_id, str)

    return run_id


def resolve_model_ref(
    experiment_name: str,
    run_id: str,
) -> ModelRef:
    """
    Resolve MLflow artifact URI for a given run.
    """
    client = MlflowClient()
    run = client.get_run(run_id)

    artifact_uri = run.info.artifact_uri
    if not artifact_uri.startswith("s3://"):
        raise RuntimeError(f"Unsupported artifact URI: {artifact_uri}")

    return ModelRef(
        experiment_name=experiment_name,
        run_id=run_id,
        artifact_uri=artifact_uri,
    )


# -------------------------
# S3 helpers
# -------------------------

def _load_env_s3_config() -> S3Config:
    """
    Unified env names for MinIO / S3.
    """
    return S3Config(
        endpoint_url=os.environ["S3_ENDPOINT_URL"],
        access_key=os.environ["AWS_ACCESS_KEY_ID"],
        secret_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    )


def _parse_s3_uri(uri: str) -> Tuple[str, str]:
    """
    Parse s3://bucket/key -> (bucket, key)
    """
    if not uri.startswith("s3://"):
        raise ValueError(f"Invalid S3 URI: {uri}")

    path = uri.replace("s3://", "", 1)
    bucket, key = path.split("/", 1)
    return bucket, key


# -------------------------
# Model loading
# -------------------------

def load_model_from_s3(model_ref: ModelRef) -> Any:
    """
    Download model.pkl from MLflow artifacts and load it.
    """
    s3_cfg = _load_env_s3_config()
    s3_client = make_s3_client(s3_cfg)

    model_uri = f"{model_ref.artifact_uri}/model_pickle/model.pkl"
    bucket, key = _parse_s3_uri(model_uri)

    local_path = (
        Path("data/serving")
        / model_ref.experiment_name
        / model_ref.run_id
        / "model.pkl"
    )
    local_path.parent.mkdir(parents=True, exist_ok=True)

    download_file(
        s3_client=s3_client,
        bucket=bucket,
        key=key,
        dst=local_path,
    )

    with local_path.open("rb") as f:
        return pickle.load(f)
