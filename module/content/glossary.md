# Metabo-Diet glossary

Terms are defined for this module's workflow. A repository or program may use a term more narrowly; prefer the source's current data dictionary when applying the workflow elsewhere.

## A

**Access pattern**  
The practical combination of identity, agreement, approval, compute, storage, and output rules governing a specific dataset, release, and action. This module uses open, agreement- or approval-gated, and controlled-compute patterns as planning aids rather than universal legal categories.

**Acute exercise response**  
A physiological or molecular change associated with a single exercise bout. Its interpretation depends on exercise modality, intensity, duration, specimen timing, feeding state, and recovery interval.

**Adduct**  
An ion formed when a molecule associates with or loses a species during ionization, such as a proton or sodium ion. An adduct label is not automatically a unique metabolite identity.

**Analysis identifier**  
A Metabolomics Workbench `AN...` identifier for a particular assay or analysis within a study. A study accession may contain multiple analyses with different chromatography, ion mode, platform, or data tables.

**Annotation resolution**  
The structural detail supported for an analyte, such as a discrete structure, lipid molecular species, lipid sum composition, compound class, or unknown feature.

## B

**Batch effect**  
Systematic variation associated with processing order, laboratory conditions, instrument behavior, reagent lot, or another technical grouping rather than the target biology.

**Biological sample**  
A specimen collected from a participant or experimental unit for biological inference. It is distinct from a pooled QC, blank, or technical standard.

## C

**Cached fallback**  
A versioned copy of a public API response used when live retrieval is unavailable. It must have a retrieval timestamp and integrity evidence and must be labeled as cached when used.

**CFDE**  
Common Fund Data Ecosystem, an NIH Common Fund effort supporting discovery, access, interoperability, and reuse across Common Fund data resources.

**Chemical class**  
A group of compounds sharing a defined chemical relationship. A class-level count of reported metabolites describes dataset coverage, not the total concentration or abundance of that class.

**Clinical or behavioral phenotype**  
A measured characteristic or exposure such as diet pattern, exercise dose, age, disease status, fitness, or adherence. The protocol and timing define what the field means.

**Controlled-compute environment**  
An approved workspace in which governed data remain and analyses run. Only policy-permitted outputs may leave the environment.

**Cross-study pooling**  
Combining participant-level or sample-level quantitative values from separate studies into one analysis as though they formed a common measurement process. Name harmonization alone does not justify pooling.

**Crosswalk**  
A provenance-preserving table linking source fields or analytes to harmonized representations, with transformation rules, evidence, information loss, status, and downstream eligibility.

## D

**Data provenance**  
Evidence describing where a value came from and how it was retrieved, transformed, reviewed, and used. In this module it includes accession, analysis ID, endpoint, timestamp, source label, mapping query, rule version, and decision.

**Data-use agreement (DUA)**  
An agreement defining permitted use, security, confidentiality, sharing, publication, and other responsibilities for a dataset. Requirements are resource- and release-specific.

**Directly comparable**  
Two fields represent the same construct at sufficient granularity for a stated use, with compatible coding or a transparent lossless conversion.

## E

**EEN**  
Exclusive enteral nutrition. In the `ST001521` study summary, an EEN diet is one of the diet conditions. The deposited factor label `Modulen` refers to the named EEN product in the protocol; preserve both the source label and protocol interpretation.

**Eligibility rule**  
An explicit rule determining whether a sample, feature, or mapping participates in a particular analysis. Eligibility may differ for exact-name overlap, class summaries, QC diagnostics, and quantitative analysis.

**Estimand**  
A precise description of the quantity a study or analysis aims to estimate, including population, exposure or intervention, outcome, time, and summary measure.

## F

**FAIR**  
Findable, accessible, interoperable, and reusable. FAIR does not mean unrestricted or free of governance; controlled data can be FAIR when access conditions are clear and machine-actionable.

**FARMM**  
Food And Resulting Microbial Metabolites, the study context represented by `ST001521`. Its longitudinal design includes three diet groups and an antibiotic/polyethylene glycol intervention.

**Fasting state**  
Whether and for how long a participant abstained from caloric intake before collection. A binary `fasted` field and a measured fasting duration are only partially comparable for some purposes.

**Feature**  
An analytical signal, often defined by mass-to-charge ratio, retention time, and other attributes. An untargeted feature may be unidentified or map ambiguously to compounds.

## H

**Harmonization**  
The documented alignment of representations while preserving provenance, incompatibility, and information loss. It improves structural comparability; it does not guarantee statistical exchangeability.

**HMDB ID**  
An identifier in the Human Metabolome Database. It can provide a useful cross-reference but is not interchangeable with a RefMet name or proof of an experimental identification.

## I

**Identification confidence**  
The evidence supporting a metabolite assignment. A standardized name does not increase the experimental evidence originally reported.

**InChIKey**  
A fixed-length hash derived from an InChI chemical representation. Its blocks encode different layers of structural and protonation information. Representation differences can yield different keys for related forms.

**Information loss**  
Detail removed or collapsed during harmonization, such as reducing fasting hours to a binary flag or combining plasma and serum under a broad blood-derived-fluid category.

**Ion mode**  
Positive or negative ionization mode in mass spectrometry. Different modes can detect different subsets of metabolites and can create analysis-specific duplicates.

## J

**Join cardinality**  
The relationship between keys in two tables: one-to-one, one-to-many, many-to-one, or many-to-many. An unexpected many-to-many join can duplicate measurements and must be resolved before analysis.

## K

**KEGG compound ID**  
An identifier used in the KEGG compound resource and pathway ecosystem. It is useful for pathway linking but is not a universal identity key.

## L

**LC-MS**  
Liquid chromatography coupled with mass spectrometry. Chromatography, ionization, instrument, acquisition, and preprocessing choices influence coverage and measurement values.

**Longitudinal design**  
A design with repeated observations over time. Samples from the same participant are correlated and must not be treated as independent people.

## M

**Mapping status**  
The reviewed state of a crosswalk row, such as accepted exact, accepted broader, review required, unmapped, excluded nonbiological, or not evaluated.

**Matrix**  
The biological material measured, such as plasma or serum. Plasma and serum are both blood-derived but differ in collection and composition and remain distinct in this module.

**Metabolite overlap**  
The intersection of two explicitly defined analyte sets. The result depends on mapping status, annotation resolution, artifact exclusions, duplicate collapse, and denominator.

**Metabolomics Workbench**  
The platform hosting the National Metabolomics Data Repository and tools including the REST service and RefMet.

**MetENP**  
A CFDE-supported resource for metabolite enrichment and network/pathway interpretation. Its output inherits the identification, background-universe, and coverage limits of its inputs.

**MoTrPAC**  
Molecular Transducers of Physical Activity Consortium. It develops molecular maps of physical activity and provides public and restricted data pathways depending on the specific release.

**mwTab**  
The sectioned data and metadata format used by Metabolomics Workbench. Blocks can describe study, subject, factors, collection, sample preparation, analytical methods, and metabolite measurements.

## N

**NMDR**  
National Metabolomics Data Repository, hosted through Metabolomics Workbench.

**NPH**  
Nutrition for Precision Health, powered by the All of Us Research Program. Public NIH documentation describes a modular precision nutrition study whose data are stored and analyzed in the All of Us Researcher Workbench.

**Not yet assessable**  
A compatibility status used when essential evidence is missing or unresolved. It must not be silently converted to comparable or not comparable.

## P

**Partially comparable**  
Two fields share a broader construct but differ in granularity, timing, protocol, matrix, or measurement. They may support a coarser or stratified use if the difference remains visible.

**PCA**  
Principal component analysis, an unsupervised linear method that summarizes major directions of variance. PCA is sensitive to preprocessing and does not identify causal mechanisms.

**Peak area**  
An integrated analytical signal. Peak areas from different assays are not made directly comparable merely by scaling or using the same metabolite name.

**Phenotype anchor**  
The exposure or intervention context around which a study is organized, such as controlled feeding or an acute endurance exercise bout.

**Physiological timepoint**  
A time label defined by an anchor event, offset, unit, and biological state, rather than only a code such as `post` or `T2`.

**Pooled QC**  
A quality-control sample created by combining aliquots, often used to monitor analytical stability. In `ST001521`, `QPP...` rows are pooled QC candidates and are excluded from biological participant counts.

**PubChem CID**  
A record identifier in PubChem. Record form and structural specificity must be reviewed when using it as a cross-reference.

## R

**REC3 and REC22**  
In `ST003348`, collection labels for 3 hours and 22 hours after exercise, respectively.

**RefMet**  
A reference nomenclature for metabolomics designed to standardize names for discrete structures and analytically reported metabolite species. A RefMet mapping is a naming result, not proof of identification or quantitative equivalence.

**REST**  
Representational State Transfer. In this module, `REST` can also appear as the `ST003348` pre-exercise timepoint label. Context distinguishes the MW REST API from the exercise collection label.

**REST API**  
Metabolomics Workbench's URL-based service for programmatic access to study, compound, RefMet, and other contexts.

## S

**Sample role**  
The analytical purpose of a row, such as biological, pooled QC, blank, technical standard, or unknown.

**Serum**  
The liquid fraction obtained after blood clotting. The `ST003348` factors endpoint says `blood`, while its collection metadata specifies serum; the module preserves both and uses serum as the supported specific matrix.

**Specimen context**  
Matrix, anatomical source, collection conditions, processing, storage, fasting state, and related evidence needed to interpret a measurement.

**STAT**  
In `ST003348`, the immediately post-exercise collection label. It does not mean a generic post-intervention timepoint.

**Structural harmonization**  
Alignment of names, fields, categories, and relationships. It does not by itself justify combining quantitative observations.

**Study accession**  
A Metabolomics Workbench `ST...` identifier. The locked case studies are `ST001521` and `ST003348`.

## T

**Targeted metabolomics**  
Measurement focused on a defined analyte panel, often with method-specific quantitative or semiquantitative procedures. It differs from untargeted coverage and must not be assumed to share scale or detection properties.

**Time semantics**  
The biological meaning of a time label, including anchor event, offset, unit, state, visit or period, and repeated-measures order.

## U

**Unit reconciliation**  
A documented conversion performed only when the same quantity, compatible matrix and denominator, quantification basis, and conversion relationship are established.

**Untargeted metabolomics**  
Broad profiling of analytical features without limiting measurement to a small predefined panel. Feature annotation and missingness require careful interpretation.

## W

**Within-study analysis**  
An analysis fit separately inside one study using its own design, repeated measures, scale, and preprocessing. It is the default quantitative strategy in this module.

## Primary sources

1. Fahy E, Subramaniam S. [RefMet: a reference nomenclature for metabolomics](https://doi.org/10.1038/s41592-020-01009-y). *Nature Methods*. 2020;17:1173-1174.
2. Metabolomics Workbench. [REST Service](https://www.metabolomicsworkbench.org/tools/mw_rest.php), [RefMet](https://www.metabolomicsworkbench.org/databases/refmet/index.php), and [mwTab documentation](https://www.metabolomicsworkbench.org/data/tutorials.php). Accessed August 10, 2026.
3. Wilkinson MD, Dumontier M, Aalbersberg IJ, et al. [The FAIR Guiding Principles for scientific data management and stewardship](https://doi.org/10.1038/sdata.2016.18). *Scientific Data*. 2016;3:160018.
4. Sumner LW, Amberg A, Barrett D, et al. [Proposed minimum reporting standards for chemical analysis](https://doi.org/10.1007/s11306-007-0082-2). *Metabolomics*. 2007;3:211-221.

