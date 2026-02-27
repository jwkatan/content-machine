---
name: google-docs
description: |
  Work with Google Docs programmatically via an Apps Script web app. Use this skill whenever
  you need to create, read, update, or manage Google Docs — including creating documents,
  managing tabs, inserting formatted content, or troubleshooting the Apps Script integration.
  Claude Desktop cannot use Apps Script through the browser, so this skill encodes the
  knowledge needed to work with Google Docs via HTTP API calls.
allowed-tools:
  - Bash(source .venv/bin/activate && python)
  - Bash(curl)
  - Read
  - Write
  - Edit
---

# Google Docs via Apps Script

This skill teaches you how to work with Google Docs through a deployed Google Apps Script web app. All operations happen via HTTP POST requests from Python (or any HTTP client) to the Apps Script endpoint.

## Architecture

```
Your Code (Python / any HTTP client)
  |
  | HTTP POST with JSON payload
  v
Google Apps Script (deployed as web app)
  |
  | Docs Advanced Service + batchUpdate API
  v
Google Docs (documents with tabs)
```

- **Caller**: Sends JSON payloads via HTTP POST using `requests` (Python) or equivalent
- **Apps Script**: Receives requests, authenticates via shared API key, creates/manages Google Docs
- **State tracking**: Doc IDs and tab IDs stored in Apps Script's `PropertiesService` (Script Properties)
- **Authentication**: Shared secret — API key stored in both Script Properties and caller's `.env`

## Prerequisites

1. A deployed Apps Script web app (see `!.claude/skills/google-docs/references/deployment-guide.md`)
2. Environment variables:
   - `GDOCS_APPS_SCRIPT_URL` — the deployed web app URL
   - `GDOCS_API_KEY` — shared secret matching the Script Properties `API_KEY`

## Working with Google Docs

### Sending requests to the Apps Script endpoint

All interactions use HTTP POST with a JSON body. Python's `requests` library handles redirects correctly (see critical learning below).

```python
import requests
import os

url = os.environ["GDOCS_APPS_SCRIPT_URL"]
api_key = os.environ["GDOCS_API_KEY"]

response = requests.post(url, json={
    "action": "publish",
    "key": api_key,
    "category": "my_category",
    "docName": "My Document Title",
    "tabs": [
        {"name": "Tab One", "markdown": "# Heading\n\nContent here..."},
        {"name": "Tab Two", "markdown": "# Another Tab\n\nMore content..."}
    ]
})

result = response.json()
# {"docId": "1abc...", "docName": "My Document Title", "results": [...]}
```

### Available actions

| Action | Purpose | Required fields |
|--------|---------|----------------|
| `publish` | Create/update tabs in a doc | `category`, `tabs` (array of `{name, markdown}`) |
| `unpublish` | Remove a tab from a doc | `category`, `tabName` |
| `status` | List all tracked docs and tabs | (none beyond `key`) |

Every request must include `"key"` for authentication.

### Creating a new document

Documents are created automatically on first `publish` to a category. The `category` string becomes the storage key; `docName` sets the Google Doc title.

New docs land in the deployer's Google Drive root. Move them to the desired folder once via the Drive web UI (drive.google.com). All future updates go to the right doc since the ID is tracked.

### Managing tabs

Tabs (sub-pages within a Google Doc) are the primary content unit:

- **Create**: Publish with a new tab name
- **Update**: Publish with an existing tab name (old tab is deleted and recreated with new content)
- **Delete**: Use the `unpublish` action with the tab name
- **List**: Use the `status` action

### Inserting formatted content

The Apps Script converts markdown to Google Docs formatting:

| Markdown | Google Docs result |
|----------|-------------------|
| `# Heading` | `HEADING_1` through `HEADING_6` |
| `**bold**` | Bold text style |
| `*italic*` | Italic text style |
| `[text](url)` | Hyperlinked text |
| `> blockquote` | Indented + italic paragraph |
| `- item` | Bulleted list |
| `1. item` | Numbered list |
| `---` | Gray horizontal line |
| Tables (`\| col \|`) | Native Google Docs table with bold header row |

Content is inserted sequentially from index 1 (start of tab body), tracking a running offset. Inline formatting is applied after text insertion via ranges.

## Critical Learnings — Read These Before Coding

These are hard-won lessons from building and debugging the integration. Each one cost significant debugging time.

### 1. The Advanced Service does NOT return `doc.tabs`

`Docs.Documents.get(docId)` via the Apps Script advanced service does NOT return the `tabs` field. The advanced service wrapper is outdated. **Never rely on reading tabs back from the API.**

**Workaround**: Track all tab IDs yourself in Script Properties (`tab_{category}_{tabName}` -> tabId). This is the single most important architectural decision.

### 2. Correct batchUpdate field: `addDocumentTab` (not `addTab`)

The field name for creating tabs is `addDocumentTab`, not `addTab`:

```javascript
Docs.Documents.batchUpdate({
  requests: [{
    addDocumentTab: {
      tabProperties: { title: "Tab Name" }
    }
  }]
}, docId);
```

Response field: `reply.addDocumentTab.tabProperties.tabId`. The `deleteTab` field name is correct as-is.

### 3. Update tabs by delete + recreate (not clear + rewrite)

To update a tab's content, you would need to read the doc to find the content range — but that requires tab data the advanced service doesn't return (see #1).

**Workaround**: Delete the tab entirely, create a new one with the same name, insert fresh content. Simpler and avoids reading the doc.

### 4. `UrlFetchApp.fetch` permission issues

Adding `script.external_request` to `appsscript.json` doesn't reliably trigger re-authorization. Avoid `UrlFetchApp` unless absolutely necessary. Use Script Properties for all state tracking instead.

### 5. POST redirects — Python works, curl doesn't

Apps Script web apps redirect POST requests (302). `curl -L` converts POST to GET on redirect, which returns an HTML error page.

**Always use Python `requests`** (which maintains POST through redirects). Don't use curl for testing Apps Script endpoints.

### 6. Guard against empty text style ranges

Malformed markdown (e.g., `*Insufficient data.**`) can produce empty ranges, causing: `Invalid requests[N].updateTextStyle: The range should not be empty.`

**Always guard style requests:**
```javascript
function addStyleRequest(matchStart, matchEnd, textStyle, fields) {
  if (matchEnd <= matchStart) return; // Skip empty ranges
  requests.push({...});
}
```

### 7. ASCII only in Apps Script code

Unicode characters (em dashes, arrows, box-drawing) get mangled by clipboard operations. Use only ASCII in the Apps Script source code.

### 8. Orphaned tabs from partial failures

If tab creation succeeds but content insertion fails, the tab exists in the doc but isn't tracked. Subsequent publishes fail with "Tab title must be unique."

**Mitigation**: The script includes a `findTabIdByTitle` fallback, but it's unreliable since the advanced service doesn't return tabs (#1). Deleting and recreating the doc is the cleanest recovery.

### 9. New docs land in Drive root — move via web UI only

`Docs.Documents.create()` puts docs in the deployer's Drive root. There's no folder parameter without the Drive API.

**NEVER move docs via the mounted Google Drive filesystem** (e.g., `/Users/.../Library/CloudStorage/GoogleDrive-.../My Drive/`). The `.gdoc` files are URL pointers — `mv` removes the pointer without moving the actual document. Docs become inaccessible in Drive. **Always use drive.google.com** web UI to move docs.

### 10. Can't delete the last tab

Google Docs requires at least one tab. When removing the last tab, either remove it from tracking only (leaving content in the doc) or delete the entire doc.

### 11. New docs get an empty default "Tab 1" — clean it up

`Docs.Documents.create()` always creates a default tab named "Tab 1". If you then add custom tabs via `addDocumentTab`, you end up with an unwanted empty tab alongside your real content.

**The script handles this automatically** (v2.1+): `getOrCreateDoc` returns `{docId, isNew, defaultTabId}`. It tries to capture the default tab ID from the `create()` response (`doc.tabs[0].tabProperties.tabId`). After all real tabs are created, `handlePublish` calls `cleanupDefaultTab()` which deletes "Tab 1" using the captured ID (or falls back to `findTabIdByTitle`). This must happen AFTER creating at least one real tab (see #10).

### 12. Native table index calculation

`insertTable` creates an empty table with predictable cell indices. For a table inserted at offset `O` with `R` rows and `C` columns:

- **Cell content index** (empty table): `O + 4 + c*2 + r*(2*C + 1)`
- **Empty table structural size**: `3 + R + 2*R*C`
- **Insert text in REVERSE cell order** (bottom-right to top-left) so earlier cells' indices stay valid
- **Final position** for styling (after all text inserted): structural index + cumulative text length of all preceding cells

Example for a 2x3 table at offset 10: cell (0,0) = 14, cell (0,1) = 16, cell (0,2) = 18, cell (1,0) = 21, etc. The formula accounts for table/row/cell structural elements that consume indices.

## Extending the Apps Script

When you need to add new functionality to the Apps Script:

1. Read the current code at `config/gdocs_publisher_apps_script.js`
2. Add your new handler function and wire it into the `doPost` switch statement
3. Use the same patterns: Script Properties for state, batchUpdate for doc modifications
4. Present the complete updated script to the user — they paste it in the Apps Script editor
5. The user deploys a new version: **Deploy** -> **Manage deployments** -> Edit -> **New version** -> **Deploy**
6. The URL stays the same when using "New version" on an existing deployment

### batchUpdate request types

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

### Script Properties keys

- `doc_{category}` -> Google Doc ID
- `tab_{category}_{tabName}` -> Tab ID
- `API_KEY` -> Shared secret

## Reference Files

- Deployment guide: `!.claude/skills/google-docs/references/deployment-guide.md`
- Full Apps Script code: `config/gdocs_publisher_apps_script.js`
- Detailed learnings: `docs/GDOCS_INTEGRATION.md`
