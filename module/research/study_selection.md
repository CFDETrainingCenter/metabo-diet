# Metabo-Diet study selection and provenance review

Status: primary accessions locked on 2026-08-10.

## Decision

Use these two public Metabolomics Workbench studies for every learner-executed activity:

| Role | Study | Why it was selected |
|---|---|---|
| Diet anchor | [ST001521](https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?Mode=Study&StudyID=ST001521), FARMM plasma metabolites of known identity | Human plasma; controlled-feeding/diet-pattern contrast; five longitudinal collection labels; four LC-MS analyses; rich study, factor, specimen, and method metadata; CC BY 4.0; valid study-level REST JSON. |
| Exercise anchor | [ST003348](https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?Mode=Study&StudyID=ST003348), untargeted race-walking serum metabolomics | Human serum; acute endurance exercise; REST, immediate post-exercise, 3-hour recovery, and 22-hour recovery samples from 19 athletes; two LC-MS analyses; CC BY 4.0; valid study-level REST and analysis-level mwTab JSON. |

The exercise study matches the revised proposal's candidate description (rest, immediate post-exercise, and two recovery timepoints). The diet study meets the proposal's scientific selection criteria, but one proposal hint needs correction: FARMM pairs plasma with stool in companion study ST001519, not urine. The verified plasma/urine crossover alternative is ST000292/ST000291 and is retained below as the diet reserve.

The exact RefMet-name intersection is 153 unique labels. An independent source-name audit found eight isotope-labeled/internal-standard rows in ST003348 mapped onto ordinary RefMet labels, including the generic label `Standard`. After excluding all eight mappings, the conservative learner-facing overlap is **145 biological metabolites**. This is enough for a useful crosswalk while still leaving unresolved and study-specific metabolites to teach honest harmonization.

## Proposal criteria audit

The revised proposal specifies the selection criteria on page 4 of [metabo_diet_proposal_MW_revised.pdf](../../tmp/cfde_career_talk_deck/proposal-mw-render/metabo_diet_proposal_MW_revised.pdf): human subjects; plasma or serum; LC-MS or comparable; one diet and one exercise anchor; a real longitudinal/timepoint problem; public release with factor/specimen metadata; and enough metabolite overlap.

| Criterion | ST001521 | ST003348 | Pair-level judgment |
|---|---|---|---|
| Human | Homo sapiens, 30 adults | Homo sapiens, 19 completers | Meets |
| Plasma or serum | Plasma | Serum | Meets, with a deliberate plasma-versus-serum caveat |
| LC-MS or comparable | Four LC-MS methods | Two reversed-phase LC-MS methods | Meets |
| Phenotype anchor | Diet pattern/controlled feeding plus microbiome depletion | Acute endurance race walking | Meets |
| Longitudinal | Baseline; days 5, 9, 12, 15 | REST; STAT; REC3; REC22 | Meets in both studies |
| Public release | Released 2021-04-01; CC BY 4.0 | Released 2024-08-09; CC BY 4.0 | Meets; all selected study-level REST endpoints were publicly retrievable |
| Factor/specimen metadata | Diet, sex, time, plasma collection, additional mwTab fields | Collection time plus serum collection metadata | Meets with documented subject-ID derivation and QC cleanup |
| RefMet overlap | 510 unique nonblank RefMet names | 475 unique nonblank RefMet names | 153 exact labels; 145 after removing eight labeled/internal-standard mappings |

## Primary study evidence

### Diet anchor: ST001521 / PR001024

Primary repository record: [ST001521](https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?Mode=Study&StudyID=ST001521)  
Project DOI: [10.21228/M8B984](https://doi.org/10.21228/M8B984)

The repository describes the Food And Resulting Microbial Metabolites (FARMM) study as a longitudinal comparison of three diets: vegan, Western/omnivore, and exclusive enteral nutrition (EEN; Modulen). Twenty omnivores were randomized to the two inpatient feeding arms; ten established vegans continued their usual diet as outpatients. Plasma was collected at baseline and on days 5, 9, 12, and 15.

The REST factor endpoint returns 160 rows:

- 150 nominal biological rows: 30 participants x 5 collection labels
- 10 pooled-plasma QC rows, local IDs `QPP01` through `QPP10`
- factor fields `Study_Diet`, `Sex`, and `Time`

The four analyses are AN002533 (HILIC positive), AN002534 (C8 reversed-phase positive), AN002535 (HILIC negative), and AN002536 (reversed-phase negative), all on Exactive/Q Exactive Orbitrap instruments. The processed-data endpoint returns 567 analyte-analysis records and 510 unique nonblank RefMet names.

Important repository details:

- The collection block calls the specimen `Blood (plasma)`.
- The narrative calls one arm omnivore while factors call it `Western`. Preserve the source labels and document any mapping.
- Antibiotics were administered on days 6-8 and polyethylene glycol bowel purge on day 7. Day 9 onward is diet plus microbiome depletion/reconstitution, not a diet-only effect.
- The vegan arm differs from the other arms in pre-existing diet and outpatient setting.
- The factor table has nine Western-male Day 5 rows and eleven Western-male Day 9 rows. Do not force a balanced panel.
- Processed measurement cells are 4.12% missing overall and 4.23% missing after QC samples are excluded.

### Exercise anchor: ST003348 / PR002083

Primary repository record: [ST003348](https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?Mode=Study&StudyID=ST003348)  
Project DOI: [10.21228/M8C802](https://doi.org/10.21228/M8C802)

The repository describes 20 male student-athletes enrolled in an endurance race-walking protocol; one withdrew, leaving 19 complete profiles. Serum was collected at:

- `rest`: fasting before exercise at approximately 08:20
- `stat`: immediately after exercise at approximately 10:30
- `rec3`: 3 hours into recovery at approximately 13:30
- `rec22`: fasting at 22 hours post-exercise the next morning

The REST factors contain exactly 76 biological rows, 19 at each timepoint. The two analyses are AN005483 and AN005484, reversed-phase C18 LC-MS in positive and negative ion modes on a Q Exactive Plus Orbitrap. The processed-data endpoint returns 593 analyte-analysis records, 475 unique nonblank RefMet names, and no null measurement cells.

Important repository details:

- The factors endpoint uses the broad source label `blood`; the collection block is more specific and calls the material `Blood (serum)`. Use serum in the harmonized specimen field and retain the original label in provenance.
- There is no explicit participant field in the factors endpoint. Derive participant ID from the integer before the underscore in `local_sample_id`, and verify that suffixes 1-4 agree with `rest`, `stat`, `rec3`, and `rec22`.
- The treatment block says `no treatment` despite the documented race-walking protocol. Treat this as a repository metadata defect and use the study design, collection, and factors blocks to define the exercise contrast.
- The project narrative reports larger metabolite totals across the untargeted/targeted project than the selected study-level REST matrix. Notebook counts must come from the endpoint actually analyzed.
- Time of day and fasting state change across the trajectory and are part of the biological and design contrast.

## REST and mwTab verification

The [Metabolomics Workbench REST documentation](https://www.metabolomicsworkbench.org/tools/mw_rest.php) defines the study-level `summary`, `factors`, `analysis`, `metabolites`, and `data` endpoints used here. All ten primary-pair responses were retrieved on 2026-08-10, validated as JSON, and cached under `module/data/raw/`.

Endpoint pattern:

```text
https://www.metabolomicsworkbench.org/rest/study/study_id/{STUDY_ID}/{summary|factors|analysis|metabolites|data}
```

Every selected analysis also has a public plain-text mwTab endpoint containing `#SUBJECT_SAMPLE_FACTORS`, `#COLLECTION`, `#ANALYSIS`, `#MS`, and `#MS_METABOLITE_DATA` blocks:

```text
https://www.metabolomicsworkbench.org/rest/study/analysis_id/{ANALYSIS_ID}/mwtab/txt
```

One repository serialization defect must be taught or hidden safely: analysis-level mwTab JSON is valid for AN002534, AN005483, and AN005484, but malformed for AN002533, AN002535, and AN002536. In those three responses, the pooled-QC source factor text `Sex:NA| Time:NA` becomes an invalid JSON object. The underlying plain mwTab text is retrievable and the selected study-level REST JSON endpoints are valid. Therefore:

1. Use study-level `summary`, `factors`, `analysis`, `metabolites`, and `data` JSON in the notebook.
2. Use plain mwTab text only when teaching record structure.
3. Do not parse the three malformed analysis-level mwTab JSON responses.

Exact cached filenames, byte sizes, URLs, SHA-256 checksums, license fields, and validation notes are recorded in [provenance.json](../data/provenance.json).

## Overlap calculation

The overlap audit used only the public `/metabolites` responses and then inspected source metabolite names:

1. Extract `refmet_name`.
2. Remove null, blank, and `-` values.
3. Deduplicate within study.
4. Intersect names exactly and case-sensitively.
5. Exclude isotope-labeled/internal-standard source rows before calling the intersection biological.

Results:

| Metric | Value |
|---|---:|
| ST001521 unique nonblank RefMet names | 510 |
| ST003348 unique nonblank RefMet names | 475 |
| Exact intersection | 153 |
| Conservative biological intersection | 145 |
| Raw overlap as a share of ST001521 | 30.0% |
| Raw overlap as a share of ST003348 | 32.2% |
| Conservative overlap as a share of ST001521 | 28.4% |
| Conservative overlap as a share of ST003348 | 30.5% |

The eight excluded ST003348 mappings are: `AcCa(12:0)-D9` to `CAR 12:0`; `AcCa(18:0)-D3` to `CAR 18:0`; `Hippuric acid-D5` to `Hippuric acid`; `Lysine-d4` to `Standard`; `Taurine-D4` to `Taurine`; `CDCA-D4` to `Chenodeoxycholic acid`; `Palmitic acid-[13C]16` to `Palmitic acid`; and `Stearic acid-D35` to `Stearic acid`. Further annotation curation may reduce the defensible overlap, so 145 is a conservative operational count rather than a claim of compound-level analytical equivalence.

RefMet agreement is a nomenclature bridge, not a guarantee of identical annotation confidence, isomer resolution, extraction recovery, or quantitation. Duplicate RefMet names across analysis modes must remain analysis-aware unless a documented collapse rule is applied.

## Analysis guardrails for the module

- Exclude ST001521 pooled-QC rows before any biological summary or PCA.
- Exclude isotope-labeled/internal-standard analyte rows before the cross-study RefMet crosswalk.
- Build participant IDs with documented parsing rules, then verify timepoint completeness instead of assuming it.
- Run normalization, scaling, PCA, and time-course summaries within each study.
- Do not concatenate the two raw peak-area matrices and do not run one cross-study PCA on uncalibrated abundance values.
- Compare metabolite presence, RefMet class, within-study direction or standardized effect summaries, and design context rather than raw abundance magnitude.
- Treat plasma versus serum as partially comparable and preserve both original and harmonized specimen terms.
- Treat diet timepoints and exercise timepoints as different physiological semantics. They can be described using abstract roles such as baseline, active perturbation, and recovery, but they are not duration-matched equivalents.
- Make the FARMM antibiotic/PEG co-intervention visible in every interpretation of days 9, 12, and 15.

## Verified reserve pair

If a primary accession becomes unavailable, use this independent reserve pair:

| Role | Study | Fit and caveat |
|---|---|---|
| Diet | [ST000292](https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?Mode=Study&StudyID=ST000292), cranberry/apple juice crossover | Human plasma; 17 women sampled at baseline and after randomized cranberry-juice and apple-juice periods; two reversed-phase LC-MS modes; 553 unique nonblank RefMet names. This is a controlled beverage intervention, not full controlled feeding. Its paired urine companion is [ST000291](https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?Mode=Study&StudyID=ST000291). |
| Exercise | [ST001789](https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?Mode=Study&StudyID=ST001789), acute endurance exercise | Human plasma; pre, immediate post, and 60-minute recovery; two targeted LC-MS/MS analyses; 669 unique RefMet names. Participants received a banana after the run, so recovery is not fasting. |

The reserve pair has 122 exact unique RefMet overlaps before standard filtering. At least one overlapping label (`Tryptophan`) is contributed by the labeled source row `Tryptophan-2,3,3-D3` in ST000292, so the known-standard-filtered count is at most 121 pending the same full source-name curation used for the primary pair. Summary, factors, analysis, metabolites, data, and mwTab endpoints were retrieved successfully for both studies during screening, but the reserve matrices are not cached because they are not needed for the current module build.

## Candidates screened but not selected

- **ST002027, flaxseed intervention serum/HILIC:** appealing title and platform, but every REST factor row is labeled `Pre-intervention`; the intervention contrast is not represented cleanly enough for the proposed hands-on workflow.
- **ST003895, four isocaloric macronutrient challenges:** rich postprandial time series, but the REST factors expose time only and omit the macronutrient condition, preventing a reproducible diet contrast from the selected endpoint alone.
- **ST001490, low/high glycemic-load crossover:** clean baseline/HGL/LGL factors and public plasma FIA-MS data, but only 35 exact RefMet overlaps with exercise fallback ST001789 and less platform alignment.
- **ST003012, high-fat eucaloric diet:** human plasma with pre/on/post labels, but only 14 post-diet rows remain for 18 participants and its 79-name overlap with ST001789 is weaker than the selected reserve.
- **ST000387, exercise training:** public plasma LC-MS with pre/post factors, but the current `/metabolites` response has no nonblank RefMet mappings, which defeats the proposed RefMet-centered workflow.

## Independent audit reconciliation

An independent audit reproduced the primary accessions, endpoint availability, specimens, timepoints, and study-design caveats. It also identified the eight labeled/internal-standard mappings that refined the 153-name raw exact overlap to 145 conservative biological names, confirmed the pooled-QC exclusion for ST001521, and recommended ST000292 plus ST001789 as the stronger reserve. Those corrections are incorporated here and in the machine-readable provenance record.

## Reproducibility record

- Selection date: 2026-08-10
- Primary cache retrieval: 2026-08-10T11:44:11Z
- Cache size: 34,717,062 bytes across ten study JSON files plus the full RefMet classification JSON
- Integrity: SHA-256 per file in [provenance.json](../data/provenance.json)
- License: both primary studies report CC BY 4.0 in the public summary endpoint
- Access: no login or controlled-access data is required
