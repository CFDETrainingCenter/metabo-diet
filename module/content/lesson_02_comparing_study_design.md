# Lesson 2 - Comparing study design and phenotype capture

**Estimated time:** 30 minutes  
**Bloom levels:** Understand, analyze  
**Module objectives addressed:** LO1, LO2

## Learning objectives

By the end of this lesson, you will be able to:

1. Extract design, specimen, timepoint, phenotype, and provenance evidence from two Metabolomics Workbench records.
2. Classify fields as directly comparable, partially comparable, or not comparable for a stated purpose.
3. Explain how diet and exercise phenotypes acquire meaning from protocol details.
4. Use MoTrPAC and NPH as design references without treating their data as module dependencies.

## Lesson map

| Activity | Minutes |
|---|---:|
| From labels to estimands | 6 |
| Five-layer study comparison | 8 |
| Consortium design references | 4 |
| Cohort-comparison worksheet | 9 |
| Knowledge check | 3 |

> **In the notebook (NB-L2):** Run the source, endpoint-size, biological-sample, and timepoint cells in order. Use the learner-edit cell to inspect one study, then enter the results in Sections 3, 5, 6, and 9 of the cohort-comparison worksheet.

## 1. Begin with the question, not the column name

A variable is comparable only relative to a purpose. Age in years may be sufficiently comparable for a descriptive cohort table but insufficient if one study reports exact age and another reports broad, top-coded categories. A `post` sample may be suitable for identifying that both studies collected after an intervention but unsuitable for modeling a common acute-response time.

Before aligning columns, write the target question as an **estimand sketch**:

- **Population:** Who is represented?
- **Exposure or intervention:** What contrast is of interest?
- **Outcome:** Which metabolite measure or derived quantity is being interpreted?
- **Time:** At what biological interval is the outcome defined?
- **Summary:** Is the target a within-person change, a group mean, a rank, an overlap count, or something else?

For this module, the safe default target is descriptive:

> Describe which metabolite identities and broad chemical classes are represented in both studies, while preserving differences in population, specimen, timepoint, platform, and measurement scale.

That target supports crosswalking and overlap summaries. It does not require the two cohorts to estimate the same intervention effect.

## 2. The five-layer comparison

Use the cohort-comparison worksheet to collect evidence at five layers. For every entry, capture the source location and avoid filling a blank by inference.

### Layer A - Study design and population

Record:

- Observational versus interventional design.
- Parallel, crossover, repeated-measures, or other structure.
- Recruitment setting and inclusion or exclusion criteria.
- Unit of assignment and unit of analysis.
- Number of participants and samples, keeping those counts distinct.
- Randomization, masking, washout, run-in, or familiarization when applicable.
- Attrition and missing visits if reported.

The number of samples is not the number of independent participants. Repeated samples from one participant are correlated. If participant identifiers are absent or cannot be linked reliably, within-person analyses may be impossible even when multiple timepoints exist.

### Layer B - Phenotype anchor

For a diet-anchored study, inspect:

- Food or dietary pattern definition.
- Controlled feeding versus advice or free-living exposure.
- Energy balance, meal timing, compliance measures, and washout.
- Fasting state and any test-meal challenge.
- Dietary assessment method and its reference period.

For an exercise-anchored study, inspect:

- Modality, intensity, duration, dose, and supervision.
- Acute bout versus chronic training.
- Fitness or performance measures.
- Pre-exercise standardization, recent activity restrictions, and feeding state.
- Recovery intervals and workload scaling.

The words `diet` and `exercise` are topic labels, not exposure definitions. The worksheet should contain protocol-level details sufficient for another analyst to understand the contrast.

### Layer C - Specimen and pre-analytical context

Record:

- Biospecimen, matrix, and anatomical source.
- Collection tube or anticoagulant when relevant.
- Fasting or fed status.
- Collection clock time if available.
- Processing delay, centrifugation, aliquoting, and storage temperature.
- Freeze-thaw information if available.

Plasma and serum are both blood-derived, but they are not identical matrices. Treat them as partially comparable at most, and only for a purpose that tolerates the distinction. A field left unreported is `not reported`, not `same`.

### Layer D - Time semantics

Translate each deposited time label into a physiological definition. Use a canonical structure such as:

`anchor | offset | duration/unit | state | visit/order`

Examples:

- `exercise_bout_end | +0 | min | acute_response | visit_2`
- `exercise_bout_end | +180 | min | recovery | visit_2`
- `diet_period_start | +14 | day | end_of_feeding_period | period_1`
- `test_meal_start | -10 | min | fasting_baseline | visit_1`

Do not translate `post` without evidence. When the necessary reference point or offset is absent, flag the timepoint as unresolved.

### Layer E - Assay and metadata provenance

Record:

- Analysis type, platform, chromatography, ion mode, and targeted or untargeted status.
- Quantification or abundance scale and units.
- Normalization, transformation, blank correction, batch correction, and missing-value handling when documented.
- Analysis identifier as well as study accession.
- mwTab block or REST response that supports each field.
- Retrieval date, endpoint, and record version or checksum when available.

A study may contain multiple analyses. Never assume a study-level description applies identically to every analysis table.

## 3. Comparability is a reasoned decision

Use these operational categories:

### Directly comparable

The two fields represent the same construct at sufficient granularity for the stated use, with compatible coding or a transparent lossless conversion.

Example: Both studies report participant age in years at enrollment, and the target is a descriptive median and range. Verify population definitions and disclosure rules before reporting.

### Partially comparable

The fields share a broader construct but differ in granularity, timing, protocol, matrix, or measurement. They may support stratified description or a coarser derived category, but the difference must remain visible.

Example: One study records exact fasting duration; another records only `fasted`. Both can support a high-level fasting-state flag, but not a dose-response model by fasting hours.

### Not comparable

The fields represent different constructs, lack essential provenance, or would require an unsupported assumption.

Example: `post_diet` after a 14-day feeding period and `post_exercise` immediately after an acute bout cannot be treated as one common post-intervention timepoint.

### Not yet assessable

Use this fourth workflow status when evidence is missing or the accession is unresolved. It prevents uncertainty from being silently converted into incompatibility or compatibility. Before analysis, resolve it or explicitly exclude it.

## 4. Worked example with the locked configuration

The following decisions are grounded in the locked Metabolomics Workbench records and remain subject to the dated verification recorded in your worksheet.

| Domain | `DIET_ACCESSION = ST001521` | `EXERCISE_ACCESSION = ST003348` | Decision for this module |
|---|---|---|---|
| Species | Human in summary and subject metadata | Human in summary and subject metadata | Direct at a broad species level |
| Matrix | Blood plasma | Collection metadata specifies blood serum, although factors say `blood` | Partial for discovery; keep plasma and serum distinct |
| Time | Baseline and Days 5, 9, 12, and 15 across feeding plus antibiotic/PEG procedures | REST, immediate post-exercise, 3-hour recovery, and 22-hour recovery | Not a shared time axis |
| Phenotype | Three diet groups in a longitudinal FARMM protocol | Acute endurance race-walking and recovery | Not one common intervention variable |
| Metabolite name | Submitted name and RefMet output | Submitted name and RefMet output | Exact-name comparison possible after Lesson 3 review |
| Intensity | Four LC-MS analyses, unitless peak areas | Two LC-MS analyses, peak area | No cross-study quantitative pooling |

It is fine to mark a row `not yet assessable` when the source does not provide enough information.

## 5. Consortium-scale design references

### MoTrPAC

MoTrPAC's published human protocol describes a multicenter effort designed to characterize molecular responses to acute exercise and exercise training. It includes structured exercise phenotyping and collection of blood, skeletal muscle, and adipose tissue in defined protocol contexts. Use the protocol as an example of how modality, dose, tissue, and time are specified. Do not copy its timepoint labels onto `EXERCISE_ACCESSION`; retrieve the actual MW study protocol and factors.

### Nutrition for Precision Health

NIH describes NPH as a modular study nested in All of Us. Public program documentation distinguishes a larger baseline/test-meal module from free-living and domiciled controlled-feeding modules. Use it as an example of how dietary exposure, test meals, and multimodal measures can be organized. Do not infer that `DIET_ACCESSION` follows the NPH design.

These examples teach **design transfer**: recognize a structure, then verify whether it exists in the target data. They do not supply missing metadata for the MW case studies.

### Accessible description of the comparison diagram

The diagram has two vertical lanes. The diet lane moves from diet assignment to adherence and feeding state, then to specimen collection. The exercise lane moves from exercise modality and dose to exertion and recovery, then to specimen collection. Both lanes feed into a shared assay box, but each arrow carries its own time, specimen, and protocol tags. A dashed line between the lanes is labeled `compare metadata`; there is no arrow labeled `pool values`.

## 6. Hands-on activity: complete the cohort-comparison worksheet

Use `module/templates/cohort_comparison_worksheet_learner.md`.

For the timed course, complete these eight rows in the comparability matrix: species, specific matrix, timepoint, participant count, repeated-measures structure, phenotype anchor, units/scale, and platform/mode. Use the larger worksheet as a project extension after the lesson. A first-time learner is not expected to fill every blank table cell in 30 minutes.

### Step 1 - Resolve and document

For `DIET_ACCESSION = ST001521` and `EXERCISE_ACCESSION = ST003348`, record:

- Resolved study accession and all analysis identifiers used.
- Landing page, REST endpoints, retrieval timestamp, and public-release evidence.
- Publication or protocol link if the record provides one.

If live retrieval fails, use only the versioned cached record supplied with the module, retain the configuration key in every source field, and mark the retrieval source as cached.

### Step 2 - Extract independently

Complete each study column without looking at the other study. This reduces the temptation to translate a field into whatever appears in the comparison study.

For every cell, use one of:

- A value plus source location.
- `NR` for not reported after a documented search.
- `NA` for not applicable.
- `UNRESOLVED` when the accession, analysis selection, or meaning is pending.

### Step 3 - State the purpose

Choose one comparison purpose:

1. Metadata inventory.
2. Metabolite-name overlap.
3. Class-level presence or coverage.
4. Within-study change followed by qualitative pattern comparison.

Do not select pooled quantitative inference for this exercise.

### Step 4 - Classify and justify

For at least eight rows, mark directly comparable, partially comparable, not comparable, or not yet assessable. Write a one-sentence evidence-based justification. A justification should name the relevant similarity or difference rather than merely repeat the category.

### Step 5 - Write an exclusion statement

Complete:

> We will not combine ________ across the two studies because ________. We can still compare ________ by ________.

### Completion criteria

Your worksheet is complete when:

- Every substantive entry has a source or an explicit missingness code.
- Participant and sample counts are not conflated.
- Timepoints have physiological anchors or are flagged.
- Assay identifiers and units are recorded.
- At least one field is intentionally not harmonized.

## 7. Comparison rules

- A shared label is a hypothesis of equivalence, not proof.
- Missing metadata does not mean the protocols were identical.
- Recoding to a broader category trades detail for compatibility; document the loss.
- A crossover period, repeated sample, or technical replicate is not an independent participant.
- Do not use consortium documentation to fill gaps in a different MW study.
- Do not select only the metadata that support a desired integration.
- Record the analysis identifier because one accession may contain multiple assays.

## 8. Knowledge check

**KC2-01.** One study records fasting duration in hours and another records only yes/no fasting status. For a binary fasted-versus-not-fasted description, how should the fields be classified?

A. Directly comparable with no documentation.  
B. Partially comparable after a documented derivation and loss of detail.  
C. Not comparable for any purpose.  
D. Directly comparable for modeling fasting duration.

**KC2-02.** What is the best evidence that two rows at three timepoints come from the same participant?

A. Similar metabolite profiles.  
B. Adjacent sample identifiers.  
C. A documented subject-sample relationship in the deposited metadata.  
D. The word `longitudinal` in the publication title.

**KC2-03.** Why is `post` insufficient as a harmonized timepoint?

A. Post-intervention samples are never useful.  
B. It lacks an intervention anchor, offset, and physiological state.  
C. It cannot appear in mwTab.  
D. It always means immediate recovery.

## Before you start the crosswalk

Decide what you want to compare first. Then extract each record on its own terms and explain why each field is or is not suitable for that purpose. Lesson 3 applies those decisions to the metabolite crosswalk.

## Primary sources and first-party documentation

1. Metabolomics Workbench. [mwTab file specification, version 1.7, and tutorials](https://www.metabolomicsworkbench.org/data/tutorials.php). Accessed August 10, 2026.
2. Metabolomics Workbench. [REST study-context endpoints](https://www.metabolomicsworkbench.org/tools/mw_rest.php). Accessed August 10, 2026.
3. MoTrPAC Study Group, Jakicic JM, Kohrt WM, et al. [Molecular Transducers of Physical Activity Consortium (MoTrPAC): human studies design and protocol](https://doi.org/10.1152/japplphysiol.00102.2024). *Journal of Applied Physiology*. 2024;137(3):473-493.
4. MoTrPAC. [Adult Study Protocol, version 3.0](https://d1yw74buhe0ts0.cloudfront.net/docs/MoTrPAC_Adult_Study_Protocol.pdf). August 22, 2023.
5. NIH Common Fund. [Nutrition for Precision Health](https://commonfund.nih.gov/nutritionforprecisionhealth) and [program FAQ](https://commonfund.nih.gov/nutritionforprecisionhealth/frequently-asked-questions). Accessed August 10, 2026.
6. All of Us Research Program. [Researcher Workbench](https://support.researchallofus.org/hc/en-us/articles/41981123613716-Researcher-Workbench). Accessed August 10, 2026.
