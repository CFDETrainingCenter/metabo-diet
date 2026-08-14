"""Reproducible helpers for the Metabo-Diet guided tutorial.

The notebook deliberately keeps orchestration visible while this module holds the
longer validation, reshaping, crosswalk, and plotting functions.  All cross-study
comparisons are metadata/name based; quantitative matrices are never stacked.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler


MW_BASE_URL = "https://www.metabolomicsworkbench.org/rest/study/study_id"
MW_ENDPOINTS = ("summary", "factors", "analysis", "metabolites", "data")

REQUIRED_FIELDS = {
    "summary": {"study_id", "study_title", "species", "license"},
    "factors": {"study_id", "local_sample_id", "sample_source", "factors"},
    "analysis": {"study_id", "analysis_id", "analysis_summary", "analysis_type"},
    "metabolites": {
        "study_id",
        "analysis_id",
        "analysis_summary",
        "metabolite_name",
        "refmet_name",
    },
    "data": {
        "study_id",
        "analysis_id",
        "metabolite_name",
        "metabolite_id",
        "refmet_name",
        "DATA",
    },
}

# Dataset-specific conservative detector.  It targets explicit hyphenated stable-
# isotope suffixes and bracketed isotope labels while avoiding biological names
# such as "25-Hydroxyvitamin D3".
ISOTOPE_STANDARD_PATTERN = re.compile(
    r"(?:-[dD]\d+\b|-\[(?:13C|15N)\]\d*)", flags=re.IGNORECASE
)

EXPECTED_EXERCISE_STANDARD_NAMES = {
    "AcCa(12:0)-D9",
    "AcCa(18:0)-D3",
    "Clenbuterol-D9",
    "Hippuric acid-D5",
    "Lysine-d4",
    "Taurine-D4",
    "CDCA-D4",
    "Chloramphenicol-D5",
    "Palmitic acid-[13C]16",
    "Stearic acid-D35",
}


def find_module_dir(start: Path | None = None) -> Path:
    """Locate ``module/`` whether execution starts at the repo or notebook."""

    start = (start or Path.cwd()).resolve()
    candidates = [start, *start.parents]
    for parent in candidates:
        direct = parent
        nested = parent / "module"
        if (direct / "data" / "raw").is_dir() and (direct / "notebooks").is_dir():
            return direct
        if (nested / "data" / "raw").is_dir() and (nested / "notebooks").is_dir():
            return nested
    raise FileNotFoundError("Could not locate module/data/raw from the current directory")


def _ordered_records(payload: Any) -> list[dict[str, Any]]:
    """Convert MW's numbered-record object into a stable list of records."""

    if isinstance(payload, list):
        records = payload
    elif isinstance(payload, dict) and all(isinstance(v, dict) for v in payload.values()):
        def sort_key(item: tuple[str, Any]) -> tuple[int, str]:
            key = str(item[0])
            return (0, f"{int(key):012d}") if key.isdigit() else (1, key)

        records = [value for _, value in sorted(payload.items(), key=sort_key)]
    else:
        raise ValueError("Expected a list or numbered object of records")
    if not all(isinstance(record, dict) for record in records):
        raise ValueError("Every endpoint record must be a JSON object")
    return records


def validate_mw_payload(study_id: str, endpoint: str, payload: Any) -> None:
    """Fail early when a REST response no longer matches the expected schema."""

    if endpoint not in MW_ENDPOINTS:
        raise ValueError(f"Unknown endpoint: {endpoint}")
    if endpoint == "summary":
        if not isinstance(payload, dict):
            raise ValueError(f"{study_id}/{endpoint}: expected one JSON object")
        missing = REQUIRED_FIELDS[endpoint] - set(payload)
        if missing:
            raise ValueError(f"{study_id}/{endpoint}: missing fields {sorted(missing)}")
        if payload["study_id"] != study_id:
            raise ValueError(f"{study_id}/{endpoint}: study_id mismatch")
        return

    records = _ordered_records(payload)
    if not records:
        raise ValueError(f"{study_id}/{endpoint}: endpoint is empty")
    for index, record in enumerate(records, start=1):
        missing = REQUIRED_FIELDS[endpoint] - set(record)
        if missing:
            raise ValueError(
                f"{study_id}/{endpoint} record {index}: missing {sorted(missing)}"
            )
        if record["study_id"] != study_id:
            raise ValueError(f"{study_id}/{endpoint} record {index}: study_id mismatch")
        if endpoint == "data" and not isinstance(record["DATA"], dict):
            raise ValueError(f"{study_id}/{endpoint} record {index}: DATA is not an object")


def load_mw_endpoint(
    study_id: str,
    endpoint: str,
    raw_dir: Path,
    *,
    prefer_live: bool = False,
    timeout_seconds: float = 20.0,
) -> tuple[Any, dict[str, str]]:
    """Retrieve one split REST endpoint, falling back to its validated cache."""

    url = f"{MW_BASE_URL}/{study_id}/{endpoint}"
    cache_path = raw_dir / f"{study_id}_{endpoint}.json"
    cache_reference = f"data/raw/{cache_path.name}"
    live_error = ""
    if prefer_live:
        try:
            response = requests.get(
                url,
                timeout=timeout_seconds,
                headers={"User-Agent": "Metabo-Diet-training-module/1.0"},
            )
            response.raise_for_status()
            payload = response.json()
            validate_mw_payload(study_id, endpoint, payload)
            return payload, {
                "study_id": study_id,
                "endpoint": endpoint,
                "source": "live REST API",
                "url": url,
                "cache_path": cache_reference,
                "fallback_reason": "",
            }
        except (requests.RequestException, ValueError, json.JSONDecodeError) as exc:
            live_error = f"{type(exc).__name__}: {exc}"

    if not cache_path.exists():
        raise FileNotFoundError(
            f"No usable live response and cached endpoint is missing: {cache_path}"
        )
    with cache_path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    validate_mw_payload(study_id, endpoint, payload)
    return payload, {
        "study_id": study_id,
        "endpoint": endpoint,
        "source": "validated cache",
        "url": url,
        "cache_path": cache_reference,
        "fallback_reason": live_error or "live retrieval disabled for deterministic run",
    }


def load_studies(
    study_ids: Iterable[str], raw_dir: Path, *, prefer_live: bool = False
) -> tuple[dict[str, dict[str, Any]], pd.DataFrame]:
    """Load and validate all five split endpoints for each accession."""

    studies: dict[str, dict[str, Any]] = {}
    source_rows: list[dict[str, str]] = []
    for study_id in study_ids:
        studies[study_id] = {}
        for endpoint in MW_ENDPOINTS:
            payload, source = load_mw_endpoint(
                study_id, endpoint, raw_dir, prefer_live=prefer_live
            )
            studies[study_id][endpoint] = payload
            source_rows.append(source)
    return studies, pd.DataFrame(source_rows)


def parse_factor_string(value: str) -> dict[str, str]:
    """Parse MW ``Key:value | Key:value`` factors without splitting values twice."""

    parsed: dict[str, str] = {}
    for part in str(value).split("|"):
        key, separator, val = part.strip().partition(":")
        if not separator or not key.strip():
            raise ValueError(f"Malformed factor component: {part!r}")
        key, val = key.strip(), val.strip()
        if key in parsed:
            raise ValueError(f"Duplicate factor key {key!r} in {value!r}")
        parsed[key] = val
    return parsed


def derive_tidy_factors(
    studies: dict[str, dict[str, Any]], diet_accession: str, exercise_accession: str
) -> pd.DataFrame:
    """Create one analysis-ready factor table with explicit ID derivation rules."""

    rows: list[dict[str, Any]] = []
    diet_time = {
        "Baseline": ("baseline", 0, "baseline", "Pre-intervention"),
        "Day 5": ("day_05", 5, "diet_exposure", "Diet exposure before antibiotics"),
        "Day 9": (
            "day_09",
            9,
            "diet_plus_microbiome_perturbation",
            "Antibiotics days 6-8 and PEG purge day 7; not a diet-only contrast",
        ),
        "Day 12": (
            "day_12",
            12,
            "diet_plus_microbiome_perturbation",
            "Post-antibiotics/PEG interval; not a diet-only contrast",
        ),
        "Day 15": (
            "day_15",
            15,
            "diet_plus_microbiome_perturbation",
            "Post-antibiotics/PEG interval; not a diet-only contrast",
        ),
    }
    exercise_time = {
        "rest": ("rest", 0, "baseline", "Fasting pre-exercise collection"),
        "stat": ("immediate_post", 1, "acute_perturbation", "Immediate post-exercise"),
        "rec3": ("recovery_3h", 2, "recovery", "Approximately 3 h recovery"),
        "rec22": ("recovery_22h", 3, "recovery", "Approximately 22 h recovery; fasting"),
    }

    diet_records = _ordered_records(studies[diet_accession]["factors"])
    qc_ids = {
        record["local_sample_id"]
        for record in diet_records
        if re.fullmatch(r"QPP(?:0[1-9]|10)", record["local_sample_id"])
    }
    expected_qc = {f"QPP{i:02d}" for i in range(1, 11)}
    if qc_ids != expected_qc:
        raise ValueError(f"Unexpected pooled-QC IDs: {sorted(qc_ids)}")

    for record in diet_records:
        sample_id = record["local_sample_id"]
        if sample_id in qc_ids:
            continue
        match = re.fullmatch(r"(?P<participant>\d+)-\d+-P[A-E]", sample_id)
        if not match:
            raise ValueError(f"Cannot derive diet participant from {sample_id!r}")
        factors = parse_factor_string(record["factors"])
        if set(factors) != {"Study_Diet", "Sex", "Time"}:
            raise ValueError(f"Unexpected diet factor keys for {sample_id}: {sorted(factors)}")
        if factors["Time"] not in diet_time:
            raise ValueError(f"Unexpected diet timepoint: {factors['Time']!r}")
        normalized, order, role, context = diet_time[factors["Time"]]
        rows.append(
            {
                "study_id": diet_accession,
                "study_role": "diet",
                "local_sample_id": sample_id,
                "mb_sample_id": record.get("mb_sample_id", ""),
                "participant_id": match.group("participant"),
                "participant_id_rule": "digits before first hyphen",
                "factor_string_original": record["factors"],
                "sample_source_original": record["sample_source"],
                "specimen_harmonized": "plasma",
                "condition_original": factors["Study_Diet"],
                "sex_original": factors["Sex"],
                "time_original": factors["Time"],
                "time_harmonized": normalized,
                "time_order": order,
                "trajectory_role": role,
                "interpretation_context": context,
                "factor_parse_status": "parsed_and_validated",
            }
        )

    expected_suffix = {"1": "rest", "2": "stat", "3": "rec3", "4": "rec22"}
    for record in _ordered_records(studies[exercise_accession]["factors"]):
        sample_id = record["local_sample_id"]
        match = re.fullmatch(r"(?P<participant>\d+)_(?P<suffix>[1-4])", sample_id)
        if not match:
            raise ValueError(f"Cannot derive exercise participant from {sample_id!r}")
        factors = parse_factor_string(record["factors"])
        if set(factors) != {"Collection_time"}:
            raise ValueError(
                f"Unexpected exercise factor keys for {sample_id}: {sorted(factors)}"
            )
        time = factors["Collection_time"].lower()
        if expected_suffix[match.group("suffix")] != time:
            raise ValueError(f"Exercise suffix/time mismatch for {sample_id}: {time}")
        normalized, order, role, context = exercise_time[time]
        rows.append(
            {
                "study_id": exercise_accession,
                "study_role": "exercise",
                "local_sample_id": sample_id,
                "mb_sample_id": record.get("mb_sample_id", ""),
                "participant_id": match.group("participant"),
                "participant_id_rule": "integer before underscore; suffix 1-4 validated",
                "factor_string_original": record["factors"],
                "sample_source_original": record["sample_source"],
                "specimen_harmonized": "serum",
                "condition_original": "acute endurance exercise",
                "sex_original": pd.NA,
                "time_original": time,
                "time_harmonized": normalized,
                "time_order": order,
                "trajectory_role": role,
                "interpretation_context": context,
                "factor_parse_status": "parsed_and_validated",
            }
        )

    factors = pd.DataFrame(rows).sort_values(
        ["study_id", "participant_id", "time_order", "local_sample_id"]
    ).reset_index(drop=True)
    observed = factors.groupby("study_id").agg(
        samples=("local_sample_id", "nunique"), participants=("participant_id", "nunique")
    )
    expected = {diet_accession: (150, 30), exercise_accession: (76, 19)}
    for study_id, counts in expected.items():
        actual = tuple(observed.loc[study_id, ["samples", "participants"]].astype(int))
        if actual != counts:
            raise ValueError(f"{study_id} factor count mismatch: {actual} != {counts}")
    return factors


def _normalize_refmet(value: Any) -> str:
    if value is None:
        return ""
    value = str(value).strip()
    return "" if value in {"", "-"} else value


def _classification_lookup(payload: Any) -> dict[str, dict[str, str]]:
    records = _ordered_records(payload)
    lookup: dict[str, dict[str, str]] = {}
    for record in records:
        name = str(record.get("name", "")).strip()
        if not name:
            continue
        value = {
            "refmet_id": str(record.get("refmet_id", "") or ""),
            "super_class": str(record.get("super_class", "") or "Unclassified"),
            "main_class": str(record.get("main_class", "") or "Unclassified"),
            "sub_class": str(record.get("sub_class", "") or "Unclassified"),
        }
        if name in lookup and lookup[name] != value:
            raise ValueError(f"Conflicting RefMet classifications for {name!r}")
        lookup[name] = value
    return lookup


def build_metabolite_crosswalk(
    studies: dict[str, dict[str, Any]],
    refmet_classification: Any,
    diet_accession: str,
    exercise_accession: str,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, int]]:
    """Create row audit, 153-name audit, conservative crosswalk, and class summary."""

    class_lookup = _classification_lookup(refmet_classification)
    audit_rows: list[dict[str, Any]] = []
    for study_id, role in ((diet_accession, "diet"), (exercise_accession, "exercise")):
        for record in _ordered_records(studies[study_id]["data"]):
            reported = str(record["metabolite_name"]).strip()
            refmet_name = _normalize_refmet(record.get("refmet_name"))
            isotope_standard = bool(
                study_id == exercise_accession and ISOTOPE_STANDARD_PATTERN.search(reported)
            )
            classification = class_lookup.get(
                refmet_name,
                {
                    "refmet_id": "",
                    "super_class": "Unclassified",
                    "main_class": "Unclassified",
                    "sub_class": "Unclassified",
                },
            )
            if isotope_standard:
                mapping_status = "excluded_isotope_labeled_or_internal_standard"
                decision = "Exclude row from biological analyses"
            elif refmet_name:
                mapping_status = "mapped_by_repository_refmet_field"
                decision = "Retain as biological candidate; preserve analysis identity"
            else:
                mapping_status = "unmapped_no_refmet_name"
                decision = "Retain for within-study PCA; omit from RefMet overlap"
            audit_rows.append(
                {
                    "study_id": study_id,
                    "study_role": role,
                    "analysis_id": record["analysis_id"],
                    "analysis_summary": record.get("analysis_summary", ""),
                    "source_metabolite_id": record.get("metabolite_id", ""),
                    "analysis_feature_id": (
                        f"{study_id}|{record['analysis_id']}|{record.get('metabolite_id', '')}"
                    ),
                    "source_reported_name": reported,
                    "refmet_name": refmet_name,
                    **classification,
                    "mapping_status": mapping_status,
                    "mapping_confidence": (
                        "repository-provided; exact class-name lookup; not independently verified"
                        if refmet_name
                        else "not mapped"
                    ),
                    "mapping_evidence": (
                        "MW /data refmet_name; RefMet classification cache exact-name match"
                        if refmet_name in class_lookup
                        else "MW /data refmet_name; no exact classification-cache match"
                    ),
                    "isotope_internal_standard_row": isotope_standard,
                    "standard_detection_evidence": (
                        "Explicit stable-isotope suffix in source-reported name"
                        if isotope_standard
                        else "No explicit stable-isotope suffix detected"
                    ),
                    "row_decision": decision,
                }
            )

    audit = pd.DataFrame(audit_rows).sort_values(
        ["study_id", "analysis_id", "source_reported_name", "source_metabolite_id"]
    ).reset_index(drop=True)
    detected = set(
        audit.loc[
            (audit["study_id"] == exercise_accession)
            & audit["isotope_internal_standard_row"],
            "source_reported_name",
        ]
    )
    if detected != EXPECTED_EXERCISE_STANDARD_NAMES:
        raise ValueError(
            "Stable-isotope audit changed. "
            f"Detected={sorted(detected)}, expected={sorted(EXPECTED_EXERCISE_STANDARD_NAMES)}"
        )

    mapped_sets = {
        study_id: set(audit.loc[(audit.study_id == study_id) & audit.refmet_name.ne(""), "refmet_name"])
        for study_id in (diet_accession, exercise_accession)
    }
    raw_overlap = mapped_sets[diet_accession] & mapped_sets[exercise_accession]
    excluded_labels = set(
        audit.loc[
            (audit.study_id == exercise_accession)
            & audit.isotope_internal_standard_row
            & audit.refmet_name.ne(""),
            "refmet_name",
        ]
    )
    conservative_overlap = raw_overlap - excluded_labels

    overlap_rows: list[dict[str, Any]] = []
    for refmet_name in sorted(raw_overlap, key=str.casefold):
        diet_rows = audit[(audit.study_id == diet_accession) & (audit.refmet_name == refmet_name)]
        exercise_rows = audit[
            (audit.study_id == exercise_accession) & (audit.refmet_name == refmet_name)
        ]
        classification = class_lookup.get(
            refmet_name,
            {
                "refmet_id": "",
                "super_class": "Unclassified",
                "main_class": "Unclassified",
                "sub_class": "Unclassified",
            },
        )
        collision = refmet_name in excluded_labels
        overlap_rows.append(
            {
                "refmet_name": refmet_name,
                **classification,
                "diet_source_reported_names": "; ".join(
                    sorted(set(diet_rows.source_reported_name), key=str.casefold)
                ),
                "diet_analysis_ids": "; ".join(sorted(set(diet_rows.analysis_id))),
                "diet_analysis_feature_ids": "; ".join(
                    sorted(set(diet_rows.analysis_feature_id))
                ),
                "exercise_source_reported_names": "; ".join(
                    sorted(set(exercise_rows.source_reported_name), key=str.casefold)
                ),
                "exercise_analysis_ids": "; ".join(sorted(set(exercise_rows.analysis_id))),
                "exercise_analysis_feature_ids": "; ".join(
                    sorted(set(exercise_rows.analysis_feature_id))
                ),
                "mapping_status": "exact_case_sensitive_refmet_name_intersection",
                "mapping_confidence": (
                    "repository-provided RefMet mapping; nomenclature bridge only"
                ),
                "mapping_evidence": (
                    "Exact case-sensitive equality of nonblank MW refmet_name fields; "
                    "RefMet class from cached exact-name lookup"
                ),
                "exercise_standard_collision": collision,
                "include_in_conservative_biological_overlap": not collision,
                "decision_reason": (
                    "Exclude label conservatively because an ST003348 isotope/internal-standard "
                    "row maps to this RefMet name"
                    if collision
                    else "Retain; no ST003348 isotope/internal-standard collision"
                ),
            }
        )
    overlap_audit = pd.DataFrame(overlap_rows)
    crosswalk = overlap_audit[
        overlap_audit.include_in_conservative_biological_overlap
    ].reset_index(drop=True)
    class_summary = (
        crosswalk.groupby(["super_class", "main_class"], dropna=False)
        .agg(refmet_count=("refmet_name", "nunique"))
        .reset_index()
        .sort_values(["refmet_count", "super_class", "main_class"], ascending=[False, True, True])
        .reset_index(drop=True)
    )
    counts = {
        "diet_unique_nonblank_refmet": len(mapped_sets[diet_accession]),
        "exercise_unique_nonblank_refmet": len(mapped_sets[exercise_accession]),
        "raw_exact_refmet_overlap": len(raw_overlap),
        "exercise_isotope_internal_standard_rows": int(
            audit.loc[
                (audit.study_id == exercise_accession)
                & audit.isotope_internal_standard_row
            ].shape[0]
        ),
        "raw_overlap_labels_with_standard_collision": len(raw_overlap & excluded_labels),
        "conservative_biological_refmet_overlap": len(conservative_overlap),
        "conservative_overlap_with_refmet_class": int(
            crosswalk.refmet_id.fillna("").ne("").sum()
        ),
    }
    expected_counts = {
        "diet_unique_nonblank_refmet": 510,
        "exercise_unique_nonblank_refmet": 475,
        "raw_exact_refmet_overlap": 153,
        "exercise_isotope_internal_standard_rows": 10,
        "raw_overlap_labels_with_standard_collision": 8,
        "conservative_biological_refmet_overlap": 145,
    }
    for key, expected in expected_counts.items():
        if counts[key] != expected:
            raise ValueError(f"Crosswalk count changed for {key}: {counts[key]} != {expected}")
    return audit, overlap_audit, crosswalk, class_summary, counts


def _save_figure(fig: plt.Figure, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def plot_overlap_counts(counts: dict[str, int], path: Path) -> None:
    """High-contrast count plot distinguishing raw and conservative overlap."""

    labels = ["Diet\nRefMet", "Exercise\nRefMet", "Raw exact\noverlap", "Conservative\nbiological overlap"]
    values = [
        counts["diet_unique_nonblank_refmet"],
        counts["exercise_unique_nonblank_refmet"],
        counts["raw_exact_refmet_overlap"],
        counts["conservative_biological_refmet_overlap"],
    ]
    colors = ["#0072B2", "#D55E00", "#6A3D9A", "#009E73"]
    fig, ax = plt.subplots(figsize=(9, 5.2))
    bars = ax.bar(labels, values, color=colors, edgecolor="black", linewidth=1.2)
    ax.bar_label(bars, padding=4, fontsize=11, fontweight="bold")
    ax.set_ylabel("Unique nonblank RefMet names")
    ax.set_title("RefMet overlap is reduced after conservative standard-label cleanup")
    ax.set_ylim(0, max(values) * 1.16)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#D0D0D0", linewidth=0.7, alpha=0.7)
    fig.text(
        0.5,
        -0.01,
        "Exact names support nomenclature comparison; they do not establish analytical equivalence.",
        ha="center",
        fontsize=9,
    )
    _save_figure(fig, path)


def plot_class_summary(class_summary: pd.DataFrame, path: Path, top_n: int = 12) -> None:
    """Plot the largest RefMet main classes in the conservative overlap."""

    plot_data = class_summary.nlargest(top_n, "refmet_count").sort_values("refmet_count")
    fig, ax = plt.subplots(figsize=(9, 6.4))
    bars = ax.barh(
        plot_data.main_class,
        plot_data.refmet_count,
        color="#0072B2",
        edgecolor="black",
        linewidth=0.9,
    )
    ax.bar_label(bars, padding=3, fontsize=9)
    ax.set_xlabel("Conservative shared RefMet names")
    ax.set_ylabel("RefMet main class")
    ax.set_title(f"Top {min(top_n, len(plot_data))} classes in the 145-name biological overlap")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="x", color="#D0D0D0", linewidth=0.7, alpha=0.7)
    _save_figure(fig, path)


def run_within_study_pca(
    study_id: str,
    analysis_id: str,
    study_payload: dict[str, Any],
    tidy_factors: pd.DataFrame,
    *,
    exclude_isotope_standards: bool,
    max_missing_fraction: float = 0.20,
) -> dict[str, Any]:
    """Log2, median-impute, autoscale, and PCA one study/analysis at a time."""

    factor_rows = (
        tidy_factors.loc[tidy_factors.study_id == study_id]
        .sort_values(["participant_id", "time_order", "local_sample_id"])
        .reset_index(drop=True)
    )
    sample_ids = factor_rows.local_sample_id.tolist()
    selected = [
        row
        for row in _ordered_records(study_payload["data"])
        if row["analysis_id"] == analysis_id
    ]
    if not selected:
        raise ValueError(f"No data rows for {study_id}/{analysis_id}")

    matrix_values: dict[str, list[float]] = {}
    feature_rows: list[dict[str, Any]] = []
    for row in selected:
        reported = str(row["metabolite_name"]).strip()
        is_standard = bool(ISOTOPE_STANDARD_PATTERN.search(reported))
        feature_id = f"{study_id}|{analysis_id}|{row.get('metabolite_id', '')}"
        values = pd.to_numeric(
            pd.Series([row["DATA"].get(sample_id) for sample_id in sample_ids]),
            errors="coerce",
        ).astype(float)
        excluded = bool(exclude_isotope_standards and is_standard)
        missing_fraction = float(values.isna().mean())
        feature_rows.append(
            {
                "study_id": study_id,
                "analysis_id": analysis_id,
                "analysis_feature_id": feature_id,
                "source_metabolite_id": row.get("metabolite_id", ""),
                "source_reported_name": reported,
                "refmet_name": _normalize_refmet(row.get("refmet_name")),
                "missing_fraction": missing_fraction,
                "isotope_internal_standard_row": is_standard,
                "excluded_as_isotope_internal_standard": excluded,
                "passes_missingness_threshold": missing_fraction <= max_missing_fraction,
            }
        )
        if not excluded and missing_fraction <= max_missing_fraction:
            matrix_values[feature_id] = values.tolist()

    matrix = pd.DataFrame(matrix_values, index=sample_ids, dtype=float)
    if matrix.empty:
        raise ValueError(f"No PCA features remain for {study_id}/{analysis_id}")
    if (matrix.dropna().to_numpy() < 0).any():
        raise ValueError("PCA preprocessing expects nonnegative peak areas")
    logged = np.log2(matrix + 1.0)
    imputer = SimpleImputer(strategy="median")
    imputed = imputer.fit_transform(logged)
    variance = np.var(imputed, axis=0, ddof=0)
    # A mathematically constant logged feature can acquire ~1e-29 variance from
    # floating-point subtraction.  Use a small explicit tolerance so it is not
    # autoscaled into numerical noise.
    nonconstant = variance > 1e-12
    if nonconstant.sum() < 2:
        raise ValueError("Fewer than two nonconstant PCA features remain")
    retained_columns = matrix.columns[nonconstant]
    scaled = StandardScaler(with_mean=True, with_std=True).fit_transform(
        imputed[:, nonconstant]
    )
    pca = PCA(n_components=2, svd_solver="full")
    score_values = pca.fit_transform(scaled)
    scores = factor_rows.copy()
    scores["PC1"] = score_values[:, 0]
    scores["PC2"] = score_values[:, 1]
    scores["PC1_variance_percent"] = pca.explained_variance_ratio_[0] * 100
    scores["PC2_variance_percent"] = pca.explained_variance_ratio_[1] * 100

    feature_qc = pd.DataFrame(feature_rows)
    feature_qc["nonconstant_after_imputation"] = feature_qc.analysis_feature_id.isin(
        retained_columns
    )
    feature_qc["included_in_pca"] = feature_qc.nonconstant_after_imputation
    loadings = pd.DataFrame(
        {
            "analysis_feature_id": retained_columns,
            "PC1_loading": pca.components_[0],
            "PC2_loading": pca.components_[1],
        }
    ).merge(
        feature_qc[
            ["analysis_feature_id", "source_reported_name", "refmet_name", "source_metabolite_id"]
        ],
        on="analysis_feature_id",
        how="left",
        validate="one_to_one",
    )
    return {
        "scores": scores,
        "feature_qc": feature_qc,
        "loadings": loadings,
        "study_id": study_id,
        "analysis_id": analysis_id,
        "n_samples": len(sample_ids),
        "n_input_features": len(selected),
        "n_pca_features": int(nonconstant.sum()),
        "max_missing_fraction": max_missing_fraction,
        "transform": "log2(peak area + 1)",
        "imputation": "feature median after log2 transform",
        "scaling": "feature autoscaling (mean 0, SD 1)",
        "explained_variance_percent": pca.explained_variance_ratio_[:2] * 100,
    }


def plot_diet_pca(result: dict[str, Any], path: Path) -> None:
    scores = result["scores"]
    colors = {"Western": "#0072B2", "Vegan": "#009E73", "Modulen": "#D55E00"}
    markers = {
        "Baseline": "o",
        "Day 5": "s",
        "Day 9": "^",
        "Day 12": "D",
        "Day 15": "P",
    }
    variance = result["explained_variance_percent"]
    fig, ax = plt.subplots(figsize=(9, 6.4))
    for diet, color in colors.items():
        for time, marker in markers.items():
            subset = scores[(scores.condition_original == diet) & (scores.time_original == time)]
            if subset.empty:
                continue
            ax.scatter(
                subset.PC1,
                subset.PC2,
                s=48,
                c=color,
                marker=marker,
                edgecolors="black",
                linewidths=0.55,
                alpha=0.82,
            )
    diet_handles = [
        plt.Line2D([0], [0], marker="o", linestyle="", markerfacecolor=color,
                   markeredgecolor="black", label=diet, markersize=8)
        for diet, color in colors.items()
    ]
    time_handles = [
        plt.Line2D([0], [0], marker=marker, linestyle="", color="black",
                   markerfacecolor="white", label=time, markersize=8)
        for time, marker in markers.items()
    ]
    first_legend = ax.legend(handles=diet_handles, title="Diet factor", loc="upper left")
    ax.add_artist(first_legend)
    ax.legend(handles=time_handles, title="Collection", loc="upper right", ncol=2)
    ax.axhline(0, color="#888888", linewidth=0.6)
    ax.axvline(0, color="#888888", linewidth=0.6)
    ax.set_xlabel(f"PC1 ({variance[0]:.1f}% variance)")
    ax.set_ylabel(f"PC2 ({variance[1]:.1f}% variance)")
    ax.set_title(f"{result['study_id']} / {result['analysis_id']}: within-study PCA")
    ax.spines[["top", "right"]].set_visible(False)
    _save_figure(fig, path)


def plot_exercise_pca(result: dict[str, Any], path: Path) -> None:
    scores = result["scores"]
    colors = {
        "rest": "#000000",
        "stat": "#D55E00",
        "rec3": "#0072B2",
        "rec22": "#6A3D9A",
    }
    labels = {
        "rest": "Rest",
        "stat": "Immediate post",
        "rec3": "3 h recovery",
        "rec22": "22 h recovery",
    }
    variance = result["explained_variance_percent"]
    fig, ax = plt.subplots(figsize=(9, 6.4))
    for time, color in colors.items():
        subset = scores[scores.time_original == time]
        ax.scatter(
            subset.PC1,
            subset.PC2,
            s=55,
            c=color,
            marker="o",
            edgecolors="black",
            linewidths=0.55,
            alpha=0.84,
            label=labels[time],
        )
    ax.axhline(0, color="#888888", linewidth=0.6)
    ax.axvline(0, color="#888888", linewidth=0.6)
    ax.set_xlabel(f"PC1 ({variance[0]:.1f}% variance)")
    ax.set_ylabel(f"PC2 ({variance[1]:.1f}% variance)")
    ax.set_title(f"{result['study_id']} / {result['analysis_id']}: within-study PCA")
    ax.legend(title="Collection time")
    ax.spines[["top", "right"]].set_visible(False)
    _save_figure(fig, path)


def write_pca_outputs(result: dict[str, Any], derived_dir: Path) -> list[Path]:
    """Write scores, loadings, and feature-QC records for one PCA."""

    stem = f"{result['study_id']}_{result['analysis_id']}_pca"
    paths = [
        derived_dir / f"{stem}_scores.csv",
        derived_dir / f"{stem}_loadings.csv",
        derived_dir / f"{stem}_feature_qc.csv",
    ]
    result["scores"].to_csv(paths[0], index=False)
    result["loadings"].to_csv(paths[1], index=False)
    result["feature_qc"].to_csv(paths[2], index=False)
    return paths


def pca_summary_frame(results: Iterable[dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for result in results:
        variance = result["explained_variance_percent"]
        rows.append(
            {
                "study_id": result["study_id"],
                "analysis_id": result["analysis_id"],
                "samples": result["n_samples"],
                "input_feature_rows": result["n_input_features"],
                "pca_features": result["n_pca_features"],
                "missingness_threshold": result["max_missing_fraction"],
                "transform": result["transform"],
                "imputation": result["imputation"],
                "scaling": result["scaling"],
                "PC1_variance_percent": variance[0],
                "PC2_variance_percent": variance[1],
            }
        )
    return pd.DataFrame(rows)
