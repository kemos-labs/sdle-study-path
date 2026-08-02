const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const errors = [];
  page.on('pageerror', e => errors.push('PAGEERROR: ' + String(e).slice(0, 300)));
  await page.goto('http://localhost:8765/', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(2000);
  await page.click('button:has-text("٣٠ يوم")');
  await page.waitForTimeout(1500);
  // start MCQs for today's subject
  const btn = await page.$('button:has-text("MCQs")');
  if (btn) { await btn.click(); await page.waitForTimeout(2000); }
  const q = await page.evaluate(() => document.getElementById('app').innerText.slice(0, 700));
  console.log('MAIN QUIZ:', q.slice(0, 550));
  // answer first option and go next
  const first = await page.$('.option');
  if (first) { await first.click(); await page.waitForTimeout(400); }
  const fb = await page.evaluate(() => document.getElementById('feedback')?.innerText.slice(0, 200) || '(no feedback)');
  console.log('FEEDBACK:', fb);
  console.log('ERRORS:', JSON.stringify(errors));
  await browser.close();
})();
