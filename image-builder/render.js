/**
 * Render HTML template to optimized PNG/WebP
 * - Replaces {{PLACEHOLDERS}} in HTML
 * - Screenshots via Puppeteer at exact dimensions
 * - Optimizes with sharp (lossless compression)
 */

const puppeteer = require('puppeteer-core');
const sharp = require('sharp');
const fs = require('fs');
const path = require('path');
const YAML = require('yaml');
const { extractPDFFirstPage } = require('./pdf-to-image');

async function renderImage(htmlContent, options = {}) {
  const {
    width = 1206,
    height = 1562,
    format = 'webp',              // 'webp' or 'png'
    lossless = true,
    background = 'transparent',    // 'transparent' or hex color
    outputPath = null,
    placeholders = {}              // { '{{KEY}}': value }
  } = options;

  // Replace placeholders in HTML
  let html = htmlContent;
  for (const [key, value] of Object.entries(placeholders)) {
    html = html.replaceAll(key, value || '');
  }

  // Wrap in minimal HTML if not already a full document
  if (!html.includes('<html')) {
    html = `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { width: ${width}px; height: ${height}px; }
  </style>
</head>
<body>
${html}
</body>
</html>`;
  }

  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  try {
    const page = await browser.newPage();

    // Set viewport
    await page.setViewport({ width, height });

    // Set HTML content
    await page.setContent(html, { waitUntil: 'networkidle0', timeout: 30000 });

    // Wait for fonts (TypeKit, Google Fonts)
    try {
      await page.evaluate(() => {
        return new Promise((resolve) => {
          if (document.fonts && document.fonts.ready) {
            document.fonts.ready.then(resolve);
          } else {
            setTimeout(resolve, 1000);
          }
        });
      });
    } catch (e) {
      // Continue on font load timeout
    }

    // Screenshot
    const screenshotOptions = {
      type: 'png'
    };

    if (background === 'transparent') {
      screenshotOptions.omitBackground = true;
    } else if (background.startsWith('#')) {
      // For opaque backgrounds, set via CSS
      await page.evaluate((bgColor) => {
        document.body.style.backgroundColor = bgColor;
      }, background);
      screenshotOptions.omitBackground = false;
    }

    const pngBuffer = await page.screenshot(screenshotOptions);

    // Optimize with sharp
    let output = sharp(pngBuffer);

    if (format === 'webp') {
      output = output.webp({ lossless });
    } else if (format === 'png') {
      output = output.png({ compressionLevel: 9 });
    }

    const optimized = await output.toBuffer();

    // Write to file if path provided
    if (outputPath) {
      const outPath = path.resolve(outputPath);
      fs.mkdirSync(path.dirname(outPath), { recursive: true });
      fs.writeFileSync(outPath, optimized);
      return { success: true, path: outPath, size: optimized.length, format };
    }

    return { success: true, buffer: optimized, size: optimized.length, format };
  } finally {
    await browser.close();
  }
}

/**
 * High-level function: template + inputs → rendered image
 * Supports: PDF + template, HTML file direct, or placeholder-based templates
 */
async function renderImageFromTemplate(templatePath, inputsObject, outputPath) {
  // Read template metadata (YAML → JSON)
  const metadataPath = path.join(path.dirname(templatePath), 'template.yaml');
  const metadata = fs.existsSync(metadataPath) ? parseYAML(fs.readFileSync(metadataPath, 'utf-8')) : {};

  // Read template HTML
  const htmlContent = fs.readFileSync(templatePath, 'utf-8');

  // Build placeholders for template substitution
  let placeholders = {};

  // If template requires PDF extraction, do it
  if (metadata.inputs?.pdf_first_page && inputsObject.pdf_path) {
    try {
      const { base64 } = await extractPDFFirstPage(inputsObject.pdf_path);
      placeholders['{{PDF_FIRST_PAGE_BASE64}}'] = base64;
    } catch (err) {
      throw new Error(`Failed to extract PDF: ${err.message}`);
    }
  }

  // Render
  return await renderImage(htmlContent, {
    width: metadata.output?.width || 1206,
    height: metadata.output?.height || 1562,
    format: metadata.output?.format || 'webp',
    lossless: metadata.output?.lossless !== false,
    background: metadata.output?.background || 'transparent',
    outputPath,
    placeholders
  });
}

/**
 * Parse YAML template metadata
 */
function parseYAML(content) {
  try {
    return YAML.parse(content);
  } catch (err) {
    console.error('YAML parse error:', err);
    return {};
  }
}

// CLI usage: node render.js <template-path> <output-path> [--pdf <pdf-path>] [--format webp|png]
if (require.main === module) {
  const args = process.argv.slice(2);
  const templatePath = args[0];
  const outputPath = args[1];
  const pdfIndex = args.indexOf('--pdf');
  const pdfPath = pdfIndex !== -1 ? args[pdfIndex + 1] : null;
  const formatIndex = args.indexOf('--format');
  const format = formatIndex !== -1 ? args[formatIndex + 1] : 'webp';

  if (!templatePath || !outputPath) {
    console.error('Usage: node render.js <template-path> <output-path> [--pdf <pdf-path>] [--format webp|png]');
    process.exit(1);
  }

  renderImageFromTemplate(templatePath, {
    pdf_path: pdfPath,
    format
  }, outputPath)
    .then((result) => {
      console.log(JSON.stringify(result));
    })
    .catch((err) => {
      console.error(JSON.stringify({ success: false, error: err.message }));
      process.exit(1);
    });
}

module.exports = { renderImage, renderImageFromTemplate };
