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
  // Click the MCQ drill button on Today page: it has id ac-mcqs or similar
  const drill = await page.$('button:has-text("MCQs (today")');
  if (!drill) {
    // list buttons
    const btns = await page.$$eval('button', els => els.map(e => ({t: e.textContent.trim().slice(0, 50), id: e.id})).filter(b => b.t.length > 3));
    console.log('TODAY BUTTONS:', JSON.stringify(btns.slice(0, 20)));
    await browser.close(); return;
  }
  await drill.click();
  await page.waitForTimeout(2000);
  const txt = await page.evaluate(() => document.getElementById('app').innerText.slice(0, 500));
  console.log('QUIZ:', txt.slice(0, 400));
  // click an option
  const first = await page.$('.option');
  if (first) { await first.click(); await page.waitForTimeout(400); }
  const fb = await page.evaluate(() => document.getElementById('feedback')?.innerText.slice(0, 250) || '(none)');
  console.log('FEEDBACK:', fb);
  console.log('ERRORS:', JSON.stringify(errors));
  await browser.close();
})();
