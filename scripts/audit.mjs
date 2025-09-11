#!/usr/bin/env node
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { chromium } from 'playwright';
import lighthouse from 'lighthouse';
import { launch as launchChrome } from 'chrome-launcher';
import axeSource from 'axe-core/axe.min.js';   // local axe-core

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const UNGOOGLED_PATH = '/Applications/Chromium.app/Contents/MacOS/Chromium';

function parseTSV(tsvPath) {
  const raw = fs.readFileSync(tsvPath, 'utf-8').trim().split('\n');
  const headers = raw[0].split('\t');
  return raw.slice(1).map(line => {
    const cols = line.split('\t');
    const obj = {};
    headers.forEach((h, i) => (obj[h] = cols[i] || ''));
    return obj;
  });
}

async function runLighthouse(url, chrome) {
  const opts = { logLevel: 'error', output: 'json', port: chrome.port };
  const config = null;
  const runnerResult = await lighthouse(url, opts, config);
  const cats = runnerResult.lhr.categories;
  return {
    performance: Math.round((cats.performance?.score || 0) * 100),
    accessibility: Math.round((cats.accessibility?.score || 0) * 100),
    bestPractices: Math.round((cats['best-practices']?.score || 0) * 100),
    seo: Math.round((cats.seo?.score || 0) * 100),
    json: runnerResult.lhr
  };
}

async function runAxe(url, browser) {
  const context = await browser.newContext();
  const page = await context.newPage();
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.addScriptTag({ content: axeSource }); // local injection
  const results = await page.evaluate(async () => {
    // @ts-ignore
    return await axe.run();
  });
  await context.close();
  return {
    violations: results.violations?.length || 0,
    passes: results.passes?.length || 0,
    incomplete: results.incomplete?.length || 0,
    details:
      results.violations?.map(v => ({
        id: v.id,
        impact: v.impact,
        nodes: v.nodes?.length
      })) || []
  };
}

async function main() {
  const args = process.argv.slice(2);
  const inIdx = args.indexOf('--in');
  const outIdx = args.indexOf('--out');
  if (inIdx === -1) {
    console.error('Usage: node audit.mjs --in data/urls.tsv --out out/audit');
    process.exit(1);
  }
  const inPath = args[inIdx + 1];
  const outDir = outIdx === -1 ? 'out/audit' : args[outIdx + 1];
  fs.mkdirSync(outDir, { recursive: true });

  const rows = parseTSV(inPath);
  const summary = [['State','Organization','URL','LH_Perf','LH_A11y','LH_BP','LH_SEO','axe_violations']];
  const errors = [['State','Organization','URL','Error']];

  const browser = await chromium.launch();

  let chrome;
  try {
    chrome = await launchChrome({
      chromePath: UNGOOGLED_PATH,
      chromeFlags: ['--headless', '--no-sandbox']
    });
    console.log('✅ Using Ungoogled-Chromium at', UNGOOGLED_PATH);
  } catch (e) {
    console.error('❌ Could not find Ungoogled-Chromium at', UNGOOGLED_PATH);
    process.exit(1);
  }

  for (const row of rows) {
    const url = row.URL;
    try {
      const lh = await runLighthouse(url, chrome);
      const axe = await runAxe(url, browser);
      const outBase = path.join(outDir, (row.Organization || 'org').replace(/[^\w]+/g, '_'));
      fs.writeFileSync(outBase + '_lighthouse.json', JSON.stringify(lh.json, null, 2));
      fs.writeFileSync(outBase + '_axe.json', JSON.stringify(axe, null, 2));
      summary.push([row.State, row.Organization, url, lh.performance, lh.accessibility, lh.bestPractices, lh.seo, axe.violations]);
      console.log('Audited:', row.Organization);
    } catch (e) {
      console.error('Error auditing', row.Organization, e.message);
      summary.push([row.State, row.Organization, url, '', '', '', '', 'ERR']);
      errors.push([row.State, row.Organization, url, e.message]);
    }
  }

  await browser.close();
  await chrome.kill();

  fs.writeFileSync(path.join(outDir, 'audit_summary.csv'), summary.map(r => r.join(',')).join('\n'));
  fs.writeFileSync(path.join(outDir, 'audit_errors.csv'), errors.map(r => r.join(',')).join('\n'));
  console.log('Wrote', path.join(outDir, 'audit_summary.csv'), 'and audit_errors.csv');
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});