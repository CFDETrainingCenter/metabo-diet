# Before you begin: first-time setup

The scientific material is written for learners who can read a data table and a scatterplot. You do not need prior experience with Metabolomics Workbench, RefMet, a terminal, Jupyter, or R. This is not an introductory Python course, and you will not be asked to write an analysis from a blank page.

The 153-minute course estimate begins after software setup. If Python, metabolomics, or principal component analysis (PCA) is new to you, allow an additional 30 to 60 minutes and keep the glossary open.

## Files you will use

Keep these files together in one working folder:

1. `metabo_diet_learner_guide.pdf` - the lessons, pretest, posttest, and worked PCA figures.
2. `metabo_diet_analysis_bundle.zip` - the Python notebook, R companion, scripts, and public cached data.
3. `metabo_diet_templates.zip` - editable learner worksheets.

Extract both ZIP files before starting. Do not run the notebook from inside a ZIP. Keep the extracted `module/` folder intact because the notebook uses its `scripts/` and `data/` subfolders.

## Install Python and open Jupyter

A terminal is the text-based app used to enter the commands below. On macOS, open **Terminal**. On Windows, open **PowerShell**. Open the terminal in the folder that contains `module/`, then type each command without a leading prompt symbol such as `$` or `>`.

Install [Python 3.12](https://www.python.org/downloads/). Python 3.11 is also supported; substitute `python3.11` or `py -3.11` if that is the version you installed.

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

The version check should report Python 3.11 or 3.12. The package installation can take several minutes. Jupyter should then open in a browser. If it asks for a kernel, choose **Python 3 (Metabo-Diet)**.

## Jupyter in one minute

- A notebook contains text cells and code cells. Click a code cell and press **Shift+Enter** to run it.
- `[*]` beside a cell means it is still running. A number such as `[1]` means it finished.
- The file contains saved example outputs. Before beginning Lesson 1, choose **Kernel > Restart Kernel**, then run the required cells yourself from top to bottom.
- Run every code cell that follows a **Run now** heading.
- At a **Learner edit** heading, change only the named ALL_CAPS value or the clearly marked response text, then run that cell.
- A red traceback means the cell failed. Keep the message, stop, and use the setup table below or ask the instructor for help. Do not skip a failed check.

## Setup help

| What you see | What to do |
|---|---|
| `command not found` or “not recognized” | Confirm Python 3.12 is installed. Try the Python 3.11 command only if its version check reports 3.11. |
| `No module named ...` | Repeat the package-install command with the `.venv` Python path shown above, then restart the kernel. |
| Jupyter uses a different Python | Choose **Kernel > Change Kernel > Python 3 (Metabo-Diet)**. |
| A notebook assertion or count check fails | Read the message and stop. Check the accession, cache, and earlier cells instead of deleting rows or changing the expected value. |
| A live request fails | Use the default validated cache. Live access is optional. |

## Optional technical check

The following command runs every code cell without pausing for the learner activities. It is useful for testing an installation, but it does not complete the course. It writes a new notebook and leaves the original file unchanged.

macOS or Linux:

```bash
./.venv/bin/python module/scripts/execute_notebook.py --output metabo_diet_smoke_test.ipynb
```

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe module\scripts\execute_notebook.py --output metabo_diet_smoke_test.ipynb
```

## R is optional

The Python notebook is the main activity. To read the R version without installing anything, open `module/notebooks/metabo_diet_R_appendix.html` in a browser.

To rerun the R companion, install R 4.3 or later plus RStudio or another Pandoc installation. First confirm Pandoc is available:

```bash
Rscript -e 'stopifnot(rmarkdown::pandoc_available()); rmarkdown::pandoc_version()'
```

Then run `Rscript module/notebooks/install_r_packages.R` and render the R Markdown file as described in `module/README.md`.

## Continue to the pretest

After Jupyter opens successfully, return to the learner guide and complete the pretest. For each lesson, read the guide first, run the matching notebook section, write the requested answer in the named worksheet or learner-edit cell, and check the “Ready to move on?” note.
