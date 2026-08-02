const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text().slice(0, 200)); });
  page.on('pageerror', e => errors.push('PAGEERROR: ' + String(e).slice(0, 300)));
  await page.goto('http://localhost:8765/', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(2000);
  // Go to Flash tab
  await page.click('#main-nav button[data-view="marjune"]');
  await page.waitForTimeout(2000);
  // Click "🎯 All Flash Notes 4026 ▶" quiz button — find by text
  const btns = await page.$$eval('button', els => els.filter(e => /All Flash Notes/.test(e.textContent)).map(e => ({ txt: e.textContent.trim().slice(0, 60), id: e.id })));
  console.log('All Flash buttons:', JSON.stringify(btns));
  // Click the start button for All Flash Notes
  const startBtn = await page.$('button:has-text("All Flash Notes")');
  if (startBtn) { await startBtn.click(); await page.waitForTimeout(2500); }
  const qtext = await page.evaluate(() => document.getElementById('app').innerText.slice(0, 1200));
  console.log('QUIZ SCREEN:', qtext.slice(0, 1000));
  console.log('ERRORS:', JSON.stringify(errors));
  await browser.close();
})();
