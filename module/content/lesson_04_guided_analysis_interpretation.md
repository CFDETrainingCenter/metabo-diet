# Lesson 4 - Guided analysis and biological interpretation

**Estimated time:** 40 minutes  
**Bloom levels:** Apply, analyze, evaluate  
**Module objectives addressed:** LO2, LO4

## Learning objectives

By the end of this lesson, you will be able to:

1. Retrieve and validate study summaries, factors, analyses, metabolites, and data through the Metabolomics Workbench REST API.
2. Apply the reviewed crosswalk without losing study, analysis, sample, specimen, or timepoint provenance.
3. Quantify name-level overlap and summarize chemical classes with explicit eligibility rules.
4. Run and interpret principal component analysis within each study as an exploratory diagnostic.
5. Separate observations supported by the output from explanations that remain biologically or technically ambiguous.

## Lesson map

| Activity | Minutes |
|---|---:|
| Configure, retrieve, and validate | 8 |
| Join and audit the crosswalk | 6 |
| Overlap and class summaries | 7 |
| Within-study PCA | 9 |
| Interpretation challenge | 7 |
| Knowledge check | 3 |

> **In the notebook (NB-L4):** Run `NB-L4-CLASS`, `NB-L4-PCA-DIET`, and `NB-L4-PCA-EXERCISE` in order. Complete both learner-edit cells and the four-sentence note before reading the sample answer. The same PCA figures appear in the appendix.

## 1. Locked case-study configuration

The release configuration is:

```text
DIET_ACCESSION = ST001521
EXERCISE_ACCESSION = ST003348
```

Keep the variable names in code and prose even though the accessions are now locked. This preserves the proposal's one-cell substitution design and makes a fallback pair possible.

### Diet case: `ST001521`

Metabolomics Workbench describes this FARMM study as a longitudinal human feeding study with three diet groups and plasma metabolomics. The study record reports 30 volunteers and five biological collection times. The factor response contains 160 rows: 150 participant-timepoint rows plus 10 pooled quality-control rows labeled `QPP...` with diet, sex, and time recorded as `NA`. Four analysis records cover different chromatography and ion-mode combinations and report unitless peak areas.

`ST001521` is not a simple three-arm diet trial. Participants also underwent antibiotic and polyethylene glycol procedures during the time course; the vegan group continued its usual diet as outpatients, while 20 omnivores were randomized to an omnivore diet or exclusive enteral nutrition in an inpatient unit. Changes across days therefore cannot be attributed to diet alone without a design-appropriate model and assumptions.

### Exercise case: `ST003348`

Metabolomics Workbench describes an endurance exercise study of race walkers with 76 samples: 19 athletes at four timepoints. The project record defines `REST` as pre-exercise, `STAT` as immediately post-exercise, `REC3` as 3 hours into recovery, and `REC22` as 22 hours post-exercise. Two analysis records cover reversed-phase positive- and negative-ion modes and report peak area.

The factors endpoint uses the broad sample-source label `blood`, while the collection record specifies `Blood (serum)` and describes clotting and serum preparation. Keep `blood` as the submitted factor value, use serum as the more specific matrix supported by the collection record, and cite both sources.

### Cross-study compatibility decision

The diet study uses plasma; the exercise study uses serum. Their time axes also represent different processes: study days spanning feeding and microbiota-depletion procedures versus minutes to hours after an endurance exercise bout. Treat both domains as partially comparable for broad discovery and not directly comparable for a pooled quantitative effect.

## 2. Open the notebook safely

Open `module/notebooks/metabo_diet_harmonization.ipynb` in a fresh **Python 3 (Metabo-Diet)** kernel. Complete `NB-SETUP` and run `NB-L1` through `NB-L3` before starting this lesson; the Lesson 4 cells depend on those validated objects. Then follow this order:

1. Run `NB-L4-CLASS` and confirm that the class counts sum to 145.
2. Run `NB-L4-PCA-DIET` and record its sample/feature counts and explained variance.
3. Run `NB-L4-PCA-EXERCISE` and record the same fields without comparing coordinate values across models.
4. Complete the shared-class and sensitivity learner-edit cells.
5. Write the bounded interpretation before revealing the sample answer.

Confirm the configuration cell shows the accessions above. The data provenance manifest at `module/data/provenance.json` should also provide:

- Selected analysis IDs or the rule used to include multiple analyses.
- Retrieval date and API base URL.
- Cached-file paths and checksums.
- Dependency versions.
- Crosswalk version.

Do not continue if the displayed accession differs from `module/data/provenance.json`.

### Live retrieval and cached fallback

For each accession, the notebook requests:

- `summary`
- `factors`
- `analysis`
- `metabolites`
- `data`

The release notebook defaults to the validated cache so every learner receives a deterministic run. Set `METABO_DIET_LIVE=1` to attempt live retrieval first. The live path falls back endpoint-by-endpoint only after recording:

- The failed endpoint and status.
- The cached retrieval timestamp.
- A checksum match.
- A visible source entry of `validated cache` in the input source log.

Cached data keep the lesson runnable; they do not establish current public availability. Record the outage and re-verify access later.

## 3. Validate before analyzing

An HTTP `200` is not sufficient validation. The notebook's audit table should answer:

1. Did every response parse in the expected format?
2. Does each record contain the requested study or analysis identifier?
3. Are sample identifiers unique at the expected level?
4. How many biological, pooled QC, blank, and unknown rows are present?
5. Do factor counts agree with the documented repeated-measures structure?
6. Are all matrix columns represented in the factor table?
7. Are metabolite labels unique after applying the chosen feature key?
8. Are units and analytical modes explicit?

### Expected structural checks for this release

These are validation targets, not biological results:

| Check | `ST001521` | `ST003348` |
|---|---:|---:|
| Factor rows | 160 | 76 |
| Biological participant-timepoint rows expected | 150 | 76 |
| Pooled `QPP...` rows expected | 10 | 0 identified from the factor table |
| Biological participants described | 30 | 19 |
| Biological timepoints per participant | 5 | 4 |
| Analysis records | 4 | 2 |
| Matrix | Plasma | Serum, supported by collection metadata |

If the live response differs, stop and inspect. A repository revision may be legitimate, but silently forcing current data to match old expectations defeats provenance tracking.

## 4. Separate analytical roles before filtering

Create a `sample_role` field with evidence. At minimum:

- `biological`
- `pooled_qc`
- `blank`
- `technical_standard`
- `unknown`

For `ST001521`, rows with local identifiers beginning `QPP` and missing diet, sex, and time are pooled QC candidates supported by the record. The notebook should keep them for assay diagnostics but exclude them from biological PCA and participant counts. Never discard QC rows before confirming their role; their clustering and drift can reveal analytical problems.

For `ST003348`, identifiers encode an apparent participant and time suffix, but the notebook must derive repeated-measures links using a documented rule and validate the expected 19 by 4 structure. A string pattern is a parsing hypothesis until confirmed against study metadata.

## 5. Join the reviewed crosswalk

Join within study and analysis first, using the most specific stable keys available. Avoid joining solely on submitted metabolite name because:

- The same name may occur in multiple analytical modes.
- Different features can map to the same broad RefMet name.
- Duplicate labels can create a many-to-many join and inflate rows.

After each join, report:

- Rows before and after.
- Matched, unmatched, and multiply matched source features.
- Duplicate join keys.
- Counts by mapping status and annotation resolution.
- Exclusions and reasons.

The learner should be able to trace any harmonized value back to accession, analysis, sample, and original feature.

> **Stop condition:** If a join unexpectedly increases the number of measurement rows, diagnose the key cardinality before continuing. Do not remove duplicates merely to restore the expected size.

## 6. Worked example: metabolite overlap as a defined set operation

An overlap count is meaningful only after defining the eligible universe and key.

The current build found **153 shared nonblank exact RefMet strings before artifact and eligibility exclusions**. Eight `ST003348` isotope-labeled or internal-standard rows mapped to ordinary RefMet labels; excluding those nonbiological rows yielded a **conservative biological overlap of 145**. Treat both numbers as versioned audit results: 153 tests the raw string-intersection step, while 145 tests the stated artifact filter. Neither is a shared-response count. The accepted overlap can change when:

- Internal standards, contaminants, or artifacts are excluded.
- Duplicate features mapping to the same RefMet name are collapsed.
- Annotation-resolution rules are applied.
- Review-required mappings are removed.
- Analysis modes are combined or kept separate.
- A repository or RefMet record is revised.

### Required overlap report

Report a flow rather than one unexplained number:

1. Distinct submitted labels in each study.
2. Nonblank RefMet results.
3. Reviewed and accepted RefMet mappings.
4. Eligible mappings after artifact and feature-role rules.
5. Unique exact-name keys in each study.
6. Intersection size.
7. Diet-only and exercise-only sizes.
8. Duplicate-to-key counts.
9. Isotope/internal-standard exclusions, expected to reduce 153 to 145 in the audited build.

Also report the denominator used for percentages. `Intersection / diet set`, `intersection / exercise set`, and Jaccard similarity answer different questions.

### What overlap does and does not mean

A shared standardized name shows that both studies reported an eligible feature under the selected key. It does not show:

- Equal concentration.
- Equal detectability or coverage.
- Equal identification confidence.
- Equal structural resolution.
- A shared intervention response.
- A pathway effect.

Absence from one study can reflect biological absence, platform coverage, annotation, filtering, ionization, detection limit, or reporting choices.

## 7. Class-level summaries

RefMet classifications can support a broad view of the reviewed shared-name set. Use counts or proportions of eligible unique names, not pooled peak areas. State how unclassified records and multi-mapped features are handled.

A defensible summary might say:

> The 145-name conservative overlap has RefMet class annotations for all 145 names. Amino acids and peptides, fatty acids, and fatty esters are the three largest classes in this shared-name set. These counts describe nomenclature coverage of the overlap and should not be interpreted as class abundance in plasma or serum.

### Accessible description of the class-summary figure

One horizontal bar chart shows the 12 most frequent RefMet main classes among the 145 conservative shared names. The leading bars are amino acids and peptides (37), fatty acids (25), fatty esters (15), purines (11), bile acids (8), and pyridine alkaloids (7); the remaining six displayed classes have four or fewer names each. The x-axis is `Conservative shared RefMet names`. Bars are counts of standardized names, not metabolite concentrations or biological class abundance, and 24 names in less frequent classes are not shown in this top-12 view.

## 8. Principal component analysis: within each study

PCA summarizes directions of variation in a numeric matrix. It is sensitive to scale, skew, missingness, outliers, preprocessing, and feature selection. The notebook should create separate PCA models for each study or compatible analysis block.

The notebook carries out the implementation for you. You are not expected to understand every line of code. Focus on which samples and features enter each PCA, how missing and large values are handled, and whether the interpretation stays within the study design.

### Pre-PCA audit

For each PCA, record:

- Included study, analysis modes, samples, and features.
- Biological versus QC sample roles.
- Missingness threshold and handling.
- Zero and near-zero variance removal.
- Transformation, centering, and scaling.
- Treatment of duplicate RefMet mappings.
- Explained variance for displayed components.

Use transformations only when compatible with the measurement scale and documented. Do not add an arbitrary pseudocount without recording its value and evaluating sensitivity. Fit imputation and scaling rules within the analyzed study; a combined fit across studies can transmit study-specific scale information.

### Diet-study PCA

Color or facet the biological samples by diet and shape them by timepoint, while keeping the concurrent antibiotic/PEG intervention visible in the caption or an annotated time axis. Display pooled QC samples separately if they are used diagnostically. A visible time pattern is not automatically a diet effect.

Questions to ask:

- Do pooled QC samples cluster more tightly than biological samples?
- Are extreme points associated with missingness or a specific analytical mode?
- Is variation aligned with time, diet, sex, participant, or batch metadata?
- Does the pattern change after reasonable sensitivity checks?
- Can diet be separated from setting and assignment differences for all groups? Not without additional assumptions.

### Exercise-study PCA

Color samples by `REST`, `STAT`, `REC3`, and `REC22`, and connect repeated observations from the same athlete only after participant linkage is validated. The four labels describe an acute and recovery trajectory; they are not interchangeable with diet-study days.

Questions to ask:

- Is any separation ordered along the known recovery sequence?
- Are trajectories consistent across athletes or driven by a subset?
- Do positive- and negative-ion analysis blocks behave differently?
- Could collection clock time, fasting status, or processing contribute?

### Why this module omits a combined PCA

Study identity is perfectly associated with diet-versus-exercise context and also differs in matrix, platform implementation, units, laboratory, population, and protocol. A PCA of the stacked raw matrices would primarily encode those inseparable study-of-origin differences. This module therefore omits that plot and teaches the confounding problem through the metadata audit plus two independent within-study PCA figures whose numeric axes are not compared.

### Accessible descriptions of the PCA figures

The diet figure is titled `ST001521 / AN002534: within-study PCA` and contains 150 biological plasma samples; the 10 pooled QPP samples are excluded. Color represents Western, Vegan, or Modulen, and marker shape represents Baseline, Day 5, Day 9, Day 12, or Day 15. PC1 explains 34.4% and PC2 explains 11.6% of variance.

The exercise figure is titled `ST003348 / AN005483: within-study PCA` and contains 76 serum samples. Color represents Rest, Immediate post, 3 h recovery, or 22 h recovery; the plot does not draw participant-trajectory lines. PC1 explains 16.1% and PC2 explains 8.4% of variance. The two PCA models have independent coordinate systems, so point distances and axis values must not be compared between figures.

## 9. Hands-on notebook activity

### Part A - Retrieval audit

1. Review `NB-L1` and run the `NB-L2` retrieval cells if they have not already been executed in this fresh kernel.
2. Confirm both locked accessions in the output.
3. Record live or cached status for each endpoint.
4. Compare the structural audit with the expected checks above.
5. Investigate any discrepancy before continuing.

### Part B - Sample-role and time audit

1. In `NB-L2`, identify the 10 `QPP...` rows in `ST001521` and verify that they are not counted as participants.
2. Create explicit physiological labels for the exercise study: pre-exercise, immediate post-exercise, 3-hour recovery, and 22-hour recovery.
3. Preserve the diet-study days and annotate the antibiotic/PEG interval rather than mapping them to the exercise labels.
4. Record plasma versus serum as a partial compatibility decision.

### Part C - Crosswalk and overlap

1. In `NB-L3-CROSSWALK`, join the reviewed crosswalk using accession, analysis, and source-feature keys.
2. Inspect the join-cardinality report.
3. Reproduce the intermediate 153 shared nonblank exact RefMet strings if the same retrieval and preliminary rules are in use.
4. Apply the nonbiological artifact rule and verify that eight `ST003348` isotope/internal-standard rows are excluded, producing 145 conservative biological overlaps in the audited build.
5. Apply any additional mapping-status and annotation-resolution eligibility rules and record every exclusion count.
6. In `NB-L4-CLASS`, produce the set summary and class-count figure.

If 153 and then 145 are not reproduced, do not tune filters merely to make them appear. Check versions, retrieved analyses, missing-value definitions, isotope/internal-standard rules, duplicate collapse, and crosswalk state; document the reason for any legitimate difference.

### Part D - PCA and sensitivity

1. Run `NB-L4-PCA-DIET` and `NB-L4-PCA-EXERCISE` separately.
2. Confirm QC samples are excluded from biological inference but available for assay diagnostics.
3. State the preprocessing choices in plain language.
4. Repeat one reasonable sensitivity analysis, such as changing the missingness threshold or analyzing ion modes separately.
5. Compare which observations persist and which change.

### Part E - Write a bounded interpretation

Use this four-sentence scaffold:

1. **Observation:** "Within `ST...`, the exploratory output shows..."
2. **Context:** "The relevant design and phenotype metadata indicate..."
3. **Alternative explanations:** "This pattern could also reflect..."
4. **Boundary:** "These data do not establish..."

Avoid the verbs `proves`, `causes`, `confirms`, or `demonstrates` unless the design and analysis truly support them.

## 10. Optional extension: MetENP

MetENP can be introduced as an optional pathway and enrichment resource supported through CFDE. Export only reviewed identifiers in a format the tool documents, retain the background universe, and record tool and database versions. Pathway output inherits all upstream identification and coverage limitations. It is hypothesis-generating, not validation of a diet-versus-exercise mechanism.

## 11. Interpretation challenge

For each statement, mark `supported`, `partially supported`, or `unsupported`, then revise it.

1. "The studies share 153 biologically identical metabolites."
2. "The diet study contains 160 participants."
3. "The exercise samples are blood, so they are the same matrix as diet plasma."
4. "PCA separates exercise timepoints, proving the race walk caused every measured change."
5. "An apparent class difference may reflect assay coverage as well as biology."

Suggested revisions are in the answer key.

## 12. Analysis boundaries

- Exclude pooled QC samples from biological sample counts and participant-level inference.
- Preserve plasma versus serum; do not call both simply blood in the analysis matrix.
- Diet-study time includes microbiota-depletion procedures; it is not a pure duration-of-diet axis.
- Analyze repeated measures with participant structure; do not treat 150 or 76 rows as independent people.
- A raw exact-name overlap is an intermediate audit value until artifacts, ambiguity, and duplicates are addressed.
- PCA is exploratory and does not assign causes to components.
- Do not compare coordinates or loadings from separately fit PCAs as if they shared a coordinate system.
- Do not quantitatively pool the two studies in this module.
- Report sensitivity to preprocessing and missingness choices.
- Phrase class summaries as coverage of reported eligible names, not class concentration.

## 13. Knowledge check

**KC4-01.** Why should the `QPP...` rows in `ST001521` not be included in biological PCA?

A. They are pooled quality-control samples rather than participant-timepoint observations.  
B. PCA cannot use plasma.  
C. Their identifiers contain letters.  
D. Quality-control samples must always be deleted from the repository.

**KC4-02.** What does the intermediate overlap of 153 represent?

A. 153 metabolites proven to respond to both diet and exercise.  
B. 153 shared nonblank exact RefMet strings before artifact and eligibility exclusions under a specific build.  
C. 153 directly comparable concentrations.  
D. A permanent repository constant.

**KC4-03.** Which PCA interpretation is defensible?

A. A separate within-study PCA is an exploratory view whose pattern must be interpreted with preprocessing, repeated measures, and design context.  
B. Separation between the two studies proves a diet-versus-exercise mechanism.  
C. Scaling removes plasma-versus-serum differences.  
D. PCA automatically corrects batch effects.

## What the analysis can support

Validate each step before interpreting the result. A count can be reproducible and still support only a narrow claim, so use the study metadata to state that claim clearly.

## Primary sources and first-party documentation

1. Metabolomics Workbench. [ST001521 study record](https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?StudyID=ST001521) and [REST summary](https://www.metabolomicsworkbench.org/rest/study/study_id/ST001521/summary). Accessed August 10, 2026.
2. Metabolomics Workbench. [ST003348 study record](https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?StudyID=ST003348) and [REST summary](https://www.metabolomicsworkbench.org/rest/study/study_id/ST003348/summary). Accessed August 10, 2026.
3. Metabolomics Workbench. [REST Service, version 1.2](https://www.metabolomicsworkbench.org/tools/mw_rest.php). Updated July 22, 2025; accessed August 10, 2026.
4. Metabolomics Workbench. [RefMet database](https://www.metabolomicsworkbench.org/databases/refmet/index.php). Accessed August 10, 2026.
5. Jolliffe IT, Cadima J. [Principal component analysis: a review and recent developments](https://doi.org/10.1098/rsta.2015.0202). *Philosophical Transactions of the Royal Society A*. 2016;374:20150202.
6. Metabolomics Workbench. [MetENP demonstration and documentation](https://www.metabolomicsworkbench.org/data/MW-MetENP-demo.pdf). Accessed August 10, 2026.
