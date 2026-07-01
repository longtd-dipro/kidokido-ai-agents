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

const found = []; // { section, kind, label, url, screenshot }
let shotCounter = 0;

async function shot(page, section, kind, label) {
  shotCounter += 1;
  const safeLabel = label.replace(/[^\w-]+/g, '_').slice(0, 40);
  const file = `${String(shotCounter).padStart(2, '0')}-${section}-${kind}-${safeLabel}.png`;
  await page.screenshot({ path: path.join(SHOT_DIR, file), fullPage: true });
  found.push({ section, kind, label, url: page.url(), screenshot: `screenshots/${file}` });
  console.log(`  [shot] ${section}/${kind}/${label} -> ${file}`);
}

(async () => {
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
    } catch (e) {
      console.log('no secret question modal:', e.message.split('\n')[0]);
    }
  }

  await page.waitForTimeout(1000);

  // Auto-discover accessible sections from the sidebar (roles may see a subset)
  const hrefs = await page.locator('a[href^="/admin/"]').evaluateAll((as) => as.map((a) => a.getAttribute('href')));
  const SECTIONS = [...new Set(
    hrefs
      .map((h) => h.split('?')[0].replace(/^\/admin\//, '').split('/')[0])
      .filter(Boolean)
      .filter((s) => !/logout|signout/i.test(s))
  )];
  console.log('Discovered sections for role', ROLE, ':', SECTIONS);

  for (const section of SECTIONS) {
    const url = `${BASE}/admin/${section}`;
    console.log(`\n== ${section} ==`);
    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 });
    } catch (e) {
      console.log('  nav failed:', e.message.split('\n')[0]);
      continue;
    }
    await page.waitForTimeout(1500);
    await shot(page, section, 'list', 'main');

    // 1) tabs
    const tabCount = await page.locator('[role="tab"]').count();
    if (tabCount > 1) {
      for (let i = 0; i < tabCount; i++) {
        try {
          const tab = page.locator('[role="tab"]').nth(i);
          const label = (await tab.textContent())?.trim() || `tab${i}`;
          await tab.click();
          await page.waitForTimeout(1000);
          await shot(page, section, 'tab', label);
        } catch (e) {
          console.log('  tab click failed:', e.message.split('\n')[0]);
        }
      }
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 });
      await page.waitForTimeout(1000);
    }

    // 2) detail/view icon (read-only) - only the FIRST occurrence
    const detailBtn = page.locator('button:has(img[alt="detail"]), button:has(img[alt="details"]), button[aria-label="details"], button[aria-label="view"]').first();
    if (await detailBtn.count() > 0) {
      try {
        await detailBtn.click({ timeout: 5000 });
        await page.waitForTimeout(1200);
        await shot(page, section, 'detail', 'first-row');
        await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 });
        await page.waitForTimeout(1000);
      } catch (e) {
        console.log('  detail click failed:', e.message.split('\n')[0]);
      }
    } else {
      const editBtn = page.locator('button:has(img[alt="update"]), button[aria-label="update"]').first();
      if (await editBtn.count() > 0) {
        try {
          await editBtn.click({ timeout: 5000 });
          await page.waitForTimeout(1200);
          await shot(page, section, 'edit-form', 'first-row');
          await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 });
          await page.waitForTimeout(1000);
        } catch (e) {
          console.log('  edit click failed:', e.message.split('\n')[0]);
        }
      }
    }

    // 3) create/new button (open form only, never submit)
    const createBtn = page.locator('button', { hasText: /新規/ }).first();
    if (await createBtn.count() > 0) {
      try {
        await createBtn.click({ timeout: 5000 });
        await page.waitForTimeout(1200);
        await shot(page, section, 'create-form', 'new');
        await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 });
        await page.waitForTimeout(1000);
      } catch (e) {
        console.log('  create click failed:', e.message.split('\n')[0]);
      }
    }
  }

  await browser.close();

  fs.writeFileSync(path.join(OUT_DIR, 'deep-flow.json'), JSON.stringify({ role: ROLE, email: LOGIN_EMAIL, sections: SECTIONS, screens: found }, null, 2));

  const bySection = {};
  for (const f of found) {
    bySection[f.section] = bySection[f.section] || [];
    bySection[f.section].push(f);
  }

  const md = [
    `# Admin Screen Flow — ${ROLE}`,
    '',
    `Sections: ${SECTIONS.length}, screens captured: ${found.length}`,
    '',
    ...Object.entries(bySection).flatMap(([section, items]) => [
      `## ${section}`,
      '',
      ...items.map((it) => `- **${it.kind}** (${it.label}) — \`${new URL(it.url).pathname}\` — ![](${it.screenshot})`),
      '',
    ]),
  ].join('\n');

  fs.writeFileSync(path.join(OUT_DIR, 'deep-flow.md'), md);
  console.log('\nDone. Output at', OUT_DIR);
})();
