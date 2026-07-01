const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

function arg(name, def) {
  const pre = `--${name}=`;
  const found = process.argv.find((a) => a.startsWith(pre));
  return found ? found.slice(pre.length) : def;
}

const BASE = 'https://dhxkf93d45vp4.cloudfront.net';
const BASIC_AUTH = { username: 'admin', password: '123123' };
const LOGIN_EMAIL = arg('email', 'nguyetntm+2@dipro.vn');
const LOGIN_PASSWORD = arg('password', '123123Ad');
const SECRET_QUESTION = arg('secretQ', '本社オフィスのドアの色は？');
const SECRET_ANSWER = arg('secretA', '赤色');
const ROLE = arg('role', 'admin');
const OUT_DIR = path.resolve(__dirname, '..', arg('out', `${ROLE}-tmp`));
const SHOT_DIR = path.join(OUT_DIR, 'screenshots');
fs.mkdirSync(SHOT_DIR, { recursive: true });

let SECTIONS = (arg('sections', '') || '').split(',').filter(Boolean);
const sectionsFrom = arg('sectionsFrom', '');
if (!SECTIONS.length && sectionsFrom) {
  const data = JSON.parse(fs.readFileSync(sectionsFrom, 'utf8'));
  SECTIONS = (data.sections || []).filter((s) => s !== 'dashboard');
}

const found = [];
let shotCounter = 100;

async function shot(page, section, kind, label) {
  shotCounter += 1;
  const safeLabel = label.replace(/[^\w-]+/g, '_').slice(0, 40);
  const file = `${shotCounter}-${section}-${kind}-${safeLabel}.png`;
  await page.screenshot({ path: path.join(SHOT_DIR, file), fullPage: true });
  found.push({ section, kind, label, url: page.url(), screenshot: `screenshots/${file}` });
  console.log(`  [shot] ${section}/${kind}/${label} -> ${file}`);
}

async function resetTo(page, url) {
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 });
  await page.waitForTimeout(1000);
}

(async () => {
  console.log('Role:', ROLE, 'Sections:', SECTIONS);
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({ httpCredentials: BASIC_AUTH, viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();

  await page.goto(`${BASE}/admin`, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(1500);
  if (page.url().includes('/signin')) {
    await page.fill('input[name="email"]', LOGIN_EMAIL);
    await page.fill('input[name="password"]', LOGIN_PASSWORD);
    await page.getByRole('button', { name: /ログイン/ }).click();
    await page.waitForTimeout(2000);
    try {
      await page.getByText('秘密の質問').first().waitFor({ timeout: 5000 });
      await page.waitForTimeout(1000);
      await page.locator('input[role="combobox"]').first().click();
      await page.getByRole('option', { name: SECRET_QUESTION }).click();
      await page.fill('input[name="answer"]', SECRET_ANSWER);
      await page.locator('button:has-text("次へ")').first().click();
      await page.waitForURL(/dashboard/, { timeout: 15000 }).catch(() => {});
      await page.waitForTimeout(1500);
    } catch (e) {}
  }

  for (const section of SECTIONS) {
    const url = `${BASE}/admin/${section}`;
    console.log(`\n== ${section} ==`);
    try {
      await resetTo(page, url);
    } catch (e) {
      console.log('  nav failed:', e.message.split('\n')[0]);
      continue;
    }

    const createBtn = page.locator('button', { hasText: /新規/ }).first();
    if (await createBtn.count() > 0) {
      try {
        await createBtn.click({ timeout: 5000 });
        await page.waitForTimeout(1200);
        await shot(page, section, 'create-form', 'new');
        await resetTo(page, url);
      } catch (e) {
        console.log('  create click failed:', e.message.split('\n')[0]);
      }
    }

    const detailBtn = page.locator('button:has(img[alt="detail"]), button:has(img[alt="details"]), button[aria-label="details"]').first();
    if (await detailBtn.count() > 0) {
      try {
        await detailBtn.click({ timeout: 5000 });
        await page.waitForTimeout(1200);
        const editFromDetail = page.getByRole('button', { name: '編集する' }).first();
        if (await editFromDetail.count() > 0) {
          await editFromDetail.click({ timeout: 5000 });
          await page.waitForTimeout(1200);
          await shot(page, section, 'edit-form-from-detail', 'first-row');
        }
        await resetTo(page, url);
      } catch (e) {
        console.log('  detail->edit failed:', e.message.split('\n')[0]);
        await resetTo(page, url);
      }
    }

    const trashBtn = page.locator('button:has(img[alt="delete"])').first();
    if (await trashBtn.count() > 0) {
      try {
        await trashBtn.click({ timeout: 5000 });
        await page.waitForTimeout(1000);
        await shot(page, section, 'delete-confirm', 'dialog');
        const cancelBtn = page.getByRole('button', { name: /キャンセル|閉じる|いいえ/ }).first();
        if (await cancelBtn.count() > 0) {
          await cancelBtn.click({ timeout: 3000 });
        } else {
          await page.keyboard.press('Escape');
        }
        await page.waitForTimeout(500);
        await resetTo(page, url);
      } catch (e) {
        console.log('  delete-confirm failed:', e.message.split('\n')[0]);
        await page.keyboard.press('Escape').catch(() => {});
        await resetTo(page, url);
      }
    }
  }

  await browser.close();

  fs.writeFileSync(path.join(OUT_DIR, 'deep-flow-2.json'), JSON.stringify({ role: ROLE, email: LOGIN_EMAIL, screens: found }, null, 2));

  const bySection = {};
  for (const f of found) {
    bySection[f.section] = bySection[f.section] || [];
    bySection[f.section].push(f);
  }
  const md = [
    `# Admin Screen Flow — ${ROLE} (pass 2: create / edit-from-detail / delete-confirm)`,
    '',
    `Screens captured: ${found.length}`,
    '',
    ...Object.entries(bySection).flatMap(([section, items]) => [
      `## ${section}`,
      '',
      ...items.map((it) => `- **${it.kind}** (${it.label}) — \`${new URL(it.url).pathname}\` — ![](${it.screenshot})`),
      '',
    ]),
  ].join('\n');
  fs.writeFileSync(path.join(OUT_DIR, 'deep-flow-2.md'), md);
  console.log('\nDone. Output at', OUT_DIR);
})();
