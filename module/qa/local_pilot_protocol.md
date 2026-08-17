# Metabo-Diet local research-assistant pilot protocol

Use this protocol before a public release. Automated execution is necessary but does not replace a human usability run. Recruit at least two research assistants who did not author the notebook; ask each tester to work from a newly extracted analysis bundle without coaching.

## What to record

For each tester, record:

- tester name or study-approved identifier and role;
- test date, operating system, and hardware architecture;
- Python, R, Jupyter, and package-install results;
- cached or live mode;
- start time, completion time, and active troubleshooting time;
- the first instruction that caused uncertainty;
- every error/warning and the resolution attempted;
- whether all five `NB-L1` through `NB-L5` sections and the posttest handoff were completed;
- pass, pass with revisions, or fail;
- issue owner and the release commit that contains the fix.

Do not record credentials, participant data, signed URLs, or governed output in this log.

## Test A - clean Python setup and cached execution

From a new directory, use the virtual environment's Python directly. Activation is not required.

macOS or Linux:

```bash
unzip metabo_diet_analysis_bundle.zip
python3.12 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -r module/notebooks/requirements-dev.txt
METABO_DIET_LIVE=0 ./.venv/bin/python module/scripts/execute_notebook.py --output executed_test.ipynb
./.venv/bin/python module/qa/validate_module.py
```

Windows PowerShell:

```powershell
Expand-Archive -Path .\metabo_diet_analysis_bundle.zip -DestinationPath .\metabo_diet_pilot
Set-Location .\metabo_diet_pilot
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r module\notebooks\requirements-dev.txt
$env:METABO_DIET_LIVE = "0"
.\.venv\Scripts\python.exe module\scripts\execute_notebook.py --output executed_test.ipynb
.\.venv\Scripts\python.exe module\qa\validate_module.py
```

Acceptance criteria:

- package installation completes without unresolved dependency errors;
- the environment diagnostic passes;
- every code cell has a sequential execution count and no error output;
- the two accessions, 153 raw overlaps, 145 conservative overlaps, 150/76 PCA samples, and two independent PCA figures appear;
- the canonical source notebook is not required to be overwritten during the test.

## Test B - learner navigation and comprehension

1. Open the learner-guide PDF and complete the pretest.
2. Follow the guide-to-notebook crosswalk without verbal hints.
3. At each `NB-L1` through `NB-L5` section, read, run, observe, record, and check the completion statement.
4. Edit the study audit, RefMet trace, class audit, sensitivity, and transfer-decision cells.
5. Locate both PCA examples in the guide appendix and state why their axes cannot be compared.
6. Complete the posttest handoff.

Acceptance criteria:

- the tester can find every referenced section in under one minute;
- the tester knows when to stop on a failed check;
- the tester distinguishes samples from participants, plasma from serum, naming overlap from quantitative equivalence, and separate PCA from causal testing;
- no instruction requires author intervention.

## Test C - R companion

```bash
Rscript module/notebooks/install_r_packages.R
Rscript module/scripts/test_R_endpoint_normalization.R
Rscript -e 'rmarkdown::render("module/notebooks/metabo_diet_R_appendix.Rmd")'
```

Acceptance criteria:

- required packages are reported with versions;
- all ten endpoint normalization cases pass;
- the R Markdown file renders from the validated cache;
- both separate PCA examples appear with the same sample/feature checks as Python.

## Pilot record

| Tester | Role | Date | OS / versions | Mode | Duration | Result | Issues / fix commit |
|---|---|---|---|---|---:|---|---|
| Pending | Research assistant 1 |  |  | Cache |  |  |  |
| Pending | Research assistant 2 |  |  | Cache |  |  |  |

The release owner changes `Pending` only after receiving the tester's completed evidence. An automated run must never be represented as a human pilot.
