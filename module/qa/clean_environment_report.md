# Metabo-Diet automated local validation report

**Date:** 2026-08-17
**Host:** macOS 26.6.1 (25G76), arm64  
**Purpose:** Record automated reproducibility evidence for the final review of the Friday delivery. This report is not a substitute for the independent research-assistant pilot in `local_pilot_protocol.md`.

## Python clean environment

- A new disposable virtual environment was created with Python 3.12.8.
- `module/notebooks/requirements-dev.txt` was installed from scratch.
- `python -m pip check` reported `No broken requirements found`.
- Core pinned versions included NumPy 2.2.6, pandas 2.2.3, requests 2.32.5, scikit-learn 1.7.1, matplotlib 3.10.5, nbformat 5.10.4, nbclient 0.10.2, ipykernel 6.30.1, IPython 9.15.0, and JupyterLab 4.6.2.
- The canonical notebook executed top to bottom in cached mode: 60 total cells, 18 code cells, sequential execution counts 1-18, and zero saved error outputs.
- The final analysis ZIP was extracted to a new temporary directory and executed with the same clean interpreter. Result: PASS in approximately 12 seconds, 18/18 code cells.
- The validator included inside that extracted ZIP ran successfully and passed every deterministic check, including the notebook kernel name, saved execution evidence, and absence of private paths.

## R cached-mode validation

- R 4.5.2 was used.
- Installed render/test packages: rmarkdown 2.31, knitr 1.51, jsonlite 2.0.0, data.table 1.18.4, httr 1.4.8, and BiocManager 1.30.27.
- `module/scripts/test_R_endpoint_normalization.R` passed all ten cached endpoint cases.
- `module/notebooks/metabo_diet_R_appendix.Rmd` rendered all 22 steps/chunks without errors in `METABO_DIET_LIVE=0` mode.
- The rendered companion contains `NB-R-SETUP`, `NB-R-L1` through `NB-R-L5`, and two separate within-study PCA panels.
- `metabolomicsWorkbenchR` remains an optional live-retrieval dependency. It is installed only when `module/notebooks/install_r_packages.R --live` is requested; the deterministic cached-mode release does not require it.

## Packaging and presentation

- The standalone SCORM 1.2 package passed manifest, launch-file, assessment, license, download-sync, and ZIP CRC checks. Its dual-color keyboard-focus indicator passed the automated contrast check at 8.31:1 for the dark ring against white.
- Learner guide: 91 PDF pages and 91 rendered PNG pages; every page was visually inspected, including a second pass after the final pagination changes.
- Instructor packet: 34 PDF pages and 34 rendered PNG pages; every page was visually inspected.
- DOCX accessibility audits reported zero high-, medium-, or low-severity findings for both documents.
- The release-packaging audit passed with no failures and regenerated the SHA-256 manifest.

## Human pilot status

The two-person research-assistant usability pilot is pending. Only named testers working from a newly extracted bundle may complete that record. Automated execution must not be presented as independent human evidence.
