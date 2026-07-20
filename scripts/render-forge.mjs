import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import playwright from "../../bridgework/node_modules/playwright/index.js";

const { chromium } = playwright;

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(scriptDirectory, "..");
const demoDirectory = path.join(root, "demo");
const fixturePath = path.join(demoDirectory, "synthetic-forge-fixture.wav");
const baseUrl = process.env.ARM_VOICE_LEDGER_URL || "http://127.0.0.1:18788";
const chromePath = process.env.CHROME_BIN || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";

await fs.mkdir(demoDirectory, { recursive: true });
const browser = await chromium.launch({ executablePath: chromePath, headless: true });
const consoleErrors = [];

async function exercise(page) {
  page.on("console", (message) => {
    if (message.type() === "error") consoleErrors.push(message.text());
  });
  await page.goto(baseUrl, { waitUntil: "networkidle" });
  await page.locator("#audio-input").setInputFiles(fixturePath);
  await page.locator("#source-player").evaluate((player) => new Promise((resolve) => {
    if (player.readyState >= 1) {
      resolve();
      return;
    }
    player.addEventListener("loadedmetadata", resolve, { once: true });
  }));
  const browserSourceUrl = await page.locator("#source-player").getAttribute("src");
  await page.getByRole("button", { name: "Transcribe locally" }).click();
  await page.waitForFunction(() => document.querySelectorAll(".word").length >= 8, null, { timeout: 90000 });
  const words = page.locator(".word");
  await words.nth(2).click();
  await words.nth(5).click();
  const transcriptCueSeconds = await page.locator("#source-player").evaluate((player) => player.currentTime);
  await page.locator("#row-note").fill("Follow up on the interview next step.");
  await page.getByRole("button", { name: "Create from selected words" }).click();
  await page.locator(".row-time").click();
  const ledgerCueSeconds = await page.locator("#source-player").evaluate((player) => player.currentTime);
  const download = page.waitForEvent("download");
  await page.getByRole("button", { name: "Export local JSON" }).click();
  await (await download).saveAs(path.join(demoDirectory, "synthetic-forge-ledger.json"));
  return {
    wordCount: await words.count(),
    ledgerRows: await page.locator(".ledger-row").count(),
    metrics: await page.locator("#metrics-status").textContent(),
    runtime: await page.locator("#runtime-status").textContent(),
    browserSourceIsLocal: browserSourceUrl?.startsWith("blob:") || false,
    transcriptCueSeconds,
    ledgerCueSeconds,
  };
}

const desktop = await browser.newPage({ viewport: { width: 1440, height: 1060 }, deviceScaleFactor: 1 });
const desktopResult = await exercise(desktop);
await desktop.screenshot({ path: path.join(demoDirectory, "forge-listening-desk-desktop.png"), fullPage: true });

const mobile = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
const mobileResult = await exercise(mobile);
await mobile.screenshot({ path: path.join(demoDirectory, "forge-listening-desk-mobile.png"), fullPage: true });

await browser.close();
const result = { baseUrl, desktop: desktopResult, mobile: mobileResult, consoleErrors };
await fs.writeFile(path.join(demoDirectory, "render-check.json"), `${JSON.stringify(result, null, 2)}\n`, "utf8");
if (
  consoleErrors.length > 0
  || desktopResult.ledgerRows !== 1
  || mobileResult.ledgerRows !== 1
  || !desktopResult.browserSourceIsLocal
  || !mobileResult.browserSourceIsLocal
  || desktopResult.transcriptCueSeconds <= 0
  || mobileResult.transcriptCueSeconds <= 0
  || desktopResult.ledgerCueSeconds <= 0
  || mobileResult.ledgerCueSeconds <= 0
) {
  throw new Error(`render_check_failed:${JSON.stringify(result)}`);
}
console.log(JSON.stringify(result, null, 2));
