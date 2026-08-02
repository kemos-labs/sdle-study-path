const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const errors = [];
  page.on('pageerror', e => errors.push('PAGEERROR: ' + String(e).slice(0, 300)));
  await page.goto('http://localhost:8765/', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(1500);
  // Set plan state so practice shows quiz options
  await page.evaluate(() => {
    localStorage.setItem('sdle3_planChosen', 'true');
    localStorage.setItem('sdle3_planPickedExplicit', 'true');
    localStorage.setItem('sdle3_planLength', '30');
  });
  await page.reload({ waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(1500);
  await page.click('#main-nav button[data-view="practice"]');
  await page.waitForTimeout(1000);
  // click Restorative
  const rows = await page.$$('text=Restorative');
  let clicked = false;
  for (const r of rows) { const ok = await r.evaluate(el => el.closest('[data-]') !== null || el.tagName === 'BUTTON').catch(() => false); }
  // try clicking the row containing Restorative count
  const clickable = await page.$$('div[data-practice], div[data-pool], li[data-practice]');
  console.log('practice rows:', clickable.length);
  if (clickable.length) { await clickable[0].click(); await page.waitForTimeout(1500); }
  const txt = await page.evaluate(() => document.getElementById('app').innerText.slice(0, 600));
  console.log('AFTER:', txt.slice(0, 500));
  const qbtns = await page.$$eval('button', els => els.map(e => e.textContent.trim().slice(0, 40)).filter(t => /start|ابدأ|بدأ|quiz|امتحان|تدرب/i.test(t)).slice(0, 10));
  console.log('QUIZ BTNS:', JSON.stringify(qbtns));
  console.log('ERRORS:', JSON.stringify(errors));
  await browser.close();
})();
