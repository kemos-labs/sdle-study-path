const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text().slice(0, 200)); });
  page.on('pageerror', e => errors.push('PAGEERROR: ' + String(e).slice(0, 300)));
  await page.goto('http://localhost:8765/', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(2000);
  // Topics tab
  await page.click('#main-nav button[data-view="topics"]');
  await page.waitForTimeout(1500);
  const topicsTxt = await page.evaluate(() => document.getElementById('app').innerText.slice(0, 600));
  console.log('TOPICS TAB:', topicsTxt.slice(0, 500));
  // Practice tab
  await page.click('#main-nav button[data-view="practice"]');
  await page.waitForTimeout(1500);
  const practTxt = await page.evaluate(() => document.getElementById('app').innerText.slice(0, 600));
  console.log('PRACTICE TAB:', practTxt.slice(0, 500));
  console.log('ERRORS:', JSON.stringify(errors));
  await browser.close();
})();
