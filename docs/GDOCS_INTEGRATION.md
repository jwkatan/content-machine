# Google Docs Integration -- Learnings & Reference

Everything learned while building the Apps Script-based Google Docs publisher, organized for reference.

---

## Architecture Overview

```
Your Code (Python / any HTTP client)
  |
  | HTTP POST (requests library)
  v
Google Apps Script (web app)
  |
  | Docs Advanced Service + batchUpdate API
  v
Google Docs (tabbed documents)
```

- **Python side**: Groups content by category, sends markdown + metadata to Apps Script endpoint
- **Apps Script** (`config/gdocs_publisher_apps_script.js`): Creates/manages Google Docs, creates tabs, converts markdown to formatted content
- **Script Properties**: Stores doc IDs and tab IDs (no Drive API needed)
- **API key**: Shared secret in Script Properties + `.env` for authentication

---

## Apps Script Deployment

### Initial Setup
1. Go to [script.google.com](https://script.google.com) -> New project
2. Paste the code from `config/gdocs_publisher_apps_script.js`
3. Go to **Services** (+) -> Add **Google Docs API v1** (userSymbol: `Docs`)
4. Go to **Project Settings** (gear) -> **Script Properties** -> Add:
   - `API_KEY` = (generate a random string, e.g., `openssl rand -base64 32`)
5. **Deploy** -> **New deployment** -> **Web app**
   - Execute as: **Me** (USER_DEPLOYING)
   - Access: **Anyone** (ANYONE_ANONYMOUS)
6. Copy the deployment URL to `.env` as `GDOCS_APPS_SCRIPT_URL`
7. Copy the API_KEY value to `.env` as `GDOCS_API_KEY`

### Updating Code
After changing the Apps Script code:
1. Paste new code in the editor
2. **Deploy** -> **Manage deployments** -> Edit (pencil icon) -> **New version** -> **Deploy**
3. The URL stays the same when using "New version" on an existing deployment

**IMPORTANT**: If you can't find "New version", create a brand new deployment. This generates a new URL that must be updated in `.env`.

### Re-authorization
When adding new permissions/scopes:
1. Update `appsscript.json` with new scopes
2. Click **Run** on any function in the editor -> approve the authorization popup
3. Deploy new version

---

## Critical Learnings (Bugs & Workarounds)

### 1. Apps Script Advanced Service Does NOT Return `doc.tabs`

**Problem**: `Docs.Documents.get(docId)` and `Docs.Documents.get(docId, {includeTabsContent: true/false})` do NOT return the `tabs` field in the response. The advanced service wrapper is outdated and doesn't support the newer tabs feature.

**Workaround**: Track tab IDs ourselves in Script Properties (`tab_{category}_{tabName}` -> tabId). Never rely on reading tabs back from the API through the advanced service.

**Alternative (requires extra permission)**: Use `UrlFetchApp.fetch()` to call the REST API directly with `ScriptApp.getOAuthToken()`. This requires the `https://www.googleapis.com/auth/script.external_request` scope, which needs explicit re-authorization.

### 2. Correct Field Name: `addDocumentTab` (not `addTab`)

**Problem**: `Docs.Documents.batchUpdate({requests: [{addTab: {...}}]}, docId)` fails with `Unknown name "addTab"`.

**Fix**: The correct field name is `addDocumentTab`:
```javascript
Docs.Documents.batchUpdate({
  requests: [{
    addDocumentTab: {
      tabProperties: { title: "Tab Name" }
    }
  }]
}, docId);
```

Response field is also `reply.addDocumentTab.tabProperties.tabId`.

The `deleteTab` field name IS correct as-is.

### 3. Tab Updates: Delete + Recreate (not Clear + Rewrite)

**Problem**: To update a tab's content, you'd need to:
1. Read the doc to find content range (`Docs.Documents.get` with `includeTabsContent: true`)
2. Delete content range
3. Insert new content

But step 1 doesn't work (see learning #1).

**Workaround**: Delete the tab entirely, create a new one with the same name, insert content. This is simpler and avoids reading the doc.

### 4. `UrlFetchApp.fetch` Permission Won't Auto-prompt

**Problem**: Adding `script.external_request` to `appsscript.json` oauthScopes doesn't always trigger a re-authorization prompt when running a function.

**Workaround**: Avoided UrlFetchApp entirely by using Script Properties for state tracking.

### 5. POST Redirects: Python `requests` Works, `curl -L` Doesn't

**Problem**: Apps Script web apps redirect POST requests (302). curl's `-L` flag converts the redirect from POST to GET, which returns an HTML error page.

**Fix**: Use Python `requests` library which correctly maintains POST method through redirects. Don't use curl for testing Apps Script endpoints.

### 6. Empty Text Style Ranges from Malformed Markdown

**Problem**: Markdown like `*Insufficient data.**` (mismatched italic/bold markers) can produce empty or invalid ranges in `updateTextStyle` requests, causing: `Invalid requests[N].updateTextStyle: The range should not be empty.`

**Fix**: Guard all text style requests:
```javascript
function addStyleRequest(matchStart, matchEnd, textStyle, fields) {
  if (matchEnd <= matchStart) return; // Skip empty ranges
  requests.push({...});
}
```

### 7. Unicode Characters Get Mangled by pbcopy

**Problem**: Copying code with em dashes, arrows, box-drawing chars via clipboard produces mojibake due to encoding issues.

**Fix**: Use only ASCII characters in the Apps Script code.

### 8. Orphaned Tabs from Partial Failures

**Problem**: If `createTab` succeeds but `insertMarkdownContent` fails (or a later tab in the batch fails), the tab exists in the doc but isn't tracked in Script Properties. Subsequent publishes fail with "Tab title must be unique".

**Partial fix**: Added `findTabIdByTitle` fallback that tries `Docs.Documents.get()` to find the orphaned tab. But since the advanced service doesn't return tabs (learning #1), this only works if the advanced service happens to return tab data (unreliable).

**Real fix for production**: Use `UrlFetchApp.fetch` for the fallback lookup (requires the extra scope), OR delete the Google Doc and start fresh.

### 9. New Docs Land in Drive Root

**Problem**: `Docs.Documents.create({title: "..."})` creates the doc in the deployer's Drive root, not in a specific folder. There's no way to specify a folder without the Drive API.

**Workaround**: Move docs to the shared folder manually via the Google Drive web UI after first creation. All future updates go to the right place since we track doc IDs.

**IMPORTANT -- Do NOT move .gdoc files via the mounted Google Drive filesystem** (`/Users/.../Library/CloudStorage/GoogleDrive-.../My Drive/`). The `.gdoc` files in the mounted filesystem are URL pointer files, not the actual documents. Using `mv` on them removes the shortcut without actually moving the Google Doc in Drive. The docs become "homeless" (still accessible by URL/ID but not visible in any folder). Use the Google Drive web UI (drive.google.com) to move docs: select -> right-click -> Organize -> Move.

### 10. Can't Delete the Last Tab

Google Docs requires at least one tab. If unpublishing the last tab, we either:
- Clear its content (if we can read it -- problematic per learning #1)
- Just remove it from tracking and leave it in the doc

### 11. New Docs Get an Empty Default "Tab 1"

`Docs.Documents.create()` always creates a default tab named "Tab 1". The script handles this automatically (v2.1+): after creating real tabs, it deletes the default tab via `cleanupDefaultTab()`.

### 12. Native Table Index Calculation

`insertTable` creates an empty table with predictable cell indices. For a table inserted at offset `O` with `R` rows and `C` columns:

- **Cell content index** (empty table): `O + 4 + c*2 + r*(2*C + 1)`
- **Empty table structural size**: `3 + R + 2*R*C`
- **Insert text in REVERSE cell order** (bottom-right to top-left) so earlier cells' indices stay valid
- **Final position** for styling (after all text inserted): structural index + cumulative text length of all preceding cells

---

## Apps Script API Reference

### batchUpdate Request Types Used

| Request | Field Name | Purpose |
|---------|-----------|---------|
| Create tab | `addDocumentTab` | `{tabProperties: {title: "..."}}` |
| Delete tab | `deleteTab` | `{tabId: "..."}` |
| Insert text | `insertText` | `{location: {index: N, tabId: "..."}, text: "..."}` |
| Style paragraph | `updateParagraphStyle` | Headings, indents |
| Style text | `updateTextStyle` | Bold, italic, links, colors |
| Create bullets | `createParagraphBullets` | Bulleted/numbered lists |
| Insert table | `insertTable` | `{rows: N, columns: N, location: {index, tabId}}` |
| Delete content | `deleteContentRange` | `{tabId, range: {startIndex, endIndex}}` |

### Named Styles for Paragraphs
- `HEADING_1` through `HEADING_6`
- `NORMAL_TEXT`

### Bullet Presets
- `BULLET_DISC_CIRCLE_SQUARE` (unordered)
- `NUMBERED_DECIMAL_ALPHA_ROMAN` (ordered)

### Script Properties Keys
- `doc_{category}` -> Google Doc ID
- `tab_{category}_{tabName}` -> Tab ID within that doc
- `API_KEY` -> Shared secret for authentication

---

## appsscript.json (Manifest)

```json
{
  "timeZone": "America/New_York",
  "dependencies": {
    "enabledAdvancedServices": [
      {
        "userSymbol": "Docs",
        "version": "v1",
        "serviceId": "docs"
      }
    ]
  },
  "oauthScopes": [
    "https://www.googleapis.com/auth/documents"
  ],
  "exceptionLogging": "STACKDRIVER",
  "runtimeVersion": "V8",
  "webapp": {
    "executeAs": "USER_DEPLOYING",
    "access": "ANYONE_ANONYMOUS"
  }
}
```

Only one OAuth scope needed: `documents`. No Drive API.

If you need `UrlFetchApp.fetch` (for direct REST API calls), add:
```json
"https://www.googleapis.com/auth/script.external_request"
```

---

## Markdown to Google Docs Conversion

The Apps Script converts markdown elements to Google Docs formatting:

| Markdown | Google Docs |
|----------|------------|
| `# Heading` | `HEADING_1` paragraph style |
| `**bold**` | `updateTextStyle` with `bold: true` |
| `*italic*` | `updateTextStyle` with `italic: true` |
| `[text](url)` | `updateTextStyle` with `link: {url}` |
| `> blockquote` | Indented paragraph + italic |
| `- item` | `createParagraphBullets` with disc preset |
| `1. item` | `createParagraphBullets` with numbered preset |
| `---` | Gray dashed line (styled text) |
| Tables | Native Google Docs table with bold header row |

Content is inserted sequentially from index 1 (start of tab body), tracking a running offset. Inline formatting (bold, italic, links) is applied after text insertion using ranges calculated from regex matches.

---

## Payload Format

```python
{
    "action": "publish",
    "key": "api-key-here",
    "category": "my_category",
    "docName": "My Document Title",
    "tabs": [
        {"name": "Tab One", "markdown": "# Tab One\n\nContent..."},
        {"name": "Tab Two", "markdown": "# Tab Two\n\nContent..."}
    ]
}
```

### Response Format
```python
{
    "docId": "1abc...",
    "docName": "My Document Title",
    "results": [
        {"tab": "Tab One", "action": "created", "tabId": "t.abc123"},
        {"tab": "Tab Two", "action": "updated", "tabId": "t.def456"}
    ]
}
```
