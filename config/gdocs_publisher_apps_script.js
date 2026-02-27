/**
 * Google Docs Publisher (Apps Script)
 *
 * Accepts markdown content via HTTP POST and creates/updates
 * Google Docs with tabs organized by category.
 *
 * Deploy as: Web app -> Execute as "Me" -> Access "Anyone with the link"
 *
 * SETUP:
 * 1. In the Apps Script editor, go to Services (+) and add:
 *    - Google Docs API (v1)
 * 2. Go to Project Settings (gear icon) -> Script Properties -> Add:
 *    - Property: API_KEY   Value: (generate a random string)
 * 3. Deploy -> New deployment -> Web app
 * 4. Copy the deployment URL into your .env as GDOCS_APPS_SCRIPT_URL
 * 5. Copy the API_KEY value into your .env as GDOCS_API_KEY
 *
 * PERMISSIONS: Only requires Google Docs API (no Drive API needed).
 * Doc IDs and tab IDs are tracked in Script Properties so we never
 * search Drive or read doc structure back from the API.
 * New docs are created in your Drive root -- move them to the shared
 * folder once and all future updates go to the right place.
 *
 * ACTIONS:
 *   publish   - Create/update tabs in a category doc with markdown content
 *   unpublish - Remove a tab from a category doc
 *   status    - Return current doc structure (doc IDs, tab names)
 */

// ---Constants -------------------------------------------------------

// Map category keys to Google Doc titles.
// Customize these for your project. The category key is used in API
// requests; the value becomes the Google Doc title on first creation.
const CATEGORY_DOC_NAMES = {
  // Example: "research": "My Project -- Research Notes",
  // Example: "drafts": "My Project -- Draft Articles",
};

// ---HTTP Entry Points -----------------------------------------------

function doPost(e) {
  try {
    const payload = JSON.parse(e.postData.contents);

    // Verify API key
    const expectedKey = PropertiesService.getScriptProperties().getProperty("API_KEY");
    if (expectedKey && payload.key !== expectedKey) {
      return jsonResponse({ error: "Invalid or missing API key" }, 403);
    }

    const action = payload.action;

    let result;
    switch (action) {
      case "publish":
        result = handlePublish(payload);
        break;
      case "unpublish":
        result = handleUnpublish(payload);
        break;
      case "status":
        result = handleStatus(payload);
        break;
      default:
        return jsonResponse({ error: `Unknown action: ${action}` }, 400);
    }

    return jsonResponse(result);
  } catch (err) {
    return jsonResponse({ error: err.message, stack: err.stack }, 500);
  }
}

function doGet(e) {
  return jsonResponse({
    service: "Google Docs Publisher",
    version: "2.1",
    actions: ["publish", "unpublish", "status"],
  });
}

// ---Publish ---------------------------------------------------------

function handlePublish(payload) {
  const { category, tabs } = payload;
  const docName = payload.docName || CATEGORY_DOC_NAMES[category] || `Docs -- ${category}`;

  if (!tabs || !tabs.length) throw new Error("tabs array is required");

  // Find or create the Google Doc
  var docInfo = getOrCreateDoc(category, docName);
  var docId = docInfo.docId;
  var isNew = docInfo.isNew;
  var defaultTabId = docInfo.defaultTabId;

  // Get our tracked tabs from Script Properties
  const existingTabMap = getStoredTabs(category);

  const results = [];

  for (const tab of tabs) {
    const tabName = tab.name;
    const markdown = tab.markdown;

    // Step 1: Remove any existing tab with this name.
    // Try stored ID first, then fall back to title search. This prevents
    // orphan tabs regardless of whether Script Properties are in sync.
    var isUpdate = false;
    if (existingTabMap[tabName]) {
      try {
        deleteTab(docId, existingTabMap[tabName]);
        isUpdate = true;
      } catch (err) {
        // Stored ID was stale -- tab may have been manually deleted
      }
    }
    // Safety net: check if a tab with this title still exists in the doc
    // (handles stale stored IDs, manual renames, or untracked tabs)
    var existingByTitle = findTabIdByTitle(docId, tabName);
    if (existingByTitle) {
      try {
        deleteTab(docId, existingByTitle);
        isUpdate = true;
      } catch (err) {
        // Already gone
      }
    }

    // Step 2: Create fresh tab and populate
    const newTabId = createTab(docId, tabName);
    insertMarkdownContent(docId, newTabId, markdown);
    storeTabId(category, tabName, newTabId);
    results.push({ tab: tabName, action: isUpdate ? "updated" : "created", tabId: newTabId });
  }

  // Clean up the empty default "Tab 1" that Google creates with every new doc.
  // We must do this AFTER creating at least one real tab (can't delete the last tab).
  if (isNew && results.length > 0) {
    cleanupDefaultTab(docId, defaultTabId);
  }

  // If replaceAll is set, delete every tab NOT in the payload.
  // Safe because our new tabs already exist (at least one always remains).
  if (payload.replaceAll && results.length > 0) {
    try {
      var doc = Docs.Documents.get(docId);
      var newTabIds = {};
      for (var i = 0; i < results.length; i++) {
        newTabIds[results[i].tabId] = true;
      }
      for (var i = 0; i < doc.tabs.length; i++) {
        var tid = doc.tabs[i].tabProperties.tabId;
        if (!newTabIds[tid]) {
          try { deleteTab(docId, tid); } catch (e) {}
        }
      }
    } catch (err) {
      Logger.log("replaceAll cleanup failed: " + err.message);
    }
  }

  // Reorder tabs to match the payload's tabs array order.
  // Tabs are recreated (delete + add) which puts them at the end, so we
  // need to explicitly set each tab's index to restore the intended order.
  reorderTabs(docId, category, tabs);

  return { docId, docName, results };
}

// ---Default Tab Cleanup ---------------------------------------------

/**
 * Remove the empty "Tab 1" that Google auto-creates with every new doc.
 * Tries the tab ID captured from the create() response first, then
 * falls back to finding it by title. Silently skips if it can't find
 * or delete it -- the doc just has an extra empty tab (cosmetic only).
 */
function cleanupDefaultTab(docId, defaultTabId) {
  try {
    var tabId = defaultTabId;
    if (!tabId) {
      // Fallback: try to find "Tab 1" by title
      tabId = findTabIdByTitle(docId, "Tab 1");
    }
    if (tabId) {
      deleteTab(docId, tabId);
    }
  } catch (err) {
    // Non-critical: the doc just keeps an extra empty tab
  }
}

// ---Tab Reordering --------------------------------------------------

/**
 * Reorder tabs in a Google Doc to match the desired order from the payload.
 * Uses updateDocumentTabProperties to set each tab's index.
 *
 * The payload's tabs array defines the desired order. We also need to
 * account for any existing tabs not in the current publish batch (they
 * keep their relative position). Strategy: read the doc's current tabs,
 * build the desired order (payload tabs first, then any others), and
 * set indices via batchUpdate.
 */
function reorderTabs(docId, category, payloadTabs) {
  try {
    // Read current doc tabs
    var doc = Docs.Documents.get(docId);
    if (!doc.tabs || doc.tabs.length <= 1) return; // Nothing to reorder

    // Build desired tab name order from payload
    var desiredOrder = payloadTabs.map(function (t) { return t.name; });

    // Get stored tab IDs for this category (name -> tabId)
    var storedTabs = getStoredTabs(category);

    // Build a map of tabId -> current tab info from the doc
    var docTabMap = {};
    for (var i = 0; i < doc.tabs.length; i++) {
      var tp = doc.tabs[i].tabProperties;
      docTabMap[tp.tabId] = { title: tp.title, currentIndex: tp.index };
    }

    // Build the full ordered list of tab IDs:
    // 1. Tabs from the payload (in payload order)
    // 2. Any remaining tabs not in the payload (preserve their relative order)
    var orderedTabIds = [];
    var usedIds = {};

    for (var i = 0; i < desiredOrder.length; i++) {
      var tabId = storedTabs[desiredOrder[i]];
      if (tabId && docTabMap[tabId]) {
        orderedTabIds.push(tabId);
        usedIds[tabId] = true;
      }
    }

    // Add remaining tabs (sorted by their current index)
    var remainingTabs = [];
    for (var tabId in docTabMap) {
      if (!usedIds[tabId]) {
        remainingTabs.push({ tabId: tabId, index: docTabMap[tabId].currentIndex });
      }
    }
    remainingTabs.sort(function (a, b) { return a.index - b.index; });
    for (var i = 0; i < remainingTabs.length; i++) {
      orderedTabIds.push(remainingTabs[i].tabId);
    }

    // Build batchUpdate requests to set each tab's index
    var requests = [];
    for (var i = 0; i < orderedTabIds.length; i++) {
      var currentIdx = docTabMap[orderedTabIds[i]].currentIndex;
      if (currentIdx !== i) {
        requests.push({
          updateDocumentTabProperties: {
            tabId: orderedTabIds[i],
            tabProperties: { index: i },
            fields: "index",
          },
        });
      }
    }

    if (requests.length > 0) {
      Docs.Documents.batchUpdate({ requests: requests }, docId);
    }
  } catch (err) {
    // Non-critical: tabs work fine, just in wrong order
    Logger.log("Tab reorder failed: " + err.message);
  }
}

// ---Unpublish -------------------------------------------------------

function handleUnpublish(payload) {
  const { category, tabName } = payload;
  const docName = payload.docName || CATEGORY_DOC_NAMES[category] || `Docs -- ${category}`;

  if (!tabName) throw new Error("tabName is required");

  const docId = getStoredDocId(category);
  if (!docId) {
    return { removed: false, reason: `No doc registered for category '${category}'` };
  }

  const tabId = getStoredTabId(category, tabName);
  if (!tabId) {
    return { removed: false, reason: `Tab '${tabName}' not tracked for '${docName}'` };
  }

  // Count tracked tabs to avoid deleting the last one
  const allTabs = getStoredTabs(category);
  const tabCount = Object.keys(allTabs).length;

  if (tabCount <= 1) {
    // Can't delete the last tab -- Google Docs requires at least one
    // Just remove from tracking (content stays but we stop managing it)
    removeStoredTabId(category, tabName);
    return { removed: true, note: "Removed from tracking (last tab -- content preserved in doc)" };
  }

  try {
    deleteTab(docId, tabId);
  } catch (err) {
    // Tab may have been manually deleted already
  }
  removeStoredTabId(category, tabName);
  return { removed: true, docId, tabName };
}

// ---Status ----------------------------------------------------------

function handleStatus(payload) {
  const categories = {};
  const props = PropertiesService.getScriptProperties();

  // Scan all Script Properties for doc_ keys to find tracked categories
  const allProps = props.getProperties();
  for (const [key, value] of Object.entries(allProps)) {
    if (key.startsWith("doc_")) {
      const category = key.substring(4); // Remove "doc_" prefix
      const docId = value;
      const docName = CATEGORY_DOC_NAMES[category] || category;
      const tabs = getStoredTabs(category);
      const tabList = Object.entries(tabs).map(([name, id]) => ({ tabId: id, title: name }));
      categories[category] = { docId, docName, tabs: tabList };
    }
  }

  return { categories };
}

// ---Doc ID Storage (Script Properties) ------------------------------

function getStoredDocId(category) {
  const props = PropertiesService.getScriptProperties();
  return props.getProperty(`doc_${category}`);
}

function storeDocId(category, docId) {
  const props = PropertiesService.getScriptProperties();
  props.setProperty(`doc_${category}`, docId);
}

function getOrCreateDoc(category, docName) {
  const existing = getStoredDocId(category);
  if (existing) {
    // Verify it still exists (just fetch metadata, no tabs needed)
    try {
      Docs.Documents.get(existing);
      return { docId: existing, isNew: false, defaultTabId: null };
    } catch (err) {
      // Doc was deleted -- create a new one
    }
  }

  // Create new Google Doc via Docs API (lands in Drive root)
  var doc = Docs.Documents.create({ title: docName });
  storeDocId(category, doc.documentId);

  // Try to capture the default tab ID from the creation response.
  // Every new Google Doc gets a "Tab 1" automatically. We need its ID
  // so we can delete it after creating the real content tabs.
  var defaultTabId = null;
  try {
    if (doc.tabs && doc.tabs.length > 0) {
      defaultTabId = doc.tabs[0].tabProperties.tabId;
    }
  } catch (e) {
    // Advanced service may not return tabs -- cleanupDefaultTab will
    // fall back to findTabIdByTitle("Tab 1")
  }

  return { docId: doc.documentId, isNew: true, defaultTabId: defaultTabId };
}

// ---Tab Lookup (fallback for orphaned tabs) -------------------------

function findTabIdByTitle(docId, title) {
  // Fallback: scan the doc's tabs via the advanced service to find a tab
  // by title. Used when a tab exists in the doc but isn't in our tracking.
  try {
    const doc = Docs.Documents.get(docId);
    // The advanced service may return tabs in the legacy body or in doc.tabs
    if (doc.tabs) {
      for (const tab of doc.tabs) {
        if (tab.tabProperties && tab.tabProperties.title === title) {
          return tab.tabProperties.tabId;
        }
        // Check child tabs
        for (const child of tab.childTabs || []) {
          if (child.tabProperties && child.tabProperties.title === title) {
            return child.tabProperties.tabId;
          }
        }
      }
    }
  } catch (err) {
    // If we can't read the doc, we can't recover
  }
  return null;
}

// ---Tab ID Storage (Script Properties) ------------------------------

function storeTabId(category, tabName, tabId) {
  const props = PropertiesService.getScriptProperties();
  props.setProperty(`tab_${category}_${tabName}`, tabId);
}

function getStoredTabId(category, tabName) {
  const props = PropertiesService.getScriptProperties();
  return props.getProperty(`tab_${category}_${tabName}`);
}

function removeStoredTabId(category, tabName) {
  const props = PropertiesService.getScriptProperties();
  props.deleteProperty(`tab_${category}_${tabName}`);
}

function getStoredTabs(category) {
  const props = PropertiesService.getScriptProperties();
  const all = props.getProperties();
  const prefix = `tab_${category}_`;
  const tabs = {};
  for (const [key, value] of Object.entries(all)) {
    if (key.startsWith(prefix)) {
      const tabName = key.substring(prefix.length);
      tabs[tabName] = value;
    }
  }
  return tabs;
}

// ---Google Docs Tab Operations --------------------------------------

function createTab(docId, title) {
  const requests = [
    {
      addDocumentTab: {
        tabProperties: {
          title: title,
        },
      },
    },
  ];

  const response = Docs.Documents.batchUpdate({ requests }, docId);
  const reply = response.replies[0];
  return reply.addDocumentTab.tabProperties.tabId;
}

function deleteTab(docId, tabId) {
  const requests = [
    {
      deleteTab: {
        tabId: tabId,
      },
    },
  ];
  Docs.Documents.batchUpdate({ requests }, docId);
}

function insertMarkdownContent(docId, tabId, markdown) {
  const elements = parseMarkdown(markdown);
  const requests = buildInsertRequests(elements, tabId);

  if (requests.length > 0) {
    Docs.Documents.batchUpdate({ requests }, docId);
  }
}

// --- Markdown -> Google Docs Conversion ------------------------------

/**
 * Parse markdown into a flat list of elements with type and content.
 * Handles: headings, paragraphs, bold, italic, blockquotes, lists,
 * tables (as formatted text), links, and horizontal rules.
 */
function parseMarkdown(markdown) {
  const lines = markdown.split("\n");
  const elements = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];

    // Heading
    const headingMatch = line.match(/^(#{1,6})\s+(.+)/);
    if (headingMatch) {
      const level = headingMatch[1].length;
      elements.push({ type: "heading", level, text: headingMatch[2] });
      i++;
      continue;
    }

    // Horizontal rule
    if (/^[-*_]{3,}\s*$/.test(line)) {
      elements.push({ type: "hr" });
      i++;
      continue;
    }

    // Code fence (```lang ... ```)
    if (line.startsWith("```")) {
      const codeLines = [];
      i++;
      while (i < lines.length && !lines[i].startsWith("```")) {
        codeLines.push(lines[i]);
        i++;
      }
      if (i < lines.length) i++; // skip closing ```
      if (codeLines.length > 0) {
        elements.push({ type: "code_block", text: codeLines.join("\n") });
      }
      continue;
    }

    // Blockquote
    if (line.startsWith(">")) {
      let quoteText = line.replace(/^>\s?/, "");
      i++;
      while (i < lines.length && lines[i].startsWith(">")) {
        quoteText += "\n" + lines[i].replace(/^>\s?/, "");
        i++;
      }
      elements.push({ type: "blockquote", text: quoteText });
      continue;
    }

    // Unordered list item
    if (/^[-*+]\s+/.test(line)) {
      const items = [];
      while (i < lines.length && /^[-*+]\s+/.test(lines[i])) {
        items.push(lines[i].replace(/^[-*+]\s+/, ""));
        i++;
      }
      elements.push({ type: "list", items });
      continue;
    }

    // Ordered list item
    if (/^\d+\.\s+/.test(line)) {
      const items = [];
      while (i < lines.length && /^\d+\.\s+/.test(lines[i])) {
        items.push(lines[i].replace(/^\d+\.\s+/, ""));
        i++;
      }
      elements.push({ type: "ordered_list", items });
      continue;
    }

    // Table
    if (line.includes("|") && i + 1 < lines.length && /^\|?\s*[-:]+/.test(lines[i + 1])) {
      const tableLines = [line];
      i++;
      while (i < lines.length && lines[i].includes("|")) {
        tableLines.push(lines[i]);
        i++;
      }
      elements.push({ type: "table", lines: tableLines });
      continue;
    }

    // Empty line
    if (line.trim() === "") {
      i++;
      continue;
    }

    // Regular paragraph (collect consecutive non-empty lines)
    let paraText = line;
    i++;
    while (i < lines.length && lines[i].trim() !== "" && !lines[i].startsWith("#") && !lines[i].startsWith(">") && !/^[-*+]\s+/.test(lines[i]) && !/^\d+\.\s+/.test(lines[i]) && !/^[-*_]{3,}/.test(lines[i])) {
      paraText += " " + lines[i];
      i++;
    }
    elements.push({ type: "paragraph", text: paraText });
  }

  return elements;
}

/**
 * Build Google Docs API batchUpdate requests from parsed elements.
 * Inserts text at position 1 (start of document) and applies styles.
 * Uses forward insertion, tracking a running offset.
 */
function buildInsertRequests(elements, tabId) {
  const requests = [];
  let offset = 1; // Start of document body

  for (const el of elements) {
    switch (el.type) {
      case "heading": {
        const stripped = stripMarkdown(el.text);
        const text = stripped.cleanText + "\n";
        requests.push({
          insertText: { location: { index: offset, tabId }, text },
        });
        const headingStyle = `HEADING_${el.level}`;
        requests.push({
          updateParagraphStyle: {
            range: { startIndex: offset, endIndex: offset + text.length, tabId },
            paragraphStyle: {
              namedStyleType: headingStyle,
              spaceAbove: { magnitude: 14, unit: "PT" },
              spaceBelow: { magnitude: 4, unit: "PT" },
            },
            fields: "namedStyleType,spaceAbove,spaceBelow",
          },
        });
        requests.push(...buildFormatRequests(stripped.formats, offset, tabId));
        offset += text.length;
        break;
      }

      case "paragraph": {
        const stripped = stripMarkdown(el.text);
        const text = stripped.cleanText + "\n";
        requests.push({
          insertText: { location: { index: offset, tabId }, text },
        });
        requests.push({
          updateParagraphStyle: {
            range: { startIndex: offset, endIndex: offset + text.length, tabId },
            paragraphStyle: {
              namedStyleType: "NORMAL_TEXT",
              spaceBelow: { magnitude: 8, unit: "PT" },
            },
            fields: "namedStyleType,spaceBelow",
          },
        });
        requests.push(...buildFormatRequests(stripped.formats, offset, tabId));
        offset += text.length;
        break;
      }

      case "blockquote": {
        const stripped = stripMarkdown(el.text);
        const text = stripped.cleanText + "\n";
        requests.push({
          insertText: { location: { index: offset, tabId }, text },
        });
        requests.push({
          updateParagraphStyle: {
            range: { startIndex: offset, endIndex: offset + text.length, tabId },
            paragraphStyle: {
              namedStyleType: "NORMAL_TEXT",
              indentFirstLine: { magnitude: 36, unit: "PT" },
              indentStart: { magnitude: 36, unit: "PT" },
              spaceAbove: { magnitude: 6, unit: "PT" },
              spaceBelow: { magnitude: 6, unit: "PT" },
            },
            fields: "namedStyleType,indentFirstLine,indentStart,spaceAbove,spaceBelow",
          },
        });
        requests.push({
          updateTextStyle: {
            range: { startIndex: offset, endIndex: offset + text.length - 1, tabId },
            textStyle: { italic: true },
            fields: "italic",
          },
        });
        requests.push(...buildFormatRequests(stripped.formats, offset, tabId));
        offset += text.length;
        break;
      }

      case "list": {
        for (let li = 0; li < el.items.length; li++) {
          const stripped = stripMarkdown(el.items[li]);
          const text = stripped.cleanText + "\n";
          requests.push({
            insertText: { location: { index: offset, tabId }, text },
          });
          requests.push({
            createParagraphBullets: {
              range: { startIndex: offset, endIndex: offset + text.length, tabId },
              bulletPreset: "BULLET_DISC_CIRCLE_SQUARE",
            },
          });
          if (li === el.items.length - 1) {
            requests.push({
              updateParagraphStyle: {
                range: { startIndex: offset, endIndex: offset + text.length, tabId },
                paragraphStyle: { spaceBelow: { magnitude: 8, unit: "PT" } },
                fields: "spaceBelow",
              },
            });
          }
          requests.push(...buildFormatRequests(stripped.formats, offset, tabId));
          offset += text.length;
        }
        break;
      }

      case "ordered_list": {
        for (let li = 0; li < el.items.length; li++) {
          const stripped = stripMarkdown(el.items[li]);
          const text = stripped.cleanText + "\n";
          requests.push({
            insertText: { location: { index: offset, tabId }, text },
          });
          requests.push({
            createParagraphBullets: {
              range: { startIndex: offset, endIndex: offset + text.length, tabId },
              bulletPreset: "NUMBERED_DECIMAL_ALPHA_ROMAN",
            },
          });
          if (li === el.items.length - 1) {
            requests.push({
              updateParagraphStyle: {
                range: { startIndex: offset, endIndex: offset + text.length, tabId },
                paragraphStyle: { spaceBelow: { magnitude: 8, unit: "PT" } },
                fields: "spaceBelow",
              },
            });
          }
          requests.push(...buildFormatRequests(stripped.formats, offset, tabId));
          offset += text.length;
        }
        break;
      }

      case "table": {
        // Native Google Docs table from markdown.
        // Index formula for empty table cell (r, c):
        //   offset + 4 + c*2 + r*(2*numCols + 1)
        // Insert text in REVERSE cell order so earlier cells stay put.
        // Style using FINAL positions (structural index + cumulative text before).
        const rawRows = el.lines
          .filter((l) => !/^\|?\s*[-:]+/.test(l)) // skip separator row
          .map((l) =>
            l
              .split("|")
              .map((c) => c.trim())
              .filter((c) => c)
          );

        if (rawRows.length === 0) break;

        const numRows = rawRows.length;
        const numCols = Math.max(...rawRows.map((r) => r.length));

        // Pad rows to uniform column count
        for (let r = 0; r < numRows; r++) {
          while (rawRows[r].length < numCols) rawRows[r].push("");
        }

        // Strip markdown from all cells upfront
        const cellGrid = []; // cellGrid[r][c] = { cleanText, formats }
        for (let r = 0; r < numRows; r++) {
          cellGrid[r] = [];
          for (let c = 0; c < numCols; c++) {
            cellGrid[r][c] = stripMarkdown(rawRows[r][c]);
          }
        }

        // 1. Insert the table structure
        requests.push({
          insertTable: {
            rows: numRows,
            columns: numCols,
            location: { index: offset, tabId },
          },
        });

        // Empty table structural size: 3 + R + 2*R*C
        const tableStructSize = 3 + numRows + 2 * numRows * numCols;

        // 2. Insert clean cell text in REVERSE order (avoids index shifting)
        const cellList = []; // row-major order for styling pass
        for (let r = numRows - 1; r >= 0; r--) {
          for (let c = numCols - 1; c >= 0; c--) {
            const cell = cellGrid[r][c];
            cellList.unshift({ r, c, cleanText: cell.cleanText, formats: cell.formats });
            if (cell.cleanText) {
              const cellIdx = offset + 4 + c * 2 + r * (2 * numCols + 1);
              requests.push({
                insertText: {
                  location: { index: cellIdx, tabId },
                  text: cell.cleanText,
                },
              });
            }
          }
        }

        // 3. Apply styling using FINAL positions (after all text inserted)
        let cumText = 0;
        for (const cell of cellList) {
          if (cell.cleanText) {
            const finalStart =
              offset + 4 + cell.c * 2 + cell.r * (2 * numCols + 1) + cumText;
            // Bold header row
            if (cell.r === 0) {
              requests.push({
                updateTextStyle: {
                  range: {
                    startIndex: finalStart,
                    endIndex: finalStart + cell.cleanText.length,
                    tabId,
                  },
                  textStyle: { bold: true },
                  fields: "bold",
                },
              });
            }
            // Inline formatting (bold, italic, links within cell text)
            requests.push(...buildFormatRequests(cell.formats, finalStart, tabId));
            cumText += cell.cleanText.length;
          }
        }

        // 4. Update running offset past the table
        offset += tableStructSize + cumText;

        // Add spacing after table
        const sep = "\n";
        requests.push({
          insertText: { location: { index: offset, tabId }, text: sep },
        });
        offset += sep.length;
        break;
      }

      case "code_block": {
        const text = el.text + "\n";
        requests.push({
          insertText: { location: { index: offset, tabId }, text },
        });
        requests.push({
          updateParagraphStyle: {
            range: { startIndex: offset, endIndex: offset + text.length, tabId },
            paragraphStyle: {
              namedStyleType: "NORMAL_TEXT",
              indentFirstLine: { magnitude: 18, unit: "PT" },
              indentStart: { magnitude: 18, unit: "PT" },
            },
            fields: "namedStyleType,indentFirstLine,indentStart",
          },
        });
        requests.push({
          updateTextStyle: {
            range: { startIndex: offset, endIndex: offset + text.length - 1, tabId },
            textStyle: {
              weightedFontFamily: { fontFamily: "Courier New" },
              fontSize: { magnitude: 9, unit: "PT" },
              foregroundColor: { color: { rgbColor: { red: 0.4, green: 0.4, blue: 0.4 } } },
            },
            fields: "weightedFontFamily,fontSize,foregroundColor",
          },
        });
        offset += text.length;
        break;
      }

      case "hr": {
        const text = "----------------------------------------------------------------\n";
        requests.push({
          insertText: { location: { index: offset, tabId }, text },
        });
        requests.push({
          updateTextStyle: {
            range: { startIndex: offset, endIndex: offset + text.length - 1, tabId },
            textStyle: {
              foregroundColor: { color: { rgbColor: { red: 0.6, green: 0.6, blue: 0.6 } } },
              fontSize: { magnitude: 8, unit: "PT" },
            },
            fields: "foregroundColor,fontSize",
          },
        });
        offset += text.length;
        break;
      }
    }
  }

  return requests;
}

/**
 * Strip inline markdown syntax and return clean text + formatting ranges.
 * Removes **, *, __, _, and []() link syntax from text. Returns clean text
 * for insertion and an array of style ranges (relative to cleanText start).
 *
 * Returns: { cleanText: string, formats: [{start, end, style, fields}] }
 */
function stripMarkdown(text) {
  var tokens = [];
  var match;

  // Links first (they may contain bold/italic inside, but we keep it simple)
  var linkRegex = /\[([^\]]+)\]\(([^)]+)\)/g;
  while ((match = linkRegex.exec(text)) !== null) {
    tokens.push({
      start: match.index,
      end: match.index + match[0].length,
      replacement: match[1],
      style: {
        link: { url: match[2] },
        foregroundColor: { color: { rgbColor: { red: 0.0, green: 0.0, blue: 0.8 } } },
        underline: true,
      },
      fields: "link,foregroundColor,underline",
    });
  }

  // Bold: **text** or __text__
  var boldRegex = /\*\*(.+?)\*\*|__(.+?)__/g;
  while ((match = boldRegex.exec(text)) !== null) {
    tokens.push({
      start: match.index,
      end: match.index + match[0].length,
      replacement: match[1] || match[2],
      style: { bold: true },
      fields: "bold",
    });
  }

  // Italic: *text* or _text_ (not ** or __)
  var italicRegex = /(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)|(?<!_)_(?!_)(.+?)(?<!_)_(?!_)/g;
  while ((match = italicRegex.exec(text)) !== null) {
    tokens.push({
      start: match.index,
      end: match.index + match[0].length,
      replacement: match[1] || match[2],
      style: { italic: true },
      fields: "italic",
    });
  }

  // Inline code: `text`
  var codeRegex = /`([^`]+)`/g;
  while ((match = codeRegex.exec(text)) !== null) {
    tokens.push({
      start: match.index,
      end: match.index + match[0].length,
      replacement: match[1],
      style: {
        weightedFontFamily: { fontFamily: "Courier New" },
        fontSize: { magnitude: 9, unit: "PT" },
        backgroundColor: { color: { rgbColor: { red: 0.95, green: 0.95, blue: 0.95 } } },
      },
      fields: "weightedFontFamily,fontSize,backgroundColor",
    });
  }

  // Sort by position, remove overlaps (keep first)
  tokens.sort(function (a, b) { return a.start - b.start; });
  var filtered = [];
  var lastEnd = 0;
  for (var i = 0; i < tokens.length; i++) {
    if (tokens[i].start >= lastEnd) {
      filtered.push(tokens[i]);
      lastEnd = tokens[i].end;
    }
  }

  // Build clean text and collect formatting ranges
  var cleanText = "";
  var cursor = 0;
  var formats = [];

  for (var i = 0; i < filtered.length; i++) {
    var t = filtered[i];
    cleanText += text.slice(cursor, t.start);
    var fmtStart = cleanText.length;
    cleanText += t.replacement;
    var fmtEnd = cleanText.length;
    if (fmtEnd > fmtStart) {
      formats.push({ start: fmtStart, end: fmtEnd, style: t.style, fields: t.fields });
    }
    cursor = t.end;
  }
  cleanText += text.slice(cursor);

  return { cleanText: cleanText, formats: formats };
}

/**
 * Build updateTextStyle requests from stripMarkdown format ranges.
 * startOffset is the document index where cleanText was inserted.
 */
function buildFormatRequests(formats, startOffset, tabId) {
  var requests = [];
  for (var i = 0; i < formats.length; i++) {
    var fmt = formats[i];
    if (fmt.end > fmt.start) {
      requests.push({
        updateTextStyle: {
          range: { startIndex: startOffset + fmt.start, endIndex: startOffset + fmt.end, tabId },
          textStyle: fmt.style,
          fields: fmt.fields,
        },
      });
    }
  }
  return requests;
}

// ---Helpers ---------------------------------------------------------

function jsonResponse(data, statusCode) {
  return ContentService.createTextOutput(JSON.stringify(data)).setMimeType(
    ContentService.MimeType.JSON
  );
}
