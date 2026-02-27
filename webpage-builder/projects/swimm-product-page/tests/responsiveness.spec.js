// @ts-check
const { test, expect } = require('@playwright/test');
const path = require('path');

// ============================================================
// CUSTOMIZE PER PROJECT — Swimm Product Page
// ============================================================

const PAGE_PATH = '../src/index.html';
const PAGE_URL = `file://${path.resolve(__dirname, PAGE_PATH)}`;

const SECTIONS = [
  '.hero',
  '.app-map',
  '.bre-flows',
  '.glossary-collections',
  '.context-ai',
  '.governance',
  '.enterprise',
  '.conversion',
];

const CTA_SELECTORS = [
  '.hero .btn-primary',
  '.mid-cta .btn-ghost',
  '.governance-cta .btn-ghost-light',
  '.conversion .btn-primary-lg',
];

const GRID_SECTIONS = [
  { selector: '.persona-cards', childSelector: '.persona-card', expectedColumns: 3 },
  { selector: '.enterprise-deploy', childSelector: '.enterprise-card', expectedColumns: 2 },
  { selector: '.enterprise-integrations', childSelector: '.integration-card', expectedColumns: 2 },
];

// Grids that go to 2-column on mobile (not single-column)
const TWO_COL_MOBILE_GRIDS = [
  { selector: '.governance-grid', childSelector: '.governance-item', expectedDesktopColumns: 5 },
];

const SUBGRID_SECTIONS = [];

const SIDE_BY_SIDE_SECTIONS = [
  { name: 'Glossary & Collections', textSelector: '.split-block .feature-block:first-child', graphicSelector: '.split-block .feature-block:last-child' },
];

// ============================================================
// END CUSTOMIZE
// ============================================================

const VIEWPORTS = {
  mobile: { width: 375, height: 812 },
  tablet: { width: 768, height: 1024 },
  desktop: { width: 1280, height: 900 },
  largeDesktop: { width: 1920, height: 1080 },
  ultrawide: { width: 2560, height: 1440 },
};

// ============================================================
// STRUCTURAL: All sections render at every viewport
// ============================================================

for (const [name, size] of Object.entries(VIEWPORTS)) {
  test(`All sections render at ${name} (${size.width}x${size.height})`, async ({ page }) => {
    await page.setViewportSize(size);
    await page.goto(PAGE_URL);

    for (const selector of SECTIONS) {
      const el = page.locator(selector);
      await expect(el).toBeVisible();
    }
  });
}

// ============================================================
// NO HORIZONTAL SCROLL at any viewport
// ============================================================

for (const [name, size] of Object.entries(VIEWPORTS)) {
  test(`No horizontal scroll at ${name} (${size.width}px)`, async ({ page }) => {
    await page.setViewportSize(size);
    await page.goto(PAGE_URL);

    const canScroll = await page.evaluate(() => {
      window.scrollTo({ left: 10000, behavior: 'instant' });
      const scrolled = window.scrollX > 0;
      window.scrollTo({ left: 0, behavior: 'instant' });
      return scrolled;
    });
    expect(canScroll).toBe(false);
  });
}

// ============================================================
// GRID ALIGNMENT: Columns at desktop, stack on mobile
// ============================================================

for (const grid of GRID_SECTIONS) {
  test(`${grid.selector}: ${grid.expectedColumns}-column grid at desktop`, async ({ page }) => {
    await page.setViewportSize(VIEWPORTS.desktop);
    await page.goto(PAGE_URL);

    const boxes = await page.locator(grid.childSelector).evaluateAll(els =>
      els.map(el => el.getBoundingClientRect())
    );

    // First row items should be on the same row (same top within tolerance)
    const firstRowTops = boxes.slice(0, grid.expectedColumns).map(b => b.top);
    const maxDiff = Math.max(...firstRowTops) - Math.min(...firstRowTops);
    expect(maxDiff).toBeLessThanOrEqual(2);
  });

  test(`${grid.selector}: stacks on mobile`, async ({ page }) => {
    await page.setViewportSize(VIEWPORTS.mobile);
    await page.goto(PAGE_URL);

    const boxes = await page.locator(grid.childSelector).evaluateAll(els =>
      els.map(el => el.getBoundingClientRect())
    );

    // All items single column — each top >= previous bottom
    for (let i = 1; i < boxes.length; i++) {
      expect(boxes[i].top).toBeGreaterThanOrEqual(boxes[i - 1].bottom - 1);
    }
  });
}

// ============================================================
// 2-COLUMN MOBILE GRIDS: Multi-col desktop, 2-col mobile
// ============================================================

for (const grid of TWO_COL_MOBILE_GRIDS) {
  test(`${grid.selector}: ${grid.expectedDesktopColumns}-column grid at desktop`, async ({ page }) => {
    await page.setViewportSize(VIEWPORTS.desktop);
    await page.goto(PAGE_URL);

    const boxes = await page.locator(grid.childSelector).evaluateAll(els =>
      els.map(el => el.getBoundingClientRect())
    );

    const firstRowTops = boxes.slice(0, grid.expectedDesktopColumns).map(b => b.top);
    const maxDiff = Math.max(...firstRowTops) - Math.min(...firstRowTops);
    expect(maxDiff).toBeLessThanOrEqual(2);
  });

  test(`${grid.selector}: 2-column grid on mobile`, async ({ page }) => {
    await page.setViewportSize(VIEWPORTS.mobile);
    await page.goto(PAGE_URL);

    const boxes = await page.locator(grid.childSelector).evaluateAll(els =>
      els.map(el => el.getBoundingClientRect())
    );

    // First two items should be on the same row (2-column)
    if (boxes.length >= 2) {
      const topDiff = Math.abs(boxes[0].top - boxes[1].top);
      expect(topDiff).toBeLessThanOrEqual(2);
    }
  });
}

// ============================================================
// SIDE-BY-SIDE: Desktop layout + mobile stacking
// ============================================================

for (const section of SIDE_BY_SIDE_SECTIONS) {
  test(`${section.name}: side-by-side layout at desktop`, async ({ page }) => {
    await page.setViewportSize(VIEWPORTS.desktop);
    await page.goto(PAGE_URL);

    const textBox = await page.locator(section.textSelector).evaluate(el => el.getBoundingClientRect());
    const graphicBox = await page.locator(section.graphicSelector).evaluate(el => el.getBoundingClientRect());

    // Graphic should be to the right of text
    expect(graphicBox.left).toBeGreaterThan(textBox.left);
  });

  test(`${section.name}: stacks vertically on mobile`, async ({ page }) => {
    await page.setViewportSize(VIEWPORTS.mobile);
    await page.goto(PAGE_URL);

    const textBox = await page.locator(section.textSelector).evaluate(el => el.getBoundingClientRect());
    const graphicBox = await page.locator(section.graphicSelector).evaluate(el => el.getBoundingClientRect());

    expect(graphicBox.top).toBeGreaterThanOrEqual(textBox.bottom - 1);
  });
}

// ============================================================
// CTA BUTTONS: All CTA moments visible at desktop
// ============================================================

test('All CTA buttons are present and visible at desktop', async ({ page }) => {
  await page.setViewportSize(VIEWPORTS.desktop);
  await page.goto(PAGE_URL);

  for (const selector of CTA_SELECTORS) {
    const cta = page.locator(selector);
    await expect(cta).toHaveCount(1);
  }
});

// ============================================================
// TABLET BREAKPOINT: Font size reduction
// ============================================================

test('Font sizes reduce at tablet breakpoint (1024px)', async ({ page }) => {
  await page.setViewportSize({ width: 1024, height: 768 });
  await page.goto(PAGE_URL);

  const fontSize = await page.locator('.hero h1').evaluate(el =>
    parseInt(window.getComputedStyle(el).fontSize)
  );
  // At tablet, headline should be reduced (2.75rem = 44px)
  expect(fontSize).toBeLessThanOrEqual(48);
});

// ============================================================
// TAB SWITCHING: Business Rules / Execution Paths
// ============================================================

test('Tab switching works correctly', async ({ page }) => {
  await page.setViewportSize(VIEWPORTS.desktop);
  await page.goto(PAGE_URL);

  // Business Rules tab is active by default
  const rulesPanel = page.locator('#panel-rules');
  const flowsPanel = page.locator('#panel-flows');
  await expect(rulesPanel).toBeVisible();

  // Click Execution Paths tab
  await page.click('#tab-flows');
  await expect(flowsPanel).toBeVisible();
  await expect(rulesPanel).not.toBeVisible();

  // Click back to Business Rules
  await page.click('#tab-rules');
  await expect(rulesPanel).toBeVisible();
  await expect(flowsPanel).not.toBeVisible();
});

// ============================================================
// DARK/LIGHT SECTION RHYTHM
// ============================================================

test('Section background colors follow dark/light rhythm', async ({ page }) => {
  await page.setViewportSize(VIEWPORTS.desktop);
  await page.goto(PAGE_URL);

  const backgrounds = await page.evaluate(() => {
    const sections = [
      '.hero',
      '.app-map',
      '.bre-flows',
      '.glossary-collections',
      '.ai-governance-unit',
      '.enterprise',
      '.conversion',
    ];
    return sections.map(sel => {
      const el = document.querySelector(sel);
      return el ? window.getComputedStyle(el).backgroundColor : null;
    });
  });

  // Navy = rgb(10, 22, 40), White = rgb(255, 255, 255), Cool Gray = rgb(247, 248, 250)
  expect(backgrounds[0]).toBe('rgb(10, 22, 40)');   // Hero: Navy
  expect(backgrounds[1]).toBe('rgb(255, 255, 255)'); // App Map: White
  expect(backgrounds[2]).toBe('rgb(247, 248, 250)'); // BRE: Cool Gray
  expect(backgrounds[3]).toBe('rgb(255, 255, 255)'); // Glossary: White
  expect(backgrounds[4]).toBe('rgb(10, 22, 40)');   // AI+Gov: Navy
  expect(backgrounds[5]).toBe('rgb(247, 248, 250)'); // Enterprise: Cool Gray
  expect(backgrounds[6]).toBe('rgb(10, 22, 40)');   // Conversion: Navy
});

// ============================================================
// SCREENSHOTS at 1440px for review
// ============================================================

test('screenshot at 1440px desktop', async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto(PAGE_URL);
  await page.screenshot({ path: 'test-results/desktop-1440.png', fullPage: true });
});

test('screenshot at 375px mobile', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 812 });
  await page.goto(PAGE_URL);
  await page.screenshot({ path: 'test-results/mobile-375.png', fullPage: true });
});
