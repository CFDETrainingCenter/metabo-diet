# Cohort-comparison worksheet - instructor version

This version supplies expected evidence and defensible classifications for the locked August 10, 2026 build. Repository records can change; learners should receive credit for a different value when they provide current, traceable evidence and update the reasoning appropriately.

## 1. Comparison purpose

Recommended purpose:

> Describe exact reviewed RefMet-name overlap and broad chemical-class coverage across the two deposited studies while retaining population, plasma-versus-serum, time, platform, and scale differences.

This purpose does not authorize pooling peak areas or estimating a diet-versus-exercise effect.

## 2. Dataset identity and access evidence

| Field | Diet study | Exercise study |
|---|---|---|
| Configuration | `DIET_ACCESSION = ST001521` | `EXERCISE_ACCESSION = ST003348` |
| Title | Plasma metabolites of known identity profiled using hybrid nontargeted methods (part-III) | An integrated LC-MS analysis of the biometric characteristics of different time cohorts of race walkers - untargeted |
| Study DOI | Project DOI `10.21228/M8B984` | Project DOI `10.21228/M8C802` |
| Landing page | `https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?StudyID=ST001521` | `https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?StudyID=ST003348` |
| REST summary | `/rest/study/study_id/ST001521/summary` | `/rest/study/study_id/ST003348/summary` |
| License in summary | CC BY 4.0 | CC BY 4.0 |
| Public status at content build | Public REST responses retrieved | Public REST responses retrieved |

The learner must add their own UTC check time and live/cached status.

## 3. Design and population key

| Field | `ST001521` expected evidence | `ST003348` expected evidence | Defensible classification |
|---|---|---|---|
| Species | Homo sapiens | Homo sapiens | `D` for species-level description |
| Design | Longitudinal FARMM feeding protocol; three diet groups; concurrent Abx/PEG perturbation; mixed assignment/setting | Repeated measures across one endurance exercise bout and recovery | `P` for repeated-measures structure; `N` as one common intervention design |
| Participants | 30 healthy volunteers described; 10 per diet group | 20 recruited male student-athletes described in collection metadata, one withdrew; 19 represented in 76 samples | `P` for descriptive counts only |
| Biological samples | 150 expected participant-timepoint rows, 30 x 5 | 76, 19 x 4 | `P`; do not treat as independent people |
| Other samples | 10 `QPP...` pooled QC candidates among 160 factor rows | No additional QC rows identified in the factor endpoint | `N` as participant data; retain for QC role |
| Repeated linkage | Local identifiers support subject and visit parsing, to be validated | Local identifiers such as `79_1` through `79_4` support athlete and time parsing, to be validated | `P` until parsing is checked against documentation |
| Assignment caveat | Twenty omnivores randomized to omnivore versus EEN; vegan participants were established vegans and continued usual diet as outpatients | No randomized comparison group in the deposited acute time-course description | `N` for a common randomized contrast |

High-quality learner answers note that the project metadata labels `ST001521` as observational while its detailed summary includes randomization within the 20 omnivores. The resolution is not to choose one label, but to describe the hybrid design at the relevant contrast.

## 4. Phenotype and protocol key

| Field | `ST001521` | `ST003348` | Decision |
|---|---|---|---|
| Anchor | Diet group plus longitudinal microbiota depletion/reconstitution context | Acute endurance race walk and recovery | `N` as one intervention variable |
| Groups/time | Deposited `Study_Diet` values include `Vegan`, `Western`, and `Modulen`; time values include Baseline and Days 5, 9, 12, 15 | `REST`, `STAT`, `REC3`, `REC22` | `N` as a common time axis |
| Concurrent procedures | Vancomycin/neomycin days 6-8 and PEG on day 7 described in summary | Exercise plus recovery; fasting noted for REST and REC22 in collection summary | `N` for diet-only versus exercise-only attribution |
| Setting | Vegan outpatients; omnivore/EEN inpatient under supervision | Athlete exercise study; exact supervision details should be sourced | `N` or `P` depending purpose |

Learners should not describe all three diet groups as randomized.

## 5. Specimen and pre-analytics key

| Field | `ST001521` | `ST003348` | Decision |
|---|---|---|---|
| Factor label | `Blood (plasma)` | `blood` | Source labels retained |
| Specific matrix | Plasma, isolated after blood collection | Collection block specifies `Blood (serum)` and clotting before centrifugation | `P` for blood-derived-fluid discovery; `N` for treating matrix as identical |
| Storage | Plasma aliquots described as immediately frozen at -80 C | Sera frozen on dry ice and stored at -80 C | `P`; other pre-analytics still differ |
| Collection timing | Study days in a feeding and Abx/PEG protocol | REST at 8:20 am, STAT at 10:30 am, REC3 at 13:30, REC22 at 8:20 am next day per collection summary | `N` as common clock/time protocol |

The factors-versus-collection difference for `ST003348` belongs in the provenance-conflict table. A good resolution preserves `blood` as the source factor, derives `serum` from the more specific collection metadata, and cites both.

## 6. Timepoint key

### `ST001521`

| Source | Canonical interpretation |
|---|---|
| Baseline | Pre-protocol or initial collection; verify exact day mapping in the study record |
| Day 5 | Longitudinal study day before the documented Abx/PEG interval |
| Day 9 | Longitudinal study day after the documented days 6-8 antibiotics and day 7 PEG |
| Day 12 | Later study day in reconstitution/feeding context |
| Day 15 | Later study day in reconstitution/feeding context |

The labels are valid within the FARMM design but should not be converted to acute recovery offsets.

### `ST003348`

| Source | Canonical interpretation |
|---|---|
| REST | Pre-exercise fasting sample |
| STAT | Immediately after exercise |
| REC3 | 3-hour recovery |
| REC22 | 22-hour recovery, fasting sample on day 2 |

The two time axes are `N` for a common post-intervention variable. A broad `within-study repeated time` flag is `P` for workflow comparison only.

## 7. Assay key

### `ST001521`

| Analysis | Summary | Chromatography | Instrument | Ion mode | Units |
|---|---|---|---|---|---|
| AN002533 | HILIC | HILIC | Thermo Exactive Plus Orbitrap | Positive | Unitless peak areas |
| AN002534 | Reversed phase | Reversed phase | Thermo Exactive Plus Orbitrap | Positive | Unitless peak areas |
| AN002535 | HILIC | HILIC | Thermo Q Exactive Plus Orbitrap | Negative | Unitless peak areas |
| AN002536 | Reversed phase | Reversed phase | Thermo Q Exactive Orbitrap | Negative | Unitless peak areas |

### `ST003348`

| Analysis | Summary | Chromatography | Instrument | Ion mode | Units |
|---|---|---|---|---|---|
| AN005483 | Reversed phase | Reversed phase | Thermo Q Exactive Plus Orbitrap | Positive | Peak area |
| AN005484 | Reversed phase | Reversed phase | Thermo Q Exactive Plus Orbitrap | Negative | Peak area |

Some instrument families and ion modes overlap, but laboratories, chromatography, specimen, feature coverage, preprocessing, and measurement scales still differ. The correct cross-study quantitative pooling decision is `No` for this module.

## 8. Minimum comparability decisions

| Domain | Purpose | Expected category | Allowed action | Prohibited inference |
|---|---|---|---|---|
| Species | Cohort description | `D` | State both are human | Assume populations are exchangeable |
| Matrix | Broad discovery | `P` | Label blood-derived plasma versus serum | Treat values as same matrix |
| Time | Within-study trajectory | `P` | Analyze each study's time course separately | Map Days 5-15 to STAT/REC3/REC22 |
| Phenotype | Metadata comparison | `N` as one field | Describe diet and exercise protocol structures | Estimate a common intervention effect |
| RefMet name | Exact reviewed overlap | `P` until annotation QC; then `D` at name-set level for accepted rows | Count eligible shared names | Infer equal concentration or response |
| Units | Quantitative cross-study comparison | `N` | Report source scales | Pool unitless/peak areas |
| Repeated measures | Workflow structure | `P` | Preserve subject linkage within each study | Treat rows as independent participants |
| Platform/mode | Assay inventory | `P` | Stratify or document modes | Assume equal coverage because both use LC-MS |

## 9. Model exclusion statement

> We will not combine peak-area measurements across the two studies because matrix, laboratory, chromatography, feature coverage, preprocessing, scale, population, and intervention context differ. We can still compare reviewed RefMet-name coverage by constructing provenance-preserving study-specific sets and reporting their intersection with explicit eligibility rules.

## 10. Acceptable bounded claim

> Under the specified mapping and eligibility rules, both public studies report a set of shared standardized metabolite names; this overlap describes deposited analyte coverage and does not establish shared abundance or intervention response.

## Sources for instructors

- [ST001521 landing page](https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?StudyID=ST001521)
- [ST001521 factors](https://www.metabolomicsworkbench.org/rest/study/study_id/ST001521/factors)
- [ST001521 analyses](https://www.metabolomicsworkbench.org/rest/study/study_id/ST001521/analysis)
- [ST003348 landing page](https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?StudyID=ST003348)
- [ST003348 factors](https://www.metabolomicsworkbench.org/rest/study/study_id/ST003348/factors)
- [ST003348 analyses](https://www.metabolomicsworkbench.org/rest/study/study_id/ST003348/analysis)

