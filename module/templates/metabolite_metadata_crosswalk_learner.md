# Metabolite and metadata crosswalk - learner version

**Module:** Metabo-Diet  
**Learner/reviewer:** ____________________  
**Crosswalk version:** ____________________  
**Created:** ____________________  
**RefMet retrieval date/version:** ____________________

## Purpose and non-purpose

This template records source evidence, harmonized representations, review decisions, and purpose-specific eligibility for `DIET_ACCESSION = ST001521` and `EXERCISE_ACCESSION = ST003348`.

It supports auditable name and metadata comparison. It does not authorize pooling quantitative values across the studies.

## Controlled values

### Mapping status

- `accepted_exact`
- `accepted_broader`
- `review_required`
- `unmapped`
- `excluded_nonbiological`
- `not_evaluated`

### Annotation resolution

- `discrete_structure`
- `stereochemistry_unspecified`
- `lipid_molecular_species`
- `lipid_sum_composition`
- `compound_class_only`
- `unknown`

### Eligibility

Use `yes`, `no`, or `review` separately for:

- `eligible_exact_name_overlap`
- `eligible_class_summary`
- `eligible_within_study_quantitative`
- `eligible_cross_study_quantitative`

For this module, `eligible_cross_study_quantitative` is `no` for both studies.

## Tab A - Metabolite mapping

Use one row per source feature per analysis. Do not deduplicate before preserving source identity.

| Column | Required meaning |
|---|---|
| `row_id` | Stable crosswalk-row identifier |
| `config_key` | `DIET_ACCESSION` or `EXERCISE_ACCESSION` |
| `study_accession` | `ST001521` or `ST003348` |
| `analysis_id` | Source `AN...` identifier |
| `source_feature_id` | Original feature/metabolite ID if present |
| `source_metabolite_name` | Exact deposited label |
| `source_refmet_name` | RefMet value returned in the MW metabolite record, including blank |
| `source_formula` | Original formula or `NR` |
| `source_inchikey` | Original InChIKey or `NR` |
| `source_external_ids` | PubChem, HMDB, KEGG, or other IDs with namespaces |
| `source_unit` | Exact analysis unit or scale |
| `source_endpoint` | Exact URL or cached file identifier |
| `retrieved_at_utc` | ISO 8601 timestamp |
| `lookup_string` | Exact string sent to RefMet, if queried separately |
| `lookup_transform` | Changes from source label to lookup string; use `none` if unchanged |
| `refmet_candidate` | Candidate standardized name; preserve multiple candidates |
| `refmet_query_url` | Exact query or versioned bulk-table source |
| `annotation_resolution` | Controlled value above |
| `identification_evidence` | Evidence reported by source; do not upgrade it |
| `mapping_status` | Controlled value above |
| `decision_reason` | Evidence-based rationale |
| `reviewer_or_rule` | Person, rule ID, or software version |
| `reviewed_at_utc` | ISO 8601 timestamp |
| `eligible_exact_name_overlap` | `yes`, `no`, or `review` |
| `eligible_class_summary` | `yes`, `no`, or `review` |
| `eligible_within_study_quantitative` | `yes`, `no`, or `review` |
| `eligible_cross_study_quantitative` | `no` for this module |
| `exclusion_reason` | Required when an eligibility field is `no` |
| `decision_log` | Append-only note for changes |

### Blank working rows

Complete at least 12 rows: six per study. Include an apparent overlap, a lipid if present, an ambiguous mapping, and an unmapped or unidentified feature when present.

| row_id | config_key | analysis_id | source_metabolite_name | source_refmet_name | candidate | resolution | status | exact overlap | class summary | within-study | cross-study | decision reason |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M001 |  |  |  |  |  |  |  |  |  |  | no |  |
| M002 |  |  |  |  |  |  |  |  |  |  | no |  |
| M003 |  |  |  |  |  |  |  |  |  |  | no |  |
| M004 |  |  |  |  |  |  |  |  |  |  | no |  |
| M005 |  |  |  |  |  |  |  |  |  |  | no |  |
| M006 |  |  |  |  |  |  |  |  |  |  | no |  |
| M007 |  |  |  |  |  |  |  |  |  |  | no |  |
| M008 |  |  |  |  |  |  |  |  |  |  | no |  |
| M009 |  |  |  |  |  |  |  |  |  |  | no |  |
| M010 |  |  |  |  |  |  |  |  |  |  | no |  |
| M011 |  |  |  |  |  |  |  |  |  |  | no |  |
| M012 |  |  |  |  |  |  |  |  |  |  | no |  |

Attach or export the complete column set for machine use. The shortened table above is for review discussion only.

## Tab B - Metadata-field mapping

Use one row per source field or coded value.

| Column | Meaning |
|---|---|
| `metadata_row_id` | Stable identifier |
| `config_key` | Study configuration key |
| `study_accession` | Resolved accession |
| `source_block_or_endpoint` | mwTab block or REST URL |
| `source_field` | Exact field name |
| `source_value` | Exact value |
| `construct_definition` | Meaning supported by protocol |
| `harmonized_field` | Derived common field, if any |
| `harmonized_value` | Derived value, if any |
| `transformation_rule` | Reproducible derivation |
| `information_lost` | Detail removed or `none` |
| `compatibility` | Direct, partial, not comparable, or not yet assessable |
| `purpose` | Analysis purpose for that decision |
| `source_url` | Exact evidence location |
| `retrieved_at_utc` | Retrieval timestamp |
| `reviewer_or_rule` | Reviewer or rule version |
| `decision_note` | Rationale and restrictions |

### Required metadata rows

| metadata_row_id | config_key | source field/value | construct | harmonized field/value | rule | information lost | compatibility | purpose | decision note |
|---|---|---|---|---|---|---|---|---|---|
| MD001 |  |  | Specimen matrix |  |  |  |  |  |  |
| MD002 |  |  | Specimen matrix |  |  |  |  |  |  |
| MD003 |  |  | Timepoint |  |  |  |  |  |  |
| MD004 |  |  | Timepoint |  |  |  |  |  |  |
| MD005 |  |  | Timepoint |  |  |  |  |  |  |
| MD006 |  |  | Participant/sample relationship |  |  |  |  |  |  |
| MD007 |  |  | Phenotype |  |  |  |  |  |  |
| MD008 |  |  | Measurement scale |  |  |  |  |  |  |

## Tab C - Unit and scale decisions

| config_key | analysis_id | source quantity | source unit/scale | candidate target | dimensionally convertible? | quantification compatible? | action | formula/rule | reason |
|---|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |

## Tab D - Cross-study overlap audit

Do not report only the final intersection.

| Stage | Diet count | Exercise count | Shared count | Rule/version | Exclusions at this stage |
|---|---:|---:|---:|---|---|
| Distinct submitted labels |  |  | NA |  |  |
| Nonblank source RefMet strings |  |  |  |  |  |
| Reviewed accepted mappings |  |  |  |  |  |
| Eligible after artifact rules |  |  |  |  |  |
| Unique exact-name keys |  |  |  |  |  |
| Final reported set |  |  |  |  |  |

**Build checks:** The current release reported 153 shared nonblank exact RefMet strings before artifact and eligibility exclusions. Excluding eight `ST003348` isotope/internal-standard rows that mapped to ordinary RefMet labels yielded a conservative biological overlap of 145. If you do not reproduce 153 and then 145 with the same source version and rules, investigate and document the difference; do not tune decisions to force either count.

## Reproducibility audit

- [ ] Original labels and identifiers are never overwritten.
- [ ] Every row includes accession, analysis ID, and source endpoint.
- [ ] Lookup transformations and query strings are recorded.
- [ ] Automated mappings are distinguishable from reviewed decisions.
- [ ] Annotation resolution is no more specific than source evidence.
- [ ] One-to-many and many-to-one cases remain visible.
- [ ] Internal standards, isotope-labeled compounds, pooled QC, and artifacts have explicit roles.
- [ ] Unmapped and review-required rows remain in the crosswalk.
- [ ] Eligibility is purpose-specific.
- [ ] Cross-study quantitative eligibility is `no`.
- [ ] Decision changes are append-only or versioned.
