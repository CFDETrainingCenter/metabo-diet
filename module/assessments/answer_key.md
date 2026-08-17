# Metabo-Diet answer key

**Instructor-only file:** Do not expose before learners submit the corresponding assessment. The JSON assessment files are the authoritative machine-readable source for item wording, options, answers, and full rationales.

## Pretest key

| Item | Answer | Objective(s) | Rationale |
|---|---|---|---|
| PRE-01 | C | LO1 | A `post` value needs an anchor, elapsed time, physiological state, specimen, and assay context. |
| PRE-02 | B | LO1, LO2 | Repeated samples from one person are correlated; sample count is not participant count. |
| PRE-03 | A | LO2 | A shared standardized name supports a naming bridge, not shared scale, specimen, preprocessing, or causal response. |
| PRE-04 | B | LO3 | RefMet supplies standardized nomenclature designed for analytical chemistry. |
| PRE-05 | C | LO3 | Ambiguity must remain visible until additional evidence supports one candidate. |
| PRE-06 | B | LO4 | The MW study-context `factors` output returns samples and experimental variables. |
| PRE-07 | B | LO2, LO4 | PCA describes variance under selected preprocessing and does not assign a cause. |
| PRE-08 | B | LO5 | Access is established with current first-party evidence for the exact release and action. |
| PRE-09 | B | LO1, LO2 | Plasma and serum can share a broad discovery category but remain different matrices. |
| PRE-10 | B | LO5 | Participant-level governed data stay in approved compute and storage; only permitted outputs leave. |

**Maximum:** 10 points. Use as a baseline, not a pass/fail gate.

## Embedded knowledge-check key

| Item | Answer | Key idea |
|---|---|---|
| KC1-01 | B | RefMet match is a candidate standardized naming bridge, not analytical equivalence. |
| KC1-02 | C | Verify exact dataset, release, action, and current first-party policy. |
| KC1-03 | C | Cross-study PCA separation is not uniquely attributable when study and phenotype are confounded. |
| KC2-01 | B | A coarser binary derivation can be partially comparable with documented information loss. |
| KC2-02 | C | Repeated measures require a documented subject-sample relationship. |
| KC2-03 | B | A physiological timepoint needs anchor, offset, and state. |
| KC3-01 | C | Preserve multiple candidates and exclude unresolved rows from exact overlap. |
| KC3-02 | B | Unit conversion also requires compatible quantity, matrix, denominator, and quantification basis. |
| KC3-03 | B | Reproducibility requires source, mapping, review, rationale, and purpose-specific eligibility. |
| KC4-01 | A | `QPP...` rows are pooled QC candidates, not participant-timepoint observations. |
| KC4-02 | B | 153 is the raw nonblank exact RefMet string intersection before exclusions; the conservative artifact-filtered count is 145. |
| KC4-03 | A | Separate within-study PCA is exploratory and remains sensitive to preprocessing and design. |
| KC5-01 | C | MoTrPAC currently has public and restricted paths depending on the release. |
| KC5-02 | A | Approved code and permitted public references move in; controlled participant-level data do not move out. |
| KC5-03 | B | Access feasibility and scientific compatibility are separate gates. |

Give feedback immediately after each embedded response and permit a retry. Record first attempts only if the delivery and evaluation plan permits.

## Posttest key

| Item | Answer | Objective(s) | Rationale |
|---|---|---|---|
| POST-01 | B | LO1 | The current `ST001521` factor table has 150 participant-timepoint rows and 10 pooled `QPP...` QC rows. |
| POST-02 | B | LO1, LO2 | Preserve plasma and serum and limit the broad blood-derived category to discovery. |
| POST-03 | B | LO1, LO2 | FARMM Day 9 and 3-hour post-exercise recovery have different anchors and protocol meaning. |
| POST-04 | B | LO2 | Study-specific population, matrix, lab, platform, time, and protocol differences confound a direct contrast. |
| POST-05 | B | LO3 | Isotope/internal-standard roles must be preserved and excluded from biological overlap. |
| POST-06 | B | LO3 | Preserve feature-level provenance; a set collapse is distinct from a quantitative feature merge. |
| POST-07 | B | LO3, LO4 | The audited flow is 153 raw nonblank exact strings and 145 after eight nonbiological `ST003348` exclusions. |
| POST-08 | A | LO2, LO4 | Quantitative exploration is fitted within study; the uncalibrated raw matrices are not stacked. |
| POST-09 | B | LO4 | Cache use requires failure evidence, timestamp, integrity verification, and a visible source flag. |
| POST-10 | C | LO5 | MoTrPAC access is dataset- and release-dependent and must be checked. |
| POST-11 | B | LO5 | NPH participant-level analysis belongs in the Researcher Workbench and output follows current policy. |
| POST-12 | C | LO3, LO4 | Unexpected row multiplication requires a join-cardinality audit before analysis. |

**Maximum:** 12 points. Suggested mastery is 10/12 plus satisfactory performance artifacts. A learner who misses both items in an objective domain should review that lesson and complete a parallel retry.

## Lesson 4 interpretation challenge

### Statement 1

**Original:** "The studies share 153 biologically identical metabolites."

**Classification:** Unsupported.

**Suggested revision:**

> The audited build found 153 shared nonblank exact RefMet strings before exclusions and 145 conservative biological overlaps after removing eight `ST003348` isotope/internal-standard rows; these are name-set results, not evidence of identical concentration or response.

### Statement 2

**Original:** "The diet study contains 160 participants."

**Classification:** Unsupported.

**Suggested revision:**

> `ST001521` describes 30 participants and the current factors response contains 150 participant-timepoint rows plus 10 pooled `QPP...` QC rows.

### Statement 3

**Original:** "The exercise samples are blood, so they are the same matrix as diet plasma."

**Classification:** Unsupported.

**Suggested revision:**

> The exercise factors use the broad label `blood`, while collection metadata specifies serum; serum and diet-study plasma are partially comparable as blood-derived fluids for discovery and are not the same quantitative matrix.

### Statement 4

**Original:** "PCA separates exercise timepoints, proving the race walk caused every measured change."

**Classification:** Unsupported.

**Suggested revision:**

> Within `ST003348`, the exploratory PCA may show variation associated with the ordered REST, STAT, REC3, and REC22 samples under the chosen preprocessing; repeated measures, collection context, technical variation, and other time-varying factors limit causal attribution for individual metabolites.

### Statement 5

**Original:** "An apparent class difference may reflect assay coverage as well as biology."

**Classification:** Supported, with a precision edit.

**Suggested revision:**

> A difference in the number or proportion of reported RefMet names by class may reflect platform coverage, annotation, filtering, matrix, and biology; it should be described as deposited analyte coverage rather than class abundance.

## Cohort-comparison worksheet key points

Use the detailed instructor worksheet for row-level evidence. Require these conclusions:

- Both studies are human, which is directly comparable only at a broad species-description level.
- `ST001521` is plasma and `ST003348` is serum. The `ST003348` factor source says `blood`, but collection metadata provides the supported specific matrix.
- `ST001521` includes five longitudinal study times in a feeding plus Abx/PEG protocol; `ST003348` includes an acute exercise and recovery sequence. They do not form one common post-intervention axis.
- `ST001521` has 30 described participants, 150 biological rows, and 10 pooled QC rows; `ST003348` has 19 represented athletes and 76 biological rows.
- The diet study has a hybrid design: established vegan outpatients and randomization of 20 omnivores to omnivore versus EEN. Do not call all three groups randomized.
- Analysis families and some ion modes overlap, but laboratory, chromatography, matrix, coverage, preprocessing, and scale differ.
- Cross-study quantitative pooling is not authorized.

### Model exclusion statement

> We will not combine peak-area values across the studies because matrix, laboratory, chromatography, feature coverage, preprocessing, population, time, and intervention context differ. We can still compare reviewed RefMet names by building one documented set for each study and reporting their overlap.

## Metabolite/metadata crosswalk key points

Use the 20-point rubric in the instructor template. Minimum acceptable evidence includes:

- Original label, source RefMet value, accession, analysis ID, and endpoint.
- Mapping and annotation-resolution status.
- Reviewer or rule version and decision rationale.
- An ambiguous or broader mapping kept visible.
- An unmapped row retained.
- A many-to-one mapping retained at feature level.
- Isotope/internal-standard rows excluded from biological overlap with a reason.
- Separate eligibility for exact overlap, class summary, within-study analysis, and cross-study quantitative analysis.
- `eligible_cross_study_quantitative = no` throughout.
- Audit flow that reproduces or explains 153 raw and 145 conservative overlaps.

## Access-pattern transfer checklist key points

Use the 20-point rubric in the instructor template. Require:

- Exact dataset, release, data level, intended action, compute, storage, and outputs.
- Current first-party evidence with a check date.
- Separate access and scientific-compatibility decisions.
- An explicit data-flow boundary.
- No credentials or governed data in the artifact.
- A `GO`, `REVISE`, `WAIT`, or `STOP` decision with unresolved items.

### MoTrPAC worked conclusion

> `Mixed`: current first-party documentation distinguishes public releases accessible without login from restricted or embargoed content requiring additional authorization. Verify the exact file and intended action.

### NPH/All of Us worked conclusion

> `Controlled compute` for participant-level work: run approved code in the Researcher Workbench, keep governed data there, and export only outputs permitted by current policy. Verify the exact Registered or Controlled Tier collection and release.

## Performance-artifact minimums

A learner should not pass the module based on multiple-choice score alone. Require:

- Comparison worksheet with sources, explicit missingness, and at least one intentional non-harmonization decision.
- Crosswalk score of at least 16/20 with all scientific-safety conditions met.
- Notebook audit that reproduces the expected structural checks and either reproduces 153/145 or explains a documented data revision.
- Four-sentence interpretation containing observation, context, alternatives, and a claim boundary.
- Transfer checklist score of at least 16/20 with no governance-safety failure.
