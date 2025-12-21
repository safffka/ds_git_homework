from pathlib import Path
from typing import Any


def download_file(
    s3_client: Any,
    bucket: str,
    key: str,
    dst: Path,
) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    s3_client.download_file(bucket, key, str(dst))


def upload_file(
    s3_client: Any,
    bucket: str,
    key: str,
    src: Path,
) -> None:
    s3_client.upload_file(str(src), bucket, key)
