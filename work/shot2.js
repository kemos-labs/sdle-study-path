const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text().slice(0, 200)); });
  page.on('pageerror', e => errors.push('PAGEERROR: ' + String(e).slice(0, 300)));
  await page.goto('http://localhost:8765/', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(2500);
  await page.screenshot({ path: '/tmp/sdle_home.png', fullPage: false });
  // go to Flash tab
  await page.click('#main-nav button[data-view="marjune"]');
  await page.waitForTimeout(2500);
  await page.screenshot({ path: '/tmp/sdle_flash.png', fullPage: false });
  const text = await page.evaluate(() => document.getElementById('app').innerText.slice(0, 2000));
  console.log('FLASH TEXT:', text.slice(0, 1500));
  console.log('ERRORS:', JSON.stringify(errors.slice(0, 10)));
  await browser.close();
})();
