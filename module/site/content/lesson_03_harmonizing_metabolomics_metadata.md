# Lesson 3 - Harmonizing metabolomics and metadata

**Estimated time:** 35 minutes  
**Bloom level:** Apply  
**Module objectives addressed:** LO2, LO3

## Learning objectives

By the end of this lesson, you will be able to:

1. Build a provenance-preserving crosswalk from submitted metabolite labels to RefMet candidates.
2. Distinguish a naming match from evidence of chemical identification and analytical equivalence.
3. Align specimen, timepoint, variable, and unit metadata without concealing information loss.
4. Flag ambiguous or unresolved mappings instead of forcing a one-to-one result.
5. Evaluate whether a crosswalk is reproducible enough for downstream use.

The locked configuration is `DIET_ACCESSION = ST001521` and `EXERCISE_ACCESSION = ST003348`. Continue using the variable names in the crosswalk so the source accession remains explicit and a fallback pair can be substituted transparently.

## Lesson map

| Activity | Minutes |
|---|---:|
| Identifier problem and RefMet | 8 |
| mwTab and provenance | 5 |
| Specimen, time, variables, and units | 7 |
| Crosswalk activity | 12 |
| Knowledge check | 3 |

> **In the notebook (NB-L3):** Run `NB-L3-CROSSWALK` and inspect the labeled-standard table. Confirm the 153 raw and 145 conservative counts. Then trace one retained RefMet name and record what the match does and does not show in Tab A of the crosswalk.

## 1. Identifier systems answer different questions

Metabolomics records can contain common names, vendor labels, abbreviations, database identifiers, formulas, masses, or structural keys. These are not interchangeable fields.

| Field | What it can help represent | Important limitation |
|---|---|---|
| Submitted name | What the depositor reported | Synonyms, punctuation, adducts, and uncertain annotation can vary |
| RefMet name | Standardized analytical-chemistry nomenclature for a structure or metabolite species | A name match does not prove the underlying feature identification or equal structural resolution |
| InChIKey | Hash derived from a chemical structure representation | Layers encode different degrees of specificity; salts, protonation, tautomer, and stereochemical representation can differ |
| PubChem CID | Record identifier in PubChem | Different records may reflect different forms or levels of structural detail |
| HMDB ID | Record identifier in the Human Metabolome Database | Coverage and record relationships differ from other resources |
| KEGG compound ID | Identifier in KEGG's compound representation | Useful for pathway linking but not a universal metabolite identity key |
| Formula or exact mass | Composition or mass evidence | Isomers can share formula or mass; mass alone is not an identification |

RefMet provides the common naming field in this crosswalk. It covers discrete structures and analytically reported species, including lipid sum compositions. Keep the submitted labels and other identifiers beside it; a standardized name should not replace the original evidence.

## 2. Annotation resolution must be preserved

Suppose one study reports `PC 34:1` and another reports a phosphatidylcholine with two specified acyl chains. Even if a database relationship connects them, the annotations have different structural resolution. Collapsing both to the more specific structure would manufacture information. Collapsing to a broader class may be defensible for a class-level presence summary, but that is a derived analysis decision that must be recorded.

For each candidate match, record an **annotation-resolution status** such as:

- `discrete_structure`
- `stereochemistry_unspecified`
- `lipid_molecular_species`
- `lipid_sum_composition`
- `compound_class_only`
- `unknown`

Also record the identification evidence reported by the study when available. The Metabolomics Standards Initiative distinguishes levels of identification confidence; a standardized label does not upgrade that confidence.

> **Mapping limit:** Normalize a label only to the level supported by the deposited analytical evidence. Never infer a specific isomer, stereoisomer, lipid chain arrangement, or identification level from a fuzzy name match.

## 3. A reproducible mapping workflow

Use the following sequence for every distinct submitted analyte label.

### Step 1 - Preserve source identity

Record:

- Study accession: `DIET_ACCESSION` or `EXERCISE_ACCESSION`, resolved in the release manifest.
- Analysis identifier.
- Original analyte label exactly as deposited.
- Original metabolite or feature identifier.
- Original database identifiers and units.
- Source endpoint, retrieval timestamp, and source-table location.

Never overwrite the original label.

### Step 2 - Apply transparent normalization for lookup

Create a separate lookup string. Permissible preprocessing may include trimming whitespace or standardizing obvious delimiter characters. Record each transformation. Do not remove stereochemical markers, lipid chain details, charge, adduct, isotope label, or derivatization information merely to obtain a match.

### Step 3 - Query RefMet

The documented REST pattern for matching a name is:

```text
https://www.metabolomicsworkbench.org/rest/refmet/match/{URL_ENCODED_NAME}/name/
```

The exact response must be captured by the module notebook. A manual web conversion is acceptable for a small exercise, but record the query date and string.

### Step 4 - Validate the candidate

Compare all available evidence:

- Submitted and standardized names.
- Formula and mass.
- InChIKey or external IDs.
- Annotation resolution.
- Analytical method and identification evidence.
- Whether the candidate represents an adduct, derivative, isotope-labeled standard, or unresolved mixture.

The absence of a contradiction is not proof of identity. Use the confidence and decision fields.

### Step 5 - Assign mapping status

Recommended statuses are:

- `accepted_exact`: evidence supports the same standardized name and resolution.
- `accepted_broader`: a broader representation is intentionally used for a stated analysis.
- `review_required`: more than one candidate or conflicting evidence remains.
- `unmapped`: no supported RefMet candidate was found.
- `excluded_nonbiological`: internal standard, contaminant, adduct-only label, or other intentionally excluded feature, with a reason.
- `not_evaluated`: mapping has not been reviewed.

Automated output should begin as `not_evaluated` or `review_required`, not `accepted_exact`, unless the validation rule and evidence are explicit.

### Step 6 - Preserve the decision

Record reviewer, date, rule or evidence, decision reason, and downstream eligibility. If a decision changes, append a new record or version the table; do not erase the earlier rationale.

### Text-only concept sketch: mapping workflow

No separate image appears here. Imagine a six-column ledger read from left to right. The deposited feature and exact label stay fixed in the first column. A separate lookup string and RefMet response occupy the next two columns. Evidence and annotation resolution appear in the fourth column. A human or versioned rule records an accepted, broader, review-required, unmapped, or excluded decision in the fifth. The final column contains separate yes/no/review flags for exact-name overlap, class summary, within-study analysis, and cross-study analysis. Arrows never replace the first column; they add traceable decisions beside it.

## 4. Worked mapping example

These source and RefMet strings appear in the current public metabolite responses. The review decisions are instructional and must be regenerated if the repository record changes.

| Source/analysis | Deposited label | Source RefMet string | Evidence question | Safe decision |
|---|---|---|---|---|
| `ST001521`, AN002533 | `2-Aminooctanoic acid` | `2-Aminocaprylic acid` | Do synonym and identifier evidence support the same structure? | `review_required`, then potentially `accepted_exact` |
| `ST001521`, AN002533 | `LPE(18:0)_A` | `LPE 18:0` | Does `_A` distinguish a separate source feature, and is sum composition the supported resolution? | Preserve feature; accepted set key only after review |
| `ST001521`, AN002533 | `LPC(P-18:0)/LPC(O-18:1)_A` | `LPC P-18:0 or LPC O-18:1` | Is the unresolved ether-lipid alternative preserved? | `accepted_broader` for class/species purposes, not a unique structure |
| `ST003348`, AN005484 | `Mannitol+Sorbitol` | `Mannitol` | Has a composite/isomeric label been narrowed without support? | `review_required` |
| `ST003348`, AN005484 | `NegX-RT295MZ165` | blank | Is this an unidentified feature? | `unmapped`; do not name from mass alone |
| `ST003348`, AN005484 | `Palmitic acid-[13C]16` | `Palmitic acid` | Is the source an isotope-labeled analytical standard rather than endogenous palmitic acid? | `excluded_nonbiological` for biological overlap |

The last row shows why a nonblank standardized field is not automatically eligible. In the audited build, eight `ST003348` isotope/internal-standard rows map to ordinary RefMet labels; excluding them reduces the raw exact-name overlap from 153 to a conservative biological overlap of 145.

## 5. mwTab as an evidence map

An mwTab record is sectioned rather than a single flat data frame. Typical content includes project and study descriptions; subject and sample factors; collection and sample-preparation protocols; chromatography and instrument metadata; and a metabolite-data block. Presence and completeness vary by record and analysis.

For the configured studies, retrieve at least the following after substituting each variable's locked value:

```text
/rest/study/study_id/{DIET_ACCESSION}/summary
/rest/study/study_id/{DIET_ACCESSION}/factors
/rest/study/study_id/{DIET_ACCESSION}/analysis
/rest/study/study_id/{DIET_ACCESSION}/metabolites
/rest/study/study_id/{DIET_ACCESSION}/data
```

Repeat with `{EXERCISE_ACCESSION}`. Retrieve each selected analysis as mwTab when analysis-specific evidence is needed:

```text
/rest/study/analysis_id/{ANALYSIS_ID}/mwtab
```

Do not assume the shape of a response from the endpoint name. Inspect the returned keys, status code, and content type. A successful HTTP response can still contain an unexpected schema or an error message encoded as text.

### Provenance minimum

Every crosswalk row must be traceable to:

- Repository and base URL.
- Study accession and analysis identifier.
- Exact endpoint or source file.
- Retrieval timestamp in UTC.
- Original label and source identifier.
- Mapping service and query string.
- Mapping result and review decision.
- Reviewer or automated rule version.

These fields make the crosswalk reusable and support FAIR principles of findability, interoperability, and reuse.

## 6. Harmonizing specimen and time metadata

Metabolite-name mapping is only one part of the crosswalk.

### Specimen crosswalk

Keep at least three fields:

1. `source_specimen_label`: exact deposited value.
2. `normalized_specimen_category`: a controlled broader category used for a specific purpose.
3. `specimen_compatibility_note`: pre-analytical differences and any information loss.

For example, plasma and serum could both receive a broad `blood_derived_fluid` category for discovery, while remaining distinct in the exact matrix field. That category does not authorize quantitative pooling.

### Timepoint crosswalk

Keep the source label and derive structured fields only when evidence supports them:

- `anchor_event`
- `offset_value`
- `offset_unit`
- `physiological_state`
- `visit_or_period`
- `within_subject_order`
- `derivation_source`

If the label is `T2` and the protocol needed to decode it is missing, use `UNRESOLVED`; do not guess.

### Variable crosswalk

Separate:

- Source field and coding.
- Construct definition.
- Harmonized field and coding.
- Transformation rule.
- Information lost.
- Eligibility by analysis purpose.

For categorical variables, document reference levels and distinguish missing, unknown, not applicable, and structurally absent.

## 7. Unit reconciliation

Convert units only when all of the following are true:

1. The values measure the same quantity.
2. Units are known and convertible.
3. Specimen basis and denominator match or can be validly transformed.
4. Calibration and quantification type support the intended comparison.
5. The conversion formula is recorded and tested.

Examples of different situations:

- `umol/L` and `mmol/L` are dimensionally convertible for the same quantified analyte and compatible matrix, subject to the remaining checks.
- Peak area and `umol/L` are not made comparable by rescaling.
- Relative abundance normalized within one study and raw area in another are not a common measurement scale.
- Log-transformed and untransformed measurements can be reconciled only if the transform base, offset, and original scale are known and the comparison is otherwise valid.

Keep `source_value` and `source_unit` even after a justified conversion. Store the converted field separately.

## 8. Hands-on activity: build and audit the crosswalk

Use `module/templates/metabolite_metadata_crosswalk_learner.md`.

For the timed course, complete three worked rows: one retained shared RefMet name, one isotope-labeled or internal-standard exclusion, and one ambiguous or unmapped example. The 12-row metabolite table and full metadata audit are a project extension. This smaller path lets a first-time learner practice each decision type before scaling up.

### Part A - Metabolites

1. For the course path, select one retained shared name, one excluded standard, and one ambiguous or unmapped label. For the project extension, select at least six labels from each study.
2. Include at least one apparent overlap, one lipid label if present, one unmapped or unidentified feature if present, and one label requiring manual review. If a requested case does not occur, document that rather than fabricating it.
3. Preserve original labels and identifiers.
4. Run or inspect the RefMet query for each distinct label.
5. Assign mapping and annotation-resolution statuses.
6. Mark eligibility separately for exact-name overlap, broad-class summary, and quantitative comparison.

### Part B - Metadata

Add at least:

- Two specimen fields.
- Three timepoint values.
- One participant or sample identifier relationship.
- One phenotype field.
- One unit or scale field.

### Part C - Reproducibility audit

Exchange the crosswalk with a partner or use the self-audit prompts:

- Can another analyst find the exact source row?
- Can they reproduce the lookup string?
- Can they tell which output was automated and which was reviewed?
- Is information loss stated?
- Are unresolved cases preserved?
- Is downstream eligibility purpose-specific?
- Could the table be regenerated after a study update?

Flag any row that fails one of these checks. The goal is an auditable table, not a maximum mapping rate.

## 9. Mapping rules

- RefMet standardizes nomenclature; it does not retroactively validate compound identification.
- A one-to-many or many-to-one mapping is not automatically an error; it may reflect different resolution.
- Do not choose a candidate solely because it creates more overlap.
- Never convert unidentified features into named metabolites using mass alone.
- Preserve exact specimen and time labels alongside broader categories.
- Do not treat unit conversion as batch correction.
- Exclude internal standards and nonbiological features by explicit rule, not by silently deleting inconvenient rows.
- Version mapping decisions because repositories and reference databases evolve.

## 10. Knowledge check

**KC3-01.** A fuzzy RefMet lookup returns two plausible candidates and the deposited record has no formula or external identifier. What should you do?

A. Select the first candidate.  
B. Select whichever candidate appears in the other study.  
C. Mark the row `review_required` or `unmapped`, preserve both candidates, and exclude it from exact overlap until resolved.  
D. Replace it with a chemical class label and call it exact.

**KC3-02.** When can `umol/L` be converted to `mmol/L` for cross-study comparison?

A. Whenever both unit strings are present.  
B. Only after confirming the same quantity, compatible matrix and denominator, quantification basis, and a recorded conversion.  
C. Only for lipids.  
D. Never.

**KC3-03.** Which crosswalk design is most reproducible?

A. One column containing the final clean name.  
B. Original and standardized names, source and query provenance, mapping status, evidence, reviewer, decision reason, and purpose-specific eligibility.  
C. A list containing only mapped analytes.  
D. A table in which all ambiguities are manually forced to one value.

## What the crosswalk should preserve

A good crosswalk preserves the source label, the proposed standardized name, the supporting record, and the decision. Keep unresolved rows marked as unresolved so later analyses do not treat them as confirmed matches.

## Primary sources and first-party documentation

1. Metabolomics Workbench. [RefMet database and name-conversion resources](https://www.metabolomicsworkbench.org/databases/refmet/index.php). Accessed August 10, 2026.
2. Metabolomics Workbench. [RefMet naming conventions](https://www.metabolomicsworkbench.org/databases/refmet/refmet_help.php). Accessed August 10, 2026.
3. Fahy E, Subramaniam S. [RefMet: a reference nomenclature for metabolomics](https://doi.org/10.1038/s41592-020-01009-y). *Nature Methods*. 2020;17:1173-1174.
4. Metabolomics Workbench. [REST Service, version 1.2](https://www.metabolomicsworkbench.org/tools/mw_rest.php). Updated July 22, 2025; accessed August 10, 2026.
5. Metabolomics Workbench. [mwTab file specification and tutorials](https://www.metabolomicsworkbench.org/data/tutorials.php). Accessed August 10, 2026.
6. Powell CD, Moseley HNB. [The mwtab Python Library for RESTful access and enhanced quality control, deposition, and curation of the Metabolomics Workbench Data Repository](https://doi.org/10.3390/metabo11030163). *Metabolites*. 2021;11(3):163.
7. Sumner LW, Amberg A, Barrett D, et al. [Proposed minimum reporting standards for chemical analysis](https://doi.org/10.1007/s11306-007-0082-2). *Metabolomics*. 2007;3:211-221.
