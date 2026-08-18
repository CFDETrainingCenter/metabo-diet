# Metabo-Diet course site

Interactive learner site for **Metabo-Diet: Harmonizing Dietary and Exercise
Phenotypes with Metabolomics Across CFDE Resources**.

The site presents five lessons, embedded checks, scored pre/post assessments,
local progress tracking, and downloads for the executable notebook, learner
guide, and worksheets. The scientific case studies are Metabolomics Workbench
`ST001521` (diet) and `ST003348` (exercise).

## Local development

Requires Node.js 22.13 or newer.

```bash
npm install
npm run dev
```

Open `http://localhost:3000`.

## Verification

```bash
npm run build
node --test tests/rendered-html.test.mjs
```

The site is stateless. Assessment progress is stored only in the learner's
browser via `localStorage`; no account or database is required.
