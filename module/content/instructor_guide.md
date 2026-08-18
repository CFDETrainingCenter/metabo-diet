# Metabo-Diet instructor guide

## Module at a glance

**Title:** Metabo-Diet: Harmonizing Dietary and Exercise Phenotypes with Metabolomics Across CFDE Resources  
**Level:** Intermediate  
**Instructional time:** 140 minutes  
**Primary format:** Guided mini-lessons, structured worksheets, and an interactive Python notebook  
**Hands-on data source:** Public Metabolomics Workbench studies only  
**Design framework:** Backward design with Bloom progression from understand to apply, analyze, evaluate, and create

This module teaches learners to decide what the two studies can support. Keeping an incompatible field, feature, matrix, timepoint, or quantitative table separate is an acceptable result.

> **Scope:** The module compares metadata structure and reviewed analyte-name coverage and performs quantitative exploration within each study. It does not pool quantitative values across the two studies or estimate a diet-versus-exercise causal effect.

## Audience and prerequisites

The module is intended for graduate students, postdoctoral scholars, research staff, and analysts in metabolomics, nutrition, exercise biology, translational omics, or computational biology.

Learners should be able to:

- Read a rectangular data table.
- Read guided Python and pandas cells and change the named values when prompted.
- Interpret a scatterplot.
- Recognize samples, variables, and missing values.
- Explain at a basic level what metabolomics measures.

No prior Metabolomics Workbench, RefMet, MoTrPAC, NPH, or All of Us experience is required.

No prior terminal or Jupyter experience is required for the guided path, but learners need basic familiarity with tables and scatterplots. The module is not a general Python course. Direct first-time setup appears before the pretest; R is optional.

## Learning objectives

By the end of the module, learners will be able to:

- **LO1:** Identify and compare intervention structure, specimen context, timepoint design, and clinical or behavioral phenotype representation across the two Metabolomics Workbench studies.
- **LO2:** Describe how study design, metadata provenance, analytical platform, and preprocessing influence what can and cannot be concluded from cross-study comparison.
- **LO3:** Apply a RefMet-centered workflow that aligns analyte names, specimen and time semantics, variables, and units while recording field-level decisions.
- **LO4:** Retrieve and analyze public MW data through the REST API and interpret overlap, class summaries, and within-study PCA in context.
- **LO5:** Evaluate the current access pattern of a candidate resource and adapt retrieval, compute, storage, cache, and output architecture accordingly.

## Objective-instruction-assessment alignment

| Objective | Instruction and practice | Embedded evidence | Summative evidence |
|---|---|---|---|
| LO1 | Lessons 1-2; cohort-comparison worksheet; sample/time audit in Lesson 4 | KC2-01 to KC2-03; sourced compatibility decisions | POST-01 to POST-03; completed comparison worksheet |
| LO2 | Lessons 1-4; interpretation limits; bounded-claim exercise | KC1-01, KC1-03, KC2 items, KC3-02, KC4-03 | POST-02 to POST-04, POST-08; four-sentence interpretation |
| LO3 | Lesson 3; crosswalk and overlap audit | KC3-01 to KC3-03; reviewed ambiguous/unmapped rows | POST-05 to POST-07, POST-12; crosswalk rubric |
| LO4 | Lesson 4; REST retrieval, audit, overlap, class summary, PCA | KC4-01 to KC4-03; notebook audit outputs | POST-07 to POST-09, POST-12; reproducible notebook execution |
| LO5 | Lessons 1 and 5; transfer checklist | KC1-02 and KC5-01 to KC5-03 | POST-10 and POST-11; sourced go/revise/wait/stop decision |

The pretest contains at least two items per objective domain when cross-listed items are included. Use objective-level change, not only total score, when evaluating module value.

## Instructional schedule

| Lesson | Minutes | Main learner artifact |
|---|---:|---|
| 1. Why phenotype-to-metabolome harmonization matters | 20 | Pretest, access evidence, reflection |
| 2. Comparing study design and phenotype capture | 30 | Cohort-comparison worksheet |
| 3. Harmonizing metabolomics and metadata | 35 | Metabolite/metadata crosswalk |
| 4. Guided analysis and biological interpretation | 40 | Retrieval audit, overlap flow, class summary, within-study PCA, bounded interpretation |
| 5. Access patterns and transfer | 15 | Transfer checklist and posttest |
| **Total** | **140** |  |

The 140 minutes include embedded knowledge checks but exclude the 5-minute pretest, 8-minute posttest, and software installation, for an expected course total of about 153 minutes after setup. If learners are new to Python, Jupyter, PCA, or metabolomics, schedule 30 to 60 additional minutes and use the reduced worksheet path stated in each lesson.

## Locked data configuration

```text
DIET_ACCESSION = ST001521
EXERCISE_ACCESSION = ST003348
```

### Diet study facts to verify before delivery

- Human plasma FARMM study with three deposited diet labels: `Vegan`, `Western`, and `Modulen`.
- Study summary describes 30 volunteers and five biological timepoints.
- Current factors response contains 160 rows: 150 participant-timepoint rows and 10 `QPP...` pooled QC candidates.
- Longitudinal time course includes an antibiotic intervention on days 6-8 and polyethylene glycol on day 7.
- Vegan participants were established vegans and remained outpatients; 20 omnivores were randomized to omnivore versus EEN in an inpatient setting.
- Four analyses: AN002533 through AN002536, reporting unitless peak areas.

### Exercise study facts to verify before delivery

- Human endurance race-walking study with 19 athletes represented at four timepoints and 76 samples.
- `REST`: pre-exercise; `STAT`: immediately post-exercise; `REC3`: 3-hour recovery; `REC22`: 22-hour recovery.
- Factors endpoint reports broad source `blood`; collection metadata specifies serum and describes clotting and processing.
- Two analyses: AN005483 and AN005484, reporting peak area.

### Overlap audit targets

- 153 shared nonblank exact RefMet strings before artifact and eligibility exclusions.
- Eight `ST003348` isotope/internal-standard rows map to ordinary RefMet labels and are excluded from biological overlap.
- 145 conservative biological overlaps after that filter.

These are versioned reproducibility checks, not scientific constants. If live data differ, investigate version, selected analyses, blank handling, duplicate collapse, and artifact rules. Do not change logic simply to force the expected values.

### Reserve pair

If a locked study is withdrawn or no longer usable, the recommended reserve pair from the scoping audit is:

```text
DIET_ACCESSION = ST000292
EXERCISE_ACCESSION = ST001789
```

Both are plasma candidates, and the scoping audit found 122 raw exact-name overlaps. `ST000291` is the urine companion to the diet project and should not be substituted for `ST000292` without redesigning the specimen comparison. Before activation, rerun all release, metadata-completeness, overlap, sample-role, and licensing checks and generate a new provenance manifest. Never switch pairs silently during a cohort.

## Instructor setup checklist

Complete within 48 hours of delivery:

- [ ] Open the current [MW REST documentation](https://www.metabolomicsworkbench.org/tools/mw_rest.php).
- [ ] Confirm both study landing pages and summary, factors, analysis, metabolites, and data endpoints are public.
- [ ] Record UTC retrieval times and license strings.
- [ ] Run the notebook from a fresh environment with live retrieval.
- [ ] Confirm the first-time setup works before opening the pretest and that the smoke-test command writes a separate notebook.
- [ ] Verify structural counts, `QPP...` sample roles, analysis IDs, and plasma-versus-serum evidence.
- [ ] Verify the 153 raw and 145 conservative overlap audit stages.
- [ ] Test the cached fallback by simulating live-retrieval failure without overwriting the live cache.
- [ ] Confirm cache checksums and visible live/cached labels.
- [ ] Confirm no credentials, tokens, signed URLs, governed data, or personal information appear in materials or outputs.
- [ ] Validate all JSON assessment files.
- [ ] Check every external link and label any time-sensitive access claim with a date.
- [ ] Review MoTrPAC and All of Us first-party access documentation for changes.
- [ ] Test keyboard-only lesson, form, and notebook navigation.
- [ ] Test headings, table headers, link labels, figure descriptions, and color contrast with accessibility tooling.
- [ ] Ensure answer rationales are hidden until submission.

## Facilitation guidance by lesson

### Lesson 1

Emphasize the difference between common retrieval, structural harmonization, and statistical exchangeability. Ask learners to identify a familiar situation where a shared column label hid a protocol difference. Do not introduce the module as a method for combining cohorts; introduce it as a method for making a defensible comparability decision.

Current-access correction: the July proposal described MoTrPAC as registration-gated. Current MoTrPAC documentation distinguishes public and restricted pathways. Explain that the module intentionally updates the proposal because access is a time-stamped dataset property.

### Lesson 2

Have learners extract each study independently before comparing columns. Watch for three common errors:

1. Calling 160 factor rows in `ST001521` participants.
2. Calling all three diet groups randomized.
3. Calling the exercise matrix simply blood and overlooking the serum-specific collection block.

Treat a documented `not reported` or `not yet assessable` as better work than an unsupported completed cell.

### Lesson 3

Reward auditability rather than mapping rate. Require at least one ambiguous, one unmapped, one many-to-one, and one artifact or nonbiological example when present. The `Palmitic acid-[13C]16` to `Palmitic acid` example illustrates why a nonblank RefMet field still requires source-role review.

Do not allow learners to overwrite the submitted name or discard blank mappings. Ask what analysis each eligibility flag serves.

### Lesson 4

Run retrieval and validation before any figure. Pause if join cardinality increases rows. Keep pooled QC samples available for assay diagnostics and excluded from biological PCA. Fit PCA separately within studies; the release module intentionally omits a combined PCA of the uncalibrated raw matrices.

When discussing the overlap, say:

> 153 tests the raw nonblank exact-string step; 145 tests the conservative exclusion of eight isotope/internal-standard mappings. Neither number measures a shared intervention response.

Require the four-sentence interpretation scaffold: observation, context, alternatives, boundary.

### Lesson 5

Require first-party, dated evidence for the exact dataset and action. A valid transfer decision may be `WAIT` or `STOP`. Correct the claim that no output can ever leave All of Us: participant-level data remain governed, while only outputs permitted under current dissemination policy may leave.

## Assessment administration

### Pretest

- Administer before Lesson 1 content.
- Do not show answers until submission.
- Use as a baseline and diagnostic, not as a gate.
- Maximum: 10 points.

### Embedded knowledge checks

- Use immediate feedback with rationale after each response.
- Permit retry after the rationale.
- Record first-attempt responses for instructional evaluation if the platform and consent permit.

### Posttest

- Administer after the transfer activity.
- Maximum: 12 points.
- Suggested mastery: 10/12, with no automatic certificate based on total score alone.
- Learners missing both items in an objective domain should review the associated lesson and complete a parallel retry.

### Performance artifacts

Knowledge items do not fully assess application. Require these artifacts for completion:

- Cohort-comparison worksheet meeting all completion checks.
- Crosswalk scoring at least 16/20 and meeting all safety conditions.
- Notebook audit reproducing or explaining the structural and overlap checkpoints.
- A bounded four-sentence interpretation with no causal cross-study claim.
- Transfer checklist scoring at least 16/20 and meeting all minimum pass conditions.

## Accessibility guidance

The lesson Markdown presents conceptual access and comparison workflows as text-only sketches and includes equivalent descriptions for generated charts. Preserve those descriptions when converting the material to dashboard components.

### Content requirements

- Use semantic heading levels in order.
- Give tables real header cells and avoid merged cells where possible.
- Do not rely on color alone; pair color with shape, line type, or direct labels.
- Use descriptive links rather than `click here`.
- Expand abbreviations on first use and maintain the glossary link.
- Provide a text table behind every chart with the plotted values and sample counts.
- Include explained variance and figure-specific axis text for each PCA.
- Label the separate figures explicitly as plasma/diet and serum/exercise.
- Avoid motion or require a pause control.

### Notebook requirements

- Every code cell needs a preceding plain-language purpose statement.
- Every output needs a short interpretation and a machine-readable or text alternative.
- Errors must be conveyed in text, not color alone.
- Interactive widgets need keyboard focus, labels, and a non-widget fallback.
- Figures need high-contrast palettes and marker shapes.
- Do not auto-scroll past warnings or stop conditions.

### Assessment requirements

- Associate each option with the prompt programmatically.
- Provide visible focus indicators.
- Do not impose a speeded time limit; listed times are estimates.
- Announce correctness and rationale to screen readers after submission.
- Make JSON content available through an accessible rendering layer rather than requiring learners to read raw JSON.

## Troubleshooting and stop conditions

| Problem | Instructor response |
|---|---|
| MW endpoint fails | Display failure evidence, use only the versioned cache, label it cached, and schedule a later access recheck. |
| Live count differs from guide | Check revision, endpoint schema, selected analyses, QC roles, and parsing; document the difference rather than forcing the old count. |
| `QPP...` rows appear in biological PCA | Stop, correct `sample_role`, rerun participant/sample counts, then refit PCA. |
| Exercise matrix appears only as `blood` | Inspect collection metadata; preserve the broad factor and derive serum from the specific supported source. |
| Crosswalk join multiplies rows | Stop and audit key cardinality; do not drop duplicates randomly. |
| RefMet mapping maximizes overlap by narrowing ambiguous labels | Restore source detail, mark review required or broader, and recompute eligible sets. |
| Learner proposes pooled diet-versus-exercise inference | Return to the estimand and confounding audit; require a within-study or descriptive name-set alternative. |
| Access policy is unclear | Pause affected movement, document the question, and use the resource's official support channel. |
| Learner lacks a working Python environment | Use the first-time setup guide and default cache. An instructor demonstration may preview the output, but schedule the learner's hands-on run after setup rather than treating the demonstration as completion. |

## Quality and fidelity audit

Before declaring the module complete, inspect evidence for every requirement:

- Five lessons total exactly 140 estimated minutes.
- Each lesson has objectives, narrative, a worked example, activity, knowledge check, guardrails, accessibility support where visual content is proposed, and primary sources.
- The locked pair and reserve pair are recorded.
- Every claim about access has current first-party evidence and a check date.
- Pretest, posttest, and embedded checks cover all five objectives and include answer rationales.
- Learner and instructor versions exist for all three templates.
- The overlap audit distinguishes 153 raw from 145 conservative biological names.
- The lesson never claims that harmonization establishes quantitative pooling, causal comparability, or shared biological response.
- Generated dashboard, notebook, and support exports render accessibly and preserve all warnings.

## Primary references

1. Metabolomics Workbench. [REST Service](https://www.metabolomicsworkbench.org/tools/mw_rest.php), [mwTab documentation](https://www.metabolomicsworkbench.org/data/tutorials.php), and [RefMet](https://www.metabolomicsworkbench.org/databases/refmet/index.php). Accessed August 10, 2026.
2. Fahy E, Subramaniam S. [RefMet: a reference nomenclature for metabolomics](https://doi.org/10.1038/s41592-020-01009-y). *Nature Methods*. 2020;17:1173-1174.
3. MoTrPAC Study Group, Jakicic JM, Kohrt WM, et al. [MoTrPAC human studies design and protocol](https://doi.org/10.1152/japplphysiol.00102.2024). *Journal of Applied Physiology*. 2024;137(3):473-493.
4. NIH Common Fund. [Nutrition for Precision Health FAQ](https://commonfund.nih.gov/nutritionforprecisionhealth/frequently-asked-questions). Accessed August 10, 2026.
5. All of Us Research Program. [Researcher Workbench](https://support.researchallofus.org/hc/en-us/articles/41981123613716-Researcher-Workbench) and [policy guidance](https://support.researchallofus.org/hc/en-us/articles/34814131370388-Policy-Questions). Accessed August 10, 2026.
6. Wilkinson MD, Dumontier M, Aalbersberg IJ, et al. [The FAIR Guiding Principles](https://doi.org/10.1038/sdata.2016.18). *Scientific Data*. 2016;3:160018.
