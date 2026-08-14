# Lesson 1 - Why phenotype-to-metabolome harmonization matters

**Estimated time:** 20 minutes  
**Bloom levels:** Remember, understand  
**Module objectives addressed:** LO1, LO2, LO5

## Learning objectives

By the end of this lesson, you will be able to:

1. Explain why metabolite measurements are not interpretable without study-design, specimen, timepoint, and phenotype context.
2. Distinguish structural harmonization from statistical pooling.
3. Recognize open, registration- or agreement-gated, and controlled-compute access patterns.
4. Locate the two configurable Metabolomics Workbench case studies used throughout the module.

## Lesson map

| Activity | Minutes |
|---|---:|
| Pretest, additional assessment time | 5 |
| The phenotype-to-metabolome problem | 5 |
| The Metabo-Diet workflow and access patterns | 5 |
| Worked triage activity | 7 |
| Knowledge check and reflection | 3 |
| **Instructional subtotal, excluding pretest** | **20** |
| **Learner time with pretest** | **25** |

> **Notebook connection - `NB-L1`.** First complete the pretest. Then open `module/notebooks/metabo_diet_harmonization.ipynb`, finish `NB-SETUP`, and go to **Lesson 1 - Why harmonization matters (`NB-L1`)**. Run the environment and configuration cells, confirm `ST001521`, `ST003348`, and the retrieval mode, then pause and record why the matrices must remain separate. Do not begin `NB-L2` until this lesson is complete.

## Before you begin

Complete the pretest before opening the answer key. Its purpose is to establish a baseline, not to determine eligibility. Record your confidence separately from correctness; confidence and knowledge can change at different rates.

This module keeps two configuration labels so a study pair can be replaced without rewriting the workflow. The release pair is now locked:

- `DIET_ACCESSION = ST001521`: the public, human FARMM diet-anchored plasma study.
- `EXERCISE_ACCESSION = ST003348`: the public, human race-walking exercise-anchored serum study.

The variable names are not accession numbers and must never be sent to the REST API literally. The notebook configuration cell resolves them to the values above. Before teaching, the instructor confirms that both studies remain public and that the release manifest still matches the retrieved records.

## 1. A metabolite value is an observation in context

Imagine two rows labeled `glucose`. One value was measured in fasting plasma before a controlled diet; the other was measured in serum immediately after a maximal exercise bout. The analyte labels look compatible, but the observations are not interchangeable.

At least five layers shape what a metabolite value means:

1. **Biological question:** What exposure, intervention, or phenotype anchors the study?
2. **Sampling context:** Which specimen was collected, from whom, and under what conditions?
3. **Time meaning:** Does a label such as `post` mean after a meal, after weeks of feeding, immediately after exercise, or during recovery?
4. **Analytical process:** Which platform, method, batch structure, preprocessing, and units produced the value?
5. **Data representation:** How are samples, factors, metabolites, missing values, and identifiers encoded?

Harmonization makes these layers explicit. It does not erase them.

> **Core guardrail:** Structural harmonization can make records easier to compare. It does not, by itself, make participants, interventions, specimens, timepoints, platforms, units, or quantitative values exchangeable.

This distinction protects against a tempting but invalid workflow: matching metabolite names, stacking two intensity matrices, and interpreting the first principal component as a diet-versus-exercise biological effect. If study and phenotype are perfectly confounded, the observed separation may arise from platform, sample handling, units, batch, population, or other design differences. No statistical technique can identify a unique biological cause from that contrast alone.

## 2. What harmonization can accomplish

The Metabo-Diet workflow supports several defensible tasks:

- Compare how studies represent intervention, specimen, timepoint, and phenotype variables.
- Standardize metabolite labels while preserving the submitted names and mapping evidence.
- Identify metabolites reported in both studies at a compatible annotation level.
- Describe where metadata concepts align, partially align, or do not align.
- Conduct exploratory analyses within each study using study-appropriate preprocessing.
- Compare patterns descriptively when the measurement and design context supports the comparison.
- Document unresolved mappings and incompatibilities for future reuse.

It does **not** automatically support:

- Direct comparison of raw or normalized intensities across platforms.
- Treating `post` timepoints as equivalent without physiological definitions.
- Treating plasma and serum as the same specimen.
- Treating a metabolite class label as a uniquely identified molecular structure.
- Inferring that an exposure caused a cross-study difference.
- Increasing effective sample size by concatenating unrelated cohorts.

The right output is sometimes a well-documented decision **not** to combine a field or analyte. A flagged incompatibility is a successful harmonization result.

## 3. The resources in this module

### Metabolomics Workbench and NMDR

The Metabolomics Workbench hosts the National Metabolomics Data Repository (NMDR). Its REST service can return study summaries, factors, analyses, metabolite annotations, measurement tables, and mwTab records. Public studies are the hands-on substrate for this module. The paired accessions are configurable so the module can survive a study revision or replacement without rewriting every lesson.

The mwTab representation organizes information into blocks. Depending on the record, these include study, subject, sample-factor, collection, sample-preparation, chromatography, mass-spectrometry or NMR, and metabolite-data content. The exact fields present vary across deposits. That variation is not an inconvenience to hide; it is evidence to inspect.

### RefMet

RefMet provides an analytical-chemistry-centered reference nomenclature for metabolite structures and metabolite species. It is especially useful when deposited names differ in punctuation, synonym choice, or lipid notation. A RefMet match is evidence about nomenclature, not proof that two measurement features have identical analytical specificity. Lesson 3 develops this distinction.

### MoTrPAC and Nutrition for Precision Health

The Molecular Transducers of Physical Activity Consortium (MoTrPAC) and Nutrition for Precision Health (NPH), powered by All of Us, appear as transfer cases rather than learner data dependencies. Their study designs show how exercise and diet phenotypes can be captured at consortium scale.

Access status is a property of a **specific dataset, release, and intended action**, not a permanent label attached to an entire program. Current MoTrPAC documentation states that public releases can be accessed without an account, while restricted or embargoed data can require authentication and a data-use agreement. NPH documentation states that data are stored and analyzed in the All of Us Researcher Workbench, which is available to approved researchers. Requirements can change, so Lesson 5 teaches verification from current first-party documentation.

## 4. Three access patterns

Use the following patterns as planning aids, not legal categories:

| Pattern | Typical learner experience | Questions to verify |
|---|---|---|
| Open public retrieval | A public study can be viewed or retrieved without personal credentials. | Is this exact accession public? Is there an embargo? Are redistribution terms stated? |
| Account, agreement, or approval gated | Access requires identity, an account, acceptance of terms, a DUA, or review. | Who may apply? What uses and exports are allowed? How long might approval take? |
| Controlled compute | Participant-level data remain inside an approved environment; only permitted outputs leave it. | What tier is needed? What institutional and training requirements apply? What disclosure review or export rules govern outputs? |

One resource may expose different datasets under different patterns. A public landing page does not prove that the desired data are public. Conversely, the existence of restricted data does not prove that all releases require registration.

### Accessible description of the access-pattern figure

Picture three workspaces arranged from left to right. The first has an open door and a download arrow. The second has a sign-in badge and an agreement document. The third has data locked inside a cloud workspace, with only a reviewed summary moving outward. A study can move between workspaces as its release status changes, so a calendar and version label appear below all three.

## 5. Worked example: a 90-second evidence triage

This example demonstrates the reasoning process for the locked study pair while reserving detailed study claims for the dated records examined in Lesson 2.

**Claim to evaluate:** "The diet and exercise datasets are both on Metabolomics Workbench, so their metabolite values can be pooled."

1. **Repository check:** Both are intended to be public MW studies. This supports a common retrieval mechanism, not common measurement properties.
2. **Identifier check:** Submitted names may be mapped to RefMet. This supports a documented analyte-name bridge, subject to annotation resolution.
3. **Specimen check:** Compare the sample source and collection protocol. Plasma versus serum, or fasting versus fed, can alter interpretation.
4. **Timepoint check:** Define each timepoint physiologically. A shared word such as `baseline` is insufficient.
5. **Platform and scale check:** Determine targeted versus untargeted analysis, chromatography, ion mode, quantification type, units, normalization, and batch structure.
6. **Design check:** Ask whether study and phenotype are separable. With one diet study and one exercise study, study membership is confounded with phenotype anchor.

**Decision:** Reject automatic quantitative pooling. Proceed with metadata comparison, identifier crosswalking, overlap description, and within-study exploratory analysis. Consider cross-study quantitative modeling only if a later, explicit compatibility assessment and design justify it.

## 6. Hands-on activity: open the evidence trail

Open the learner cohort-comparison worksheet and complete the first four fields for both configured accessions.

1. Record `DIET_ACCESSION = ST001521` and `EXERCISE_ACCESSION = ST003348` from the release manifest.
2. For each accession, record the study landing-page URL and REST summary URL.
3. Record the date and time you verified public availability.
4. Label the access evidence as `verified`, `not verified`, or `conflicting`.
5. Write one sentence describing what public access does and does not imply about scientific comparability.

**Stop condition:** If either configured accession differs from the release manifest or its public release cannot be verified, do not substitute another study silently. Continue with the versioned cache if available, mark the source as cached, and report the discrepancy to the instructor.

## 7. Interpretation guardrails

- Repository co-location supports common discovery and retrieval, not common measurement.
- A RefMet match supports a name-level bridge, not a common concentration or identification level.
- A broad specimen category must not erase plasma-versus-serum or other matrix differences.
- Physiological time must be defined before labels such as `baseline` or `post` are aligned.
- Public access does not establish scientific compatibility.
- Study-confounded separation must not be labeled a diet-versus-exercise effect.
- An unresolved or incompatible decision is a valid harmonization result.

## 8. Knowledge check

Answer before viewing the rationale in `module/assessments/knowledge_checks.json`.

**KC1-01.** Two studies report a RefMet match for the same metabolite. Which conclusion is justified?

A. Their quantitative values may be concatenated without further checks.  
B. Their submitted labels have a shared standardized-name candidate; analytical specificity and context still require review.  
C. The metabolite was confirmed by an authentic standard in both studies.  
D. Any between-study difference is biological.

**KC1-02.** Which evidence establishes the access pattern for a candidate dataset?

A. The reputation of the research consortium.  
B. The access tier remembered from a prior release.  
C. Current first-party documentation and a dated check of the exact dataset and intended action.  
D. The fact that a publication cites the dataset.

**KC1-03.** When phenotype anchor and study are perfectly confounded, what is the safest interpretation of a PCA separation between studies?

A. It proves diet and exercise have different metabolic effects.  
B. It proves the exercise cohort is more heterogeneous.  
C. It is exploratory separation that may reflect biological, technical, or design differences that cannot be uniquely attributed.  
D. It validates quantitative pooling.

## 9. Reflection

Complete this sentence in one or two lines:

> A cross-study comparison would be useful for my work if it helped me ________, but it would become misleading if I ________.

Keep the response. You will revisit it after the analysis lesson.

## Take-home message

Harmonization is disciplined preservation of meaning across representations. It helps you discover what is comparable, what is only partially comparable, and what should remain separate. The rest of this module turns that principle into an auditable workflow.

## Primary sources and first-party documentation

1. Metabolomics Workbench. [REST Service, version 1.2](https://www.metabolomicsworkbench.org/tools/mw_rest.php). Updated July 22, 2025; accessed August 10, 2026.
2. Metabolomics Workbench. [mwTab file specification and repository tutorials](https://www.metabolomicsworkbench.org/data/tutorials.php). Accessed August 10, 2026.
3. Sud M, Fahy E, Cotter D, et al. [Metabolomics Workbench: an international repository for metabolomics data and metadata, metabolite standards, protocols, tutorials and training, and analysis tools](https://academic.oup.com/nar/article/44/D1/D463/2502588). *Nucleic Acids Research*. 2016;44(D1):D463-D470.
4. Fahy E, Subramaniam S. [RefMet: a reference nomenclature for metabolomics](https://doi.org/10.1038/s41592-020-01009-y). *Nature Methods*. 2020;17:1173-1174.
5. MoTrPAC. [Data access FAQ](https://www.motrpac-data.org/knowledge-center/project-overview/faq) and [Data Hub documentation](https://www.motrpac-data.org/knowledge-center/dissemination/data-access/data-hub). Accessed August 10, 2026.
6. NIH Common Fund. [Nutrition for Precision Health frequently asked questions](https://commonfund.nih.gov/nutritionforprecisionhealth/frequently-asked-questions). Accessed August 10, 2026.
7. Wilkinson MD, Dumontier M, Aalbersberg IJ, et al. [The FAIR Guiding Principles for scientific data management and stewardship](https://doi.org/10.1038/sdata.2016.18). *Scientific Data*. 2016;3:160018.
