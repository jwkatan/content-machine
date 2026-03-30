/**
 * Extract first page of PDF as image (PNG or base64)
 * Uses ImageMagick (convert) to extract PDF page directly (no browser UI chrome)
 */

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

async function extractPDFFirstPage(pdfPath, options = {}) {
  const {
    format = 'base64',  // 'base64' or 'file'
    outputPath = null,  // if format=file, where to save
    scale = 2,          // render scale (2x for crisp quality)
    width = 788,        // first-page area width (card inner width)
    height = 954        // first-page area height (card inner height)
  } = options;

  // Resolve PDF path
  const absPath = path.resolve(pdfPath);
  if (!fs.existsSync(absPath)) {
    throw new Error(`PDF not found: ${absPath}`);
  }

  try {
    // Use ImageMagick's convert command to extract first page at native aspect ratio
    // -density: resolution (higher = better quality)
    // [0]: first page only
    // No resize - let CSS object-fit: cover handle the cropping in the template
    const density = 150 * scale;
    const tmpFile = path.join(os.tmpdir(), `pdf-extract-${Date.now()}.png`);

    // Render PDF at full resolution without forcing dimensions
    // This preserves the native aspect ratio
    const cmd = `convert -density ${density} "${absPath}[0]" "${tmpFile}"`;

    execSync(cmd, { stdio: 'pipe' });

    if (!fs.existsSync(tmpFile)) {
      throw new Error('ImageMagick conversion failed');
    }

    // Read the converted PNG
    const pngBuffer = fs.readFileSync(tmpFile);
    fs.unlinkSync(tmpFile); // Clean up temp file

    // Just optimize with sharp, don't resize
    // Template CSS (object-fit: cover) will handle fitting to 788x954
    const sharp = require('sharp');
    const optimized = await sharp(pngBuffer)
      .toBuffer();

    if (format === 'file' && outputPath) {
      const outPath = path.resolve(outputPath);
      fs.writeFileSync(outPath, optimized);
      return { success: true, path: outPath, size: optimized.length };
    } else if (format === 'base64') {
      const base64 = optimized.toString('base64');
      return { success: true, base64: `data:image/png;base64,${base64}`, size: optimized.length };
    } else {
      return { success: true, buffer: optimized, size: optimized.length };
    }
  } catch (err) {
    throw new Error(`PDF extraction failed: ${err.message}`);
  }
}

// CLI usage: node pdf-to-image.js <pdf-path> [output-file]
if (require.main === module) {
  const pdfPath = process.argv[2];
  const outputFile = process.argv[3];

  if (!pdfPath) {
    console.error('Usage: node pdf-to-image.js <pdf-path> [output-file]');
    process.exit(1);
  }

  extractPDFFirstPage(pdfPath, {
    format: outputFile ? 'file' : 'base64',
    outputPath: outputFile
  })
    .then((result) => {
      if (outputFile) {
        console.log(JSON.stringify({ success: true, path: result.path, size: result.size }));
      } else {
        // Return base64 data URL for use in HTML
        console.log(JSON.stringify({ success: true, base64: result.base64, size: result.size }));
      }
    })
    .catch((err) => {
      console.error(JSON.stringify({ success: false, error: err.message }));
      process.exit(1);
    });
}

module.exports = { extractPDFFirstPage };
