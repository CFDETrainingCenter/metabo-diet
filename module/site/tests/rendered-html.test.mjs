import assert from "node:assert/strict";
import test from "node:test";

async function render() {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}`);
  const { default: worker } = await import(workerUrl.href);

  return worker.fetch(
    new Request("http://localhost/", { headers: { accept: "text/html" } }),
    { ASSETS: { fetch: async () => new Response("Not found", { status: 404 }) } },
    { waitUntil() {}, passThroughOnException() {} },
  );
}

test("renders the Metabo-Diet course shell", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  const html = await response.text();
  assert.match(html, /<title>Metabo-Diet \| CFDE training module<\/title>/i);
  assert.match(html, /Harmonize phenotype metadata with public metabolomics data/);
  assert.match(html, /Why phenotype-to-metabolome harmonization matters/);
  assert.match(html, /Run the guided analysis/);
  assert.match(html, /Assess access tiers and transfer/);
  assert.match(html, /Skip to lesson content/);
  assert.match(html, /http:\/\/localhost:3000\/og\.png/);
  assert.doesNotMatch(html, /codex-preview|Your site is taking shape|SkeletonPreview/);
});
