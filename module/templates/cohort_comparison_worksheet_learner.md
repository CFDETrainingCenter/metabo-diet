# Cohort-comparison worksheet - learner version

**Module:** Metabo-Diet  
**Learner:** ____________________  
**Date:** ____________________  
**Retrieval timezone:** ____________________

## Purpose

Use this worksheet to compare `DIET_ACCESSION = ST001521` and `EXERCISE_ACCESSION = ST003348` without assuming that a shared label makes records quantitatively exchangeable.

Use these codes:

- `D` - directly comparable for the stated purpose
- `P` - partially comparable; retain the difference and information loss
- `N` - not comparable for the stated purpose
- `U` - not yet assessable from available evidence
- `NR` - searched but not reported
- `NA` - not applicable

Every factual entry needs a source URL, mwTab block, REST endpoint, publication location, or explicit missingness code.

## 1. Comparison purpose and estimand sketch

**Choose one primary purpose:**

- [ ] Metadata inventory
- [ ] Exact standardized-name overlap
- [ ] Broad RefMet class coverage
- [ ] Within-study change followed by qualitative pattern comparison
- [ ] Other non-pooled purpose: ______________________________________

**Population:** ____________________________________________________________

**Exposure/intervention:** _________________________________________________

**Outcome or analyte set:** ________________________________________________

**Biological time definition:** ___________________________________________

**Summary measure:** ______________________________________________________

**What you will not use this comparison to claim:** _______________________

For the timed lesson, complete the eight named rows in Section 9 plus the supporting fields in Sections 2, 3, 5, and 6. The remaining rows are a project extension.

## 2. Dataset identity and access evidence

| Field | Diet study | Exercise study |
|---|---|---|
| Configuration key | `DIET_ACCESSION` | `EXERCISE_ACCESSION` |
| Resolved accession |  |  |
| Study title |  |  |
| Project/study DOI |  |  |
| Study landing page |  |  |
| REST summary endpoint |  |  |
| License shown |  |  |
| Public status check result |  |  |
| Check timestamp, UTC |  |  |
| Live or cached retrieval |  |  |
| Cache timestamp/checksum, if used |  |  |

## 3. Study design and population

| Field | Diet study evidence | Exercise study evidence | D/P/N/U | Justification and intended use |
|---|---|---|---|---|
| Species |  |  |  |  |
| Study design |  |  |  |  |
| Recruitment/setting |  |  |  |  |
| Inclusion/exclusion features |  |  |  |  |
| Participants recruited |  |  |  |  |
| Participants analyzed |  |  |  |  |
| Biological samples |  |  |  |  |
| QC/blank/other samples |  |  |  |  |
| Unit of assignment |  |  |  |  |
| Unit of analysis |  |  |  |  |
| Repeated-measures linkage |  |  |  |  |
| Randomization |  |  |  |  |
| Blinding/masking |  |  |  |  |
| Attrition |  |  |  |  |

## 4. Phenotype anchor and intervention

| Field | Diet study evidence | Exercise study evidence | D/P/N/U | Justification and intended use |
|---|---|---|---|---|
| Phenotype anchor |  |  |  |  |
| Intervention/exposure groups |  |  |  |  |
| Dose or intensity |  |  |  |  |
| Duration |  |  |  |  |
| Adherence or supervision |  |  |  |  |
| Feeding state |  |  |  |  |
| Concurrent interventions |  |  |  |  |
| Behavioral/clinical covariates |  |  |  |  |
| Assignment/selection caveat |  |  |  |  |

## 5. Specimen and pre-analytical context

| Field | Diet study evidence | Exercise study evidence | D/P/N/U | Justification and intended use |
|---|---|---|---|---|
| Broad factor label |  |  |  |  |
| Specific biological matrix |  |  |  |  |
| Collection method/tube |  |  |  |  |
| Processing |  |  |  |  |
| Storage |  |  |  |  |
| Collection clock time |  |  |  |  |
| Fasting status/duration |  |  |  |  |
| Pre-analytical gaps |  |  |  |  |

## 6. Timepoint semantics

Do not use the same harmonized time label merely because both studies contain `baseline`, `rest`, or `post` concepts.

### Diet study timepoints

| Source label | Anchor event | Offset/unit | Physiological/protocol state | Visit/order | Source | Resolved? |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |

### Exercise study timepoints

| Source label | Anchor event | Offset/unit | Physiological/protocol state | Visit/order | Source | Resolved? |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |

**Time-axis compatibility decision:** ______________________________________

**Evidence-based reason:** _________________________________________________

## 7. Assay and measurement context

List one row per analysis ID.

| Accession | Analysis ID | Analysis summary | Chromatography | Instrument | Ion mode | Targeted status | Units/scale | Source |
|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |

**Can quantitative values be pooled across studies?** Yes / No / Not yet assessable

**Reason:** ________________________________________________________________

## 8. Metadata provenance conflicts

Record fields for which two source locations differ or one source is more specific.

| Accession | Field | Source A/value | Source B/value | Resolution rule | Preserved evidence |
|---|---|---|---|---|---|
|  |  |  |  |  |  |
|  |  |  |  |  |  |

## 9. Comparability decision matrix

Complete at least eight rows. Name the purpose in each row; a field can receive a different decision for a different purpose.

| Domain/field | Intended purpose | D/P/N/U | Evidence-based justification | Allowed action | Prohibited inference |
|---|---|---|---|---|---|
| Species |  |  |  |  |  |
| Matrix |  |  |  |  |  |
| Timepoint |  |  |  |  |  |
| Participant count |  |  |  |  |  |
| Repeated-measures structure |  |  |  |  |  |
| Phenotype anchor |  |  |  |  |  |
| RefMet name |  |  |  |  |  |
| Annotation resolution |  |  |  |  |  |
| Units/scale |  |  |  |  |  |
| Platform/mode |  |  |  |  |  |
| Other: ______ |  |  |  |  |  |

## 10. Decision summary

**Directly comparable elements:** __________________________________________

**Partially comparable elements:** _________________________________________

**Elements that must remain separate:** ___________________________________

**Unresolved evidence:** ___________________________________________________

Complete the required exclusion statement:

> We will not combine __________________ across the two studies because __________________. We can still compare __________________ by __________________.

Write one bounded comparison claim:

> ________________________________________________________________________

Write one tempting but unsupported claim you will avoid:

> ________________________________________________________________________

## Completion check

- [ ] Every factual entry has a source or explicit `NR`, `NA`, or `U` code.
- [ ] Participant counts are separate from biological sample and QC counts.
- [ ] Plasma and serum remain visible.
- [ ] All time labels have protocol meanings or are unresolved.
- [ ] Concurrent interventions and selection/assignment caveats are recorded.
- [ ] All analysis IDs and units are listed.
- [ ] At least one field is intentionally not harmonized.
- [ ] No conclusion relies on pooled cross-study quantitative values.
