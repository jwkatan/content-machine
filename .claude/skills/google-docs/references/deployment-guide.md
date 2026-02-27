# Apps Script Deployment Guide

## Initial Setup

1. Go to [script.google.com](https://script.google.com) -> New project
2. Paste the Apps Script code (from `config/gdocs_publisher_apps_script.js` or a new script you create)
3. Go to **Services** (+) -> Add **Google Docs API v1** (userSymbol: `Docs`)
4. Go to **Project Settings** (gear) -> **Script Properties** -> Add:
   - `API_KEY` = (generate a random string, e.g., `openssl rand -base64 32`)
5. **Deploy** -> **New deployment** -> **Web app**
   - Execute as: **Me** (USER_DEPLOYING)
   - Access: **Anyone** (ANYONE_ANONYMOUS)
6. Copy the deployment URL to `.env` as `GDOCS_APPS_SCRIPT_URL`
7. Copy the API_KEY value to `.env` as `GDOCS_API_KEY`

## Updating Code

After changing the Apps Script code:
1. Paste new code in the editor
2. **Deploy** -> **Manage deployments** -> Edit (pencil icon) -> **New version** -> **Deploy**
3. The URL stays the same when using "New version" on an existing deployment

If you can't find "New version", create a brand new deployment. This generates a new URL that must be updated in `.env`.

## Re-authorization

When adding new permissions/scopes:
1. Update `appsscript.json` with new scopes
2. Click **Run** on any function in the editor -> approve the authorization popup
3. Deploy new version

## Manifest (appsscript.json)

Minimal manifest for Google Docs operations:

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
Note: this scope doesn't reliably trigger re-authorization — avoid if possible.

## Testing the Endpoint

Use Python (not curl — curl converts POST to GET on redirect):

```python
import requests
url = "YOUR_DEPLOYMENT_URL"
r = requests.post(url, json={"action": "status", "key": "YOUR_API_KEY"})
print(r.json())
```

A GET request to the URL returns service metadata (no auth required):
```python
r = requests.get(url)
print(r.json())
# {"service": "...", "version": "...", "actions": [...]}
```
