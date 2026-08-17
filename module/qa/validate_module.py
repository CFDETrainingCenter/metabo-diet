#!/usr/bin/env python3
"""Deterministic release checks for the Metabo-Diet training package."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE = ROOT / "module"


def ok(condition: bool, message: str, failures: list[str]) -> None:
    if condition:
        print(f"PASS  {message}")
    else:
        print(f"FAIL  {message}")
        failures.append(message)


def load_json(path: Path) -> object:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    failures: list[str] = []
    required = [
        MODULE / "content" / f"lesson_{index:02d}_{name}.md"
        for index, name in [
            (1, "why_harmonization_matters"),
            (2, "comparing_study_design"),
            (3, "harmonizing_metabolomics_metadata"),
            (4, "guided_analysis_interpretation"),
            (5, "access_tiers_transfer"),
        ]
    ]
    required += [
        ROOT / "LICENSE",
        MODULE / "content" / "glossary.md",
        MODULE / "content" / "instructor_guide.md",
        MODULE / "assessments" / "pretest.json",
        MODULE / "assessments" / "posttest.json",
        MODULE / "assessments" / "knowledge_checks.json",
        MODULE / "assessments" / "answer_key.md",
        MODULE / "templates" / "cohort_comparison_worksheet_learner.md",
        MODULE / "templates" / "cohort_comparison_worksheet_instructor.md",
        MODULE / "templates" / "metabolite_metadata_crosswalk_learner.md",
        MODULE / "templates" / "metabolite_metadata_crosswalk_instructor.md",
        MODULE / "templates" / "access_tier_transfer_checklist_learner.md",
        MODULE / "templates" / "access_tier_transfer_checklist_instructor.md",
        MODULE / "data" / "provenance.json",
        MODULE / "research" / "study_selection.md",
        MODULE / "notebooks" / "metabo_diet_harmonization.ipynb",
        MODULE / "notebooks" / "metabo_diet_R_appendix.Rmd",
        MODULE / "notebooks" / "install_r_packages.R",
        MODULE / "scripts" / "metabo_diet_R_normalization.R",
        MODULE / "qa" / "local_pilot_protocol.md",
        MODULE / "qa" / "live_mw_audit.json",
    ]
    for path in required:
        ok(path.is_file() and path.stat().st_size > 0, f"required file: {path.relative_to(ROOT)}", failures)

    lesson_text = "\n".join(path.read_text(encoding="utf-8") for path in required[:5] if path.exists())
    ok("ST001521" in lesson_text and "ST003348" in lesson_text, "locked accessions appear in lesson sources", failures)
    provisional_phrases = ["not-yet-locked", "until the final public study pair is locked", "not-yet-resolved"]
    ok(not any(phrase in lesson_text.lower() for phrase in provisional_phrases), "no provisional-study language remains", failures)
    source_claim_text = lesson_text + "\n" + (MODULE / "research" / "study_selection.md").read_text(encoding="utf-8")
    ok(not re.search(r"\b152\b", source_claim_text), "no stale 152-overlap claim remains", failures)
    for key in ("NB-L1", "NB-L2", "NB-L3", "NB-L4", "NB-L5"):
        ok(key in lesson_text, f"learner guide sources cross-reference {key}", failures)

    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8") if (ROOT / "LICENSE").exists() else ""
    attribution_text = (MODULE / "ATTRIBUTION.md").read_text(encoding="utf-8")
    ok("Creative Commons Attribution 4.0" in license_text, "English CC BY 4.0 repository license", failures)
    ok(
        all(section in license_text for section in ("Section 1 -- Definitions", "Section 8 -- Interpretation")),
        "repository contains the canonical CC BY 4.0 legal code",
        failures,
    )
    ok("third-party" in attribution_text.lower(), "attribution excludes unauthorized third-party relicensing", failures)
    ok("Creative Commons Attribution 4.0" in attribution_text, "module attribution states training-material license", failures)

    live_audit_path = MODULE / "qa" / "live_mw_audit.json"
    if live_audit_path.exists():
        live_audit = load_json(live_audit_path)
        ok(live_audit.get("all_ten_endpoints_structurally_valid") is True, "all ten live MW endpoints pass structural validation", failures)
        ok(live_audit.get("all_ten_endpoints_byte_for_byte_cache_match") is True, "all ten live MW endpoints match the immutable cache", failures)
        ok(len(live_audit.get("records", [])) == 10, "live MW audit contains ten endpoint records", failures)

    provenance_path = MODULE / "data" / "provenance.json"
    if provenance_path.exists():
        provenance = load_json(provenance_path)
        pair = provenance.get("primary_pair", {}) if isinstance(provenance, dict) else {}
        overlap = pair.get("overlap", {}) if isinstance(pair, dict) else {}
        ok(pair.get("diet_study_id") == "ST001521", "diet accession in provenance", failures)
        ok(pair.get("exercise_study_id") == "ST003348", "exercise accession in provenance", failures)
        ok(overlap.get("raw_exact_overlap") == 153, "raw RefMet overlap is 153", failures)
        conservative_overlap = overlap.get(
            "recommended_conservative_biological_overlap",
            overlap.get("recommended_biological_overlap"),
        )
        ok(conservative_overlap == 145, "conservative biological RefMet overlap is 145", failures)

        cache_entries = []
        if isinstance(provenance, dict):
            for study in provenance.get("studies", []):
                if isinstance(study, dict):
                    cache_entries.extend(study.get("cached_files", []))
            refmet_cache = provenance.get("refmet_cache")
            if isinstance(refmet_cache, dict):
                cache_entries.append(refmet_cache)
        ok(len(cache_entries) == 11, "provenance enumerates all 11 cached JSON files", failures)
        for entry in cache_entries:
            if not isinstance(entry, dict) or not entry.get("path"):
                ok(False, "cached-file provenance entry is well formed", failures)
                continue
            cached_path = ROOT / entry["path"]
            label = entry["path"]
            ok(cached_path.is_file(), f"cached source exists: {label}", failures)
            if cached_path.is_file():
                content = cached_path.read_bytes()
                ok(len(content) == entry.get("bytes"), f"cached byte count matches: {label}", failures)
                ok(
                    hashlib.sha256(content).hexdigest() == entry.get("sha256"),
                    f"cached SHA-256 matches: {label}",
                    failures,
                )

    for name in ("pretest.json", "posttest.json", "knowledge_checks.json"):
        path = MODULE / "assessments" / name
        if not path.exists():
            continue
        payload = load_json(path)
        questions = payload.get("items", payload.get("questions", payload)) if isinstance(payload, dict) else payload
        ok(isinstance(questions, list) and len(questions) > 0, f"{name} has questions", failures)
        if isinstance(questions, list):
            ids = []
            for question in questions:
                if not isinstance(question, dict):
                    failures.append(f"{name} contains a non-object question")
                    continue
                ids.append(question.get("id"))
                choices = question.get("options", question.get("choices", []))
                answer = question.get(
                    "answer",
                    question.get(
                        "correct_answer",
                        question.get("correctIndex", question.get("correct_index")),
                    ),
                )
                if isinstance(choices, dict):
                    has_answer = isinstance(answer, str) and answer in choices
                else:
                    has_answer = (
                        isinstance(answer, int)
                        and isinstance(choices, list)
                        and 0 <= answer < len(choices)
                    )
                    has_answer = has_answer or (
                        isinstance(answer, str)
                        and isinstance(choices, list)
                        and answer in choices
                    )
                ok(bool(question.get("rationale")), f"{name}:{question.get('id')} has rationale", failures)
                ok(has_answer, f"{name}:{question.get('id')} has valid answer", failures)
            ok(len(ids) == len(set(ids)), f"{name} question IDs are unique", failures)

    answer_key_path = MODULE / "assessments" / "answer_key.md"
    posttest_path = MODULE / "assessments" / "posttest.json"
    if answer_key_path.exists() and posttest_path.exists():
        answer_key_text = answer_key_path.read_text(encoding="utf-8")
        answer_key_rows: dict[str, list[str]] = {}
        for line in answer_key_text.splitlines():
            if re.match(r"^\| POST-\d{2} \|", line):
                fields = [field.strip() for field in line.strip().strip("|").split("|")]
                if len(fields) == 4:
                    answer_key_rows[fields[0]] = fields
        posttest_payload = load_json(posttest_path)
        posttest_items = posttest_payload.get("items", []) if isinstance(posttest_payload, dict) else []
        ok(
            len(answer_key_rows) == len(posttest_items) == 12,
            "posttest answer-key table has all 12 four-column rows",
            failures,
        )
        for item in posttest_items:
            if not isinstance(item, dict):
                continue
            item_id = item.get("id", "")
            row = answer_key_rows.get(item_id)
            expected_objectives = ", ".join(item.get("objective_ids", []))
            ok(
                row is not None
                and row[1] == item.get("answer")
                and row[2] == expected_objectives
                and bool(row[3]),
                f"answer key matches {item_id} answer, objectives, and rationale",
                failures,
            )

    notebook_path = MODULE / "notebooks" / "metabo_diet_harmonization.ipynb"
    if notebook_path.exists():
        notebook = load_json(notebook_path)
        cells = notebook.get("cells", []) if isinstance(notebook, dict) else []
        code_cells = [cell for cell in cells if cell.get("cell_type") == "code"]
        ok(len(cells) >= 20, "notebook has a substantial tutorial sequence", failures)
        ok(all(cell.get("execution_count") is not None for cell in code_cells if "raise NotImplementedError" not in "".join(cell.get("source", []))), "notebook code cells have saved execution evidence", failures)
        execution_counts = [cell.get("execution_count") for cell in code_cells]
        ok(
            execution_counts == list(range(1, len(code_cells) + 1)),
            "notebook code cells have sequential saved execution counts",
            failures,
        )
        error_outputs = [
            output
            for cell in code_cells
            for output in cell.get("outputs", [])
            if output.get("output_type") == "error"
        ]
        ok(not error_outputs, "notebook contains no saved error outputs", failures)
        all_source = "\n".join("".join(cell.get("source", [])) for cell in cells)
        for token in ("ST001521", "ST003348", "QPP", "PCA", "RefMet"):
            ok(token in all_source, f"notebook contains required concept: {token}", failures)
        cell_ids = [cell.get("id") for cell in cells]
        ok(all(cell_ids), "notebook cells have stable IDs", failures)
        ok(len(cell_ids) == len(set(cell_ids)), "notebook cell IDs are unique", failures)
        required_notebook_ids = {
            "nb-setup",
            "nb-l1",
            "nb-l2",
            "nb-l3",
            "nb-l4",
            "nb-l5",
            "nb-l3-crosswalk",
            "nb-l4-pca-diet",
            "nb-l4-pca-exercise",
            "nb-repro",
        }
        ok(required_notebook_ids <= set(cell_ids), "notebook has all stable guide cross-reference IDs", failures)
        for lesson in range(1, 6):
            heading = f"## Lesson {lesson} -"
            ok(all_source.count(heading) == 1, f"notebook has exactly one Lesson {lesson} section", failures)
        setup_tokens = (
            "requirements-dev.txt",
            "python3.12 -m venv",
            "Windows PowerShell",
            "install_r_packages.R",
            "jupyter lab",
            "Virtual environment: active",
            "module/templates/cohort_comparison_worksheet_learner.md",
            "module/templates/metabolite_metadata_crosswalk_learner.md",
            "module/templates/access_tier_transfer_checklist_learner.md",
        )
        ok(all(token in all_source for token in setup_tokens), "notebook contains complete Python/R setup instructions", failures)
        kernelspec = notebook.get("metadata", {}).get("kernelspec", {})
        ok(
            kernelspec.get("display_name") == "Python 3 (ipykernel)",
            "notebook names the kernel that a clean virtual environment provides",
            failures,
        )
        serialized_notebook = json.dumps(notebook)
        private_path_tokens = ("/Users/", "/private/", "\\\\Users\\\\")
        ok(
            not any(token in serialized_notebook for token in private_path_tokens),
            "notebook contains no saved private user or temporary paths",
            failures,
        )
        learner_edit_cells = [
            cell
            for cell in code_cells
            if "learner-edit" in cell.get("metadata", {}).get("tags", [])
        ]
        ok(len(learner_edit_cells) >= 5, "notebook includes learner-edit scaffolds across lessons", failures)
        action_predecessors = []
        for index, cell in enumerate(cells):
            if cell.get("cell_type") != "code":
                continue
            previous = "".join(cells[index - 1].get("source", [])) if index else ""
            action_predecessors.append("Run now" in previous or "Learner edit" in previous)
        ok(all(action_predecessors), "every code cell has an explicit preceding learner action", failures)
        ok(not re.search(r"concat\([^\n]*(diet|exercise)[^\n]*(exercise|diet)", all_source, flags=re.I), "no obvious raw cross-study matrix concatenation", failures)

    overlap_table = MODULE / "data" / "derived" / "refmet_overlap_counts.csv"
    if overlap_table.exists():
        with overlap_table.open(encoding="utf-8", newline="") as handle:
            overlap_rows = {row["metric"]: int(row["value"]) for row in csv.DictReader(handle)}
        ok(overlap_rows.get("raw_exact_refmet_overlap") == 153, "derived overlap table reports 153 raw names", failures)
        ok(overlap_rows.get("conservative_biological_refmet_overlap") == 145, "derived overlap table reports 145 conservative names", failures)

    pca_table = MODULE / "data" / "derived" / "pca_preprocessing_summary.csv"
    if pca_table.exists():
        with pca_table.open(encoding="utf-8", newline="") as handle:
            pca_rows = {row["study_id"]: row for row in csv.DictReader(handle)}
        expected_pca = {"ST001521": (150, 212), "ST003348": (76, 313)}
        for study_id, (sample_count, feature_count) in expected_pca.items():
            row = pca_rows.get(study_id, {})
            ok(int(row.get("samples", -1)) == sample_count, f"{study_id} PCA sample count is {sample_count}", failures)
            ok(int(row.get("pca_features", -1)) == feature_count, f"{study_id} PCA feature count is {feature_count}", failures)

    scorm_zip = MODULE / "scorm" / "metabo_diet_scorm_1_2.zip"
    if scorm_zip.exists():
        with zipfile.ZipFile(scorm_zip) as archive:
            names = set(archive.namelist())
            ok("imsmanifest.xml" in names, "SCORM archive contains root manifest", failures)
            ok("index.html" in names, "SCORM archive contains launch page", failures)
            ok(archive.testzip() is None, "SCORM archive passes CRC checks", failures)

    if failures:
        print(f"\n{len(failures)} validation check(s) failed.")
        return 1
    print("\nAll deterministic module checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
