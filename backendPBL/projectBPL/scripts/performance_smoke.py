from __future__ import annotations

import argparse
import json
import statistics
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


def make_request(url: str, timeout: int, token: str | None) -> dict:
    start = time.perf_counter()
    request = urllib.request.Request(url)
    if token:
        request.add_header("Authorization", f"Bearer {token}")

    with urllib.request.urlopen(request, timeout=timeout) as response:
        response.read()
        status = response.status
    duration_ms = (time.perf_counter() - start) * 1000
    return {"status": status, "duration_ms": duration_ms}


def run_smoke(
    url: str, requests_count: int, concurrency: int, timeout: int, token: str | None
) -> dict:
    started_at = time.strftime("%Y-%m-%d %H:%M:%S")
    durations = []
    failures = 0

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [
            executor.submit(make_request, url, timeout, token)
            for _ in range(requests_count)
        ]
        for future in as_completed(futures):
            try:
                result = future.result()
                durations.append(result["duration_ms"])
                if result["status"] >= 400:
                    failures += 1
            except Exception:
                failures += 1

    if not durations:
        raise RuntimeError("No successful responses were collected.")

    total_time_ms = sum(durations)
    throughput = len(durations) / (total_time_ms / 1000) if total_time_ms else 0

    return {
        "started_at": started_at,
        "url": url,
        "requests": requests_count,
        "concurrency": concurrency,
        "successful_requests": len(durations),
        "failed_requests": failures,
        "min_ms": round(min(durations), 2),
        "avg_ms": round(statistics.mean(durations), 2),
        "median_ms": round(statistics.median(durations), 2),
        "max_ms": round(max(durations), 2),
        "p95_ms": round(sorted(durations)[max(0, int(len(durations) * 0.95) - 1)], 2),
        "throughput_rps": round(throughput, 2),
    }


def write_report(result: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        "\n".join(
            [
                "# Performance Smoke Report",
                "",
                f"- Timestamp: {result['started_at']}",
                f"- Endpoint: `{result['url']}`",
                f"- Requests: {result['requests']}",
                f"- Concurrency: {result['concurrency']}",
                f"- Successful requests: {result['successful_requests']}",
                f"- Failed requests: {result['failed_requests']}",
                f"- Min response time: {result['min_ms']} ms",
                f"- Avg response time: {result['avg_ms']} ms",
                f"- Median response time: {result['median_ms']} ms",
                f"- P95 response time: {result['p95_ms']} ms",
                f"- Max response time: {result['max_ms']} ms",
                f"- Throughput: {result['throughput_rps']} req/s",
                "",
                "## Interpretation",
                "",
                "Use this report to document response times, throughput, and bottlenecks before submission.",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Simple performance smoke test for Buildly APIs."
    )
    parser.add_argument("--url", default="http://127.0.0.1:8000/api/courses/")
    parser.add_argument("--requests", type=int, default=30)
    parser.add_argument("--concurrency", type=int, default=5)
    parser.add_argument("--timeout", type=int, default=10)
    parser.add_argument("--token", default=None)
    parser.add_argument(
        "--output",
        default=str(
            Path(__file__).resolve().parents[3] / "docs" / "performance-report.md"
        ),
    )
    args = parser.parse_args()

    result = run_smoke(
        args.url, args.requests, args.concurrency, args.timeout, args.token
    )
    write_report(result, Path(args.output))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
