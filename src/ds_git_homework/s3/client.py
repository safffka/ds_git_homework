import os
from dataclasses import dataclass
from typing import Any
import boto3


@dataclass(frozen=True)
class S3Config:
    endpoint_url: str
    access_key: str
    secret_key: str


def load_s3_config_from_env() -> S3Config:
    endpoint_url = os.environ["S3_ENDPOINT_URL"]
    access_key = os.environ["S3_ACCESS_KEY"]
    secret_key = os.environ["S3_SECRET_KEY"]
    return S3Config(endpoint_url=endpoint_url, access_key=access_key, secret_key=secret_key)


def make_s3_client(cfg: S3Config) -> Any:
    return boto3.client(
        service_name="s3",
        endpoint_url=cfg.endpoint_url,
        aws_access_key_id=cfg.access_key,
        aws_secret_access_key=cfg.secret_key,
    )
