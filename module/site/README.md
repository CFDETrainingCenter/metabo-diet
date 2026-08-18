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

## Deployment

The site builds to a Cloudflare Worker. It needs no database, environment
variable, or other binding; learner progress stays in the browser.

```bash
npx wrangler login
npm run deploy
```

This publishes to `metabo-diet-course.<subdomain>.workers.dev`. To preview the
upload without publishing, run:

```bash
npm run build
npx wrangler deploy --dry-run -c dist/server/wrangler.json
```
