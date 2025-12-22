from __future__ import annotations
from typing import Any
import argparse
import asyncio
import time
from typing import List

import httpx
import numpy as np
import pandas as pd
from rich.console import Console
from rich.table import Table
from pathlib import Path

DEFAULT_PAYLOAD = {
    "Pclass": 3,
    "Sex": "male",
    "Age": 22,
    "SibSp": 1,
    "Parch": 0,
    "Fare": 7.25,
}


async def _send_request(
    client: httpx.AsyncClient,
    url: str,
    payload: dict[str, Any],
    semaphore: asyncio.Semaphore,
    timings: List[float],
) -> None:
    async with semaphore:
        start = time.perf_counter()
        response = await client.post(url, json=payload)
        response.raise_for_status()
        end = time.perf_counter()
        timings.append(end - start)


async def run_load_test(
    url: str,
    payload: dict[str, Any],
    total_requests: int,
    concurrency: int,
) -> dict[str, float]:
    semaphore = asyncio.Semaphore(concurrency)
    timings: List[float] = []

    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = [
            _send_request(client, url, payload, semaphore, timings)
            for _ in range(total_requests)
        ]
        await asyncio.gather(*tasks)

    latencies = np.array(timings)

    return {
        "concurrency": concurrency,
        "avg": float(latencies.mean()),
        "q25": float(np.percentile(latencies, 25)),
        "q50": float(np.percentile(latencies, 50)),
        "q90": float(np.percentile(latencies, 90)),
        "q95": float(np.percentile(latencies, 95)),
        "q99": float(np.percentile(latencies, 99)),
    }


def print_results(results: list[dict[str, float]]) -> None:
    table = Table(title="Load test results (latency in seconds)")

    table.add_column("N", justify="right")
    table.add_column("avg")
    table.add_column("q25")
    table.add_column("q50")
    table.add_column("q90")
    table.add_column("q95")
    table.add_column("q99")

    for r in results:
        table.add_row(
            str(r["concurrency"]),
            f"{r['avg']:.4f}",
            f"{r['q25']:.4f}",
            f"{r['q50']:.4f}",
            f"{r['q90']:.4f}",
            f"{r['q95']:.4f}",
            f"{r['q99']:.4f}",
        )

    Console().print(table)


def main() -> None:
    parser = argparse.ArgumentParser(description="ML model load testing")
    parser.add_argument("--url", required=True, help="Predict endpoint URL")
    parser.add_argument("--requests", type=int, default=500, help="Total requests")
    parser.add_argument(
        "--concurrency",
        type=int,
        nargs="+",
        default=[1, 2, 5, 10, 20, 50],
        help="Concurrency levels",
    )
    parser.add_argument(
        "--output",
        default="results/load_test.csv",
        help="CSV output path",
    )

    args = parser.parse_args()

    results: list[dict[str, float]] = []

    for n in args.concurrency:
        print(f"Running load test: concurrency={n}")
        metrics = asyncio.run(
            run_load_test(
                url=args.url,
                payload=DEFAULT_PAYLOAD,
                total_requests=args.requests,
                concurrency=n,
            )
        )
        results.append(metrics)

    df = pd.DataFrame(results)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False)

    print_results(results)
    print(f"\nSaved results to: {args.output}")


if __name__ == "__main__":
    main()
