const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push('CONSOLE: ' + m.text().slice(0, 200)); });
  page.on('pageerror', e => errors.push('PAGEERROR: ' + String(e).slice(0, 300)));
  await page.goto('http://localhost:8765/', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(2000);
  // Main bank quiz — Practice tab → start a quick quiz
  await page.click('#main-nav button[data-view="practice"]');
  await page.waitForTimeout(1000);
  // Look for a quiz start button in practice
  const buttons = await page.$$eval('button', els => els.map(e => ({ t: e.textContent.trim().slice(0, 40), id: e.id, vis: !e.hidden })).slice(0, 30));
  console.log('PRACTICE BUTTONS:', JSON.stringify(buttons.slice(0, 15)));
  // Try "start" on first option
  const startBtns = await page.$$('button:has-text("ابدأ"), button:has-text("Start"), button:has-text("بدأ")');
  console.log('start buttons found:', startBtns.length);
  await browser.close();
})();
