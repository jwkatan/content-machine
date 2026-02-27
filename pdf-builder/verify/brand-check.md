# Brand Verification Checklist

Run this checklist after generating the PDF. Every item must pass before the output is considered brand-approved.

Also run the automated color checker:
```bash
node verify/brand-check.js reference/template.html
# or point at your own HTML output
```

---

## 1. PDF dimensions and structure

- [ ] PDF opens at A4 size (210mm × 297mm / 8.27" × 11.69")
- [ ] Zero visible margins — content bleeds to page edge
- [ ] Page count matches content (cover + body pages + back cover)
- [ ] No pages are blank, cut off, or overflowing

---

## 2. Cover page

- [ ] White background with a subtle square grid (light blue `#E8EAFF` lines, ~7mm cells)
- [ ] Two gradient fades visible — white softening the grid at top and bottom
- [ ] Swimm logo in top-left corner, not stretched (correct aspect ratio)
- [ ] "Whitepaper" label in Mulish Regular above the title
- [ ] Title renders in two lines: first line **bold**, second line regular weight — both same size
- [ ] Title color is dark charcoal `#1D1E2B`, not black
- [ ] Swimm ✳ asterisk icon visible below the title block
- [ ] Wave illustration visible in the lower half of the page
- [ ] No bleed or overflow from the wave image

---

## 3. Body pages

- [ ] White background
- [ ] Thin indigo stripe at the very top of each body page (color `#5E6EFF`)
- [ ] Chapter heading in Roc Grotesk Bold — noticeably larger than body text
- [ ] Body text in Mulish — readable at ~12pt
- [ ] Content does not overflow below the footer divider
- [ ] Swimm logo in footer (bottom-left), correctly sized (not stretched)
- [ ] Page number in bottom-right, muted blue `#8D98FF`
- [ ] Thin divider line above footer (`#D7DBFF`)

**Callout box (if present):**
- [ ] Indigo `#5E6EFF` left border (3pt wide)
- [ ] Light blue `#E4E7FF` background fill
- [ ] Text in Roc Grotesk Bold

**Stats row (if present):**
- [ ] Tiles sit side-by-side (flex row)
- [ ] Large stat value in indigo `#5E6EFF`
- [ ] Background of each tile is `#F4F6FA` (very light grey)
- [ ] No more than 3 tiles per row

**Table (if present):**
- [ ] Header row has `#E4E7FF` background
- [ ] All borders are `#D7DBFF` (light lavender)
- [ ] Header text noticeably bolder than cell text

**Graphic placeholder (if present):**
- [ ] `#E4E7FF` background
- [ ] Small uppercase label centered inside

---

## 4. Back cover

- [ ] Dark charcoal background `#1D1E2B` — not black
- [ ] Swimm logo centered, rendered in white (inverted from dark SVG)
- [ ] Tagline text in white, Mulish Regular, centered
- [ ] CTA button: indigo `#5E6EFF`, rounded corners, white Roc Grotesk Bold text
- [ ] Decorative hand/cursor icon visible overlapping the button
- [ ] No other content — clean, minimal

---

## 5. Typography spot-check

Open the PDF in a viewer that shows font info (e.g., Adobe Acrobat → Properties → Fonts):
- [ ] Heading font present: `RocGrotesk` (or `roc-grotesk`)
- [ ] Body font present: `Mulish`
- [ ] No system fallback fonts (Arial, Helvetica, Times) unless Roc Grotesk is unavailable

*Note: Roc Grotesk loads via Adobe Fonts TypeKit and requires internet during PDF generation. If generated offline, the heading font may fall back to sans-serif — this is a known limitation.*

---

## 6. Color spot-check

Run the automated checker:
```bash
node verify/brand-check.js your-template.html
```

Then visually confirm:
- [ ] No bright red, green, or orange anywhere (these are not in the Swimm palette)
- [ ] Blues are cool-toned indigo, not sky blue or royal blue
- [ ] Dark areas use `#1D1E2B` charcoal, not pure `#000000` black
- [ ] Light grey areas use `#F4F6FA`, not pure `#FFFFFF` white

---

## 7. Final export check

- [ ] PDF file size is reasonable (under 10MB for a text-heavy whitepaper)
- [ ] File opens without errors in Preview, Chrome, and Adobe Reader
- [ ] Text in the PDF is selectable (not rasterized)
- [ ] Images/graphics appear sharp, not blurry
