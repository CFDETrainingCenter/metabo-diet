# Access-pattern and transfer checklist - learner version

**Learner:** ____________________  
**Date:** ____________________  
**Resource support contact, if known:** ____________________

## Instructions

Assess one exact dataset, release, and intended action. Use current first-party documentation. Do not infer access from the program name, a search-result snippet, or a past release.

This checklist supports planning and is not legal advice or a replacement for the resource's terms, institutional review, or data-governance process.

For the timed lesson, complete five items: the exact dataset and action in Section 1, one first-party source and date in Section 2, one planning pattern in Section 3, the compute/storage boundary in Section 6, and the decision in Section 8. Use the remaining rows for a full project transfer.

## 1. Scope the request

| Item | Entry |
|---|---|
| Program/resource |  |
| Exact dataset or collection |  |
| Release/version/date |  |
| Assay/data level |  |
| Requested fields/files |  |
| Intended scientific question |  |
| Intended action: view/query/download/join/analyze/export/share/publish |  |
| Intended users/collaborators |  |
| Intended compute location |  |
| Intended storage location |  |
| Intended outputs |  |

## 2. Record first-party evidence

| Evidence question | Answer | First-party URL/document section | Checked at UTC | Status: verified/conflicting/unclear |
|---|---|---|---|---|
| Is the exact release discoverable? |  |  |  |  |
| Is it released, embargoed, or pending? |  |  |  |  |
| Can it be viewed without an account? |  |  |  |  |
| Can the desired data be downloaded? |  |  |  |  |
| Is an individual account required? |  |  |  |  |
| Is institutional authorization required? |  |  |  |  |
| Is training or identity verification required? |  |  |  |  |
| Is a DUA, code of conduct, or click-through agreement required? |  |  |  |  |
| Is project or access-committee approval required? |  |  |  |  |
| Must analysis occur in a governed workspace? |  |  |  |  |
| Can participant-level data leave the environment? |  |  |  |  |
| What aggregate/count/output rules apply? |  |  |  |  |
| Can external reference data or APIs enter the environment? |  |  |  |  |
| Can code leave the environment, and under what conditions? |  |  |  |  |
| Can collaborators receive or share access? |  |  |  |  |
| What citation/acknowledgment is required? |  |  |  |  |
| What license or reuse terms apply? |  |  |  |  |

## 3. Assign a planning pattern

Select only after completing the evidence table.

- [ ] **Open public retrieval:** The intended public data action is available without personal credentials.
- [ ] **Account/agreement/approval gated:** The intended action requires identity, terms, a DUA, or approval.
- [ ] **Controlled compute:** Participant-level work must remain in a governed environment and only permitted outputs leave.
- [ ] **Mixed:** Different files, levels, actions, or releases use different patterns.
- [ ] **Unclear:** Current evidence is insufficient or conflicting.

**Evidence statement:**

> The first-party source states ____________________________________________.

**Your interpretation:**

> For my intended action, I infer _________________________________________.

## 4. Check scientific fit separately

| Check | Evidence | Compatible/partial/not compatible/unclear | Required action |
|---|---|---|---|
| Population and design |  |  |  |
| Phenotype/exposure definition |  |  |  |
| Specimen and pre-analytics |  |  |  |
| Timepoint semantics |  |  |  |
| Assay/platform and coverage |  |  |  |
| Units/scale and preprocessing |  |  |  |
| Identifier/annotation resolution |  |  |  |
| Repeated-measures structure |  |  |  |
| Missingness and QC metadata |  |  |  |

**Scientific comparison the data can support:** ____________________________

**Scientific comparison the data cannot support:** _________________________

## 5. Adapt the Metabo-Diet workflow

| Component | Keep unchanged | Modify | Remove/replace | Planned implementation |
|---|---|---|---|---|
| Question and estimand | [ ] | [ ] | [ ] |  |
| Retrieval adapter/API | [ ] | [ ] | [ ] |  |
| Authentication handling | [ ] | [ ] | [ ] |  |
| Local public cache | [ ] | [ ] | [ ] |  |
| Provenance manifest | [ ] | [ ] | [ ] |  |
| Specimen/time crosswalk | [ ] | [ ] | [ ] |  |
| RefMet mapping | [ ] | [ ] | [ ] |  |
| QC/sample-role logic | [ ] | [ ] | [ ] |  |
| Within-study analysis | [ ] | [ ] | [ ] |  |
| Cross-resource join | [ ] | [ ] | [ ] |  |
| Output disclosure review | [ ] | [ ] | [ ] |  |
| Collaboration/sharing | [ ] | [ ] | [ ] |  |
| Publication/citation | [ ] | [ ] | [ ] |  |

## 6. Data-flow sketch

Write each boundary explicitly.

```text
[Public documentation/reference] --permitted input?--> [Compute environment]
[Governed/raw data] ----------------stays where?------> [Compute environment]
[Derived participant-level data] ---stays where?------> [Approved storage]
[Aggregate/output] -----------------review rule?------> [Permitted destination]
[Code] -----------------------------review rule?------> [Repository/collaborator]
```

**Credentials/tokens location:** ___________________________________________

**Credential rule:** Never enter credentials or signed URLs in this worksheet, a notebook, a cache, or version control.

## 7. Risk and dependency log

| Risk or dependency | Evidence | Owner | Mitigation | Stop condition |
|---|---|---|---|---|
| Access approval |  |  |  |  |
| Dataset release/change |  |  |  |  |
| Compute/storage policy |  |  |  |  |
| Export/disclosure |  |  |  |  |
| Identifier mapping |  |  |  |  |
| Scientific compatibility |  |  |  |  |
| Other |  |  |  |  |

## 8. Decision

- [ ] `GO` - requirements are verified and the planned action is permitted and scientifically appropriate.
- [ ] `REVISE` - the goal is possible, but architecture, scope, output, or analysis must change.
- [ ] `WAIT` - a documented approval, release, or clarification is pending.
- [ ] `STOP` - the planned action is prohibited or cannot answer the scientific question.

**Decision statement:** ____________________________________________________

**Unresolved items:** ______________________________________________________

**Next evidence check and date:** __________________________________________

## Final safety check

- [ ] I evaluated an exact dataset, release, and action.
- [ ] I used current first-party evidence and recorded a date.
- [ ] I separated policy evidence from my inference.
- [ ] I did not copy credentials or governed data into the worksheet.
- [ ] I separated access feasibility from scientific comparability.
- [ ] I identified where data, code, and outputs may move.
- [ ] I identified an official support path for unclear requirements.
- [ ] My decision can be revisited when the release or policy changes.
