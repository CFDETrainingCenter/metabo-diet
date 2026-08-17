# Module acceptance checklist

This checklist translates the revised July 2026 proposal into verifiable deliverables. A checked item requires direct evidence in the current workspace; intent or placeholder text is insufficient.

## Scope and data

- [x] One public human diet-anchored MW/NMDR study is locked and documented.
- [x] One public human exercise-anchored MW/NMDR study is locked and documented.
- [x] A scientifically defensible reserve pair is documented.
- [x] Public release status, API retrieval, metadata completeness, and metabolite overlap are verified.
- [x] Cached fallback data include checksums, retrieval dates, source URLs, and transformation provenance.

## Instruction

- [x] Five complete lessons cover the proposed 20/30/35/40/15-minute sequence.
- [x] Each lesson has aligned objectives, activities, knowledge checks, interpretation limits, and sources.
- [x] Current access-tier language accurately distinguishes open, mixed/restricted, and controlled resources.
- [x] MoTrPAC and NPH are instructional case studies and are not required data dependencies.

## Hands-on artifacts

- [x] Pre-test and post-test measure all five learning objectives.
- [x] Embedded knowledge checks include feedback and rationales.
- [x] Cohort-comparison worksheet has learner and instructor versions.
- [x] Metabolite crosswalk template includes provenance and decision-log fields.
- [x] Access-tier transfer checklist can be applied to a learner-selected resource.
- [x] Glossary and instructor answer key are complete.

## Computation

- [x] Python tutorial notebook retrieves or loads both studies, harmonizes metadata/metabolites, quantifies overlap, performs PCA, summarizes classes, and interprets limitations.
- [x] Notebook has pinned requirements, small runnable cells, exercises, answer scaffolds, and cached fallback.
- [x] Notebook executes top-to-bottom without hidden state or errors.
- [x] R appendix demonstrates equivalent retrieval/loading and core harmonization steps.

## Packaging and accessibility

- [x] The SCORM course shell is keyboard accessible, high contrast, and uses semantic headings and labels.
- [x] SCORM progress and assessment interactions work without a server-side dependency.
- [x] Export-ready DOCX and PDF support files render without clipping, overlap, or broken tables.
- [x] Figures have text alternatives; transcript/caption text is available for narrated or visual material.
- [x] SCORM-compatible package contains a valid manifest and launches the course.

## QA

- [x] Scientific claims and access statements are source-verified.
- [x] Assessment keys and scoring are validated programmatically.
- [x] Cached and live data paths produce structurally consistent analysis inputs.
- [x] Notebook outputs agree with derived tables and plotted values.
- [x] The standalone SCORM package passes manifest, launch, interaction, download-sync, and ZIP integrity checks.
- [x] DOCX and PDF pages receive full visual inspection.
- [x] Final file manifest and checksums are generated.

## Comment closure and external handoff

- [x] The Python notebook is divided into five guide-aligned lessons with stable `NB-L1` through `NB-L5` references.
- [x] Python, R, package installation, cached mode, and optional live mode are documented at the start of the notebook and in the repository README.
- [x] First-time terminal and Jupyter setup appears before the pretest and the analysis bundle contains the guide and worksheets it references.
- [x] The guide tells learners when to read, run, observe, record, stop, and continue.
- [x] Every lesson points to its matching notebook section, and the guide includes a complete crosswalk.
- [x] The learner-guide appendix contains two separate, captioned PCA examples with text alternatives.
- [x] Automated clean-environment Python execution and cached-mode R validation are recorded in `clean_environment_report.md`.
- [x] An English Creative Commons Attribution 4.0 International license notice is included in the repository and release packages, with third-party data excluded from the grant.
- [ ] Two non-author research assistants complete the local pilot and sign the record in `local_pilot_protocol.md`.
- [ ] A repository administrator confirms public visibility; a public license does not by itself change GitHub visibility.
- [ ] The team reviews the Friday delivery and sends final comments/payment closure by email.
