const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text().slice(0, 200)); });
  page.on('pageerror', e => errors.push('PAGEERROR: ' + String(e).slice(0, 300)));
  await page.goto('http://localhost:8765/', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(2000);
  await page.click('#main-nav button[data-view="marjune"]');
  await page.waitForTimeout(2000);
  // Click the "All Flash Notes" div (data-dept-quiz=all)
  await page.click('[data-dept-quiz="all"]');
  await page.waitForTimeout(2500);
  const qtext = await page.evaluate(() => document.getElementById('app').innerText.slice(0, 1500));
  console.log('QUIZ SCREEN:', qtext.slice(0, 1300));
  console.log('ERRORS:', JSON.stringify(errors));
  await browser.close();
})();
