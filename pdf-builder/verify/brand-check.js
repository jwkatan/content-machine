#!/usr/bin/env node
/**
 * brand-check.js — Whitepaper brand compliance checker
 *
 * Usage:
 *   node verify/brand-check.js reference/template.html
 *   node verify/brand-check.js path/to/your/output.html
 *
 * Checks:
 *   1. All hex colors are in the approved palette
 *   2. Required font families are declared
 *   3. Page size is set to A4
 *   4. print-color-adjust is set (backgrounds will print)
 */

const fs = require('fs');
const path = require('path');

// ─── Approved color palette ────────────────────────────────────────────────
const APPROVED_COLORS = new Set([
  // Blues
  '#1f35ff', '#4154ff', '#5e6eff', '#8d98ff', '#e4e7ff',
  // Yellows
  '#fdf150', '#fff78e',
  // Neutrals
  '#1d1e2b', '#2f3142', '#696b80', '#f4f6fa', '#ffffff',
  // Off-palette exceptions (documented in BRIEF.md)
  '#d7dbff',  // table borders, body divider
  '#e8eaff',  // cover page grid
  '#e2e5ed',  // page-footer border (in designer's styles.css)
  // Transparency / rgba variants — skip (handled separately)
]);

// Colors only used as rgba() — allowed but not checked against palette
const RGBA_PATTERN = /rgba\([^)]+\)/gi;

// ─── Required CSS strings ─────────────────────────────────────────────────
const REQUIRED_CHECKS = [
  {
    label: 'Roc Grotesk font declared',
    pattern: /roc-grotesk/i,
    failMsg: 'Missing roc-grotesk font declaration. Headings must use Roc Grotesk.',
  },
  {
    label: 'Mulish font declared',
    pattern: /mulish/i,
    failMsg: "Missing Mulish font declaration. Body text must use Mulish.",
  },
  {
    label: 'A4 page size set',
    pattern: /size:\s*A4/i,
    failMsg: 'Missing @page { size: A4 }. Page dimensions must be A4.',
  },
  {
    label: 'print-color-adjust: exact set',
    pattern: /print-color-adjust:\s*exact/i,
    failMsg: 'Missing print-color-adjust: exact. Background colors will be stripped from PDF.',
  },
];

// ─── Helpers ──────────────────────────────────────────────────────────────
function normaliseHex(hex) {
  // Expand shorthand #abc → #aabbcc
  if (/^#[0-9a-f]{3}$/i.test(hex)) {
    return '#' + hex[1] + hex[1] + hex[2] + hex[2] + hex[3] + hex[3];
  }
  return hex.toLowerCase();
}

function extractHexColors(source) {
  // Remove rgba() blocks first so their hex-like args don't get flagged
  const stripped = source.replace(RGBA_PATTERN, 'rgba(...)');
  const matches = stripped.match(/#[0-9a-fA-F]{3,6}\b/g) || [];
  return [...new Set(matches.map(normaliseHex))];
}

// ─── Main ─────────────────────────────────────────────────────────────────
function run(filePath) {
  if (!filePath) {
    console.error('Usage: node verify/brand-check.js <path-to-html>');
    process.exit(1);
  }

  const absPath = path.resolve(filePath);
  if (!fs.existsSync(absPath)) {
    console.error(`File not found: ${absPath}`);
    process.exit(1);
  }

  const source = fs.readFileSync(absPath, 'utf-8');
  let violations = 0;
  let warnings = 0;

  console.log(`\nBrand Checker — ${path.basename(absPath)}`);
  console.log('─'.repeat(60));

  // ── 1. Color check ──────────────────────────────────────────────────────
  console.log('\n[1] Color palette check');
  const hexColors = extractHexColors(source);
  const unknownColors = hexColors.filter(c => !APPROVED_COLORS.has(c));

  if (unknownColors.length === 0) {
    console.log('  ✓  All hex colors are in the approved palette');
  } else {
    unknownColors.forEach(color => {
      console.log(`  ✗  Off-palette color: ${color}`);
      violations++;
    });
    console.log(`\n  Approved palette for reference:`);
    [...APPROVED_COLORS].forEach(c => console.log(`       ${c}`));
  }

  // ── 2. Required strings ────────────────────────────────────────────────
  console.log('\n[2] Required declarations check');
  REQUIRED_CHECKS.forEach(({ label, pattern, failMsg }) => {
    if (pattern.test(source)) {
      console.log(`  ✓  ${label}`);
    } else {
      console.log(`  ✗  ${label}`);
      console.log(`     → ${failMsg}`);
      violations++;
    }
  });

  // ── 3. Expiring asset URL warning ──────────────────────────────────────
  console.log('\n[3] Asset URL check');
  const expiringPattern = /figma\.com\/api\/mcp\/asset\//g;
  const expiringMatches = source.match(expiringPattern);
  if (expiringMatches && expiringMatches.length > 0) {
    console.log(`  ⚠️  ${expiringMatches.length} expiring Figma asset URL(s) found`);
    console.log(`     → These expire in ~7 days. Re-fetch from Figma node 3614:4`);
    console.log(`       (fileKey: UYfMt04X79c7y7YXAhy3DI) before final delivery.`);
    warnings++;
  } else {
    console.log('  ✓  No expiring Figma asset URLs detected');
  }

  // ── 4. Summary ─────────────────────────────────────────────────────────
  console.log('\n' + '─'.repeat(60));
  if (violations === 0 && warnings === 0) {
    console.log('PASS — No violations found. Output is brand-compliant.\n');
  } else if (violations === 0) {
    console.log(`PASS with warnings — 0 violations, ${warnings} warning(s).\n`);
  } else {
    console.log(`FAIL — ${violations} violation(s), ${warnings} warning(s).\n`);
    console.log('Fix all violations before delivering the final PDF.\n');
    process.exit(1);
  }
}

run(process.argv[2]);
