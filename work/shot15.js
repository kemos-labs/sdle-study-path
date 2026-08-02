const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const errors = [];
  page.on('pageerror', e => errors.push('PAGEERROR: ' + String(e).slice(0, 300)));
  await page.goto('http://localhost:8765/', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(2000);
  // click Restorative department row in practice pane
  const resto = await page.$('text=Restorative');
  if (resto) { await resto.click(); await page.waitForTimeout(1500); }
  const txt = await page.evaluate(() => document.getElementById('app').innerText.slice(0, 500));
  console.log('AFTER RESTO:', txt.slice(0, 400));
  // look for start quiz button
  const btns = await page.$$eval('button', els => els.map(e => ({t: e.textContent.trim().slice(0, 40), id: e.id, cls: e.className.slice(0, 30)})));
  console.log('BTNS:', JSON.stringify(btns.slice(0, 12)));
  // try a "start" / "go" 
  const go = await page.$('#start-quiz, #go-quiz, [data-go]');
  if (go) { await go.click(); await page.waitForTimeout(1500); }
  const q = await page.evaluate(() => document.getElementById('app').innerText.slice(0, 500));
  console.log('QUIZ?:', q.slice(0, 350));
  console.log('ERRORS:', JSON.stringify(errors));
  await browser.close();
})();
