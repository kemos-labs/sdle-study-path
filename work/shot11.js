const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const errors = [];
  page.on('pageerror', e => errors.push('PAGEERROR: ' + String(e).slice(0, 300)));
  await page.goto('http://localhost:8765/', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(2000);
  // pick 30-day plan
  await page.click('button:has-text("٣٠ يوم")');
  await page.waitForTimeout(1500);
  const txt = await page.evaluate(() => document.getElementById('app').innerText.slice(0, 700));
  console.log('AFTER PLAN:', txt.slice(0, 500));
  // start the day's quiz
  const qstart = await page.$('button:has-text("Start"), button:has-text("ابدأ"), button:has-text("Q")');
  if (qstart) { await qstart.click(); await page.waitForTimeout(1500); }
  const q = await page.evaluate(() => document.getElementById('app').innerText.slice(0, 600));
  console.log('QUIZ:', q.slice(0, 400));
  console.log('ERRORS:', JSON.stringify(errors));
  await browser.close();
})();
