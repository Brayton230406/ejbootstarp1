const { chromium } = require('playwright');

const baseUrl = process.argv[2] || 'http://127.0.0.1:4173/paginaCristianoRonaldo/';
const pages = ['bootstrap-online.html', 'bootstrap-offline.html'];
const viewports = [320, 390, 768, 1440];

(async () => {
  const browser = await chromium.launch({ headless: true });
  const failures = [];
  try {
    for (const file of pages) {
      const page = await browser.newPage();
      for (const width of viewports) {
        const errors = [];
        page.on('pageerror', (error) => errors.push(error.message));
        page.on('requestfailed', (request) => errors.push(`request failed: ${request.url()}`));
        await page.setViewportSize({ width, height: 900 });
        await page.goto(`${baseUrl}${file}`, { waitUntil: 'networkidle' });
        await page.locator('img').evaluateAll((images) => images.forEach((image) => image.scrollIntoView()));
        await page.waitForTimeout(250);
        const result = await page.evaluate(() => ({
          scrollWidth: document.documentElement.scrollWidth,
          clientWidth: document.documentElement.clientWidth,
          images: [...document.images].every((image) => image.complete && image.naturalWidth > 0),
          unsafeLinks: [...document.querySelectorAll('a[target="_blank"]')].filter((link) => !/\bnoopener\b/.test(link.rel) || !/\bnoreferrer\b/.test(link.rel)).length,
        }));
        if (result.scrollWidth > result.clientWidth || !result.images || result.unsafeLinks || errors.length) {
          failures.push(`${file} @ ${width}px: ${JSON.stringify({ ...result, errors })}`);
        }
      }
      await page.close();
    }
  } finally {
    await browser.close();
  }
  if (failures.length) {
    console.error('Auditoría responsive fallida:\n' + failures.join('\n'));
    process.exitCode = 1;
  } else {
    console.log('Auditoría responsive OK: 320, 390, 768 y 1440 px sin overflow, errores ni imágenes rotas.');
  }
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
