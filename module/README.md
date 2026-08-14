# Metabo-Diet training module

**Title:** Metabo-Diet: Harmonizing Dietary and Exercise Phenotypes with Metabolomics Across CFDE Resources

This directory is the complete source package for the 2.5-hour, intermediate, asynchronous training module proposed to the Common Fund Data Ecosystem Training Center.

## Start here: local environment

The primary artifact is `notebooks/metabo_diet_harmonization.ipynb`. Keep the full `module/` tree intact because the notebook imports `scripts/metabo_diet_pipeline.py` and reads the versioned cache under `data/raw/`.

Install Python 3.11 or 3.12, then from the directory containing `module/` run:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r module/notebooks/requirements-dev.txt
jupyter lab module/notebooks/metabo_diet_harmonization.ipynb
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`. The notebook's `NB-SETUP` section contains the complete Windows/macOS/Linux sequence and a package diagnostic.

For the optional R companion, install R 4.3 or later and run:

```bash
Rscript module/notebooks/install_r_packages.R
Rscript -e 'rmarkdown::render("module/notebooks/metabo_diet_R_appendix.Rmd")'
```

## Learner pathway

1. Why phenotype-to-metabolome harmonization matters (20 minutes)
2. Comparing study design and phenotype capture (30 minutes)
3. Harmonizing metabolomics and metadata (35 minutes)
4. Guided analysis and biological interpretation (40 minutes)
5. Access tiers and transfer to additional resources (15 minutes)

The remaining time is allocated to the pre-test, transitions, embedded checks, and post-test.

## Package map

- `content/` - five learner-facing lessons, glossary, and instructor guide
- `assessments/` - pre-test, post-test, embedded checks, and answer key
- `templates/` - cohort comparison, metabolite crosswalk, and access-tier transfer tools
- `notebooks/` - guided Python notebook and R appendix
- `data/` - cached public data, derived analysis-ready tables, and provenance
- `research/` - study-selection rationale and source audit
- `site/` - accessible learner-facing course shell
- `support/` - export-ready Word and PDF learner materials
- `qa/` - scientific, instructional, technical, accessibility, and packaging checks
- `scorm/` - SCORM-compatible package output

## Scientific boundary

The two case studies are compared to teach metadata reasoning and harmonization. They are not pooled as if they were one experiment. PCA is fitted separately within one study and selected analysis at a time; the release intentionally omits a stacked cross-study PCA of uncalibrated peak areas.

## Reproducibility contract

- Live retrieval uses the documented Metabolomics Workbench/NMDR API.
- Cached public files allow the module to run during API downtime.
- Every cached or derived file is recorded with its source URL, retrieval date, checksum, and transformation history.
- The notebook runs top-to-bottom from a clean environment and writes deterministic derived outputs.

## Public reuse license

Original educational materials are released under [CC BY 4.0](../LICENSE). Cached third-party data retain their source licenses; see `ATTRIBUTION.md` and `data/provenance.json`.

## Run the analysis

The downloadable `metabo_diet_analysis_bundle.zip` preserves this `module/` tree so the cached path is runnable without network access. From the directory containing `module/`:

```bash
python -m venv .venv
.venv/bin/pip install -r module/notebooks/requirements-dev.txt
.venv/bin/python module/scripts/execute_notebook.py
```

To render the R companion from the validated cache:

```bash
Rscript -e 'rmarkdown::render("module/notebooks/metabo_diet_R_appendix.Rmd")'
```

Set `METABO_DIET_LIVE=1` only when intentionally testing the live REST path. Both implementations record the source used for each endpoint and fall back to the immutable cache when the live request is unavailable or incompatible.

For a read-only pre-delivery comparison of all ten public study endpoints against the cache:

```bash
.venv/bin/python module/scripts/audit_live_mw.py
```
