"""Populate the scaffolded Metabo-Diet tutorial notebook.

Run with the pinned development environment from the repository root:

    .venv/bin/python module/scripts/build_metabo_diet_notebook.py
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import nbformat


REPO_DIR = Path(__file__).resolve().parents[2]
NOTEBOOK_PATH = REPO_DIR / "module" / "notebooks" / "metabo_diet_harmonization.ipynb"


def _stable_cell_id(kind: str, source: str) -> str:
    """Return a deterministic notebook cell ID derived from its source."""
    digest = hashlib.sha1(source.strip().encode("utf-8")).hexdigest()[:12]
    return f"{kind}-{digest}"


def md(source: str, *, cell_id: str | None = None, tags: tuple[str, ...] = ()):
    normalized = source.strip()
    cell = nbformat.v4.new_markdown_cell(normalized)
    cell["id"] = cell_id or _stable_cell_id("md", normalized)
    if tags:
        cell.metadata["tags"] = list(tags)
    return cell


def code(source: str, *, cell_id: str | None = None, tags: tuple[str, ...] = ()):
    normalized = source.strip()
    cell = nbformat.v4.new_code_cell(normalized)
    cell["id"] = cell_id or _stable_cell_id("code", normalized)
    if tags:
        cell.metadata["tags"] = list(tags)
    return cell


def build() -> None:
    notebook = nbformat.read(NOTEBOOK_PATH, as_version=4)
    notebook.metadata["kernelspec"] = {
        "display_name": "Python 3 (Metabo-Diet)",
        "language": "python",
        "name": "python3",
    }
    notebook.metadata["language_info"] = {"name": "python", "version": "3.12"}
    notebook.cells = [
        md(
            """
# Metabo-Diet: harmonizing public diet and exercise metabolomics

**Audience.** Learners who can read a data table and a scatterplot. No prior experience with Metabolomics Workbench (MW), RefMet, a terminal, or Jupyter is required. The notebook guides the analysis; it is not a general introduction to Python.

**Prerequisites.** Python 3.11 or 3.12 and the packages in `requirements-dev.txt`. The optional R companion uses R 4.3 or later. All learner data are public Metabolomics Workbench records.

**By the end, you can:**

1. retrieve and validate MW's split `summary`, `factors`, `analysis`, `metabolites`, and `data` endpoints;
2. derive participant IDs and tidy longitudinal factors without inventing a balanced panel;
3. distinguish repository-provided RefMet mappings from analytical equivalence;
4. audit isotope-labeled/internal-standard collisions before reporting biological overlap;
5. run PCA within one study and analysis after the notebook explains and applies its preprocessing; and
6. state interpretation limits created by plasma-versus-serum, platform, timepoint, and co-intervention differences.

**Guided-analysis time:** about 40 minutes. The full asynchronous module is 2.5 hours.
""",
            cell_id="nb-overview",
        ),
        md(
            """
## How to use the notebook with the learner guide

Complete the setup section below, then take the pretest in the learner guide. For each lesson:

1. Read the matching lesson in the guide.
2. Open the notebook section with the same key (`NB-L1` through `NB-L5`).
3. Run each code cell after a **Run now** heading, from top to bottom.
4. At a **Learner edit** heading, change only the named ALL_CAPS value or clearly marked response text, then run that cell.
5. Compare the output with the stated result. Stop if a check fails.
6. Write the requested response and use the **Ready to move on?** note before continuing.

| Learner guide | Notebook section | Main notebook action |
|---|---|---|
| Lesson 1 - Why harmonization matters | `NB-L1` | Verify the environment, configuration, and scientific boundary |
| Lesson 2 - Comparing study design | `NB-L2` | Retrieve endpoints and audit study/sample structure |
| Lesson 3 - Harmonizing metadata/metabolites | `NB-L3` | Build and inspect the RefMet crosswalk |
| Lesson 4 - Guided analysis and interpretation | `NB-L4` | Summarize classes, run separate PCAs, and complete the class exercise |
| Lesson 5 - Access patterns and transfer | `NB-L5` | Draft a transfer decision and run the reproducibility audit |

The exact filename is `module/notebooks/metabo_diet_harmonization.ipynb`. Headings and visible keys, rather than cell numbers, are the durable cross-references used by the PDF guide.
""",
            cell_id="nb-guide-crosswalk",
        ),
        md(
            """
<a id="nb-setup"></a>
## Environment setup (`NB-SETUP`) - complete before Lesson 1

Keep the extracted `module/` tree intact. Open a terminal in the directory that contains `module/`. If you have not used a terminal or Jupyter before, read `module/content/getting_started.md` or the **Before you begin** section of the learner guide first.

### 1. Install the runtimes once

- Install **Python 3.11 or 3.12** from <https://www.python.org/downloads/>. During Windows installation, enable the option that adds Python to `PATH`.
- Install **R 4.3 or later** from <https://cran.r-project.org/> only if you plan to use the R companion.
- A Jupyter interface is included in `requirements-dev.txt`; VS Code with the Jupyter extension is also acceptable.

### 2. Create the Python environment and install packages

macOS or Linux:

```bash
python3.12 --version
python3.12 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -r module/notebooks/requirements-dev.txt
./.venv/bin/python -m jupyter lab module/notebooks/metabo_diet_harmonization.ipynb
```

Windows PowerShell:

```powershell
py -3.12 --version
py -3.12 -m venv .venv
.\\.venv\\Scripts\\python.exe -m pip install --upgrade pip
.\\.venv\\Scripts\\python.exe -m pip install -r module\\notebooks\\requirements-dev.txt
.\\.venv\\Scripts\\python.exe -m jupyter lab module\\notebooks\\metabo_diet_harmonization.ipynb
```

Python 3.11 is also supported; substitute the 3.11 command if its version check reports Python 3.11. Select the **Python 3 (Metabo-Diet)** kernel if prompted.

### 3. Use Jupyter

- Choose **Kernel > Restart Kernel** before Lesson 1 so you run the required cells yourself rather than relying on saved example outputs.
- Click a code cell and press **Shift+Enter**. `[*]` means running; a number such as `[1]` means complete.
- Edit only cells introduced by a **Learner edit** heading.
- A red traceback means stop. Keep the error message and fix the environment or the earlier failed check before continuing.

For an optional noninteractive installation test, write to a separate file: `./.venv/bin/python module/scripts/execute_notebook.py --output metabo_diet_smoke_test.ipynb` on macOS/Linux or `.\\.venv\\Scripts\\python.exe module\\scripts\\execute_notebook.py --output metabo_diet_smoke_test.ipynb` on Windows. This test does not complete the learner activities.

### 4. Use the optional R companion

You can read the pre-rendered `module/notebooks/metabo_diet_R_appendix.html` without installing R. To rerun it, install R 4.3 or later and RStudio or another Pandoc installation. Confirm Pandoc with `Rscript -e 'stopifnot(rmarkdown::pandoc_available())'`, then run:

```bash
Rscript module/notebooks/install_r_packages.R
Rscript -e 'rmarkdown::render("module/notebooks/metabo_diet_R_appendix.Rmd")'
```

The cached path needs no network after package installation. For optional live R retrieval, run the installer with `--live` before setting `METABO_DIET_LIVE=1`. Python live retrieval uses the packages already listed in `requirements-dev.txt`.
""",
            cell_id="nb-setup",
            tags=("setup",),
        ),
        md(
            """
### Run now - verify Python and the complete package set

Run this diagnostic before importing the analysis libraries. **Stop** if it reports a missing package or an unsupported Python version. Reinstall `requirements-dev.txt` with the `.venv` Python command from setup, restart the kernel, and run this cell again.
""",
            cell_id="nb-setup-action",
        ),
        code(
            """
from importlib.metadata import PackageNotFoundError, version
import platform
import sys

SUPPORTED_PYTHON = {(3, 11), (3, 12)}
REQUIRED_DISTRIBUTIONS = (
    "numpy",
    "pandas",
    "requests",
    "scikit-learn",
    "matplotlib",
    "IPython",
    "nbformat",
    "nbclient",
    "ipykernel",
    "jupyterlab",
)

if sys.version_info[:2] not in SUPPORTED_PYTHON:
    raise RuntimeError(
        f"Use Python 3.11 or 3.12; this kernel is {platform.python_version()}."
    )

installed = {}
missing = []
for distribution in REQUIRED_DISTRIBUTIONS:
    try:
        installed[distribution] = version(distribution)
    except PackageNotFoundError:
        missing.append(distribution)

if missing:
    raise RuntimeError(
        "Missing packages: " + ", ".join(missing)
        + ". Install module/notebooks/requirements-dev.txt and restart the kernel."
    )

print(f"Python {platform.python_version()} - environment check passed")
for distribution, installed_version in installed.items():
    print(f"  {distribution}=={installed_version}")
""",
            cell_id="nb-setup-check",
            tags=("setup", "execute"),
        ),
        md(
            """
<a id="nb-l1"></a>
## Lesson 1 - Why harmonization matters (`NB-L1`)

### Before you start

Read Lesson 1 in the learner guide before running the configuration cell. Then:

1. Review the scientific boundary below.
2. Run the configuration cell once.
3. Confirm the two accessions and the retrieval mode.
4. Record why the two quantitative matrices must remain separate.

### Scientific boundary before any analysis

The studies answer different questions. ST001521 is longitudinal plasma metabolomics during controlled feeding, with antibiotics on days 6–8 and a polyethylene glycol purge on day 7. ST003348 is serum metabolomics around an acute endurance race-walking bout. Exact RefMet names let us compare *nomenclature and coverage*; they do not prove matching isomers, annotation certainty, extraction recovery, or quantitative calibration.

For that reason, this tutorial compares metadata, mapped-name presence, class coverage, and separately standardized within-study patterns. It never concatenates the raw peak-area matrices.
""",
            cell_id="nb-l1",
            tags=("lesson-1",),
        ),
        md(
            """
### Run now - configure paths, packages, and locked accessions

Expected output: the local `module/` directory and either `validated cache` (default) or `live with cache fallback`. **Stop** if either accession differs from `ST001521` and `ST003348`.
""",
            cell_id="nb-l1-config-action",
        ),
        code(
            """
from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
from IPython.display import display


def locate_module_dir(start: Path) -> Path:
    for parent in [start.resolve(), *start.resolve().parents]:
        if (parent / "data" / "raw").is_dir() and (parent / "scripts").is_dir():
            return parent
        if (parent / "module" / "data" / "raw").is_dir():
            return parent / "module"
    raise FileNotFoundError("Could not locate module/data/raw")


MODULE_DIR = locate_module_dir(Path.cwd())
RAW_DIR = MODULE_DIR / "data" / "raw"
DERIVED_DIR = MODULE_DIR / "data" / "derived"
FIGURES_DIR = MODULE_DIR / "figures"
DERIVED_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Keep plotting caches out of learner artifacts while remaining sandbox-friendly.
os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "metabo_diet_mpl"))
sys.path.insert(0, str(MODULE_DIR / "scripts"))

from metabo_diet_pipeline import (
    MW_ENDPOINTS,
    build_metabolite_crosswalk,
    derive_tidy_factors,
    load_studies,
    pca_summary_frame,
    plot_class_summary,
    plot_diet_pca,
    plot_exercise_pca,
    plot_overlap_counts,
    run_within_study_pca,
    write_pca_outputs,
)

# Required accession constants: change these only after re-auditing study design.
DIET_ACCESSION = "ST001521"
EXERCISE_ACCESSION = "ST003348"

# Matched positive-ion, reversed-phase analyses chosen for readable demonstrations.
# Each is analyzed on its own scale; this selection does not make them quantitatively equivalent.
DIET_ANALYSIS_ID = "AN002534"
EXERCISE_ANALYSIS_ID = "AN005483"

# Set METABO_DIET_LIVE=1 to try each split REST endpoint first. The validated cache
# is the deterministic default and is also used whenever a live request fails.
PREFER_LIVE_API = os.getenv("METABO_DIET_LIVE", "0") == "1"

pd.set_option("display.max_colwidth", 80)
print("Module directory located successfully: module/")
print(f"Diet accession: {DIET_ACCESSION}")
print(f"Exercise accession: {EXERCISE_ACCESSION}")
print(f"Retrieval mode: {'live with cache fallback' if PREFER_LIVE_API else 'validated cache'}")
""",
            cell_id="nb-l1-config",
            tags=("lesson-1", "execute"),
        ),
        md(
            """
### Ready to move on?

In Section 1 of the cohort-comparison worksheet, write one sentence explaining why the two peak-area matrices must stay separate. Continue when the output shows `ST001521`, `ST003348`, and the intended retrieval mode.
""",
            cell_id="nb-l1-complete",
            tags=("lesson-1",),
        ),
        md(
            """
<a id="nb-l2"></a>
## Lesson 2 - Comparing study design and phenotype capture (`NB-L2`)

### Before you start

Read Lesson 2 in the learner guide and open `cohort_comparison_worksheet.md`. In this section:

1. Load all five split endpoints for each study.
2. Verify endpoint and analysis counts.
3. Derive biological samples, participant IDs, specimen, condition, and time.
4. Record at least one direct, partial, and non-comparable field in the worksheet.

### L2.1 Retrieve and validate split MW endpoints

MW publishes different record types at separate URLs. `load_studies` requests each endpoint independently when live mode is enabled, validates required fields and study IDs, and then falls back endpoint-by-endpoint to `data/raw/{accession}_{endpoint}.json` if needed. This is safer than treating a partial or malformed response as complete data.
""",
            cell_id="nb-l2",
            tags=("lesson-2",),
        ),
        md(
            """
### Run now - load the ten endpoint responses

Expected output: ten rows, one for each study-endpoint pair. **Stop** if any source is neither `validated cache` nor a recorded live response with cache fallback.
""",
            cell_id="nb-l2-load-action",
        ),
        code(
            """
studies, source_log = load_studies(
    [DIET_ACCESSION, EXERCISE_ACCESSION],
    RAW_DIR,
    prefer_live=PREFER_LIVE_API,
)
source_log_path = DERIVED_DIR / "input_source_log.csv"
source_log.to_csv(source_log_path, index=False)

assert set(source_log.endpoint) == set(MW_ENDPOINTS), (
    f"Expected endpoints {sorted(MW_ENDPOINTS)}; found {sorted(source_log.endpoint.unique())}. "
    "Stop and verify the configured accessions and cache files."
)
assert source_log.shape[0] == 10, (
    f"Expected 10 study-endpoint rows; found {source_log.shape[0]}. "
    "Stop and review the source log before continuing."
)
display(source_log[["study_id", "endpoint", "source", "url"]])
""",
            cell_id="nb-l2-load",
            tags=("lesson-2", "execute"),
        ),
        md(
            """
### Run now - compare endpoint sizes and analytical modes

Observe the factor, metabolite, and analysis counts. Record the analysis IDs, modes, and units in the cohort-comparison worksheet before continuing.
""",
            cell_id="nb-l2-endpoint-action",
        ),
        code(
            """
endpoint_counts = []
for study_id, payloads in studies.items():
    for endpoint, payload in payloads.items():
        endpoint_counts.append(
            {
                "study_id": study_id,
                "endpoint": endpoint,
                "records": 1 if endpoint == "summary" else len(payload),
            }
        )
endpoint_counts = pd.DataFrame(endpoint_counts)
display(endpoint_counts.pivot(index="endpoint", columns="study_id", values="records"))

analysis_table = pd.concat(
    [pd.DataFrame(payloads["analysis"].values()) for payloads in studies.values()],
    ignore_index=True,
)
display(
    analysis_table[
        ["study_id", "analysis_id", "analysis_summary", "chromatography_type", "ion_mode", "units"]
    ]
)
""",
            cell_id="nb-l2-endpoint-audit",
            tags=("lesson-2", "execute"),
        ),
        md(
            """
**Observe and record.** The expected endpoint sizes are 160 versus 76 factor rows, 567 versus 593 analyte-analysis rows, and four versus two analyses. Counts describe the endpoint actually used - not larger project-level totals that may appear in a paper or narrative. If these values differ, record the discrepancy and stop to investigate the release/cache version.
"""
        ),
        md(
            """
### L2.2 Tidy factors and derive participant IDs

Factor strings are parsed at the first colon in each pipe-separated component. The rules are explicit:

- ST001521 participant ID = digits before the first hyphen; pooled-plasma QC IDs `QPP01`–`QPP10` are excluded.
- ST003348 participant ID = integer before the underscore. Suffixes 1–4 must agree with `rest`, `stat`, `rec3`, and `rec22`.
- Original source terms remain in the table; a separate field harmonizes plasma versus serum.
""",
            cell_id="nb-l2-factors",
        ),
        md(
            """
### Run now - create the biological sample table

Expected output: 150 diet-study biological samples from 30 participants and 76 exercise-study samples from 19 participants. The displayed rows retain original labels beside harmonized fields.
""",
            cell_id="nb-l2-factor-action",
        ),
        code(
            """
tidy_factors = derive_tidy_factors(
    studies, DIET_ACCESSION, EXERCISE_ACCESSION
)
tidy_factors_path = DERIVED_DIR / "tidy_factors.csv"
tidy_factors.to_csv(tidy_factors_path, index=False)

factor_counts = (
    tidy_factors.groupby(["study_id", "study_role"], as_index=False)
    .agg(
        samples=("local_sample_id", "nunique"),
        participants=("participant_id", "nunique"),
        timepoints=("time_original", "nunique"),
    )
)
display(factor_counts)
display(tidy_factors.head(8))
""",
            cell_id="nb-l2-factor-table",
            tags=("lesson-2", "execute"),
        ),
        md(
            """
### Run now - audit timepoints and stop conditions

The assertions verify exclusion of `QPP...` pooled-QC samples from biological counts and the expected study-specific sample totals. **Stop** on any assertion failure; do not repair counts by dropping rows without evidence.
""",
            cell_id="nb-l2-time-action",
        ),
        code(
            """
timepoint_counts = (
    tidy_factors.groupby(
        ["study_id", "condition_original", "time_original", "time_order"],
        dropna=False,
        as_index=False,
    )
    .agg(samples=("local_sample_id", "nunique"))
    .sort_values(["study_id", "condition_original", "time_order"])
)
display(timepoint_counts)

diet_biological = tidy_factors.query("study_id == @DIET_ACCESSION")
exercise_biological = tidy_factors.query("study_id == @EXERCISE_ACCESSION")
diet_qpp_count = diet_biological.local_sample_id.str.startswith("QPP").sum()
assert diet_qpp_count == 0, (
    f"Expected 0 QPP rows in the biological table; found {diet_qpp_count}. "
    "Stop and review sample_role assignment."
)
assert diet_biological.shape[0] == 150, (
    f"Expected 150 diet-study biological samples; found {diet_biological.shape[0]}. "
    "Stop and review the factor parsing and cache version."
)
assert exercise_biological.shape[0] == 76, (
    f"Expected 76 exercise-study biological samples; found {exercise_biological.shape[0]}. "
    "Stop and review the factor parsing and cache version."
)
""",
            cell_id="nb-l2-time-audit",
            tags=("lesson-2", "execute"),
        ),
        md(
            """
### Learner edit - inspect one study before comparing it

Choose `DIET_ACCESSION` or `EXERCISE_ACCESSION`, predict the number of participants and timepoints, then run the scaffold. Record the result in Sections 3 and 6 of the cohort-comparison worksheet, and put one unsafe design difference in Section 9.
""",
            cell_id="nb-l2-learner-prompt",
        ),
        code(
            """
# Learner-edit cell: change this to EXERCISE_ACCESSION for the second case.
STUDY_TO_AUDIT = DIET_ACCESSION

study_audit = (
    tidy_factors.query("study_id == @STUDY_TO_AUDIT")
    .groupby(["condition_original", "time_original"], dropna=False, as_index=False)
    .agg(samples=("local_sample_id", "nunique"), participants=("participant_id", "nunique"))
)
display(study_audit)
""",
            cell_id="nb-l2-learner-edit",
            tags=("lesson-2", "learner-edit", "execute"),
        ),
        md(
            """
### Interpretation guardrail: a time label is not a treatment label

Do not force a balanced panel: the FARMM factor endpoint has nine Western-male Day 5 rows and eleven Western-male Day 9 rows. More importantly, days 9, 12, and 15 occur during or after antibiotic/PEG perturbation, so they are not diet-only contrasts. Exercise collections also differ in fasting status and clock time. `interpretation_context` keeps those design facts beside every sample.

### Ready to move on?

Continue when the endpoint checks pass and Sections 3, 5, 6, and 9 of the cohort-comparison worksheet distinguish samples from participants, plasma from serum, and diet-study days from exercise-recovery hours.
"""
        ),
        md(
            """
<a id="nb-l3"></a>
## Lesson 3 - Harmonizing metabolomics and metadata (`NB-L3`)

### Before you start

Read Lesson 3 in the learner guide and open `metabolite_metadata_crosswalk.md`. In this section:

1. Preserve source names and analysis identifiers.
2. Build the raw exact-name overlap.
3. Audit labeled-standard collisions before calling an overlap biological.
4. Trace one retained RefMet name back to both studies.

### L3.1 Build an auditable RefMet crosswalk (`NB-L3-CROSSWALK`)

The pipeline preserves every source-reported name, analysis ID, MW metabolite ID, RefMet name/class, mapping evidence, confidence language, and inclusion decision.

The raw exact intersection is intentionally shown before cleanup. ST003348 contains ten explicit stable-isotope/internal-standard rows. Eight RefMet labels from those rows collide with the raw overlap. We conservatively remove those labels - even when an unlabeled row shares the same RefMet label - because the study-level endpoint alone does not tell us which signal should represent the biological compound. This produces the pre-specified conservative overlap of 145.
""",
            cell_id="nb-l3",
            tags=("lesson-3",),
        ),
        md(
            """
### Run now - construct and save the crosswalk audit tables

Expected output: 510 diet names, 475 exercise names, 153 raw exact overlaps, and 145 conservatively retained overlaps. **Stop** if the output skips the raw audit stage or drops provenance columns.
""",
            cell_id="nb-l3-build-action",
        ),
        code(
            """
with (RAW_DIR / "refmet_classification.json").open(encoding="utf-8") as handle:
    refmet_classification = json.load(handle)

(
    mapping_audit,
    overlap_audit,
    metabolite_crosswalk,
    class_summary,
    overlap_counts,
) = build_metabolite_crosswalk(
    studies,
    refmet_classification,
    DIET_ACCESSION,
    EXERCISE_ACCESSION,
)

derived_tables = {
    "metabolite_mapping_audit.csv": mapping_audit,
    "refmet_overlap_audit.csv": overlap_audit,
    "metabolite_crosswalk.csv": metabolite_crosswalk,
    "refmet_class_summary.csv": class_summary,
    "refmet_overlap_counts.csv": pd.DataFrame(
        [{"metric": key, "value": value} for key, value in overlap_counts.items()]
    ),
}
for filename, table in derived_tables.items():
    table.to_csv(DERIVED_DIR / filename, index=False)

display(pd.DataFrame([overlap_counts]).T.rename(columns={0: "count"}))
""",
            cell_id="nb-l3-crosswalk",
            tags=("lesson-3", "execute"),
        ),
        md(
            """
### Run now - inspect the excluded labeled-standard evidence

Observe the source-reported label, RefMet label, detection evidence, and row decision. The assertions require 153 raw rows, eight standard-label collisions, and 145 retained names.
""",
            cell_id="nb-l3-standard-action",
        ),
        code(
            """
standard_audit = mapping_audit.query(
    "study_id == @EXERCISE_ACCESSION and isotope_internal_standard_row"
)[
    [
        "analysis_id",
        "source_reported_name",
        "refmet_name",
        "mapping_status",
        "standard_detection_evidence",
        "row_decision",
    ]
]
display(standard_audit)

assert overlap_audit.shape[0] == 153, (
    f"Expected 153 raw exact RefMet overlaps; found {overlap_audit.shape[0]}. "
    "Stop and review source versions, blank handling, and duplicate collapse."
)
standard_collisions = int(overlap_audit.exercise_standard_collision.sum())
assert standard_collisions == 8, (
    f"Expected 8 labeled-standard collisions; found {standard_collisions}. "
    "Stop and inspect the source labels before applying exclusions."
)
assert metabolite_crosswalk.shape[0] == 145, (
    f"Expected 145 retained RefMet names; found {metabolite_crosswalk.shape[0]}. "
    "Stop and review the standard-collision rule."
)
""",
            cell_id="nb-l3-standard-audit",
            tags=("lesson-3", "execute"),
        ),
        md(
            """
### Run now - plot the overlap stages and preview retained provenance

The bar chart must distinguish the raw and conservative counts. The table underneath should let you trace a retained name to both source labels and analysis IDs.
""",
            cell_id="nb-l3-overlap-action",
        ),
        code(
            """
plot_overlap_counts(overlap_counts, FIGURES_DIR / "refmet_overlap_summary.png")
display(
    metabolite_crosswalk[
        [
            "refmet_name",
            "main_class",
            "diet_source_reported_names",
            "diet_analysis_ids",
            "exercise_source_reported_names",
            "exercise_analysis_ids",
            "mapping_confidence",
            "decision_reason",
        ]
    ].head(10)
)
""",
            cell_id="nb-l3-overlap-plot",
            tags=("lesson-3", "execute"),
        ),
        md(
            """
![High-contrast bar chart showing 510 diet RefMet names, 475 exercise RefMet names, a raw exact overlap of 153, and a conservative biological overlap of 145 after standard-label cleanup.](../figures/refmet_overlap_summary.png)

**What the result means.** The crosswalk shows which RefMet names occur in both studies and preserves the source evidence. It does not make the measurements quantitatively interchangeable.
""",
            cell_id="nb-l3-overlap-figure",
        ),
        md(
            """
### Learner edit - trace one retained name

Choose a different row if desired. In Tab A of the metabolite/metadata crosswalk, record the submitted names and analysis IDs from both studies. Add one sentence explaining why the shared RefMet key does not prove equal concentration or identification certainty.
""",
            cell_id="nb-l3-learner-prompt",
        ),
        code(
            """
# Learner-edit cell: replace this value with another retained RefMet name.
REFMET_TO_TRACE = metabolite_crosswalk.iloc[0]["refmet_name"]

trace_columns = [
    "refmet_name",
    "main_class",
    "diet_source_reported_names",
    "diet_analysis_ids",
    "exercise_source_reported_names",
    "exercise_analysis_ids",
    "mapping_confidence",
    "decision_reason",
]
display(metabolite_crosswalk.query("refmet_name == @REFMET_TO_TRACE")[trace_columns])
""",
            cell_id="nb-l3-learner-edit",
            tags=("lesson-3", "learner-edit", "execute"),
        ),
        md(
            """
### Ready to move on?

Continue when all three overlap checks pass and Tab A of the crosswalk records the source names, analysis IDs, mapping evidence, uncertainty, and exclusion decision for at least one retained example and one labeled standard.
""",
            cell_id="nb-l3-complete",
        ),
        md(
            """
<a id="nb-l4"></a>
## Lesson 4 - Guided analysis and biological interpretation (`NB-L4`)

### Before you start

Read Lesson 4 in the learner guide before generating figures. Use the `NB-L4-CLASS`, `NB-L4-PCA-DIET`, and `NB-L4-PCA-EXERCISE` keys cited there.

### L4.1 Summarize overlap by RefMet class (`NB-L4-CLASS`)

Class counts come from the cached RefMet classification table using exact name lookup. The full CSV keeps both super-class and main-class labels so a broad class cannot silently replace a specific one.
""",
            cell_id="nb-l4",
            tags=("lesson-4",),
        ),
        md(
            """
### Run now - create the class summary

Expected output: the class counts sum to 145. Treat the result as assay/name coverage, not pathway enrichment.
""",
            cell_id="nb-l4-class-action",
        ),
        code(
            """
plot_class_summary(class_summary, FIGURES_DIR / "refmet_class_summary.png")
display(class_summary.head(15))

class_total = int(class_summary.refmet_count.sum())
assert class_total == 145, (
    f"Expected class counts to sum to 145; found {class_total}. "
    "Stop and review the RefMet classification join."
)
classified_overlap = overlap_counts["conservative_overlap_with_refmet_class"]
assert classified_overlap == 145, (
    f"Expected 145 retained names with class data; found {classified_overlap}. "
    "Stop and inspect missing or duplicate class mappings."
)
""",
            cell_id="nb-l4-class-summary",
            tags=("lesson-4", "execute"),
        ),
        md(
            """
![Horizontal high-contrast bar chart of the twelve largest RefMet main classes among the 145 conservative shared metabolite names.](../figures/refmet_class_summary.png)

Class abundance reflects what these assays annotated and what RefMet classified. It is not pathway enrichment and does not adjust for how many compounds exist in each class.
""",
            cell_id="nb-l4-class-figure",
        ),
        md(
            """
### L4.2 PCA - within each study and selected analysis only

For a transparent teaching workflow, each selected matrix is processed independently:

1. keep biological sample IDs from the validated factor table;
2. for ST003348, remove explicit isotope/internal-standard feature rows;
3. exclude features with more than 20% missing values;
4. transform as `log2(peak area + 1)`;
5. median-impute each feature on the logged scale;
6. remove zero-variance features and autoscale each remaining feature; and
7. fit a two-component PCA to that one study/analysis matrix.

In plain language, `log2(peak area + 1)` compresses very large values, median imputation fills a missing entry with the middle observed value for that feature, and autoscaling puts features on comparable standardized scales so the largest raw ranges do not dominate. You do not need to understand every line of the implementation to follow the audit; focus on what enters the model, what the preprocessing changes, and what the plot can support.

PCA is exploratory. Separation can reflect biology, time, diet, fasting, collection, analytical mode, or other unmodeled structure. PCA does not establish differential abundance or causal effects.
""",
            cell_id="nb-l4-pca-method",
        ),
        md(
            """
### Run now - fit the diet-study PCA (`NB-L4-PCA-DIET`)

Expected output: 150 biological plasma samples from `AN002534`; pooled `QPP...` samples are excluded. Record PC1/PC2 explained variance and two plausible sources of pattern besides diet.
""",
            cell_id="nb-l4-pca-diet-action",
        ),
        code(
            """
diet_pca = run_within_study_pca(
    DIET_ACCESSION,
    DIET_ANALYSIS_ID,
    studies[DIET_ACCESSION],
    tidy_factors,
    exclude_isotope_standards=False,
    max_missing_fraction=0.20,
)
write_pca_outputs(diet_pca, DERIVED_DIR)
plot_diet_pca(diet_pca, FIGURES_DIR / "ST001521_AN002534_pca.png")

display(pca_summary_frame([diet_pca]))
""",
            cell_id="nb-l4-pca-diet",
            tags=("lesson-4", "execute"),
        ),
        md(
            """
![ST001521 positive reversed-phase PCA with points colored by original diet factor and marker shapes indicating Baseline, Day 5, Day 9, Day 12, and Day 15; axes report explained variance.](../figures/ST001521_AN002534_pca.png)

### What this plot shows

The plot summarizes 150 plasma samples from AN002534. It does not isolate a diet effect: arms differ in setting and prior diet, while post-day-5 collections are entangled with antibiotics and PEG. Overlapping points do not prove equivalence, and separated points do not identify the features or mechanisms responsible.
""",
            cell_id="nb-l4-pca-diet-figure",
        ),
        md(
            """
### Run now - fit the exercise-study PCA (`NB-L4-PCA-EXERCISE`)

Expected output: 76 serum samples from `AN005483`, after explicit labeled-standard exclusion. Record PC1/PC2 explained variance and why this is not a repeated-measures hypothesis test.
""",
            cell_id="nb-l4-pca-exercise-action",
        ),
        code(
            """
exercise_pca = run_within_study_pca(
    EXERCISE_ACCESSION,
    EXERCISE_ANALYSIS_ID,
    studies[EXERCISE_ACCESSION],
    tidy_factors,
    exclude_isotope_standards=True,
    max_missing_fraction=0.20,
)
write_pca_outputs(exercise_pca, DERIVED_DIR)
plot_exercise_pca(exercise_pca, FIGURES_DIR / "ST003348_AN005483_pca.png")

pca_summary = pca_summary_frame([diet_pca, exercise_pca])
pca_summary.to_csv(DERIVED_DIR / "pca_preprocessing_summary.csv", index=False)
display(pca_summary)
""",
            cell_id="nb-l4-pca-exercise",
            tags=("lesson-4", "execute"),
        ),
        md(
            """
![ST003348 positive reversed-phase PCA of 76 serum samples, with high-contrast colors for rest, immediate post-exercise, 3-hour recovery, and 22-hour recovery; axes report explained variance.](../figures/ST003348_AN005483_pca.png)

### What this plot shows

The plot summarizes AN005483 only, after excluding its explicit labeled-standard rows. Within-person repeated measures remain correlated, and collection time overlaps with fasting and clock-time changes. PCA alone is not a repeated-measures test.
""",
            cell_id="nb-l4-pca-exercise-figure",
        ),
        md(
            """
### Why the two matrices stay separate

There is intentionally no code that stacks ST001521 and ST003348 peak areas. Plasma versus serum, separate extraction and chromatography methods, different analytical analyses, and uncalibrated peak-area scales make a combined PCA dominated by study/platform effects and therefore uninterpretable as a diet-versus-exercise contrast.

Safe cross-study targets here are RefMet presence, class coverage, mapping provenance, and separately computed within-study summaries.
""",
            cell_id="nb-l4-pca-guardrail",
        ),
        md(
            """
### L4.3 Learner edit - audit one shared class

Choose one RefMet main class and answer:

1. How many conservative shared names belong to it?
2. Do any names map to more than one analysis within either study?
3. What claim can you make, and what claim must you avoid?

Predict your result before running the scaffold. Change `CLASS_TO_INSPECT` to explore another class, then record the class, count, and claim limit in your Lesson 4 notes.
""",
            cell_id="nb-l4-exercise-prompt",
        ),
        code(
            """
# Answer scaffold (runs with a safe default; edit the class name to explore).
CLASS_TO_INSPECT = class_summary.iloc[0]["main_class"]

class_crosswalk = metabolite_crosswalk.query("main_class == @CLASS_TO_INSPECT").copy()
class_answer = {
    "main_class": CLASS_TO_INSPECT,
    "shared_refmet_names": class_crosswalk.refmet_name.nunique(),
    "diet_names_with_multiple_analyses": int(
        class_crosswalk.diet_analysis_ids.str.contains(";").sum()
    ),
    "exercise_names_with_multiple_analyses": int(
        class_crosswalk.exercise_analysis_ids.str.contains(";").sum()
    ),
}
display(pd.DataFrame([class_answer]))
display(
    class_crosswalk[
        [
            "refmet_name",
            "diet_source_reported_names",
            "diet_analysis_ids",
            "exercise_source_reported_names",
            "exercise_analysis_ids",
        ]
    ].head(12)
)
""",
            cell_id="nb-l4-exercise",
            tags=("lesson-4", "learner-edit", "execute"),
        ),
        md(
            """
### Learner edit - run one preprocessing sensitivity check

Predict whether a stricter missingness threshold will change the retained feature count or explained variance. Change `SENSITIVITY_MAX_MISSING` to a value from 0 through 1, run the cell, and record which observations persist in the four-sentence note below. This is a within-study sensitivity check, not a license to tune the threshold for a preferred plot.
""",
            cell_id="nb-l4-sensitivity-prompt",
        ),
        code(
            """
# Learner-edit cell: try 0.10, 0.15, or another justified threshold.
SENSITIVITY_STUDY = DIET_ACCESSION
SENSITIVITY_MAX_MISSING = 0.10

if not 0 <= SENSITIVITY_MAX_MISSING <= 1:
    raise ValueError("SENSITIVITY_MAX_MISSING must be between 0 and 1")

if SENSITIVITY_STUDY == DIET_ACCESSION:
    sensitivity_analysis_id = DIET_ANALYSIS_ID
    sensitivity_payload = studies[DIET_ACCESSION]
    sensitivity_baseline = diet_pca
    sensitivity_exclude_standards = False
elif SENSITIVITY_STUDY == EXERCISE_ACCESSION:
    sensitivity_analysis_id = EXERCISE_ANALYSIS_ID
    sensitivity_payload = studies[EXERCISE_ACCESSION]
    sensitivity_baseline = exercise_pca
    sensitivity_exclude_standards = True
else:
    raise ValueError("SENSITIVITY_STUDY must be DIET_ACCESSION or EXERCISE_ACCESSION")

sensitivity_pca = run_within_study_pca(
    SENSITIVITY_STUDY,
    sensitivity_analysis_id,
    sensitivity_payload,
    tidy_factors,
    exclude_isotope_standards=sensitivity_exclude_standards,
    max_missing_fraction=SENSITIVITY_MAX_MISSING,
)
sensitivity_comparison = pd.concat(
    [
        pca_summary_frame([sensitivity_baseline]).assign(run="primary threshold 0.20"),
        pca_summary_frame([sensitivity_pca]).assign(
            run=f"sensitivity threshold {SENSITIVITY_MAX_MISSING:.2f}"
        ),
    ],
    ignore_index=True,
)
display(sensitivity_comparison)
""",
            cell_id="nb-l4-sensitivity-edit",
            tags=("lesson-4", "learner-edit", "execute"),
        ),
        md(
            """
### Learner edit - write the four-sentence interpretation

Double-click this cell, replace the bracketed text, and run the cell with **Shift+Enter** to save the rendered note.

1. **Observation:** Within `[study and analysis]`, the exploratory output shows `[visible pattern or count]`.
2. **Context:** The relevant design and phenotype metadata indicate `[time, specimen, intervention, or repeated-measures fact]`.
3. **Other explanations:** The pattern could also reflect `[technical or biological alternative]`.
4. **Limit:** These data do not establish `[causal or cross-study claim that is unsupported]`.
""",
            cell_id="nb-l4-interpretation",
            tags=("lesson-4", "learner-edit"),
        ),
        md(
            """
### Sample answer

Reveal this only after writing your own answer:

This class contains the reported number of shared RefMet names after the stated exclusions. Some names occur in more than one analysis mode. The result shows shared naming coverage, but it does not tell us whether concentrations, identification confidence, pathway activity, or biological responses match across studies.
"""
        ),
        md(
            """
### L4.4 Common pitfall and repair

**Pitfall:** collapsing duplicate RefMet names across analysis modes before checking their analytical origin—or selecting whichever duplicate gives the desired pattern.

**Repair:** keep `analysis_feature_id`, reported name, analysis ID, and RefMet name together. Select an analysis prospectively for PCA. If a later analysis collapses modes, specify and justify one deterministic rule, evaluate sensitivity, and preserve the pre-collapse audit table.
"""
        ),
        md(
            """
### Optional extension

For a statistically stronger next step, choose a small set of well-audited features within one study and estimate participant-centered change from baseline using a repeated-measures or mixed-effects model. Handle FARMM's imbalance explicitly and include the antibiotic/PEG period in the estimand. Repeat independently in ST003348, then compare effect *direction and uncertainty* rather than raw peak-area magnitude.

A second extension is to replace the conservative name-collision rule with verified assay documentation. That requires evidence beyond the study-level REST table; record every decision in the mapping audit rather than silently restoring a label.
"""
        ),
        md(
            """
### Ready to move on?

Continue when both PCAs use separate study/analysis matrices, the expected sample and feature summaries appear, and your four-sentence note above covers observation, context, alternatives, and the limit of the claim.
""",
            cell_id="nb-l4-complete",
        ),
        md(
            """
<a id="nb-l5"></a>
## Lesson 5 - Access patterns and transfer (`NB-L5`)

### Before you start

Read Lesson 5 in the learner guide and open `access_tier_transfer_checklist.md`. This section does not retrieve governed data. Instead:

1. Review which inputs came from live endpoints versus the validated public cache.
2. Choose a target dataset/release and intended action.
3. Record dated first-party access evidence outside the notebook.
4. Edit the transfer-decision scaffold and select `GO`, `REVISE`, `WAIT`, or `STOP`.
5. Finish with the reproducibility audit, then return to the guide for the posttest.

### L5.1 Learner edit - draft a transfer decision

The defaults describe this public cached tutorial. Replace them with evidence for your exact target. Do not place credentials, governed data, signed URLs, or personal information in this notebook.
""",
            cell_id="nb-l5",
            tags=("lesson-5",),
        ),
        code(
            """
# Learner-edit cell: replace every value with dated evidence for your target resource.
TARGET_RESOURCE = "Metabolomics Workbench ST001521/ST003348 public release"
INTENDED_ACTION = "Run the cached educational workflow locally"
ACCESS_EVIDENCE_DATE = "2026-08-17"
INPUT_BOUNDARY = "Public split REST responses or versioned public cache"
COMPUTE_LOCATION = "Local learner environment"
PERMITTED_OUTPUT = "Aggregate tables, figures, code, and provenance records"
UNRESOLVED_REQUIREMENTS = []
DECISION = "GO"  # Choose GO, REVISE, WAIT, or STOP after reviewing current evidence.

if DECISION not in {"GO", "REVISE", "WAIT", "STOP"}:
    raise ValueError("DECISION must be GO, REVISE, WAIT, or STOP")

transfer_decision = pd.DataFrame(
    [
        {
            "target_resource": TARGET_RESOURCE,
            "intended_action": INTENDED_ACTION,
            "evidence_date": ACCESS_EVIDENCE_DATE,
            "input_boundary": INPUT_BOUNDARY,
            "compute_location": COMPUTE_LOCATION,
            "permitted_output": PERMITTED_OUTPUT,
            "unresolved_requirements": "; ".join(UNRESOLVED_REQUIREMENTS) or "none recorded",
            "decision": DECISION,
        }
    ]
)
display(transfer_decision.T)
""",
            cell_id="nb-l5-transfer-edit",
            tags=("lesson-5", "learner-edit", "execute"),
        ),
        md(
            """
### L5.2 Run now - final reproducibility audit (`NB-REPRO`)

The final cell inventories every tutorial-generated CSV and PNG with its byte size and SHA-256 checksum. It also asserts that the expected counts and figures exist and that no SVG artifact was produced.
""",
            cell_id="nb-repro-action",
        ),
        code(
            """
expected_csvs = {
    "input_source_log.csv",
    "tidy_factors.csv",
    "metabolite_mapping_audit.csv",
    "refmet_overlap_audit.csv",
    "metabolite_crosswalk.csv",
    "refmet_class_summary.csv",
    "refmet_overlap_counts.csv",
    "ST001521_AN002534_pca_scores.csv",
    "ST001521_AN002534_pca_loadings.csv",
    "ST001521_AN002534_pca_feature_qc.csv",
    "ST003348_AN005483_pca_scores.csv",
    "ST003348_AN005483_pca_loadings.csv",
    "ST003348_AN005483_pca_feature_qc.csv",
    "pca_preprocessing_summary.csv",
}
expected_pngs = {
    "refmet_overlap_summary.png",
    "refmet_class_summary.png",
    "ST001521_AN002534_pca.png",
    "ST003348_AN005483_pca.png",
}

found_csvs = {path.name for path in DERIVED_DIR.glob("*.csv")}
found_pngs = {path.name for path in FIGURES_DIR.glob("*.png")}
missing_csvs = sorted(expected_csvs - found_csvs)
missing_pngs = sorted(expected_pngs - found_pngs)
assert not missing_csvs, f"Missing expected CSV files: {missing_csvs}. Rerun the earlier analysis cells in order."
assert not missing_pngs, f"Missing expected PNG files: {missing_pngs}. Rerun the earlier figure cells in order."
svg_files = sorted(path.name for path in FIGURES_DIR.glob("*.svg"))
assert not svg_files, f"Unexpected SVG files found: {svg_files}. Use the release PNG outputs."
assert overlap_counts["raw_exact_refmet_overlap"] == 153, (
    f"Expected raw overlap 153; found {overlap_counts['raw_exact_refmet_overlap']}."
)
assert overlap_counts["conservative_biological_refmet_overlap"] == 145, (
    f"Expected conservative overlap 145; found {overlap_counts['conservative_biological_refmet_overlap']}."
)

artifact_paths = sorted(
    [DERIVED_DIR / name for name in expected_csvs]
    + [FIGURES_DIR / name for name in expected_pngs]
)
manifest = pd.DataFrame(
    [
        {
            "artifact": str(path.relative_to(MODULE_DIR)),
            "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
        for path in artifact_paths
    ]
)
manifest_path = DERIVED_DIR / "tutorial_output_manifest.csv"
manifest.to_csv(manifest_path, index=False)
display(manifest)
print("Tutorial completed: 226 biological samples, 145 conservative shared RefMet names, two separate PCAs.")
""",
            cell_id="nb-repro",
            tags=("lesson-5", "execute"),
        ),
        md(
            """
### Ready to finish?

The notebook is complete when the artifact manifest appears without errors, your transfer checklist cites dated first-party evidence, and your decision states any unresolved requirements. Save the notebook, return to the learner guide, and complete the posttest.
""",
            cell_id="nb-l5-complete",
        ),
    ]
    nbformat.write(notebook, NOTEBOOK_PATH)


if __name__ == "__main__":
    build()
    print(f"Wrote {NOTEBOOK_PATH}")
