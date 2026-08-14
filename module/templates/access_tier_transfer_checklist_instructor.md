# Access-pattern and transfer checklist - instructor version

This key provides two worked cases and a scoring rubric. Access rules change; instructors must recheck all linked first-party documentation immediately before delivery. A learner with newer documented evidence should not be penalized for a different conclusion.

## Core rule

The unit of assessment is:

> specific dataset + release + data level + intended action + user/institution + compute/storage/output plan + check date

Answers that label an entire program `open`, `gated`, or `controlled` without those qualifiers are incomplete.

## Worked case A - MoTrPAC

### Scenario

The learner wants to download a public MoTrPAC analysis-result file for local, noncommercial exploratory work and compare its metadata structure with `ST003348`.

### Evidence expected as of August 10, 2026

- The MoTrPAC FAQ states that public data are available through the portal and that public data are accessible without login, while restricted data require authentication.
- The Data Hub documentation describes public releases and also an embargoed limited acute exercise rat subset requiring an account and DUA.
- Consortium-member onboarding explicitly says it does not apply to community users accessing public data.

Primary pages:

- [MoTrPAC FAQ](https://www.motrpac-data.org/knowledge-center/project-overview/faq)
- [MoTrPAC Data Hub](https://www.motrpac-data.org/knowledge-center/dissemination/data-access/data-hub)
- [MoTrPAC onboarding](https://motrpac-data.org/knowledge-center/dissemination/data-access/onboarding)

### Correct planning classification

`Mixed`, with the exact public file potentially following open public retrieval. Restricted or embargoed files follow an agreement/approval-gated path. The learner must still record license/terms for the selected public file.

### Architecture

For a verified public file, local analysis and a public cache may be possible under the applicable terms. Replace the MW REST retrieval adapter with the documented MoTrPAC download method. Retain provenance, crosswalk, sample-role, and scientific-compatibility checks.

For a restricted file, the learner must obtain authorization, honor storage and publication rules, and exclude restricted content from module caches and public repositories.

### Scientific decision

Access does not establish compatibility. Compare exercise modality, tissue, participant structure, timepoint, assay, preprocessing, and scale before any integration. A MoTrPAC exercise dataset is not automatically comparable with the race-walking serum data.

## Worked case B - NPH/All of Us

### Scenario

The learner wants to adapt the crosswalk and within-study analysis to a specified NPH release in the All of Us Researcher Workbench.

### Evidence expected as of August 10, 2026

- The NIH NPH FAQ says NPH data are stored in and analyzed within the All of Us Researcher Workbench and that the platform is available to approved researchers.
- All of Us documentation describes Registered and Controlled Tier collections and governed access requirements.
- Current support documentation prohibits participant-level data and direct or inferable small counts outside the Workbench and provides dissemination guidance for allowable outputs.

Primary pages:

- [NPH FAQ](https://commonfund.nih.gov/nutritionforprecisionhealth/frequently-asked-questions)
- [All of Us Researcher Workbench](https://support.researchallofus.org/hc/en-us/articles/41981123613716-Researcher-Workbench)
- [All of Us policy questions](https://support.researchallofus.org/hc/en-us/articles/34814131370388-Policy-Questions)
- [All of Us access-tier overview](https://www.allofus.nih.gov/protecting-data-and-privacy/research-projects-all-us-data/)

### Correct planning classification

`Controlled compute` for participant-level analysis, with the exact Registered or Controlled Tier and NPH release verified. Do not claim that no outputs can ever leave; state that only policy-permitted outputs may leave under current dissemination rules.

### Architecture

- Move approved analysis code and permitted public reference resources into the Workbench.
- Keep participant-level and restricted derived data inside approved storage.
- Do not populate the module's local cache with NPH participant data.
- Use a dated RefMet snapshot if live external calls are unavailable or inappropriate.
- Review plots, counts, tables, code outputs, and model artifacts against current policy before export.
- Keep secrets out of code, notebooks, logs, and repositories.

### Scientific decision

NPH may support richer diet-response questions, but each module, diet period, test meal, specimen, assay, repeated measure, and target estimand must be defined. Controlled access does not make a study scientifically suitable, and a richer dataset does not justify a vague question.

## Common misconceptions

| Misconception | Corrective feedback |
|---|---|
| "MoTrPAC is registration-gated." | Current documentation shows both public and restricted paths. Assess the exact release and action. |
| "MoTrPAC is open." | Some releases are public, while restricted or embargoed content can require authentication and a DUA. |
| "NPH data can never produce an external result." | Participant-level data remain governed, but policy-permitted aggregate outputs can be disseminated. Verify current rules. |
| "A public landing page means the data can be downloaded." | Discovery and download are separate actions; document each. |
| "I have approval, so I can put data in GitHub." | Authorization is bounded by storage, sharing, and output rules. |
| "Access is the only gate." | Scientific design and measurement compatibility remain independent gates. |

## Suggested scoring, 20 points

| Criterion | Points |
|---|---:|
| Exact dataset, release, action, and intended flow scoped | 3 |
| Current first-party evidence and check dates recorded | 4 |
| Account/agreement/compute/output rules correctly separated | 4 |
| Scientific compatibility assessed independently | 3 |
| Workflow and data-flow adaptations are concrete and compliant | 4 |
| Decision and unresolved dependencies are explicit | 2 |

## Minimum pass conditions

Regardless of numeric score, require revision if the learner:

- Places credentials or sensitive identifiers in the worksheet.
- Proposes exporting participant-level governed data without authority.
- Uses a program-wide access label without checking the selected release.
- Treats access approval as scientific compatibility.
- Proposes local or public caching of controlled participant data.

