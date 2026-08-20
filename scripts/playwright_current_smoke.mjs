/** Current student-eye smoke test for the eight-tab SDLE SPA. */
import { chromium } from "playwright";

const BASE = process.env.SDLE_BASE || "http://127.0.0.1:8765";
const expectedViews = ["today", "topics", "practice", "recentqa", "marjune", "notes", "progress", "feedback"];
const failures = [];
const errors = [];
const check = (ok, message) => {
  console.log(`${ok ? "  OK " : " FAIL"} ${message}`);
  if (!ok) failures.push(message);
};

const browser = await chromium.launch({ headless: true });
try {
  for (const viewport of [{ width: 1280, height: 900 }, { width: 390, height: 844 }]) {
    const context = await browser.newContext({ viewport });
    const page = await context.newPage();
    page.on("console", msg => { if (msg.type() === "error") errors.push(msg.text()); });
    page.on("pageerror", err => errors.push(err.message));
    await page.goto(`${BASE}/index.html`, { waitUntil: "networkidle", timeout: 90000 });
    await page.waitForFunction(() => window.QUESTION_BANK?.length > 100 && window.FLASH_NOTES, { timeout: 30000 });

    if (await page.locator("[data-pick-plan='30']").count()) {
      await page.locator("[data-pick-plan='30']").first().click();
      await page.waitForTimeout(150);
    }
    const closeGuide = page.getByRole("button", { name: /Close/ });
    if (await closeGuide.count()) await closeGuide.first().click();

    const label = `${viewport.width}px`;
    check(await page.locator("#main-nav button").count() === 8, `${label}: eight primary tabs render`);
    for (const view of expectedViews) {
      const tab = page.locator(`#main-nav button[data-view='${view}']`);
      check(await tab.count() === 1, `${label}: ${view} tab exists`);
      if (await tab.count()) {
        await tab.click();
        await page.waitForTimeout(100);
        check((await page.locator("#app").innerText()).trim().length > 20, `${label}: ${view} renders content`);
      }
    }
    const widths = await page.evaluate(() => ({ viewport: innerWidth, document: document.documentElement.scrollWidth }));
    check(widths.document <= widths.viewport + 1, `${label}: no horizontal page overflow`);

    await page.locator("#main-nav button[data-view='practice']").click();
    const practicePool = page.locator("button[data-pick-pool]").first();
    if (await practicePool.count()) await practicePool.click();
    const startQuiz = page.locator("button[data-qz]").first();
    check(await startQuiz.count() === 1, `${label}: practice offers a sized drill`);
    if (await startQuiz.count()) {
      await startQuiz.click();
      await page.waitForTimeout(150);
      check(await page.locator(".option").count() >= 2, `${label}: practice quiz shows answer options`);
      if (await page.locator(".option").count()) {
        await page.locator(".option").first().click();
        await page.waitForTimeout(80);
        check((await page.locator("#app").innerText()).includes("Why"), `${label}: practice answer reveals reasoning`);
      }
    }

    await page.locator("#main-nav button[data-view='marjune']").click();
    const mcqType = page.locator("button[data-fn-type='mcq']");
    if (await mcqType.count()) await mcqType.click();
    const flashPool = page.locator("button[data-fn-scope]").first();
    if (await flashPool.count()) await flashPool.click();
    const startFlash = page.locator("button[data-fn-qz]").first();
    check(await startFlash.count() === 1, `${label}: Flash offers a sized drill`);
    if (await startFlash.count()) {
      await startFlash.click();
      await page.waitForTimeout(150);
      const flashText = await page.locator("#app").innerText();
      check(!flashText.includes("Reveal answer"), `${label}: Flash has no fake Reveal-answer option`);
      check(await page.locator(".option").count() >= 2, `${label}: Flash MCQ shows pickable options`);
    }
    await context.close();
  }
} finally {
  await browser.close();
}

check(errors.length === 0, `console/page errors: ${errors.length}`);
if (errors.length) console.error(errors.join("\n"));
if (failures.length) process.exit(1);
console.log("\nCURRENT SPA SMOKE PASSED");
