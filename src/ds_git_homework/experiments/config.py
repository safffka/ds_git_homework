from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ModelType = Literal["decision_tree"]


@dataclass(frozen=True)
class S3DatasetConfig:
    bucket: str
    processed_key: str


@dataclass(frozen=True)
class SplitConfig:
    test_size: float
    random_state: int


@dataclass(frozen=True)
class ModelConfig:
    type: ModelType
    params: dict[str, object]


@dataclass(frozen=True)
class OutputConfig:
    model_s3_prefix: str


@dataclass(frozen=True)
class ExperimentConfig:
    experiment_name: str
    run_name: str
    s3: S3DatasetConfig
    target_col: str
    features: list[str]
    model: ModelConfig
    split: SplitConfig
    output: OutputConfig
