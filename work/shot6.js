const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text().slice(0, 250)); });
  page.on('pageerror', e => errors.push('PAGEERROR: ' + String(e).slice(0, 300)));
  await page.goto('http://localhost:8765/', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(2000);
  await page.click('#main-nav button[data-view="marjune"]');
  await page.waitForTimeout(2000);
  const flashTxt = await page.evaluate(() => document.getElementById('app').innerText);
  console.log('Has [object Object]:', flashTxt.includes('[object Object]'));
  // Start all-flash quiz
  await page.click('[data-dept-quiz="all"]');
  await page.waitForTimeout(2000);
  let qtext = await page.evaluate(() => document.getElementById('app').innerText.slice(0, 800));
  console.log('QUIZ 1:', qtext.slice(0, 500));
  // Step through 30 questions, count fake reveal options
  let fakeOpts = 0, realMCQs = 0, qna = 0;
  for (let i = 0; i < 30; i++) {
    const txt = await page.evaluate(() => document.getElementById('app').innerText);
    const opts = await page.$$eval('.option', els => els.map(e => e.textContent.trim()));
    if (txt.includes('Reveal answer') && opts.some(o => o.includes('Reveal answer'))) fakeOpts++;
    else if (txt.includes('recall Q&A')) qna++;
    else realMCQs++;
    // advance: click next if visible else pick first option
    const next = await page.$('#btn-next');
    if (next && !(await next.isHidden())) { await next.click(); }
    else { const first = await page.$('.option'); if (first) await first.click(); const n2 = await page.$('#btn-next'); if (n2 && !(await n2.isHidden())) await n2.click(); }
    await page.waitForTimeout(80);
  }
  console.log('In 30 Qs → real MCQs:', realMCQs, '| honest Q&A:', qna, '| fake Reveal-answer options:', fakeOpts);
  console.log('ERRORS:', JSON.stringify(errors.slice(0, 5)));
  await browser.close();
})();
