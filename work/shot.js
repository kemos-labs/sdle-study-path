const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text().slice(0, 200)); });
  page.on('pageerror', e => errors.push('PAGEERROR: ' + String(e).slice(0, 300)));
  await page.goto('http://localhost:8765/', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(3000);
  await page.screenshot({ path: '/tmp/sdle_home.png', fullPage: false });
  console.log('TITLE:', await page.title());
  console.log('ERRORS:', JSON.stringify(errors.slice(0, 10), null, 1));
  // Check nav buttons
  const nav = await page.$$eval('#main-nav button', els => els.map(e => e.textContent.trim()));
  console.log('NAV:', JSON.stringify(nav));
  await browser.close();
})();
