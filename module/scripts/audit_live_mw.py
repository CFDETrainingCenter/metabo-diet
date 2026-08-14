#!/usr/bin/env python3
"""Audit live MW split endpoints without modifying the immutable cache."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import requests

from metabo_diet_pipeline import MW_BASE_URL, MW_ENDPOINTS, validate_mw_payload


MODULE = Path(__file__).resolve().parents[1]
STUDY_IDS = ("ST001521", "ST003348")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=MODULE / "qa" / "live_mw_audit.json",
    )
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args()

    records: list[dict[str, object]] = []
    for study_id in STUDY_IDS:
        for endpoint in MW_ENDPOINTS:
            url = f"{MW_BASE_URL}/{study_id}/{endpoint}"
            cache_path = MODULE / "data" / "raw" / f"{study_id}_{endpoint}.json"
            record: dict[str, object] = {
                "study_id": study_id,
                "endpoint": endpoint,
                "url": url,
                "authentication_used": False,
                "cache_path": str(cache_path.relative_to(MODULE.parent)),
            }
            try:
                response = requests.get(
                    url,
                    timeout=args.timeout,
                    headers={"User-Agent": "Metabo-Diet-training-module/1.0"},
                )
                response.raise_for_status()
                payload = response.json()
                validate_mw_payload(study_id, endpoint, payload)
                content = response.content
                cached = cache_path.read_bytes()
                record.update(
                    {
                        "http_status": response.status_code,
                        "content_type": response.headers.get("content-type", ""),
                        "live_bytes": len(content),
                        "live_sha256": hashlib.sha256(content).hexdigest(),
                        "cache_bytes": len(cached),
                        "cache_sha256": hashlib.sha256(cached).hexdigest(),
                        "byte_for_byte_cache_match": content == cached,
                        "structural_validation": "passed",
                        "record_count": 1 if endpoint == "summary" else len(payload),
                    }
                )
            except Exception as exc:  # Preserve endpoint-level evidence before failing.
                record.update(
                    {
                        "structural_validation": "failed",
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                )
            records.append(record)

    all_structural = all(row.get("structural_validation") == "passed" for row in records)
    all_cache_match = all(row.get("byte_for_byte_cache_match") is True for row in records)
    report = {
        "audit_time_utc": datetime.now(timezone.utc).isoformat(),
        "purpose": "Read-only live-path compatibility audit; cached files were not modified.",
        "all_ten_endpoints_structurally_valid": all_structural,
        "all_ten_endpoints_byte_for_byte_cache_match": all_cache_match,
        "records": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(args.output),
        "structural_pass": all_structural,
        "exact_cache_match": all_cache_match,
        "endpoint_count": len(records),
    }))
    return 0 if all_structural else 1


if __name__ == "__main__":
    raise SystemExit(main())
