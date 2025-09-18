#!/usr/bin/env node
import fs from 'fs';
import path from 'path';
import { chromium } from 'playwright';

function parseTSV(tsvPath) {
  const raw = fs.readFileSync(tsvPath, 'utf-8').trim().split('\n');
  const headers = raw[0].split('\t');
  return raw.slice(1).map(line => {
    const cols = line.split('\t');
    const obj = {};
    headers.forEach((h,i)=> obj[h] = cols[i] || '');
    return obj;
  });
}

async function main() {
  const args = process.argv.slice(2);
  const inIdx = args.indexOf('--in');
  const outIdx = args.indexOf('--out');
  if (inIdx === -1) {
    console.error('Usage: node screenshot.mjs --in data/urls.tsv --out out/screens');
    process.exit(1);
  }
  const inPath = args[inIdx+1];
  const outDir = outIdx === -1 ? 'out/screens' : args[outIdx+1];
  fs.mkdirSync(outDir, { recursive: true });

  const rows = parseTSV(inPath);
  const browser = await chromium.launch();
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });

  for (const row of rows) {
    try {
      const page = await context.newPage();
      await page.goto(row.URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
      const safeName = row.Organization.replace(/[^\w]+/g,'_');
      const shotPath = path.join(outDir, safeName + '_homepage.png');
      await page.screenshot({ path: shotPath, fullPage: true });

      // Try to capture logo
      const logoHandle = await page.$('header img, .logo img, img[alt*="logo" i]');
      if (logoHandle) {
        const logoPath = path.join(outDir, safeName + '_logo.png');
        await logoHandle.screenshot({ path: logoPath });
      }

      console.log('Captured:', row.Organization);
      await page.close();
    } catch (e) {
      console.error('Error capturing', row.Organization, e.message);
    }
  }

  await context.close();
  await browser.close();
}

main().catch(err => { console.error(err); process.exit(1); });