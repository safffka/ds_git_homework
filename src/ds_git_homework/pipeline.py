import os
from pathlib import Path

from ds_git_homework.processing.transform import add_processed_flag
from ds_git_homework.s3.client import load_s3_config_from_env, make_s3_client
from ds_git_homework.s3.io import download_file, upload_file


def run_pipeline() -> None:
    bucket = os.environ["S3_BUCKET"]
    raw_key = os.environ["S3_RAW_KEY"]
    processed_key = os.environ["S3_PROCESSED_KEY"]

    raw_local = Path("data/raw/titanic.csv")
    processed_local = Path("data/processed/titanic_processed.csv")

    cfg = load_s3_config_from_env()
    s3 = make_s3_client(cfg)

    download_file(s3, bucket=bucket, key=raw_key, dst=raw_local)
    add_processed_flag(raw_local, processed_local)
    upload_file(s3, bucket=bucket, key=processed_key, src=processed_local)
