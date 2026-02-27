"""
Google Docs Registry

Local registry for Google Docs managed by the Apps Script integration.
Stores doc/tab/category mappings in config/gdocs_registry.json as the
source of truth, replacing reliance on Apps Script's PropertiesService.

Usage:
    from data_sources.modules.gdocs_registry import GDocsRegistry

    reg = GDocsRegistry()

    # Sync from Apps Script (seed or refresh)
    reg.sync()

    # Look up a doc ID for a category
    doc_id = reg.get_doc_id("research")

    # Look up a tab ID
    tab_id = reg.get_tab_id("research", "My Tab")

    # Publish with local registry (passes doc_id to Apps Script to skip getOrCreateDoc)
    result = reg.publish(category="research", doc_name="Research", tabs=[...])

    # Unpublish with local registry
    result = reg.unpublish(category="research", tab_name="My Tab")

    # List all tracked categories
    print(reg.list_categories())
"""

import os
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import requests

# Load environment from config/.env
_env_path = Path(__file__).parent.parent / "config" / ".env"
if _env_path.exists():
    with open(_env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                if key not in os.environ:
                    os.environ[key] = value

# Registry file path
_registry_path = Path(__file__).parent.parent.parent / "config" / "gdocs_registry.json"


class GDocsRegistry:
    """
    Local registry for Google Docs doc/tab/category mappings.
    Wraps the Apps Script HTTP API with local state tracking.
    """

    def __init__(self, registry_path: Optional[Path] = None):
        self.path = registry_path or _registry_path
        self.url = os.environ.get("GDOCS_APPS_SCRIPT_URL", "")
        self.api_key = os.environ.get("GDOCS_API_KEY", "")
        self._data = self._load()

    def _load(self) -> dict:
        if self.path.exists():
            with open(self.path) as f:
                return json.load(f)
        return {"_meta": {"description": "Google Docs registry", "last_synced": None, "version": 1}, "categories": {}}

    def _save(self):
        with open(self.path, 'w') as f:
            json.dump(self._data, f, indent=2)
            f.write('\n')

    def _post(self, payload: dict) -> dict:
        payload["key"] = self.api_key
        resp = requests.post(self.url, json=payload)
        resp.raise_for_status()
        return resp.json()

    # -- Lookups --

    def get_doc_id(self, category: str) -> Optional[str]:
        cat = self._data["categories"].get(category)
        return cat["docId"] if cat else None

    def get_tab_id(self, category: str, tab_name: str) -> Optional[str]:
        cat = self._data["categories"].get(category)
        if not cat:
            return None
        for tab in cat.get("tabs", []):
            if tab["title"] == tab_name:
                return tab["tabId"]
        return None

    def list_categories(self) -> dict:
        return {k: {"docId": v["docId"], "docName": v["docName"], "tabs": [t["title"] for t in v.get("tabs", [])]}
                for k, v in self._data["categories"].items()}

    # -- Sync from Apps Script --

    def sync(self) -> dict:
        """Fetch current state from Apps Script and update local registry."""
        result = self._post({"action": "status"})
        categories = result.get("categories", {})

        for cat_key, cat_data in categories.items():
            self._data["categories"][cat_key] = {
                "docId": cat_data["docId"],
                "docName": cat_data["docName"],
                "tabs": cat_data.get("tabs", []),
            }

        # Remove local categories not present on server
        for cat_key in list(self._data["categories"].keys()):
            if cat_key not in categories:
                del self._data["categories"][cat_key]

        self._data["_meta"]["last_synced"] = datetime.now(timezone.utc).isoformat()
        self._save()
        return self.list_categories()

    # -- Publish / Unpublish (registry-aware) --

    def publish(self, category: str, tabs: list, doc_name: Optional[str] = None,
                replace_all: bool = False) -> dict:
        """
        Publish tabs to a category doc. If the doc ID is known locally,
        passes it to Apps Script to skip getOrCreateDoc lookup.
        Updates the local registry with the result.
        """
        payload = {
            "action": "publish",
            "category": category,
            "tabs": tabs,
        }
        if doc_name:
            payload["docName"] = doc_name
        if replace_all:
            payload["replaceAll"] = True

        # Pass known doc ID so Apps Script skips getOrCreateDoc
        local_doc_id = self.get_doc_id(category)
        if local_doc_id:
            payload["docId"] = local_doc_id

        result = self._post(payload)

        # Update local registry with response
        doc_id = result.get("docId")
        returned_doc_name = result.get("docName", doc_name or category)
        if doc_id:
            existing = self._data["categories"].get(category, {"tabs": []})
            tab_map = {t["title"]: t["tabId"] for t in existing.get("tabs", [])}

            # Update with new/updated tabs from result
            for r in result.get("results", []):
                tab_map[r["tab"]] = r["tabId"]

            self._data["categories"][category] = {
                "docId": doc_id,
                "docName": returned_doc_name,
                "tabs": [{"tabId": tid, "title": name} for name, tid in tab_map.items()],
            }
            self._save()

        return result

    def unpublish(self, category: str, tab_name: str) -> dict:
        """
        Remove a tab from a category doc.
        Updates the local registry on success.
        """
        payload = {
            "action": "unpublish",
            "category": category,
            "tabName": tab_name,
        }

        # Pass known doc ID
        local_doc_id = self.get_doc_id(category)
        if local_doc_id:
            payload["docId"] = local_doc_id

        result = self._post(payload)

        # Update local registry
        if result.get("removed"):
            cat = self._data["categories"].get(category)
            if cat:
                cat["tabs"] = [t for t in cat["tabs"] if t["title"] != tab_name]
                if not cat["tabs"]:
                    del self._data["categories"][category]
                self._save()

        return result


# -- Convenience functions for CLI usage --

def sync():
    """Sync local registry from Apps Script and print results."""
    reg = GDocsRegistry()
    categories = reg.sync()
    for cat, info in categories.items():
        print(f"\n{cat}: {info['docName']} ({info['docId'][:20]}...)")
        for tab in info['tabs']:
            print(f"  - {tab}")
    if not categories:
        print("No categories found. Is the Apps Script deployed and configured?")
    return categories


def lookup(category: str, tab_name: str = None):
    """Look up a doc or tab ID from the local registry."""
    reg = GDocsRegistry()
    if tab_name:
        tid = reg.get_tab_id(category, tab_name)
        print(f"Tab '{tab_name}' in '{category}': {tid or 'not found'}")
        return tid
    else:
        did = reg.get_doc_id(category)
        print(f"Doc for '{category}': {did or 'not found'}")
        return did


def status():
    """Print the current local registry state (no network call)."""
    reg = GDocsRegistry()
    meta = reg._data.get("_meta", {})
    print(f"Last synced: {meta.get('last_synced', 'never')}")
    cats = reg.list_categories()
    for cat, info in cats.items():
        print(f"\n{cat}: {info['docName']} ({info['docId'][:20]}...)")
        for tab in info['tabs']:
            print(f"  - {tab}")
    if not cats:
        print("Registry is empty. Run sync() to populate from Apps Script.")
    return cats
