const { chromium } = require('playwright');
const axe = require('axe-core');

const url = process.argv[2] || 'http://127.0.0.1:4173/paginaCristianoRonaldo/';

(async () => {
  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    await page.goto(url, { waitUntil: 'networkidle' });
    await page.addScriptTag({ content: axe.source });
    const results = await page.evaluate(async () => axe.run(document, {
      runOnly: ['wcag2a', 'wcag2aa'],
    }));

    if (results.violations.length > 0) {
      console.error(`axe-core detecto ${results.violations.length} incumplimiento(s):`);
      for (const violation of results.violations) {
        console.error(`\n[${violation.id}] ${violation.help} (${violation.helpUrl})`);
        for (const node of violation.nodes) {
          console.error(`- ${node.target.join(', ')}`);
          console.error(`  ${node.failureSummary}`);
        }
      }
      process.exitCode = 1;
      return;
    }

    console.log('axe-core WCAG 2.0 A/AA OK: no se detectaron incumplimientos.');
  } finally {
    await browser.close();
  }
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
