# Resolution of delivery comments

Final-review status as of Monday, 2026-08-17. The Friday delivery itself was pushed on 2026-08-14.

| Comment | Resolution and evidence | Status |
|---|---|---|
| Divide the notebook by module lesson | The Python notebook now has stable `NB-L1` through `NB-L5` sections; the R companion mirrors them as `NB-R-L1` through `NB-R-L5`. | Complete |
| Add Python, R, and package setup | `NB-SETUP`, `requirements-dev.txt`, `install_r_packages.R`, and the README provide macOS/Linux and Windows commands, version checks, cached mode, and optional live mode. | Complete |
| Make learner instructions explicit | The guide and notebook state what to read, which ordinary code cells to run, which learner-edit values to change, where to record responses, when to stop, and how to continue. A first-time Jupyter primer explains `Shift+Enter`, execution indicators, saved outputs, and tracebacks. | Complete |
| Cross-reference PDF and notebook | The guide contains a global crosswalk and a notebook-connection callout for each lesson, using stable notebook keys. | Complete |
| Add PCA examples to the appendix | Figures A1 and A2 are embedded as separate within-study PCA examples with captions, alt text, explained variance, and interpretation limits. | Complete |
| Have someone run the code locally | Clean automated Python execution, extracted-ZIP execution, R normalization, and cached R Markdown rendering passed on the final artifacts. The required two-person research-assistant usability pilot is defined but has not yet been performed. | Automated complete; human pilot pending |
| Upload by Friday | The requested release files were pushed to the GitHub `sam_work` branch on Friday, 2026-08-14. Final QA revisions were added on Monday, 2026-08-17. | Complete |
| Add a public English Creative Commons license | Root `LICENSE` applies CC BY 4.0 to original training materials and excludes third-party datasets and dependencies; the notice is copied into downloadable packages and SCORM. | Complete |
| Team review and final email | This is an external post-delivery action for the team. | Pending external action |
| Make the repository public | The license is public, but the repository is still private and its default `main` branch does not contain the release. A GitHub organization administrator must merge or promote `sam_work`, make the release branch the public default, and change repository visibility. | Pending administrator action |

The authoritative automated results are in `release_packaging_audit.json`, `release_manifest.json`, `MANIFEST.sha256`, `clean_environment_report.md`, and `scorm_validation.json`.
