# Lesson 5 - Access patterns and transfer to additional resources

**Estimated time:** 15 minutes  
**Bloom levels:** Evaluate, create  
**Module objective addressed:** LO5

## Learning objectives

By the end of this lesson, you will be able to:

1. Determine the current access pattern of a specific dataset and intended action using dated first-party evidence.
2. Identify which parts of the Metabo-Diet workflow transfer unchanged and which must be redesigned.
3. Draft a compliant analysis architecture for open, agreement-gated, or controlled-compute data.
4. Produce a go, revise, wait, or stop decision with unresolved requirements stated explicitly.

## Lesson map

| Activity | Minutes |
|---|---:|
| Revisit access as a dataset property | 3 |
| Worked transfer cases | 4 |
| Transfer checklist | 5 |
| Knowledge check | 3 |
| **Instructional subtotal, excluding posttest** | **15** |
| Posttest, additional assessment time | 8 |
| **Learner time with posttest** | **23** |

> **In the notebook (NB-L5):** Review the source log and edit the transfer-decision cell with dated evidence for one exact target. Choose `GO`, `REVISE`, `WAIT`, or `STOP`, then run `NB-REPRO`. Complete the posttest after the artifact manifest appears without errors.

## 1. Access tier is not a logo

In Lesson 1, access was introduced as a planning problem. After completing an open-data workflow, you can now see exactly where access rules affect the analysis.

Access is determined by the combination of:

- A specific dataset and release.
- The requested data level.
- Your identity, institution, training, and approvals.
- The intended use.
- The compute location.
- What inputs and outputs may cross the environment boundary.
- Current terms and policies.

Do not assign a permanent tier to an entire program. Current MoTrPAC documentation, for example, distinguishes public releases that community users can access without an account from restricted or embargoed data that require authentication, a data-use agreement, or other authorization. The access pattern is dataset-dependent. All of Us provides Registered and Controlled Tier collections in a governed Researcher Workbench and restricts external release of participant-level data and small counts under its policies.

The July 2026 proposal used MoTrPAC as a simplified registration-gated example. This module intentionally updates that framing to match current first-party documentation: **verify the exact release and action every time**.

## 2. What stays the same, and what must change

Some harmonization practices transfer across environments:

- Define the scientific question and estimand.
- Preserve original identifiers and metadata.
- Record provenance and decision rules.
- Separate naming, specimen, time, and unit compatibility.
- Flag unresolved mappings.
- Validate join cardinality.
- Respect repeated measures.
- Bound interpretation by design.

Other parts may need redesign:

- Authentication and API calls.
- Where code executes.
- Where raw, derived, and cached data are stored.
- Whether external reference resources can be queried from the environment.
- Whether data can be joined across resources.
- Whether row-level outputs, logs, plots, models, or counts can be exported.
- Who reviews an export and what disclosure thresholds apply.
- How collaborators receive access.

You can reuse the analysis steps even when the data must remain in a governed workspace.

## 3. Worked transfer case A: a MoTrPAC dataset

### Scenario

You find a MoTrPAC metabolomics release that may complement the exercise case study.

### Verification sequence

1. Identify the exact collection, study, release, assay level, and files.
2. Open current MoTrPAC Data Hub and Knowledge Center documentation.
3. Test whether the desired public file can be browsed or downloaded without an account.
4. If the file is restricted or embargoed, document authentication, DUA, publication, confidentiality, and review requirements.
5. Record the evidence URL, page version if available, date, and result.

### Architecture decision

- **Public file:** The local or Colab-style workflow may remain possible, subject to license, size, and terms. Replace the MW-specific retrieval adapter while retaining provenance and crosswalk logic.
- **Restricted file:** Obtain authorization before access. Store and analyze only in permitted locations; do not add restricted content to the module cache. Adapt collaboration and output review to the DUA.
- **Unclear status:** Pause data retrieval and ask the program help desk. Continue with public metadata or synthetic schema only.

### Scientific decision

MoTrPAC's detailed exercise design can improve phenotype context, but repository membership does not make its measurements quantitatively compatible with `ST003348`. Repeat the full platform, specimen, time, and unit assessment.

## 4. Worked transfer case B: Nutrition for Precision Health in All of Us

### Scenario

You want to adapt the diet harmonization workflow to NPH data stored in the All of Us Researcher Workbench.

### Verification sequence

1. Confirm that the desired NPH data type and release are available.
2. Determine whether the required collection is Registered or Controlled Tier.
3. Verify current institutional, researcher, identity, training, workspace, and project requirements.
4. Review the Data User Code of Conduct and Data and Statistics Dissemination Policy.
5. Determine what participant-level data, code outputs, counts, plots, models, or aggregate results may leave the Workbench.

### Architecture decision

The safe default is to move approved code and public reference mappings **into** the governed workspace, run participant-level work there, and export only outputs permitted under current policy. Do not download NPH participant-level data to populate this module's local files or cached fallback. If external RefMet calls are unavailable or inappropriate, import a dated, approved reference table without participant data and record its version.

### Scientific decision

NPH's modular diet design and multimodal context may support questions that the small FARMM case cannot. It does not remove the need to define diet period, test-meal timing, specimen, assay, repeated measures, and the intended estimand.

## 5. Text-only concept sketch: transfer workflow

No separate image appears here. Picture a central box labeled `portable harmonization logic`. Three arrows point to an open laptop, a sign-in workspace, and a locked cloud workspace. The logic moves to all three. Raw data arrows move freely only into the open laptop; gated data remain in approved storage; controlled participant-level data remain inside the locked cloud. A single outbound arrow from the cloud is labeled `reviewed outputs permitted by policy`.

## 6. Hands-on activity: make a transfer decision

Use `module/templates/access_tier_transfer_checklist_learner.md` for a resource of your choice. You may use a specific MoTrPAC release, an NPH/All of Us collection, another Metabolomics Workbench accession, MetaboLights, or a consortium repository relevant to your work.

For the timed course, complete five items: the exact dataset and intended action, one first-party source with its check date, the access pattern, the compute/storage boundary, and a `GO`, `REVISE`, `WAIT`, or `STOP` decision. The full checklist is a project extension.

### Required evidence

- Exact resource, dataset, and version or release.
- Intended data and action.
- First-party access documentation URL and check date.
- Account, agreement, institutional, training, or approval requirements.
- Permitted compute and storage location.
- Input and output movement rules.
- Metadata and identifier availability.
- Required changes to retrieval, cache, crosswalk, and reporting.
- One scientific compatibility risk distinct from access.

### Decision options

- `GO`: Requirements are verified and the planned workflow is permitted and scientifically appropriate.
- `REVISE`: The goal is possible, but architecture, scope, output, or analysis must change.
- `WAIT`: A documented approval, release, or clarification is pending.
- `STOP`: The planned action is prohibited or cannot answer the scientific question.

Write one sentence that distinguishes policy evidence from your interpretation. Example:

> The first-party page states that this public release can be downloaded without an account; I infer that the local retrieval step is feasible, but I still need to confirm license and scientific compatibility before reuse.

## 7. Safety and governance rules

- Verify current first-party terms; do not rely on this lesson as legal or policy authority.
- Dataset landing-page visibility does not prove participant-level download permission.
- Public metadata can be useful even when data are restricted, but it does not authorize reconstruction or access.
- Do not place credentials, tokens, signed URLs, or controlled data in notebooks, caches, logs, version control, or training artifacts.
- Do not evade a governed environment by exporting row-level data, small cells, recoverable embeddings, or model artifacts that policy treats as sensitive.
- Access approval does not establish scientific comparability.
- If rules conflict or remain unclear, pause the affected data movement and seek the resource's official support channel.

## 8. Knowledge check

**KC5-01.** What is the most accurate access description for MoTrPAC?

A. Every MoTrPAC dataset requires registration.  
B. Every MoTrPAC dataset is fully open.  
C. Access is dataset- and release-dependent; public and restricted paths exist and must be verified.  
D. MoTrPAC data can be used only inside All of Us.

**KC5-02.** What should move into a controlled-compute environment?

A. Approved analysis code and public reference resources that comply with environment policy.  
B. A public link that silently downloads participant data to a local laptop.  
C. Shared credentials.  
D. A module cache populated with participant-level records.

**KC5-03.** A dataset is publicly downloadable and scientifically incompatible with your target estimand. What is the correct decision?

A. Pool it because access is open.  
B. Treat access and scientific compatibility separately; revise or stop the integration.  
C. Standardize names and ignore the design.  
D. Call it controlled access.

## 9. Posttest and transfer commitment

Complete `module/assessments/posttest.json` through the delivery platform, then finish this statement:

> Within the next month, I will apply the workflow to ________. My first evidence check will be ________, and the first incompatibility I will test is ________.

## Final decision rule

The harmonization workflow transfers when its logic, provenance, and guardrails are preserved. Access changes the analysis architecture; study design changes the claims. Both must be checked before data move or models run.

## Primary sources and first-party documentation

1. MoTrPAC. [Data access FAQ](https://motrpac-data.org/knowledge-center/project-overview/faq). Accessed August 17, 2026.
2. MoTrPAC. [Data Hub access documentation](https://motrpac-data.org/knowledge-center/dissemination/data-access/data-hub) and [consortium/restricted onboarding](https://motrpac-data.org/knowledge-center/dissemination/data-access/onboarding). Accessed August 17, 2026.
3. NIH Common Fund. [Nutrition for Precision Health FAQ](https://commonfund.nih.gov/nutritionforprecisionhealth/frequently-asked-questions). Accessed August 10, 2026.
4. All of Us Research Program. [Researcher Workbench overview](https://support.researchallofus.org/hc/en-us/articles/41981123613716-Researcher-Workbench). Accessed August 10, 2026.
5. All of Us Research Program. [Policy questions and dissemination guidance](https://support.researchallofus.org/hc/en-us/articles/34814131370388-Policy-Questions). Accessed August 10, 2026.
6. All of Us Research Program. [Research project directory and access-tier requirements](https://www.allofus.nih.gov/protecting-data-and-privacy/research-projects-all-us-data/). Accessed August 10, 2026.
