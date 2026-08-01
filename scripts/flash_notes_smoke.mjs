// Flash Notes tab smoke test — verify app renders, counts match gate, no errors
import { chromium } from "playwright";

const BASE = process.env.SDLE_BASE || "http://127.0.0.1:8765";
const results = { ok: 0, warn: 0, fail: 0 };
const log = (sev, msg) => {
  results[sev]++;
  console.log(` ${sev.toUpperCase().padEnd(4)} ${msg}`);
};

const browser = await chromium.launch();
const page = await browser.newPage();
const errors = [];
page.on("console", (m) => m.type() === "error" && errors.push(m.text()));
page.on("pageerror", (e) => errors.push(String(e)));

await page.goto(BASE, { waitUntil: "networkidle" });
await page.waitForFunction(() => window.QUESTION_BANK && window.FLASH_NOTES, { timeout: 15000 });

// 1. Data loaded
const fnTotal = await page.evaluate(() => window.FLASH_NOTES.total);
const fnActual = await page.evaluate(() => Object.values(window.FLASH_NOTES.byDept || {}).flat().length);
log(fnTotal === 4026 ? "ok" : "fail", `FLASH_NOTES.total=${fnTotal} (expected 4026)`);
log(fnActual === 4026 ? "ok" : "warn", `actual flattened items=${fnActual}`);

// 2. Navigate to Flash Notes tab
const navBtn = page.locator('button:has-text("Flash Notes"), a:has-text("Flash Notes"), [data-fn-go]').first();
if (await navBtn.count()) {
  await navBtn.click();
  await page.waitForTimeout(800);
  log("ok", "Flash Notes tab opened");
} else {
  log("warn", "Flash Notes tab button not found — trying via view switch");
  await page.evaluate(() => {
    if (window.__sdleState) { /* noop */ }
  });
  // click the marjune view button
  const marjune = page.locator('[data-view="marjune"], button:has-text("Mar-June")').first();
  if (await marjune.count()) { await marjune.click(); await page.waitForTimeout(800); log("ok", "marjune view opened"); }
}

// 3. Check study card renders
const card = page.locator(".fn-study-card, #fn-study-widget, .fn-card").first();
const hasCard = await card.count() > 0;
log(hasCard ? "ok" : "warn", "study card widget present");

// 4. Audit stats line
const bodyText = await page.evaluate(() => document.body.innerText);
const statsMatch = bodyText.match(/🤖\s*\d+\s*AI-reviewed/i) || bodyText.match(/AI-reviewed/i);
log(statsMatch ? "ok" : "warn", "AI-reviewed stats line visible");

// 5. Disputed button
const disputedBtn = page.locator('[data-fn-disputed]').first();
if (await disputedBtn.count()) {
  await disputedBtn.click();
  await page.waitForTimeout(500);
  const dr = page.locator("#fn-dispute-list, [data-fn-dr]").first();
  log((await dr.count()) > 0 ? "ok" : "warn", "disputed review list rendered");
}

// 6. Page errors
log(errors.length === 0 ? "ok" : "fail", `page errors: ${errors.length} ${errors.slice(0, 3).join(" | ")}`);

// 7. Check answer coverage stats from data
const stats = await page.evaluate(() => {
  const items = Object.values(window.FLASH_NOTES.byDept || {}).flat();
  const withAns = items.filter((i) => i.answerLetter || i.answerIdx !== undefined || i._embedded_answer || i._model_suggested_answer).length;
  const verified = items.filter((i) => i._verification_verdict === "supported").length;
  return { total: items.length, withAns, verified };
});
log("ok", `answers present: ${stats.withAns}/${stats.total}, supported evidence: ${stats.verified}`);
const breakdown = await page.evaluate(() => {
  const items = Object.values(window.FLASH_NOTES.byDept || {}).flat();
  return {
    answerLetter: items.filter((i) => i.answerLetter).length,
    answerIdx: items.filter((i) => i.answerIdx !== undefined).length,
    embedded: items.filter((i) => i._embedded_answer).length,
    suggested: items.filter((i) => i._model_suggested_answer).length,
  };
});
log("ok", `breakdown: ${JSON.stringify(breakdown)}`);

await browser.close();
console.log(`\nRESULT: ${results.ok} ok, ${results.warn} warn, ${results.fail} fail`);
process.exit(results.fail > 0 ? 1 : 0);
