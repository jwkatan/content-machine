const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

/**
 * Branded PDF generator.
 *
 * Usage:
 *   node generate-pdf.js <input.html> [output.pdf]
 *
 * If output path is omitted, writes to input filename with .pdf extension.
 */
async function generatePDF(inputPath, outputPath) {
  const absInput = path.resolve(inputPath);

  if (!fs.existsSync(absInput)) {
    console.error(`Error: HTML file not found: ${absInput}`);
    process.exit(1);
  }

  if (!outputPath) {
    outputPath = absInput.replace(/\.html$/, '.pdf');
  }
  const absOutput = path.resolve(outputPath);

  console.log('Launching Chromium...');
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  const page = await browser.newPage();

  console.log(`Loading ${path.basename(absInput)}...`);
  await page.goto(`file://${absInput}`, {
    waitUntil: 'networkidle0',
    timeout: 30_000,
  });

  // Wait for web fonts (Roc Grotesk via TypeKit + Mulish via Google Fonts)
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 800));

  console.log('Rendering PDF...');
  await page.pdf({
    path: absOutput,
    format: 'A4',
    printBackground: true,
    preferCSSPageSize: true,
    margin: { top: 0, right: 0, bottom: 0, left: 0 },
  });

  await browser.close();
  console.log(`\n✓  PDF saved → ${absOutput}`);
}

// CLI entry point
const args = process.argv.slice(2);
if (args.length === 0) {
  console.error('Usage: node generate-pdf.js <input.html> [output.pdf]');
  process.exit(1);
}

generatePDF(args[0], args[1]).catch(err => {
  console.error('PDF generation failed:', err);
  process.exit(1);
});
