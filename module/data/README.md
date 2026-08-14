# Data cache and sanitization contract

The files in `raw/` are immutable snapshots of public Metabolomics Workbench REST responses retrieved on 2026-08-10. Do not edit source JSON in place. File URLs, byte counts, retrieval timestamps, licenses/access notes, and SHA-256 checksums are recorded in `provenance.json`.

## Factor sanitization

### ST001521 (diet; plasma)

1. Trim factor-field whitespace without changing source category labels.
2. Mark local sample IDs `QPP01` through `QPP10` as pooled QC. Exclude all ten from participant counts, biological summaries, PCA, and longitudinal models.
3. For biological rows, derive `participant_id` from the leading four digits of `local_sample_id` and retain the original ID.
4. Preserve source factors `Study_Diet`, `Sex`, and `Time`. Keep `Western` as the factor label even though the narrative calls the arm omnivore.
5. Validate observed visits instead of forcing a balanced panel: Western males have nine Day 5 rows and eleven Day 9 rows.
6. Use the split study-level REST JSON. Analysis-level mwTab JSON for AN002533, AN002535, and AN002536 is malformed at pooled-QC factors; the plain mwTab text remains valid.

### ST003348 (exercise; serum)

1. Derive `participant_id` from the integer before the underscore in `local_sample_id` and retain the original ID.
2. Validate suffixes 1, 2, 3, and 4 against `rest`, `stat`, `rec3`, and `rec22`, respectively.
3. Preserve source `sample_source=blood`, but set the harmonized specimen to `serum` from the more specific collection block.
4. Treat the treatment-block value `no treatment` as a metadata defect; define the exercise exposure from the documented protocol, collection, and time factors.

## Metabolite sanitization

Construct the raw RefMet intersection from unique, nonblank `refmet_name` values while retaining `analysis_id` and source `metabolite_name`. Before labeling the intersection biological, remove the eight ST003348 isotope-labeled/internal-standard mappings enumerated in `provenance.json`. The resulting operational overlap is 145 names, down from 153 raw exact labels. Do not merge raw peak-area matrices across studies; ST001521 is plasma and ST003348 is serum, with different analytical methods and scales.

`raw/refmet_classification.json` is the complete public RefMet classification response used for offline class lookups. A smaller derived subset may be distributed with learner materials, but it must cite the full-source checksum in `provenance.json`.
