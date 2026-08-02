const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push('CONSOLE: ' + m.text().slice(0, 200)); });
  page.on('pageerror', e => errors.push('PAGEERROR: ' + String(e).slice(0, 300)));
  await page.goto('http://localhost:8765/', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(2000);
  const tabs = ['today', 'topics', 'practice', 'recentqa', 'notes', 'marjune', 'progress', 'feedback'];
  const results = {};
  for (const tab of tabs) {
    const btn = await page.$(`#main-nav button[data-view="${tab}"]`);
    if (!btn) { results[tab] = 'NO BUTTON'; continue; }
    await btn.click();
    await page.waitForTimeout(700);
    const hasObj = (await page.evaluate(() => document.getElementById('app').innerText)).includes('[object Object]');
    results[tab] = hasObj ? 'RENDERS [object Object]' : 'OK';
  }
  console.log('TABS:', JSON.stringify(results, null, 1));
  // Flash quiz full flow
  await page.click('#main-nav button[data-view="marjune"]');
  await page.waitForTimeout(800);
  await page.click('[data-dept-quiz="all"]');
  await page.waitForTimeout(1000);
  let qna=0, mcq=0, fake=0;
  for (let i = 0; i < 40; i++) {
    const txt = await page.evaluate(() => document.getElementById('app').innerText);
    if (txt.includes('recall Q&A')) qna++;
    else if (txt.includes('Reveal answer')) fake++;
    else mcq++;
    const nxt = await page.$('#btn-next');
    if (nxt && !(await nxt.isHidden())) { await nxt.click(); await page.waitForTimeout(100); continue; }
    const first = await page.$('.option');
    if (first) { await first.click(); await page.waitForTimeout(120); }
    const rv = await page.$('#fn-reveal');
    if (rv && !(await rv.isHidden())) { await rv.click(); await page.waitForTimeout(120); }
    const n2 = await page.$('#btn-next');
    if (n2 && !(await n2.isHidden())) { await n2.click(); await page.waitForTimeout(100); }
    const stem = await page.evaluate(() => document.querySelector('.q-stem')?.innerText || '');
    // safety: if stuck on same stem 3x, click show answer then next
    if (i > 0) {
      const n3 = await page.$('#btn-next');
      if (n3 && !(await n3.isHidden())) { await n3.click(); await page.waitForTimeout(100); }
    }
  }
  console.log('FLASH QUIZ 40Q → MCQs:', mcq, '| Q&A:', qna, '| fake Reveal:', fake);
  console.log('ERRORS:', JSON.stringify(errors.slice(0, 8)));
  await browser.close();
})();
