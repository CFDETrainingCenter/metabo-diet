# Metabo-Diet training module

**Title:** Metabo-Diet: Harmonizing Dietary and Exercise Phenotypes with Metabolomics Across CFDE Resources

This directory contains the materials for a 2.5-hour, self-paced CFDE Training Center module. The scientific content is intermediate, but the setup below is written for someone using Jupyter for the first time. If Python, metabolomics, or PCA is new to you, allow an extra 30 to 60 minutes.

## Start here

1. Download or clone the repository. If you downloaded a ZIP, extract it before opening any files.
2. Open `support/metabo_diet_learner_guide.pdf` and keep the learner worksheets nearby.
3. Complete the Python setup below before the pretest. R is optional.
4. Work through Lessons 1 to 5 in order, moving between the guide and the matching `NB-L1` through `NB-L5` notebook sections.

Start the code work in `notebooks/metabo_diet_harmonization.ipynb`. Keep the full `module/` folder together because the notebook uses the scripts and cached public data inside it.

The same setup, with a one-minute Jupyter orientation, appears in `content/getting_started.md` and at the front of the learner guide.

## First-time Python setup

A terminal is the text-based app used to run the commands below. On macOS, open **Terminal**; on Windows, open **PowerShell**. Open it in the folder that contains `module/`. Type each command without copying a leading prompt symbol such as `$` or `>`.

Install Python 3.12, then use the version-check command for your system below. The result should begin with `Python 3.12`. Python 3.11 is also supported; substitute 3.11 only if its version check reports a supported version.

### macOS or Linux

```bash
python3.12 --version
python3.12 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -r module/notebooks/requirements-dev.txt
./.venv/bin/python -m jupyter lab module/notebooks/metabo_diet_harmonization.ipynb
```

### Windows PowerShell

```powershell
py -3.12 --version
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r module\notebooks\requirements-dev.txt
.\.venv\Scripts\python.exe -m jupyter lab module\notebooks\metabo_diet_harmonization.ipynb
```

Jupyter should open in a browser. If it asks for a kernel, choose **Python 3 (ipykernel)** from the `.venv` environment. Click a cell and press **Shift+Enter** to run it. A number such as `[1]` means the cell finished; `[*]` means it is still running. The first diagnostic confirms that a virtual environment is active; stop if that check fails or if you see a red traceback.

Do not open the notebook while it is still inside a ZIP archive. Do not move it away from the `module/` folder.

## Optional R companion

You can complete the core module without R. If you want the R version, install R 4.3 or later and Pandoc (RStudio includes Pandoc), then run:

```bash
Rscript module/notebooks/install_r_packages.R
Rscript -e 'rmarkdown::render("module/notebooks/metabo_diet_R_appendix.Rmd")'
```

Open the generated `module/notebooks/metabo_diet_R_appendix.html` in a browser. The R file follows the same five lessons, but the Python notebook remains the main activity.

The default installer supports the cached path. For the optional live R path, run `Rscript module/notebooks/install_r_packages.R --live` before setting `METABO_DIET_LIVE=1`.

## Common setup problems

| What you see | What to do |
|---|---|
| `command not found: python3.12` | Install Python 3.12, or use `python3.11` if `python3.11 --version` reports a supported version. |
| PowerShell blocks `Activate.ps1` | Use the direct `.venv\Scripts\python.exe` commands above; activation is not required. |
| `No module named ...` | Reinstall `requirements-dev.txt` with the direct `.venv` Python path and restart the Jupyter kernel. |
| Jupyter opens the wrong kernel | Choose **Kernel > Change Kernel > Python 3 (ipykernel)** after launching Jupyter with the direct `.venv` command above. The first diagnostic must report `Virtual environment: active`. |
| A notebook check fails | Read the message, keep the output, and stop. Do not delete rows or change expected counts just to make the check pass. |
| Live retrieval fails | Leave live mode off and use the included validated cache. |

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
python3.12 -m venv .venv
.venv/bin/python -m pip install -r module/notebooks/requirements-dev.txt
.venv/bin/python module/scripts/execute_notebook.py --output metabo_diet_harmonization_executed.ipynb
```

This last command is a noninteractive verification run. It creates a separate executed notebook and does not replace the learner activity in Jupyter.

To render the R companion from the validated cache:

```bash
Rscript -e 'rmarkdown::render("module/notebooks/metabo_diet_R_appendix.Rmd")'
```

Set `METABO_DIET_LIVE=1` only when intentionally testing the live REST path. Both implementations record the source used for each endpoint and fall back to the immutable cache when the live request is unavailable or incompatible.

For a read-only pre-delivery comparison of all ten public study endpoints against the cache:

```bash
.venv/bin/python module/scripts/audit_live_mw.py
```
