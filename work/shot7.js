const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const errors = [];
  page.on('pageerror', e => errors.push('PAGEERROR: ' + String(e).slice(0, 300)));
  await page.goto('http://localhost:8765/', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(2000);
  await page.click('#main-nav button[data-view="marjune"]');
  await page.waitForTimeout(1500);
  await page.click('[data-dept-quiz="all"]');
  await page.waitForTimeout(1500);
  let mcq = 0, qna = 0, fake = 0, unknown = 0;
  const sampleStems = [];
  for (let i = 0; i < 120; i++) {
    const txt = await page.evaluate(() => document.getElementById('app').innerText);
    if (txt.includes('recall Q&A')) qna++;
    else if (txt.includes('Reveal answer')) fake++;
    else { mcq++; if (sampleStems.length < 5) { const stem = await page.evaluate(() => document.querySelector('.q-stem')?.innerText || ''); sampleStems.push(stem.slice(0, 80)); } }
    // advance: show answer if Q&A & hidden; then next
    const nxt = await page.$('#btn-next');
    if (nxt && !(await nxt.isHidden())) { await nxt.click(); }
    else {
      const reveal = await page.$('#fn-reveal');
      if (reveal && !(await reveal.isHidden())) await reveal.click();
      await page.waitForTimeout(60);
      const n2 = await page.$('#btn-next');
      if (n2 && !(await n2.isHidden())) await n2.click();
      else { const first = await page.$('.option'); if (first) await first.click(); const n3 = await page.$('#btn-next'); if (n3 && !(await n3.isHidden())) await n3.click(); }
    }
    await page.waitForTimeout(60);
  }
  console.log('120 Q sample → MCQs:', mcq, '| Q&A:', qna, '| fake Reveal:', fake);
  console.log('MCQ stems sample:', JSON.stringify(sampleStems, null, 1));
  console.log('ERRORS:', JSON.stringify(errors));
  await browser.close();
})();
