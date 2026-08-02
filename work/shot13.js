const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const errors = [];
  page.on('pageerror', e => errors.push('PAGEERROR: ' + String(e).slice(0, 300)));
  await page.goto('http://localhost:8765/', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(2000);
  // Jump straight to a department quiz via the mcqs view
  await page.click('#main-nav button[data-view="practice"]');
  await page.waitForTimeout(800);
  // click Restorative row (first department card)
  const firstDept = await page.$$('[data-practice]');
  if (firstDept.length) { await firstDept[0].click(); await page.waitForTimeout(1200); }
  const txt = await page.evaluate(() => document.getElementById('app').innerText.slice(0, 500));
  console.log('AFTER DEPT CLICK:', txt.slice(0, 400));
  // find a start button
  const btns = await page.$$eval('button', els => els.map(e => e.textContent.trim().slice(0, 30)).filter(t => /start|ابدأ|بدأ|go|quiz/i.test(t)).slice(0, 8));
  console.log('START BTNS:', JSON.stringify(btns));
  await browser.close();
})();
