# Data attribution and reuse notes

## Primary public datasets

This training package includes cached copies and derived educational artifacts from two public Metabolomics Workbench/NMDR studies. Each study's public summary endpoint reports a Creative Commons Attribution 4.0 International license.

### Diet-anchored case study

- Metabolomics Workbench study: `ST001521`
- Project: `PR001024`
- Project DOI: <https://doi.org/10.21228/M8B984>
- Repository record: <https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?Mode=Study&StudyID=ST001521>
- License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

### Exercise-anchored case study

- Metabolomics Workbench study: `ST003348`
- Project: `PR002083`
- Project DOI: <https://doi.org/10.21228/M8C802>
- Repository record: <https://www.metabolomicsworkbench.org/data/DRCCMetadata.php?Mode=Study&StudyID=ST003348>
- License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

### RefMet classification

- Source: Metabolomics Workbench RefMet REST service
- Endpoint: <https://www.metabolomicsworkbench.org/rest/refmet/classification>
- Documentation: <https://www.metabolomicsworkbench.org/tools/mw_rest.php>

Exact retrieval times, response sizes, SHA-256 checksums, release fields, and transformations are recorded in [`data/provenance.json`](data/provenance.json).

## Training materials

Except for third-party material identified here or in `data/provenance.json`, the lesson text, original templates, notebook narrative and code, scripts, figures, and assessments in this package are licensed under the [Creative Commons Attribution 4.0 International Public License](https://creativecommons.org/licenses/by/4.0/). Reusers must give appropriate credit, link to the license, and indicate changes. The English repository license notice is available at [`../LICENSE`](../LICENSE).

This grant does not relicense third-party datasets, repository records, software dependencies, trademarks, or logos. Dataset attribution does not imply that the original investigators, the Metabolomics Workbench, NIH, CFDE, MoTrPAC, NPH, All of Us, or any affiliated institution reviewed or endorsed the module.

## Interpretation notice

The package uses these studies to teach metadata reasoning, identifier harmonization, and within-study exploratory analysis. It does not treat the studies as one experiment, estimate a diet-versus-exercise causal effect, or claim that plasma and serum peak areas are quantitatively interchangeable.
