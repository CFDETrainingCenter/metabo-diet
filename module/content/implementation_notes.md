# Implementation notes and intentional updates from the proposal

The July 2026 proposal is the design authority for the module's learning goals and deliverable set. The implementation updates several provisional statements where current repository evidence or scientific review requires greater precision.

## Locked case studies

- Diet anchor: `ST001521` (FARMM; plasma; diet-pattern/controlled-feeding context; baseline and days 5, 9, 12, and 15).
- Exercise anchor: `ST003348` (race walking; serum; rest, immediate post-exercise, 3-hour recovery, and 22-hour recovery).
- Learners use valid study-level split REST endpoints and cached JSON. They do not depend on malformed analysis-level mwTab JSON from selected FARMM analyses.

## Scientific safeguards added during development

- `ST001521` pooled-QC samples `QPP01` through `QPP10` are excluded from biological summaries and PCA.
- ST003348 isotope-labeled/internal-standard features are excluded before reporting biological RefMet overlap.
- The raw exact RefMet intersection is reported separately from the conservative biological intersection.
- PCA is performed within each study and selected analysis. The module does not concatenate raw peak-area matrices or present a cross-study PCA as a biological contrast.
- Plasma and serum remain distinct source terms. A broader `blood-derived` label may support inventory-level description, but it never replaces the original specimen context.
- FARMM days 9, 12, and 15 are interpreted as diet plus antibiotic/PEG and microbiome reconstitution phases, not diet-only effects.

## Access-tier language updated

The proposal described MoTrPAC as registration-gated. Current MoTrPAC documentation distinguishes public releases, which can be accessible without an account, from restricted or embargoed datasets that require authentication and agreements. The implemented lesson therefore teaches access as a property of the exact dataset, release, intended action, and verification date. NPH remains a controlled-compute transfer case through the All of Us Researcher Workbench.

## Delivery architecture

- All required hands-on analysis runs on public Metabolomics Workbench data.
- Live REST retrieval is attempted first, with cached public data as a documented fallback.
- The Python notebook is the primary guided analysis.
- The R appendix demonstrates the corresponding retrieval and harmonization path with `metabolomicsWorkbenchR` plus cached fallback logic.
- Learner-facing site, Word/PDF support materials, and the SCORM-compatible package are generated from the same source lessons and assessments to minimize content drift.

