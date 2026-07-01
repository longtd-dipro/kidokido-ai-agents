const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

function arg(name, def) {
  const pre = `--${name}=`;
  const found = process.argv.find((a) => a.startsWith(pre));
  return found ? found.slice(pre.length) : def;
}

const BASE = 'https://dhxkf93d45vp4.cloudfront.net';
const LOGIN_EMAIL = arg('email', 'nguyetntm+10@dipro.vn');
const LOGIN_PASSWORD = arg('password', 'Minhnguyet1505');
const OUT_DIR = path.resolve(__dirname, '..', arg('out', 'user'));
const SHOT_DIR = path.join(OUT_DIR, 'screenshots');
fs.mkdirSync(SHOT_DIR, { recursive: true });

// never click into a real payment/purchase-confirmation step
const NEVER_DRILL = /payment|checkout|confirm|purchase|credit|card|決済|カード|購入完了|お支払い/i;
// pages that never require login to view — used to decide crawl order, informational only
const TOP_LEVEL_PATHS = [
  '/', '/signup', '/signin',
  '/booking/use-in-day', '/booking/buy-times-limit-ticket', '/booking/payment-online', '/booking/buy-monthly-ticket',
  '/vacancy-status', '/tenant-list', '/price-list',
  '/terms-of-use', '/privacy-policy', '/commercial-law',
];

const found = [];
let shotCounter = 0;

async function shot(page, section, kind, label) {
  shotCounter += 1;
  const safeLabel = label.replace(/[^\w-]+/g, '_').slice(0, 40);
  const file = `${String(shotCounter).padStart(2, '0')}-${section.replace(/\//g, '_') || 'home'}-${kind}-${safeLabel}.png`;
  await page.screenshot({ path: path.join(SHOT_DIR, file), fullPage: true });
  found.push({ section, kind, label, url: page.url(), screenshot: `screenshots/${file}` });
  console.log(`  [shot] ${section}/${kind}/${label} -> ${file}`);
}

(async () => {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();

  // 1) logged-out views first (home, signup, signin)
  await page.goto(BASE, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(1500);
  await shot(page, '/', 'list', 'home-logged-out');

  await page.goto(`${BASE}/signup`, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(1200);
  await shot(page, '/signup', 'list', 'main');

  await page.goto(`${BASE}/signin`, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(1200);
  await shot(page, '/signin', 'list', 'main');

  // 2) login
  await page.fill('input[name="email"]', LOGIN_EMAIL);
  await page.fill('input[name="password"]', LOGIN_PASSWORD);
  await page.getByRole('button', { name: /^ログイン$/ }).click();
  await page.waitForTimeout(2500);
  console.log('Logged in, at:', page.url());
  await shot(page, '/', 'list', 'home-logged-in');

  // 3) マイページ (my page) — find its link from header
  const myPageLink = page.getByRole('link', { name: /マイページ/ }).first();
  if (await myPageLink.count() > 0) {
    await myPageLink.click();
    await page.waitForTimeout(1500);
    await shot(page, new URL(page.url()).pathname, 'list', 'mypage');
    await page.goto(BASE, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(1000);
  }

  // 4) remaining top-level pages (skip ones already captured)
  const already = new Set(['/', '/signup', '/signin']);
  for (const p of TOP_LEVEL_PATHS) {
    if (already.has(p)) continue;
    console.log(`\n== ${p} ==`);
    try {
      await page.goto(`${BASE}${p}`, { waitUntil: 'domcontentloaded', timeout: 20000 });
    } catch (e) {
      console.log('  nav failed:', e.message.split('\n')[0]);
      continue;
    }
    await page.waitForTimeout(1500);
    await shot(page, p, 'list', 'main');

    // for booking flows, drill ONE level into the first non-payment card/button/link
    if (p.startsWith('/booking/')) {
      const candidate = page.locator('a, button').filter({ hasNotText: NEVER_DRILL }).first();
      try {
        const href = await candidate.getAttribute('href').catch(() => null);
        if (href && NEVER_DRILL.test(href)) throw new Error('matched never-drill pattern, skipping');
        await candidate.click({ timeout: 5000 });
        await page.waitForTimeout(1500);
        if (NEVER_DRILL.test(page.url())) {
          console.log('  landed on a payment-like URL, capturing but going no further:', page.url());
        }
        await shot(page, p, 'drill-1', 'first-step');
      } catch (e) {
        console.log('  drill failed/skipped:', e.message.split('\n')[0]);
      }
    }
  }

  await browser.close();

  fs.writeFileSync(path.join(OUT_DIR, 'flow.json'), JSON.stringify(found, null, 2));

  const bySection = {};
  for (const f of found) {
    bySection[f.section] = bySection[f.section] || [];
    bySection[f.section].push(f);
  }
  const md = [
    '# User Site Screen Flow',
    '',
    `Screens captured: ${found.length}`,
    '',
    '## Ghi chú quan trọng',
    '',
    '- Các luồng đặt vé (`/booking/*`) chỉ đi sâu **1 bước** để tránh chạm vào form thanh toán thật (GMO Payment) — không nhập thẻ, không submit thanh toán.',
    '',
    ...Object.entries(bySection).flatMap(([section, items]) => [
      `## ${section}`,
      '',
      ...items.map((it) => `- **${it.kind}** (${it.label}) — \`${new URL(it.url).pathname}\` — ![](${it.screenshot})`),
      '',
    ]),
  ].join('\n');
  fs.writeFileSync(path.join(OUT_DIR, 'flow.md'), md);
  console.log('\nDone. Output at', OUT_DIR);
})();
