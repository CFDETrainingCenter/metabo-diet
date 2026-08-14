# Resolution of delivery comments

Status as of Friday, 2026-08-14.

| Comment | Resolution and evidence | Status |
|---|---|---|
| Divide the notebook by module lesson | The Python notebook now has stable `NB-L1` through `NB-L5` sections; the R companion mirrors them as `NB-R-L1` through `NB-R-L5`. | Complete |
| Add Python, R, and package setup | `NB-SETUP`, `requirements-dev.txt`, `install_r_packages.R`, and the README provide macOS/Linux and Windows commands, version checks, cached mode, and optional live mode. | Complete |
| Make learner instructions explicit | Each lesson uses explicit read/run/observe/record/stop/continue language, completion checks, and learner-edit cells. | Complete |
| Cross-reference PDF and notebook | The guide contains a global crosswalk and a notebook-connection callout for each lesson, using stable notebook keys. | Complete |
| Add PCA examples to the appendix | Figures A1 and A2 are embedded as separate within-study PCA examples with captions, alt text, explained variance, and interpretation limits. | Complete |
| Have someone run the code locally | Clean automated Python execution, extracted-ZIP execution, R normalization, and R Markdown rendering passed. The required two-person research-assistant usability pilot is defined but has not yet been performed. | Automated complete; human pilot pending |
| Upload by Friday | Prepared for Git publication on the `sam_work` branch after final repository checks. | Pending push |
| Add a public English Creative Commons license | Root `LICENSE` applies CC BY 4.0 to original training materials and excludes third-party datasets and dependencies; the notice is copied into downloadable packages and SCORM. | Complete |
| Team review and final email | This is an external post-delivery action for the team. | Pending external action |
| Make the repository public | The license is public, but repository visibility requires GitHub organization administration. | Pending administrator action |

The authoritative automated results are in `release_packaging_audit.json`, `release_manifest.json`, `MANIFEST.sha256`, `clean_environment_report.md`, and `scorm_validation.json`.
