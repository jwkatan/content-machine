/**
 * Google Slides Publisher - Apps Script Web App
 *
 * Creates branded presentations by duplicating a template and filling
 * placeholder tokens. Deployed as a web app, called via HTTP POST.
 *
 * Script Properties required:
 *   API_KEY - shared secret for authentication
 *
 * OAuth scopes required:
 *   https://www.googleapis.com/auth/presentations
 *   https://www.googleapis.com/auth/drive
 */

// ============================================================
// Entry points
// ============================================================

function doGet() {
  return ContentService.createTextOutput(JSON.stringify({
    service: "Content Machine Slides Publisher",
    version: "1.0",
    actions: ["create", "update", "status", "template"]
  })).setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  try {
    var payload = JSON.parse(e.postData.contents);

    // Authenticate
    var storedKey = PropertiesService.getScriptProperties().getProperty("API_KEY");
    if (!storedKey || payload.key !== storedKey) {
      return jsonResponse({ error: "Unauthorized" }, 401);
    }

    var action = payload.action;
    if (action === "create") return handleCreate(payload);
    if (action === "update") return handleUpdate(payload);
    if (action === "status") return handleStatus();
    if (action === "template") return handleTemplate(payload);
    if (action === "tokenize") return handleTokenize(payload);
    if (action === "share") return handleShare(payload);
    if (action === "reposition") return handleReposition(payload);

    return jsonResponse({ error: "Unknown action: " + action });
  } catch (err) {
    Logger.log("Error: " + err.message + "\n" + err.stack);
    return jsonResponse({ error: err.message });
  }
}

// ============================================================
// Action handlers
// ============================================================

/**
 * Create a new presentation by duplicating the template and filling tokens.
 *
 * Payload: { action: "create", key, title, templateId, slides: [...] }
 *
 * Each slide: { layout: "LAYOUT_NAME", tokens: { TOKEN: "value" }, speakerNotes: "..." }
 */
function handleCreate(payload) {
  var templateId = payload.templateId;
  var title = payload.title || "Untitled Presentation";
  var slideSpecs = payload.slides || [];

  // 1. Duplicate the template
  var copy = DriveApp.getFileById(templateId).makeCopy(title);
  var presentationId = copy.getId();
  var presentation = SlidesApp.openById(presentationId);

  // 2. Get all slides from the duplicated deck
  var slides = presentation.getSlides();

  // 3. Build a map of layout name -> slide index from the template
  var layoutMap = buildLayoutMap(slides);

  // 4. Track which template slides are used
  var usedIndices = {};

  // 5. Process each slide spec
  for (var i = 0; i < slideSpecs.length; i++) {
    var spec = slideSpecs[i];
    if (spec.skip) continue;

    var layoutName = spec.layout;
    if (!(layoutName in layoutMap)) {
      // Layout not found -- skip with warning
      Logger.log("Warning: layout '" + layoutName + "' not found in template");
      continue;
    }

    var slideIndex = layoutMap[layoutName];
    usedIndices[slideIndex] = true;
    var slide = slides[slideIndex];

    // Replace tokens
    if (spec.tokens) {
      replaceTokens(slide, spec.tokens);
    }

    // Add speaker notes
    if (spec.speakerNotes) {
      setSpeakerNotes(slide, spec.speakerNotes);
    }
  }

  // 6. Handle slide ordering: duplicate used slides in spec order, then remove originals
  reorderSlides(presentation, slides, slideSpecs, layoutMap);

  // 7. Track the presentation
  var props = PropertiesService.getScriptProperties();
  var key = "pres_" + sanitizeKey(title);
  props.setProperty(key, presentationId);

  return jsonResponse({
    presentationId: presentationId,
    url: "https://docs.google.com/presentation/d/" + presentationId + "/edit",
    title: title,
    slidesCreated: slideSpecs.filter(function(s) { return !s.skip; }).length
  });
}

/**
 * Update tokens in an existing presentation.
 *
 * Payload: { action: "update", key, presentationId, slides: [...] }
 *
 * Each slide: { slideIndex: 0, tokens: { TOKEN: "value" }, speakerNotes: "..." }
 */
function handleUpdate(payload) {
  var presentationId = payload.presentationId;
  var slideSpecs = payload.slides || [];

  var presentation = SlidesApp.openById(presentationId);
  var slides = presentation.getSlides();

  var updated = 0;
  for (var i = 0; i < slideSpecs.length; i++) {
    var spec = slideSpecs[i];
    var idx = spec.slideIndex;
    if (idx < 0 || idx >= slides.length) continue;

    var slide = slides[idx];
    if (spec.tokens) {
      replaceTokens(slide, spec.tokens);
    }
    if (spec.speakerNotes) {
      setSpeakerNotes(slide, spec.speakerNotes);
    }
    updated++;
  }

  return jsonResponse({
    presentationId: presentationId,
    slidesUpdated: updated
  });
}

/**
 * List all tracked presentations.
 */
function handleStatus() {
  var props = PropertiesService.getScriptProperties().getProperties();
  var presentations = [];

  for (var key in props) {
    if (key.indexOf("pres_") === 0) {
      var name = key.substring(5);
      presentations.push({
        name: name,
        presentationId: props[key],
        url: "https://docs.google.com/presentation/d/" + props[key] + "/edit"
      });
    }
  }

  return jsonResponse({ presentations: presentations });
}

/**
 * Analyze the template and return layout information.
 *
 * Payload: { action: "template", key, templateId }
 */
function handleTemplate(payload) {
  var templateId = payload.templateId;
  var presentation = SlidesApp.openById(templateId);
  var slides = presentation.getSlides();
  var layouts = [];

  for (var i = 0; i < slides.length; i++) {
    var slide = slides[i];
    var layoutName = getSlideLayoutName(slide, i);
    var tokens = findTokens(slide);
    var textBoxes = getTextBoxInfo(slide);

    layouts.push({
      index: i,
      layout: layoutName,
      tokens: tokens,
      textBoxes: textBoxes
    });
  }

  return jsonResponse({
    templateId: templateId,
    slideCount: slides.length,
    layouts: layouts
  });
}

/**
 * Tokenize a template: add LAYOUT: names to speaker notes and replace
 * placeholder text with {{TOKEN}} markers. This is a one-time setup action.
 *
 * Payload: { action: "tokenize", key, templateId, slideMap: [...] }
 *
 * Each slideMap entry: { index: N, layout: "NAME", replacements: [{ find: "old text", token: "TOKEN_NAME" }] }
 */
function handleTokenize(payload) {
  var templateId = payload.templateId;
  var slideMap = payload.slideMap || [];

  var presentation = SlidesApp.openById(templateId);
  var slides = presentation.getSlides();
  var results = [];

  for (var i = 0; i < slideMap.length; i++) {
    var spec = slideMap[i];
    var idx = spec.index;
    if (idx < 0 || idx >= slides.length) {
      results.push({ index: idx, status: "skipped", reason: "out of range" });
      continue;
    }

    var slide = slides[idx];
    var slideResult = { index: idx, layout: spec.layout, tokensAdded: [] };

    // Set LAYOUT: in speaker notes
    if (spec.layout) {
      var notesShape = slide.getNotesPage().getSpeakerNotesShape();
      notesShape.getText().setText("LAYOUT:" + spec.layout);
    }

    // Replace placeholder text with {{TOKEN}} markers
    // Optional "nth" param (0-based) targets only the Nth matching shape
    if (spec.replacements) {
      var elements = slide.getPageElements();
      for (var r = 0; r < spec.replacements.length; r++) {
        var rep = spec.replacements[r];
        var findText = rep.find;
        var tokenText = "{{" + rep.token + "}}";
        var targetNth = (typeof rep.nth === "number") ? rep.nth : -1;
        var matchCount = 0;

        for (var e = 0; e < elements.length; e++) {
          var el = elements[e];
          if (el.getPageElementType() === SlidesApp.PageElementType.SHAPE) {
            var shape = el.asShape();
            var currentText = shape.getText().asString();
            if (currentText.indexOf(findText) !== -1) {
              if (targetNth === -1 || matchCount === targetNth) {
                shape.getText().replaceAllText(findText, tokenText);
                slideResult.tokensAdded.push(rep.token);
                if (targetNth !== -1) break;
              }
              matchCount++;
            }
          }
        }
      }
    }

    results.push(slideResult);
  }

  return jsonResponse({
    templateId: templateId,
    slidesProcessed: results.length,
    results: results
  });
}

// ============================================================
// Core functions
// ============================================================

/**
 * Build a map of layout name -> slide index.
 * Uses the slide's layout name, or falls back to speaker notes annotation,
 * or falls back to "SLIDE_N".
 */
function buildLayoutMap(slides) {
  var map = {};
  for (var i = 0; i < slides.length; i++) {
    var name = getSlideLayoutName(slides[i], i);
    map[name] = i;
  }
  return map;
}

/**
 * Get a slide's layout name. Checks:
 * 1. The predefined layout name from the slide's layout
 * 2. Speaker notes starting with "LAYOUT:" as an override
 * 3. Falls back to "SLIDE_N"
 */
function getSlideLayoutName(slide, index) {
  // Check speaker notes for explicit layout name
  try {
    var notes = slide.getNotesPage().getSpeakerNotesShape().getText().asString().trim();
    if (notes.indexOf("LAYOUT:") === 0) {
      var rest = notes.substring(7);
      var nl = rest.indexOf("\n");
      return (nl > -1 ? rest.substring(0, nl) : rest).trim();
    }
  } catch (e) {
    // No notes, continue
  }

  // Try the layout object name
  try {
    var layout = slide.getLayout();
    var layoutName = layout.getLayoutName();
    if (layoutName) return layoutName;
  } catch (e) {
    // No layout info
  }

  return "SLIDE_" + index;
}

/**
 * Find all {{TOKEN}} placeholders in a slide's text elements.
 */
function findTokens(slide) {
  var tokens = [];
  var elements = slide.getPageElements();
  var re = /\{\{([A-Z0-9_]+)\}\}/g;

  for (var i = 0; i < elements.length; i++) {
    var el = elements[i];
    if (el.getPageElementType() === SlidesApp.PageElementType.SHAPE) {
      var text = el.asShape().getText().asString();
      var match;
      while ((match = re.exec(text)) !== null) {
        tokens.push(match[1]);
      }
      re.lastIndex = 0;
    }
  }
  return tokens;
}

/**
 * Get text box info (dimensions, placeholder text) for constraint documentation.
 */
function getTextBoxInfo(slide) {
  var boxes = [];
  var elements = slide.getPageElements();

  for (var i = 0; i < elements.length; i++) {
    var el = elements[i];
    if (el.getPageElementType() === SlidesApp.PageElementType.SHAPE) {
      var shape = el.asShape();
      var text = shape.getText().asString().trim();
      if (!text) continue;

      var transform = el.getTransform();
      boxes.push({
        text: text.substring(0, 100),
        width: el.getWidth(),
        height: el.getHeight(),
        left: el.getLeft(),
        top: el.getTop()
      });
    }
  }
  return boxes;
}

/**
 * Replace all {{TOKEN}} placeholders in a slide with provided values.
 * The replacement text inherits the formatting of the placeholder.
 */
function replaceTokens(slide, tokens) {
  var elements = slide.getPageElements();

  for (var i = 0; i < elements.length; i++) {
    var el = elements[i];
    if (el.getPageElementType() === SlidesApp.PageElementType.SHAPE) {
      var shape = el.asShape();
      for (var token in tokens) {
        var placeholder = "{{" + token + "}}";
        var value = tokens[token] || "";
        shape.getText().replaceAllText(placeholder, value);
      }
    }
  }
}

/**
 * Set speaker notes for a slide.
 * Preserves any "LAYOUT:" prefix line if present.
 */
function setSpeakerNotes(slide, notes) {
  var notesShape = slide.getNotesPage().getSpeakerNotesShape();
  var existing = notesShape.getText().asString().trim();

  // Preserve LAYOUT: annotation
  if (existing.indexOf("LAYOUT:") === 0) {
    var firstNewline = existing.indexOf("\n");
    var layoutLine = firstNewline > -1 ? existing.substring(0, firstNewline + 1) : existing + "\n";
    notesShape.getText().setText(layoutLine + "\n" + notes);
  } else {
    notesShape.getText().setText(notes);
  }
}

/**
 * Reorder slides to match the spec order, and remove unused template slides.
 *
 * Strategy:
 * 1. For each spec (in order), find its source slide by layout name
 * 2. Move it to the correct position
 * 3. After ordering, delete any slides that weren't in the spec
 */
function reorderSlides(presentation, originalSlides, slideSpecs, layoutMap) {
  // Collect which layout indices are used, in order
  var usedLayouts = [];
  for (var i = 0; i < slideSpecs.length; i++) {
    if (slideSpecs[i].skip) continue;
    var layoutName = slideSpecs[i].layout;
    if (layoutName in layoutMap) {
      usedLayouts.push({ specIndex: i, layoutName: layoutName, originalIndex: layoutMap[layoutName] });
    }
  }

  // Move slides to correct positions
  for (var j = 0; j < usedLayouts.length; j++) {
    var slides = presentation.getSlides();
    var targetSlide = null;

    // Find the slide by its object ID (stable across moves)
    for (var k = 0; k < slides.length; k++) {
      var name = getSlideLayoutName(slides[k], k);
      if (name === usedLayouts[j].layoutName) {
        targetSlide = slides[k];
        break;
      }
    }

    if (targetSlide) {
      targetSlide.move(j);
    }
  }

  // Delete unused slides (reverse order to preserve indices)
  var usedLayoutNames = {};
  for (var m = 0; m < usedLayouts.length; m++) {
    usedLayoutNames[usedLayouts[m].layoutName] = true;
  }

  var finalSlides = presentation.getSlides();
  for (var n = finalSlides.length - 1; n >= 0; n--) {
    var slideName = getSlideLayoutName(finalSlides[n], n);
    if (!(slideName in usedLayoutNames)) {
      // Only delete if we'd still have at least 1 slide
      if (finalSlides.length > 1) {
        finalSlides[n].remove();
      }
    }
  }
}

/**
 * Reposition elements in a presentation by matching text content.
 *
 * Payload: { action: "reposition", key, presentationId, adjustments: [...] }
 *
 * Each adjustment: {
 *   slideIndex: N,
 *   findText: "text to match",
 *   setTop: 204,
 *   setLeft: 100,
 *   setWidth: 200,
 *   setHeight: 150
 * }
 *
 * Only provided properties are changed; omitted ones stay as-is.
 */
function handleReposition(payload) {
  var presentationId = payload.presentationId;
  var adjustments = payload.adjustments || [];

  var presentation = SlidesApp.openById(presentationId);
  var slides = presentation.getSlides();
  var results = [];

  for (var i = 0; i < adjustments.length; i++) {
    var adj = adjustments[i];
    var idx = adj.slideIndex;
    if (idx < 0 || idx >= slides.length) {
      results.push({ slideIndex: idx, status: "skipped", reason: "out of range" });
      continue;
    }

    var slide = slides[idx];
    var elements = slide.getPageElements();
    var found = false;

    for (var e = 0; e < elements.length; e++) {
      var el = elements[e];
      if (el.getPageElementType() === SlidesApp.PageElementType.SHAPE) {
        var text = el.asShape().getText().asString();
        if (text.indexOf(adj.findText) !== -1) {
          if (typeof adj.setTop === "number") el.setTop(adj.setTop);
          if (typeof adj.setLeft === "number") el.setLeft(adj.setLeft);
          if (typeof adj.setWidth === "number") el.setWidth(adj.setWidth);
          if (typeof adj.setHeight === "number") el.setHeight(adj.setHeight);
          found = true;
          results.push({
            slideIndex: idx,
            findText: adj.findText,
            status: "repositioned",
            newTop: typeof adj.setTop === "number" ? adj.setTop : el.getTop(),
            newLeft: typeof adj.setLeft === "number" ? adj.setLeft : el.getLeft()
          });
          break;
        }
      }
    }

    if (!found) {
      results.push({ slideIndex: idx, findText: adj.findText, status: "not_found" });
    }
  }

  return jsonResponse({
    presentationId: presentationId,
    adjustmentsProcessed: results.length,
    results: results
  });
}

/**
 * Share a presentation (anyone with the link can view).
 *
 * Payload: { action: "share", key, presentationId }
 */
function handleShare(payload) {
  var file = DriveApp.getFileById(payload.presentationId);
  file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
  return jsonResponse({
    presentationId: payload.presentationId,
    url: "https://docs.google.com/presentation/d/" + payload.presentationId + "/edit",
    shared: true
  });
}

// ============================================================
// Utilities
// ============================================================

function sanitizeKey(str) {
  return str.toLowerCase().replace(/[^a-z0-9]+/g, "_").substring(0, 50);
}

function jsonResponse(data, statusCode) {
  return ContentService.createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}
