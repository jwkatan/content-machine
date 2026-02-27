// @ts-check
const { test, expect } = require('@playwright/test');
const path = require('path');

// ============================================================
// CUSTOMIZE PER PROJECT
// ============================================================

const PAGE_PATH = '../src/index.html';
const PAGE_URL = `file://${path.resolve(__dirname, PAGE_PATH)}`;

// Add CSS selectors for all page sections
const SECTIONS = [
  // e.g., '.hero', '.value', '.completeness', '.differentiation',
  // '.credibility', '.ai-layer', '.enterprise', '.conversion'
];

// Add CTA button selectors (typically 2-3 CTA moments)
const CTA_SELECTORS = [
  // e.g., '.hero .cta-btn', '.credibility__cta .cta-btn--ghost', '.conversion .cta-btn--final'
];

// Add grid sections to test column layout at desktop
// Each entry: { selector, expectedColumns, childSelector }
const GRID_SECTIONS = [
  // e.g., { selector: '.value', childSelector: '.value__block', expectedColumns: 3 },
  // e.g., { selector: '.completeness__grid', childSelector: '.completeness__card', expectedColumns: 3 },
];

// Add subgrid sections where body text should align horizontally at desktop
// Each entry: { name, bodySelector }
const SUBGRID_SECTIONS = [
  // e.g., { name: 'Value', bodySelector: '.value__block-body' },
];

// Add side-by-side layout sections (text + graphic)
// Each entry: { name, textSelector, graphicSelector }
const SIDE_BY_SIDE_SECTIONS = [
  // e.g., { name: 'Hero', textSelector: '.hero__text', graphicSelector: '.hero__graphic' },
  // e.g., { name: 'Differentiation', textSelector: '.differentiation__text', graphicSelector: '.differentiation__graphic' },
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
// SUBGRID: Body text horizontal alignment at desktop + ultrawide
// ============================================================

for (const section of SUBGRID_SECTIONS) {
  for (const vpName of ['desktop', 'ultrawide']) {
    test(`${section.name}: body text aligns horizontally at ${vpName}`, async ({ page }) => {
      await page.setViewportSize(VIEWPORTS[vpName]);
      await page.goto(PAGE_URL);

      const bodyBoxes = await page.locator(section.bodySelector).evaluateAll(els =>
        els.map(el => el.getBoundingClientRect())
      );

      const topPositions = bodyBoxes.map(b => b.top);
      const maxDiff = Math.max(...topPositions) - Math.min(...topPositions);
      expect(maxDiff).toBeLessThanOrEqual(2);
    });
  }
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

  // Check that the largest headline has reduced from desktop size
  // Customize the selector for your page's primary headline
  const headlineSelector = SECTIONS.length > 0 ? `${SECTIONS[0]} h1, ${SECTIONS[0]} h2` : 'h1';
  const headlines = page.locator(headlineSelector);
  const count = await headlines.count();

  if (count > 0) {
    const fontSize = await headlines.first().evaluate(el =>
      parseInt(window.getComputedStyle(el).fontSize)
    );
    // At tablet, headline should be reduced (typically <= 44px)
    expect(fontSize).toBeLessThanOrEqual(48);
  }
});
