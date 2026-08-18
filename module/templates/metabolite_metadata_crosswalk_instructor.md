# Metabolite and metadata crosswalk - instructor version

Use this key to model decision quality. It is not a substitute for the machine-generated full crosswalk, whose current counts and rows must be created from the versioned repository responses.

## 1. What earns full credit

A full-credit crosswalk:

- Preserves accession, analysis ID, source identifier, submitted name, and source RefMet result.
- Records exact endpoints and retrieval dates.
- Treats mapping as a reviewable decision rather than a truth assignment.
- Preserves annotation resolution and identification evidence.
- Retains ambiguous, unmapped, isotope-labeled, and duplicated cases.
- Separates exact-name, class-summary, within-study, and cross-study eligibility.
- Marks cross-study quantitative eligibility `no` for every row in this module.
- Produces an overlap flow with exclusion counts, not only an intersection.

## 2. Completed metabolite examples

These examples use values visible in the Metabolomics Workbench metabolite responses. Review status is an instructional decision based on the visible naming evidence; a production crosswalk should incorporate all available identifiers and methods.

| Source | Analysis | Deposited name | Source RefMet | Recommended status | Exact overlap | Class summary | Key reason |
|---|---|---|---|---|---|---|---|
| `ST001521` | AN002533 | `2-Aminooctanoic acid` | `2-Aminocaprylic acid` | `review_required` until synonym/identifier evidence is checked; then potentially `accepted_exact` | review | review/yes | Name changed to a synonym; verify it represents the same supported structure |
| `ST001521` | AN002533 | `LPC(P-18:0)/LPC(O-18:1)_A` | `LPC P-18:0 or LPC O-18:1` | `accepted_broader` at the explicitly ambiguous species level | no for a unique molecular structure; yes only if exact key is the ambiguous RefMet string | yes | The source does not distinguish plasmanyl and plasmenyl alternatives |
| `ST001521` | AN002533 | `LPE(18:0)_A` | `LPE 18:0` | `accepted_exact` at reported sum-composition level, with duplicate flag | yes as a set key | yes | `_A` and another source feature can map to one RefMet name; do not merge intensities silently |
| `ST001521` | AN002533 | `LPE(18:0)_B` | `LPE 18:0` | `accepted_exact` at reported sum-composition level, with duplicate flag | yes as same set key | yes | Many-to-one mapping must remain visible |
| `ST003348` | AN005484 | `Mannitol+Sorbitol` | `Mannitol` | `review_required` or `accepted_broader` only for a stated broad purpose | no | review | Composite/isomeric label has been narrowed by the returned name; information loss is material |
| `ST003348` | AN005484 | `NegX-RT295MZ165` | blank | `unmapped` | no | no/unclassified only if rule allows | Unidentified feature must not be assigned from mass alone |
| `ST003348` | AN005484 | `Palmitic acid-[13C]16` | `Palmitic acid` | `excluded_nonbiological` for biological overlap | no | no | Isotope-labeled analyte/standard must not create a biological overlap with endogenous palmitic acid |
| `ST003348` | AN005484 | `Linoleic acid(FFA(18:2n6)` | `Linoleic acid` | `review_required`, then potentially accepted at supported resolution | review | yes/review | Preserve source notation and verify structural-resolution equivalence |

Important: the exact handling of `_A`/`_B` features depends on source-method context. They may be chromatographic isomers or distinct signals. Set overlap can collapse identical accepted keys while the quantitative matrix retains source features.

## 3. Completed metadata examples

| Source field/value | Harmonized representation | Compatibility | Purpose | Decision note |
|---|---|---|---|---|
| `ST001521`: `sample_source = Blood (plasma)` | `broad_source = blood_derived_fluid`; `matrix = plasma` | Partial with exercise specimen | Name-set discovery | Preserve plasma; broad category is not quantitative equivalence |
| `ST003348` factors: `sample_source = blood`; collection: `Sample Type = Blood (serum)` | `source_factor = blood`; `matrix = serum`; `matrix_evidence = collection` | Partial with diet specimen | Name-set discovery | Preserve both sources; prefer the specific supported matrix for analysis |
| `ST001521`: `Time = Day 9` | `study_day = 9`; `protocol_state = post_Abx_PEG_interval` if supported by summary | Not comparable with REC time | Within-study description | Do not call it generic `post` or map to exercise recovery |
| `ST003348`: `Collection_time = stat` | `anchor = exercise_end`; `offset = 0 min`; `state = immediate_post_exercise` | Not comparable with diet days | Exercise trajectory | Meaning comes from project/collection summary, not the code alone |
| `ST003348`: `Collection_time = rec3` | `anchor = exercise_end`; `offset = 3 h`; `state = recovery` | Direct only inside exercise study | Exercise trajectory | Preserve `REC3` source label |
| `ST001521`: `QPP01` with diet/sex/time NA | `sample_role = pooled_qc` after evidence check | Not a participant observation | QC diagnostics | Exclude from biological PCA and participant counts; retain for QC |
| `ST001521`: `units = unitless peak areas` | Keep source scale; no common target | Not compatible for pooled quantitative analysis | Measurement audit | Scaling cannot create a calibrated common unit |
| `ST003348`: `units = Peak area` | Keep source scale; no common target | Not compatible for pooled quantitative analysis | Measurement audit | Different assay, lab, matrix, and preprocessing remain |

## 4. Overlap audit key

The build-level checks are 153 shared nonblank exact RefMet strings before artifact and eligibility exclusions, then 145 conservative biological overlaps after excluding eight `ST003348` isotope/internal-standard rows that map to ordinary RefMet labels. A full-credit learner response:

1. Labels this as preliminary.
2. Records the retrieval and crosswalk versions.
3. Shows how isotope-labeled compounds, artifacts, blanks, duplicates, ambiguous mappings, and annotation rules change the set.
4. Reports diet, exercise, and shared denominators.
5. Does not describe shared strings as shared intervention responses or comparable concentrations.

Require learners to distinguish the 153 raw check from the 145 conservative artifact-filtered check. Further justified eligibility rules may reduce the reported set below 145; they must be versioned and counted.

## 5. Common errors and feedback

| Error | Instructor feedback |
|---|---|
| Replacing source names with RefMet names | Add separate source and standardized columns so the mapping remains auditable. |
| Accepting every nonblank RefMet value | A repository-provided mapping still needs role, resolution, artifact, and ambiguity review. |
| Dropping blank mappings | Retain them as `unmapped`; missing mapping is a meaningful result. |
| Mapping isotope-labeled standards to endogenous names | Preserve isotope labels and exclude nonbiological standards from biological overlap. |
| Merging duplicate RefMet features before preserving analysis IDs | Keep feature-level rows; create a separate set-level key for overlap. |
| Marking plasma and serum identical | Retain exact matrix and use a broad category only for a purpose that tolerates the distinction. |
| Converting peak areas to a common z-score and calling them comparable | Standardization changes scale but does not remove platform, matrix, batch, or design differences. |
| Maximizing the mapping rate | Mapping quality and explicit uncertainty matter more than the percentage mapped. |

## 6. Suggested scoring, 20 points

| Criterion | Points |
|---|---:|
| Source identity and provenance complete | 4 |
| Mapping and annotation-resolution decisions justified | 4 |
| Ambiguous, unmapped, isotope-labeled, and duplicate cases handled | 4 |
| Specimen/time/unit metadata aligned with information loss visible | 4 |
| Purpose-specific eligibility and non-pooling guardrail applied | 4 |
