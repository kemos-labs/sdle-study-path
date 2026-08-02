const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  await page.goto('http://localhost:8765/', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(2000);
  await page.click('#main-nav button[data-view="marjune"]');
  await page.waitForTimeout(1500);
  await page.click('[data-dept-quiz="all"]');
  await page.waitForTimeout(1500);
  for (let i = 0; i < 4; i++) {
    const stem = await page.evaluate(() => document.querySelector('.q-stem')?.innerText || '(no stem)');
    const opts = await page.$$eval('.option', els => els.map(e => ({ t: e.textContent.trim().slice(0, 40), dis: e.disabled })));
    const nextHidden = await page.$eval('#btn-next', e => e.hidden).catch(() => 'no-btn');
    const revealHidden = await page.$eval('#fn-reveal', e => e.hidden).catch(() => 'no-reveal');
    console.log(`[${i}] stem:`, stem.slice(0, 60), '| opts:', JSON.stringify(opts.slice(0, 3)), '| nextHidden:', nextHidden, '| revealHidden:', revealHidden);
    // try clicking first option
    const first = await page.$('.option');
    if (first) { await first.click(); await page.waitForTimeout(300); }
    const nextHidden2 = await page.$eval('#btn-next', e => e.hidden).catch(() => 'no-btn');
    console.log('   after click → nextHidden:', nextHidden2);
    const nxt = await page.$('#btn-next');
    if (nxt && !(await nxt.isHidden())) { await nxt.click(); await page.waitForTimeout(300); }
    else { const rv = await page.$('#fn-reveal'); if (rv && !(await rv.isHidden())) { await rv.click(); await page.waitForTimeout(200); const n2 = await page.$('#btn-next'); if (n2 && !(await n2.isHidden())) await n2.click(); await page.waitForTimeout(200); } }
  }
  await browser.close();
})();
