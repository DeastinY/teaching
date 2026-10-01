// Render the social preview card: tools/og-card.html -> assets/images/og-card.png
//
//   node tools/make_og_card.mjs        (needs the playwright package and a Chromium)
//
// The forecast figure is lifted out of index.html at render time, so the card
// always shows the same drawing as the homepage. Re-run it after changing the
// chart, the name or the strapline, and commit the PNG.
import { chromium } from 'playwright';
import { readFileSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { dirname, join } from 'node:path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const home = readFileSync(join(root, 'index.html'), 'utf8');
const svg = home.match(/<svg class="forecast"[\s\S]*?<\/svg>/)[0]
  .replace(/<title[\s\S]*?<\/desc>/, '')            // the card has its own alt text
  .replace(/role="img" aria-labelledby="[^"]*"/, 'aria-hidden="true"')
  .replace('viewBox="0 0 1200 350"', 'viewBox="0 80 1200 270"');  // drop the empty rows above the trace

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1200, height: 630 } });
await page.goto(pathToFileURL(join(root, 'tools', 'og-card.html')).href, { waitUntil: 'networkidle' });
await page.evaluate(html => { document.getElementById('chart').innerHTML = html; }, svg);
await page.evaluate(() => document.fonts.ready);
await page.screenshot({ path: join(root, 'assets', 'images', 'og-card.png') });
await browser.close();
console.log('wrote assets/images/og-card.png');
