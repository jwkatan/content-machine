"""
HubSpot Client — Create forms, emails, workflows, and file uploads for landing pages.

Supports:
- Form creation via Forms API v3
- Marketing email creation via Marketing Emails API v3
- Workflow creation via Automation API v4
- File upload via Files API v3
- End-to-end landing page pipeline orchestration

Usage:
    from data_sources.modules.hubspot_client import HubSpotClient, setup_landing_page_pipeline

    client = HubSpotClient()
    success, result = client.create_form("Download - COBOL Whitepaper", form_type="download")
    # result = {'id': 'form-guid', 'portal_id': '...', ...}
"""

import os
import json
import random
import requests
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv

# Load environment variables
_env_path = Path(__file__).parent.parent / 'config' / '.env'
load_dotenv(_env_path)


class HubSpotClient:
    """Client for HubSpot Marketing API interactions."""

    REGION = os.getenv('HUBSPOT_REGION', 'na1')  # default region (na1 for most accounts)
    BASE_URL = "https://api.hubapi.com"

    # Standard form field definitions for landing pages
    # Labels are empty; placeholder text is used instead (matches site CSS styling)
    DOWNLOAD_FORM_FIELDS = [
        {"name": "firstname", "label": "", "placeholder": "First name", "fieldType": "single_line_text", "required": True},
        {"name": "jobtitle", "label": "", "placeholder": "Job title", "fieldType": "single_line_text", "required": False},
        {"name": "company", "label": "", "placeholder": "Company", "fieldType": "single_line_text", "required": True},
        {"name": "email", "label": "", "placeholder": "Email", "fieldType": "single_line_text", "required": True},
    ]

    WEBINAR_FORM_FIELDS = [
        {"name": "firstname", "label": "", "placeholder": "First name", "fieldType": "single_line_text", "required": True},
        {"name": "jobtitle", "label": "", "placeholder": "Job title", "fieldType": "single_line_text", "required": False},
        {"name": "company", "label": "", "placeholder": "Company", "fieldType": "single_line_text", "required": True},
        {"name": "email", "label": "", "placeholder": "Email", "fieldType": "single_line_text", "required": True},
    ]

    def __init__(self):
        self.access_token = os.getenv('HUBSPOT_ACCESS_TOKEN')
        if not self.access_token:
            raise ValueError("HUBSPOT_ACCESS_TOKEN not found in environment variables")

        self.portal_id = os.getenv('HUBSPOT_PORTAL_ID')
        self._app_base = f"https://app-{self.REGION}.hubspot.com"

    def _portal_url(self, path: str) -> str:
        """Build a HubSpot app URL for the current portal."""
        return f"{self._app_base}/{path}/{self.portal_id}"

    def form_url(self, form_id: str) -> str:
        return f"{self._app_base}/forms/{self.portal_id}/editor/{form_id}/edit/form"

    def email_url(self, email_id: str) -> str:
        return f"{self._app_base}/email/{self.portal_id}/edit/{email_id}"

    def workflow_url(self, workflow_id: str) -> str:
        return f"{self._app_base}/workflows/{self.portal_id}/flow/{workflow_id}/edit"

    def list_url(self, list_id: str) -> str:
        return f"{self._app_base}/contacts/{self.portal_id}/lists/{list_id}"

    def _headers(self) -> Dict:
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
        }

    def _api_request(
        self,
        endpoint: str,
        method: str = 'GET',
        data: Optional[Dict] = None,
    ) -> Tuple[bool, any]:
        """
        Make an API request to HubSpot.

        Returns:
            Tuple of (success, response_data or error_message)
        """
        url = f"{self.BASE_URL}{endpoint}"
        try:
            if method == 'GET':
                resp = requests.get(url, headers=self._headers(), timeout=30)
            elif method == 'POST':
                resp = requests.post(url, headers=self._headers(), json=data, timeout=30)
            elif method == 'PATCH':
                resp = requests.patch(url, headers=self._headers(), json=data, timeout=30)
            elif method == 'DELETE':
                resp = requests.delete(url, headers=self._headers(), timeout=30)
            else:
                return False, f"Unsupported HTTP method: {method}"

            if resp.status_code in (200, 201):
                return True, resp.json() if resp.text else {}
            elif resp.status_code == 204:
                return True, {}
            else:
                error_body = resp.text[:500]
                return False, f"HTTP {resp.status_code}: {error_body}"

        except requests.exceptions.RequestException as e:
            return False, f"Request failed: {str(e)}"

    @staticmethod
    def _get_3digit_random() -> str:
        """
        Generate a random 3-digit suffix (000-999).

        Returns:
            3-digit string (e.g., "042", "789", "001")
        """
        return str(random.randint(0, 999)).zfill(3)

    def create_form(
        self,
        name: str,
        form_type: str = "download",
        custom_fields: Optional[List[Dict]] = None,
        submit_button_text: str = "Download now",
        redirect_url: Optional[str] = None,
        push: bool = False,
    ) -> Tuple[bool, any]:
        """
        Create a new HubSpot form for a landing page.

        Args:
            name: Form name (for HubSpot dashboard)
            form_type: 'download' or 'webinar' (determines default fields)
            custom_fields: Override default fields with custom field definitions
            submit_button_text: Text for the submit button
            redirect_url: URL to redirect after submission (optional)
            push: If True, create on HubSpot. If False, show preview.

        Returns:
            Tuple of (success, form_data or preview_message)
        """
        # Select default fields based on form type
        if custom_fields:
            fields = custom_fields
        elif form_type == 'webinar':
            fields = self.WEBINAR_FORM_FIELDS
            if submit_button_text == "Download now":
                submit_button_text = "Register now"
        else:
            fields = self.DOWNLOAD_FORM_FIELDS

        # Build form field groups for API
        field_groups = []
        for field in fields:
            field_groups.append({
                "groupType": "default_group",
                "richTextType": "text",
                "fields": [{
                    "objectTypeId": "0-1",
                    "name": field["name"],
                    "label": field["label"],
                    "placeholder": field.get("placeholder", ""),
                    "fieldType": field.get("fieldType", "single_line_text"),
                    "required": field.get("required", True),
                    "hidden": False,
                }]
            })

        form_data = {
            "name": name,
            "formType": "hubspot",
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "fieldGroups": field_groups,
            "configuration": {
                "language": "en",
                "createNewContactForNewEmail": True,
                "editable": True,
                "allowLinkToResetKnownValues": False,
                "lifecycleStages": [
                    {"objectTypeId": "0-1", "value": "lead"},
                    {"objectTypeId": "0-2", "value": "lead"},
                ],
            },
            "displayOptions": {
                "renderRawHtml": False,
                "submitButtonText": submit_button_text,
                "style": {
                    "fontFamily": "arial, helvetica, sans-serif",
                    "labelTextColor": "#33475b",
                    "submitColor": "#4154ff",
                    "submitFontColor": "#ffffff",
                },
            },
            "legalConsentOptions": {
                "type": "legitimate_interest",
                "lawfulBasis": "lead",
                "privacyText": "<p>We will use the information you provide consistent with our <a href=\"https://[your-domain.com]/privacy-policy\" rel=\"noopener\">Privacy Policy.</a></p>",
                "subscriptionTypeIds": [137634845, 129684080],
            },
        }

        if redirect_url:
            form_data["configuration"]["postSubmitAction"] = {
                "type": "redirect_url",
                "value": redirect_url,
            }
        else:
            form_data["configuration"]["postSubmitAction"] = {
                "type": "thank_you",
                "value": "Thanks for your submission!",
            }

        if not push:
            summary = (
                f"=== HUBSPOT FORM PREVIEW (not pushed) ===\n"
                f"Name: {name}\n"
                f"Type: {form_type}\n"
                f"Submit Button: {submit_button_text}\n"
                f"Redirect URL: {redirect_url or '(inline thank you)'}\n"
                f"Fields:\n"
            )
            for field in fields:
                req = "required" if field.get("required", True) else "optional"
                summary += f"  - {field['label']} ({field['name']}) [{req}]\n"
            summary += f"\nTo actually create on HubSpot, run with push=True\n"
            summary += f"==================================="
            return True, summary

        success, result = self._api_request(
            '/marketing/v3/forms',
            method='POST',
            data=form_data,
        )

        if not success:
            return False, f"Failed to create form: {result}"

        form_id = result.get('id', '')
        return True, {
            'id': form_id,
            'name': result.get('name', name),
            'portal_id': self.portal_id,
            'created_at': result.get('createdAt', ''),
            'embed_url': f"https://share-{self.REGION}.hsforms.com/{form_id}",
            'hubspot_url': self.form_url(form_id),
        }

    def get_form(self, form_id: str) -> Tuple[bool, any]:
        """Fetch a form by its ID."""
        return self._api_request(f'/marketing/v3/forms/{form_id}')

    def list_forms(self, limit: int = 20) -> Tuple[bool, any]:
        """List forms in the account."""
        return self._api_request(f'/marketing/v3/forms?limit={limit}')

    def create_marketing_email(
        self,
        name: str,
        subject: str,
        content: Optional[Dict] = None,
        body_html: str = "",
        from_name: str = os.getenv('HUBSPOT_FROM_NAME', '[COMPANY] Team'),
        from_email: Optional[str] = None,
        reply_to_email: Optional[str] = None,
        folder_id: Optional[str] = None,
        push: bool = False,
    ) -> Tuple[bool, any]:
        """
        Create a marketing email (for autoresponder workflows).

        Supports two content modes:
        1. DnD structure (preferred): Pass `content` dict with flexAreas, widgets, etc.
        2. Raw HTML (legacy): Pass `body_html` string.

        Args:
            name: Internal email name
            subject: Email subject line
            content: DnD email content dict (from build_autoresponder_email_content)
            body_html: HTML body content (legacy fallback)
            from_name: Sender name
            from_email: Sender email (from .env default if not provided)
            reply_to_email: Reply-to email address (separate from sender)
            folder_id: HubSpot email folder ID (e.g. os.getenv("HUBSPOT_EMAIL_FOLDER_ID"))
            push: If True, create on HubSpot. If False, show preview.

        Returns:
            Tuple of (success, email_data or preview_message)
        """
        if not from_email:
            from_email = os.getenv('HUBSPOT_FROM_EMAIL', os.getenv('HUBSPOT_FROM_EMAIL'))

        if not reply_to_email:
            reply_to_email = os.getenv('HUBSPOT_REPLY_TO_EMAIL', os.getenv('HUBSPOT_REPLY_TO_EMAIL'))

        if not push:
            summary = (
                f"=== HUBSPOT EMAIL PREVIEW (not pushed) ===\n"
                f"Name: {name}\n"
                f"Subject: {subject}\n"
                f"From: {from_name} <{from_email}>\n"
                f"Reply-To: {reply_to_email}\n"
                f"Folder: {folder_id or '(none)'}\n"
                f"Template: {'DnD modules' if content else 'raw HTML'}\n"
                f"\nTo actually create on HubSpot, run with push=True\n"
                f"==================================="
            )
            return True, summary

        email_data = {
            "name": name,
            "subject": subject,
            "from": {
                "fromName": from_name,
                "replyTo": reply_to_email or "",
            },
        }

        # Use DnD content structure if provided, otherwise fall back to raw HTML
        if content:
            email_data["content"] = content
        else:
            email_data["content"] = {
                "body": body_html,
                "plainTextVersion": "",
            }

        if folder_id:
            email_data["folderId"] = folder_id

        success, result = self._api_request(
            '/marketing/v3/emails',
            method='POST',
            data=email_data,
        )

        if not success:
            return False, f"Failed to create email: {result}"

        email_id = result.get('id', '')
        return True, {
            'id': email_id,
            'name': name,
            'subject': subject,
            'hubspot_url': self.email_url(email_id),
        }

    def update_email(
        self,
        email_id: str,
        updates: Optional[Dict] = None,
        html: Optional[str] = None,
        subject: Optional[str] = None,
        from_name: Optional[str] = None,
        reply_to: Optional[str] = None,
        push: bool = False,
    ) -> Tuple[bool, any]:
        """
        Update an existing marketing email via PATCH.

        Safe pattern: GETs the email first, modifies in-place, PATCHes back.
        This preserves the template mode and any manual editor changes.

        Supports two usage modes:
        1. Simple: Pass html/subject/from_name to update common fields.
           The html is placed into the correct widget automatically
           (module-1-0-0 for DnD, hs_email_body for Design Manager).
        2. Advanced: Pass updates dict with raw PATCH fields.

        Args:
            email_id: HubSpot email ID to update
            updates: Raw PATCH payload dict (advanced usage)
            html: New HTML body content (simple usage)
            subject: New subject line
            from_name: New sender name
            reply_to: New reply-to email
            push: If True, apply changes. If False, show preview.

        Returns:
            Tuple of (success, result_data or preview_message)
        """
        # GET current email to preserve structure
        success, current = self._api_request(f'/marketing/v3/emails/{email_id}')
        if not success:
            return False, f"Failed to fetch email {email_id}: {current}"

        patch_data = updates.copy() if updates else {}

        # Simple field updates
        if subject:
            patch_data['subject'] = subject
        if from_name or reply_to:
            patch_data['from'] = current.get('from', {}).copy()
            if from_name:
                patch_data['from']['fromName'] = from_name
            if reply_to:
                patch_data['from']['replyTo'] = reply_to

        # HTML body update — detect template mode and update correct widget
        if html:
            content = current.get('content', {})
            widgets = content.get('widgets', {})

            if 'hs_email_body' in widgets:
                # Design Manager (plain-text template)
                content['widgets']['hs_email_body']['body']['html'] = html
            elif 'module-1-0-0' in widgets:
                # DnD — rich_text widget
                content['widgets']['module-1-0-0']['body']['html'] = html
            else:
                return False, f"Cannot find body widget in email {email_id}. Widget keys: {list(widgets.keys())}"

            patch_data['content'] = content

        if not patch_data:
            return False, "No updates provided"

        if not push:
            summary = (
                f"=== HUBSPOT EMAIL UPDATE PREVIEW (not pushed) ===\n"
                f"Email ID: {email_id}\n"
                f"Current name: {current.get('name')}\n"
                f"Fields to update: {list(patch_data.keys())}\n"
                f"\nTo actually update on HubSpot, run with push=True\n"
                f"==================================="
            )
            return True, summary

        success, result = self._api_request(
            f'/marketing/v3/emails/{email_id}',
            method='PATCH',
            data=patch_data,
        )

        if not success:
            return False, f"Failed to update email {email_id}: {result}"

        return True, {
            'id': email_id,
            'name': result.get('name', ''),
            'subject': result.get('subject', ''),
            'hubspot_url': self.email_url(email_id),
        }

    def upload_file(
        self,
        file_path: str,
        folder: str = "Gated Documents",
        push: bool = False,
    ) -> Tuple[bool, any]:
        """
        Upload a file to HubSpot file manager.

        Args:
            file_path: Local path to the file to upload
            folder: HubSpot folder path (default: "Gated Documents")
            push: If True, upload to HubSpot. If False, show preview.

        Returns:
            Tuple of (success, file_data or preview_message)
        """
        path = Path(file_path)
        if not path.exists():
            return False, f"File not found: {file_path}"

        file_size_kb = path.stat().st_size / 1024

        if not push:
            summary = (
                f"=== HUBSPOT FILE UPLOAD PREVIEW (not pushed) ===\n"
                f"File: {path.name}\n"
                f"Size: {file_size_kb:.1f} KB\n"
                f"Folder: /{folder}\n"
                f"Access: PUBLIC_NOT_INDEXABLE\n"
                f"\nTo actually upload to HubSpot, run with push=True\n"
                f"==================================="
            )
            return True, summary

        url = f"{self.BASE_URL}/files/v3/files"
        headers = {'Authorization': f'Bearer {self.access_token}'}

        options = json.dumps({
            "access": "PUBLIC_NOT_INDEXABLE",
            "overwrite": False,
            "duplicateValidationStrategy": "NONE",
        })

        with open(path, 'rb') as f:
            files = {
                'file': (path.name, f, 'application/octet-stream'),
                'options': (None, options, 'application/json'),
                'folderPath': (None, f'/{folder}'),
            }
            try:
                resp = requests.post(url, headers=headers, files=files, timeout=60)
            except requests.exceptions.RequestException as e:
                return False, f"Upload failed: {str(e)}"

        if resp.status_code in (200, 201):
            result = resp.json()
            file_id = result.get('id', '')
            return True, {
                'id': file_id,
                'name': result.get('name', ''),
                'url': result.get('url', ''),
                'default_hosting_url': result.get('defaultHostingUrl', ''),
                'size': result.get('size', 0),
                'hubspot_url': f"{self._app_base}/files/{self.portal_id}?selectedFile={file_id}",
            }
        else:
            return False, f"HTTP {resp.status_code}: {resp.text[:500]}"

    def create_autoresponder_email(
        self,
        asset_type: str,
        asset_title: str,
        download_url: str = "",
        replay_url: str = "",
        benefit_bullets: Optional[List[str]] = None,
        folder_id: Optional[str] = None,
        name_suffix: Optional[str] = None,
        push: bool = False,
    ) -> Tuple[bool, any]:
        """
        Create a marketing email for use as an autoresponder in a workflow.

        Generates DnD email content matching autoresponder design:
        banner image → content with download link → benefit bullets → CTA → footer.

        Args:
            asset_type: 'download' or 'webinar'
            asset_title: Title of the asset/webinar
            download_url: Direct download URL (for gated downloads)
            replay_url: Replay page URL (for recorded webinars)
            benefit_bullets: List of 2-4 bullet points summarizing the content
            folder_id: HubSpot email folder ID (defaults per asset type)
            name_suffix: Optional suffix to append to email name (e.g., #123)
            push: If True, create on HubSpot. If False, show preview.

        Returns:
            Tuple of (success, email_data or preview_message)
        """
        subject, email_content = self.build_autoresponder_email_content(
            asset_type=asset_type,
            asset_title=asset_title,
            download_url=download_url,
            replay_url=replay_url,
            benefit_bullets=benefit_bullets,
        )

        name = f"Autoresponder - {asset_title}" + (f" #{name_suffix}" if name_suffix else "")

        # Default folder per asset type
        if not folder_id:
            folder_id = self.EMAIL_FOLDER_GATED_DOCUMENT

        return self.create_marketing_email(
            name=name,
            subject=subject,
            content=email_content,
            from_name=os.getenv('HUBSPOT_FROM_NAME', '[COMPANY] Team'),
            from_email=os.getenv('HUBSPOT_FROM_EMAIL'),
            reply_to_email=os.getenv('HUBSPOT_REPLY_TO_EMAIL'),
            folder_id=folder_id,
            push=push,
        )

    def create_autoresponder_workflow(
        self,
        form_id: str,
        email_id: str,
        name: str,
        list_id: Optional[str] = None,
        salesforce_campaign_id: Optional[str] = None,
        push: bool = False,
    ) -> Tuple[bool, any]:
        """
        Create a workflow triggered by form submission.

        Action order (matches existing GD workflows):
        1. Add to static list
        2. Send autoresponder email
        3. Set Salesforce campaign status to "Responded"
        4. Delay 4 hours (14400 seconds)

        Uses EVENT_BASED enrollment with refinement to exclude
        emails containing "[COMPANY domain]" or "test".

        The workflow is always created as DISABLED. Enable manually after review.

        Args:
            form_id: HubSpot form GUID (trigger)
            email_id: HubSpot marketing email ID (action)
            name: Workflow name
            list_id: Static list ID to add contacts to
            salesforce_campaign_id: Salesforce campaign ID (e.g. "701Q500000ipIOAIA2")
            push: If True, create on HubSpot. If False, show preview.

        Returns:
            Tuple of (success, workflow_data or preview_message)
        """
        # Build action chain: list → email → salesforce → delay
        actions = []
        action_id = 1

        # Action 1: Add to list
        if list_id:
            action = {
                "actionId": str(action_id),
                "actionTypeId": "0-63809083",
                "actionTypeVersion": 3,
                "fields": {"listId": str(list_id)},
                "type": "SINGLE_CONNECTION",
            }
            actions.append(action)
            action_id += 1

        # Action 2: Send email
        email_action = {
            "actionId": str(action_id),
            "actionTypeId": "0-4",
            "actionTypeVersion": 0,
            "fields": {"content_id": str(email_id)},
            "type": "SINGLE_CONNECTION",
        }
        actions.append(email_action)
        action_id += 1

        # Action 3: Salesforce campaign
        if salesforce_campaign_id:
            sf_action = {
                "actionId": str(action_id),
                "actionTypeId": "0-18",
                "actionTypeVersion": 0,
                "fields": {
                    "campaign_id": salesforce_campaign_id,
                    "status": "Responded",
                },
                "type": "SINGLE_CONNECTION",
            }
            actions.append(sf_action)
            action_id += 1

        # Action 4: Delay 4 hours
        delay_action = {
            "actionId": str(action_id),
            "actionTypeId": "0-1",
            "actionTypeVersion": 0,
            "fields": {"delta": "14400", "time_unit": "MINUTES"},
            "type": "SINGLE_CONNECTION",
        }
        actions.append(delay_action)
        action_id += 1

        # Wire up connections between actions
        for i in range(len(actions) - 1):
            actions[i]["connection"] = {
                "edgeType": "STANDARD",
                "nextActionId": actions[i + 1]["actionId"],
            }

        flow_data = {
            "name": f"GD - {name}" if "download" in name.lower() or not name.startswith("GD") else name,
            "type": "CONTACT_FLOW",
            "flowType": "WORKFLOW",
            "objectTypeId": "0-1",
            "isEnabled": False,
            "enrollmentCriteria": {
                "type": "EVENT_BASED",
                "shouldReEnroll": False,
                "eventFilterBranches": [{
                    "filterBranches": [],
                    "filters": [{
                        "property": "hs_form_id",
                        "operation": {
                            "operator": "IS_ANY_OF",
                            "includeObjectsWithNoValueSet": False,
                            "values": [form_id],
                            "operationType": "ENUMERATION",
                        },
                        "filterType": "PROPERTY",
                    }],
                    "eventTypeId": "4-1639801",
                    "operator": "HAS_COMPLETED",
                    "filterBranchType": "UNIFIED_EVENTS",
                    "filterBranchOperator": "AND",
                }],
                "refinementCriteria": {
                    "filterBranches": [{
                        "filterBranches": [],
                        "filters": [{
                            "property": "email",
                            "operation": {
                                "operator": "DOES_NOT_CONTAIN",
                                "includeObjectsWithNoValueSet": False,
                                "values": [os.getenv('HUBSPOT_COMPANY_DOMAIN', ''), "test"],
                                "operationType": "MULTISTRING",
                            },
                            "filterType": "PROPERTY",
                        }],
                        "filterBranchType": "AND",
                        "filterBranchOperator": "AND",
                    }],
                    "filters": [],
                    "filterBranchType": "OR",
                    "filterBranchOperator": "OR",
                },
                "listMembershipFilterBranches": [],
            },
            "actions": actions,
            "startActionId": "1",
            "nextAvailableActionId": str(action_id),
        }

        if not push:
            lines = [
                f"=== HUBSPOT WORKFLOW PREVIEW (not pushed) ===",
                f"Name: {flow_data['name']}",
                f"Trigger: Form submission (form {form_id})",
                f"  Excludes: emails containing '[COMPANY domain]' or 'test'",
            ]
            step = 1
            if list_id:
                lines.append(f"  Action {step}: Add to list (list ID {list_id})")
                step += 1
            lines.append(f"  Action {step}: Send email (email ID {email_id})")
            step += 1
            if salesforce_campaign_id:
                lines.append(f"  Action {step}: Salesforce campaign ({salesforce_campaign_id}) → Responded")
                step += 1
            lines.append(f"  Action {step}: Delay 4 hours")
            lines.append(f"Status: DISABLED (enable manually after review)")
            lines.append(f"\nTo actually create on HubSpot, run with push=True")
            lines.append(f"===================================")
            return True, "\n".join(lines)

        success, result = self._api_request(
            '/automation/v4/flows',
            method='POST',
            data=flow_data,
        )

        if not success:
            return False, f"Failed to create workflow: {result}"

        wf_id = result.get('id', '')
        return True, {
            'id': wf_id,
            'name': result.get('name', ''),
            'is_enabled': result.get('isEnabled', False),
            'hubspot_url': self.workflow_url(wf_id),
        }

    def create_webinar_workflow(
        self,
        form_id: str,
        zoom_webinar_id: str,
        salesforce_campaign_id: str,
        name: str,
        webinar_year: int,
        webinar_month: int,
        webinar_day: int,
        webinar_hour: int = 11,
        webinar_minute: int = 0,
        timezone: str = "US/Eastern",
        wait_hour: int = 14,
        wait_minute: int = 0,
        attended_email_id: Optional[str] = None,
        noshow_email_id: Optional[str] = None,
        list_id: Optional[str] = None,
        push: bool = False,
    ) -> Tuple[bool, any]:
        """
        Create a webinar registration workflow matching the proven pattern
        based on standard webinar workflow.

        Flow:
        Start → Filter test emails → Branch on-demand vs live
          On-demand path: SF "On Demand" → delay → end
          Live path: SF "Registered" → Add to Zoom → Wait until webinar →
            Branch attended? → SF "Attended"/"No Show" → follow-up emails → end

        Args:
            form_id: HubSpot form GUID (enrollment trigger)
            zoom_webinar_id: Zoom webinar ID (e.g. "83485036578")
            salesforce_campaign_id: Salesforce campaign ID
            name: Workflow name
            webinar_year/month/day: Webinar date
            webinar_hour/minute: Webinar start time (in timezone)
            timezone: Timezone for date checks (default US/Eastern)
            wait_hour/minute: Time to check attendance after webinar (default 14:00)
            attended_email_id: HubSpot email ID for attended follow-up (optional)
            noshow_email_id: HubSpot email ID for no-show follow-up (optional)
            list_id: Static list ID to add contacts to (optional, future use)
            push: If True, create on HubSpot. If False, show preview.

        Returns:
            Tuple of (success, workflow_data or preview_message)
        """
        import calendar
        from datetime import datetime as dt

        # Calculate wait-until timestamp (midnight UTC of webinar day)
        webinar_date = dt(webinar_year, webinar_month, webinar_day)
        wait_timestamp_ms = str(int(calendar.timegm(webinar_date.timetuple()) * 1000))

        # Build all actions using the same IDs as the sample workflow
        actions = []

        # Action 12 (START): Filter test emails
        actions.append({
            "actionId": "12",
            "listBranches": [{
                "filterBranch": {
                    "filterBranches": [{
                        "filterBranches": [],
                        "filters": [{
                            "property": "email",
                            "operation": {
                                "operator": "CONTAINS",
                                "includeObjectsWithNoValueSet": False,
                                "values": ["test"],
                                "operationType": "MULTISTRING",
                            },
                            "filterType": "PROPERTY",
                        }],
                        "filterBranchType": "AND",
                        "filterBranchOperator": "AND",
                    }],
                    "filters": [],
                    "filterBranchType": "OR",
                    "filterBranchOperator": "OR",
                },
                "branchName": "Test emails",
                # No connection = dead end for test emails
            }],
            "defaultBranchName": "Real registrations",
            "defaultBranch": {
                "edgeType": "STANDARD",
                "nextActionId": "1",
            },
            "type": "LIST_BRANCH",
        })

        # Action 1: Branch - Is webinar on demand?
        actions.append({
            "actionId": "1",
            "listBranches": [{
                "filterBranch": {
                    "filterBranches": [{
                        "filterBranches": [],
                        "filters": [{
                            "property": "today",
                            "operation": {
                                "operator": "IS_AFTER",
                                "includeObjectsWithNoValueSet": False,
                                "timePoint": {
                                    "timezoneSource": "CUSTOM",
                                    "zoneId": timezone,
                                    "year": webinar_year,
                                    "month": webinar_month,
                                    "day": webinar_day,
                                    "hour": 23,
                                    "minute": 59,
                                    "second": 59,
                                    "millisecond": 999,
                                    "timeType": "DATE",
                                },
                                "endpointBehavior": "EXCLUSIVE",
                                "propertyParser": "VALUE_WITH_ZONE_SAME_LOCAL_CONVERSION",
                                "operationType": "TIME_POINT",
                                "type": "TIME_POINT",
                            },
                            "filterType": "PROPERTY",
                        }],
                        "filterBranchType": "AND",
                        "filterBranchOperator": "AND",
                    }],
                    "filters": [],
                    "filterBranchType": "OR",
                    "filterBranchOperator": "OR",
                },
                "branchName": "Webinar is on demand",
                "connection": {
                    "edgeType": "STANDARD",
                    "nextActionId": "2",
                },
            }],
            "defaultBranchName": "Webinar is before on demand",
            "defaultBranch": {
                "edgeType": "STANDARD",
                "nextActionId": "3",
            },
            "type": "LIST_BRANCH",
        })

        # === ON-DEMAND PATH ===

        # Action 2: Set SF campaign "On Demand"
        actions.append({
            "actionId": "2",
            "actionTypeVersion": 0,
            "actionTypeId": "0-18",
            "connection": {
                "edgeType": "STANDARD",
                "nextActionId": "4",
            },
            "fields": {
                "campaign_id": salesforce_campaign_id,
                "status": "On Demand",
            },
            "type": "SINGLE_CONNECTION",
        })

        # Action 4: Delay (terminal for on-demand path)
        actions.append({
            "actionId": "4",
            "actionTypeVersion": 0,
            "actionTypeId": "0-1",
            "fields": {"delta": "14400", "time_unit": "MINUTES"},
            "type": "SINGLE_CONNECTION",
        })

        # === LIVE REGISTRATION PATH ===

        # Action 3: Set SF campaign "Registered"
        actions.append({
            "actionId": "3",
            "actionTypeVersion": 0,
            "actionTypeId": "0-18",
            "connection": {
                "edgeType": "STANDARD",
                "nextActionId": "5",
            },
            "fields": {
                "campaign_id": salesforce_campaign_id,
                "status": "Registered",
            },
            "type": "SINGLE_CONNECTION",
        })

        # Action 5: Add contact to Zoom webinar
        actions.append({
            "actionId": "5",
            "actionTypeVersion": 11,
            "actionTypeId": "1-67",
            "connection": {
                "edgeType": "STANDARD",
                "nextActionId": "9",
            },
            "fields": {
                "webinarId": str(zoom_webinar_id),
            },
            "type": "SINGLE_CONNECTION",
        })

        # Action 9: Wait until webinar date + wait_hour
        actions.append({
            "actionId": "9",
            "actionTypeVersion": 0,
            "actionTypeId": "0-35",
            "connection": {
                "edgeType": "STANDARD",
                "nextActionId": "6",
            },
            "fields": {
                "date": {
                    "staticValue": wait_timestamp_ms,
                    "type": "STATIC_VALUE",
                },
                "delta": "0",
                "time_unit": "DAYS",
                "time_of_day": {
                    "hour": wait_hour,
                    "minute": wait_minute,
                },
            },
            "type": "SINGLE_CONNECTION",
        })

        # Action 6: Branch - Did they attend? (Zoom integration event)
        actions.append({
            "actionId": "6",
            "listBranches": [{
                "filterBranch": {
                    "filterBranches": [{
                        "filterBranches": [],
                        "filters": [{
                            "eventTypeId": 391778,
                            "filterLines": [
                                {
                                    "property": "webinarId",
                                    "operation": {
                                        "operator": "IS_EQUAL_TO",
                                        "includeObjectsWithNoValueSet": False,
                                        "values": [str(zoom_webinar_id)],
                                        "operationType": "MULTISTRING",
                                    },
                                },
                                {
                                    "property": "durationSeconds",
                                    "operation": {
                                        "operator": "IS_GREATER_THAN",
                                        "includeObjectsWithNoValueSet": False,
                                        "value": 10.0,
                                        "operationType": "NUMBER",
                                    },
                                },
                            ],
                            "filterType": "INTEGRATION_EVENT",
                        }],
                        "filterBranchType": "AND",
                        "filterBranchOperator": "AND",
                    }],
                    "filters": [],
                    "filterBranchType": "OR",
                    "filterBranchOperator": "OR",
                },
                "branchName": "Attended Webinar",
                "connection": {
                    "edgeType": "STANDARD",
                    "nextActionId": "7",
                },
            }],
            "defaultBranchName": "Did not attend webinar",
            "defaultBranch": {
                "edgeType": "STANDARD",
                "nextActionId": "8",
            },
            "type": "LIST_BRANCH",
        })

        # === ATTENDED PATH ===

        # Action 7: Set SF campaign "Attended"
        attended_next = "10" if attended_email_id else None
        action_7 = {
            "actionId": "7",
            "actionTypeVersion": 0,
            "actionTypeId": "0-18",
            "fields": {
                "campaign_id": salesforce_campaign_id,
                "status": "Attended",
            },
            "type": "SINGLE_CONNECTION",
        }
        if attended_next:
            action_7["connection"] = {
                "edgeType": "STANDARD",
                "nextActionId": attended_next,
            }
        actions.append(action_7)

        # Action 10 + 13 + 14: Delay → Send attended email → Delay (if email provided)
        if attended_email_id:
            actions.append({
                "actionId": "10",
                "actionTypeVersion": 0,
                "actionTypeId": "0-1",
                "connection": {
                    "edgeType": "STANDARD",
                    "nextActionId": "13",
                },
                "fields": {"delta": "1", "time_unit": "MINUTES"},
                "type": "SINGLE_CONNECTION",
            })
            actions.append({
                "actionId": "13",
                "actionTypeVersion": 0,
                "actionTypeId": "0-4",
                "connection": {
                    "edgeType": "STANDARD",
                    "nextActionId": "14",
                },
                "fields": {"content_id": str(attended_email_id)},
                "type": "SINGLE_CONNECTION",
            })
            actions.append({
                "actionId": "14",
                "actionTypeVersion": 0,
                "actionTypeId": "0-1",
                "fields": {"delta": "14400", "time_unit": "MINUTES"},
                "type": "SINGLE_CONNECTION",
            })

        # === NO-SHOW PATH ===

        # Action 8: Set SF campaign "No Show"
        noshow_next = "11" if noshow_email_id else None
        action_8 = {
            "actionId": "8",
            "actionTypeVersion": 0,
            "actionTypeId": "0-18",
            "fields": {
                "campaign_id": salesforce_campaign_id,
                "status": "No Show",
            },
            "type": "SINGLE_CONNECTION",
        }
        if noshow_next:
            action_8["connection"] = {
                "edgeType": "STANDARD",
                "nextActionId": noshow_next,
            }
        actions.append(action_8)

        # Action 11 + 16 + 15: Delay → Send no-show email → Delay (if email provided)
        if noshow_email_id:
            actions.append({
                "actionId": "11",
                "actionTypeVersion": 0,
                "actionTypeId": "0-1",
                "connection": {
                    "edgeType": "STANDARD",
                    "nextActionId": "16",
                },
                "fields": {"delta": "1", "time_unit": "MINUTES"},
                "type": "SINGLE_CONNECTION",
            })
            actions.append({
                "actionId": "16",
                "actionTypeVersion": 0,
                "actionTypeId": "0-4",
                "connection": {
                    "edgeType": "STANDARD",
                    "nextActionId": "15",
                },
                "fields": {"content_id": str(noshow_email_id)},
                "type": "SINGLE_CONNECTION",
            })
            actions.append({
                "actionId": "15",
                "actionTypeVersion": 0,
                "actionTypeId": "0-1",
                "fields": {"delta": "14400", "time_unit": "MINUTES"},
                "type": "SINGLE_CONNECTION",
            })

        # Calculate next available action ID
        all_ids = [int(a["actionId"]) for a in actions]
        next_id = max(all_ids) + 1

        flow_data = {
            "name": name,
            "type": "CONTACT_FLOW",
            "flowType": "WORKFLOW",
            "objectTypeId": "0-1",
            "isEnabled": False,
            "enrollmentCriteria": {
                "type": "EVENT_BASED",
                "shouldReEnroll": False,
                "eventFilterBranches": [{
                    "filterBranches": [],
                    "filters": [{
                        "property": "hs_form_id",
                        "operation": {
                            "operator": "IS_ANY_OF",
                            "includeObjectsWithNoValueSet": False,
                            "values": [form_id],
                            "operationType": "ENUMERATION",
                        },
                        "filterType": "PROPERTY",
                    }],
                    "eventTypeId": "4-1639801",
                    "operator": "HAS_COMPLETED",
                    "filterBranchType": "UNIFIED_EVENTS",
                    "filterBranchOperator": "AND",
                }],
                "listMembershipFilterBranches": [],
            },
            "actions": actions,
            "startActionId": "12",
            "nextAvailableActionId": str(next_id),
        }

        if not push:
            date_str = f"{webinar_year}-{webinar_month:02d}-{webinar_day:02d}"
            lines = [
                f"=== WEBINAR WORKFLOW PREVIEW (not pushed) ===",
                f"Name: {name}",
                f"Trigger: Form submission (form {form_id})",
                f"  Excludes: emails containing 'test'",
                f"",
                f"  Start → Filter test emails",
                f"  → Branch: Is webinar on demand? (after {date_str} {timezone})",
                f"    On-demand: SF '{salesforce_campaign_id}' → 'On Demand' → delay → end",
                f"    Live registration:",
                f"      SF → 'Registered'",
                f"      → Add to Zoom webinar ({zoom_webinar_id})",
                f"      → Wait until {date_str} at {wait_hour:02d}:{wait_minute:02d}",
                f"      → Branch: Attended webinar? (Zoom event, duration > 10s)",
                f"        Attended: SF → 'Attended'" + (f" → send email {attended_email_id} → delay" if attended_email_id else ""),
                f"        No-show: SF → 'No Show'" + (f" → send email {noshow_email_id} → delay" if noshow_email_id else ""),
                f"",
                f"Status: DISABLED (enable manually after review)",
                f"\nTo create on HubSpot, run with push=True",
                f"===================================",
            ]
            return True, "\n".join(lines)

        success, result = self._api_request(
            '/automation/v4/flows',
            method='POST',
            data=flow_data,
        )

        if not success:
            return False, f"Failed to create webinar workflow: {result}"

        wf_id = result.get('id', '')
        return True, {
            'id': wf_id,
            'name': result.get('name', ''),
            'is_enabled': result.get('isEnabled', False),
            'hubspot_url': self.workflow_url(wf_id),
        }

    def create_contact_list(
        self,
        name: str,
        folder_id: Optional[str] = None,
        push: bool = False,
    ) -> Tuple[bool, any]:
        """
        Create a static contact list in HubSpot.

        Args:
            name: List name
            folder_id: Folder ID to place the list in (optional)
            push: If True, create on HubSpot. If False, show preview.

        Returns:
            Tuple of (success, list_data or preview_message)
        """
        if not push:
            summary = (
                f"=== HUBSPOT LIST PREVIEW (not pushed) ===\n"
                f"Name: {name}\n"
                f"Type: STATIC\n"
                f"Folder: {folder_id or '(root)'}\n"
                f"\nTo actually create on HubSpot, run with push=True\n"
                f"==================================="
            )
            return True, summary

        list_data = {
            "name": name,
            "objectTypeId": "0-1",
            "processingType": "MANUAL",
        }
        if folder_id:
            list_data["folderId"] = folder_id

        success, result = self._api_request(
            '/crm/v3/lists',
            method='POST',
            data=list_data,
        )

        if not success:
            return False, f"Failed to create list: {result}"

        list_id = str(result.get('listId', ''))
        return True, {
            'id': list_id,
            'name': result.get('name', name),
            'hubspot_url': self.list_url(list_id),
        }

    def list_folders(self) -> Tuple[bool, any]:
        """List all contact list folders."""
        return self._api_request('/crm/v3/lists/folders')

    def find_or_create_folder(
        self,
        folder_name: str,
        parent_folder_id: str = "0",
        push: bool = False,
    ) -> Tuple[bool, any]:
        """
        Find an existing list folder by name, or create it.

        Args:
            folder_name: Name of the folder to find or create
            parent_folder_id: Parent folder ID (default "0" = root)
            push: If True, create if not found. If False, search only.

        Returns:
            Tuple of (success, folder_data)
        """
        # Search existing folders
        success, folders_data = self.list_folders()
        if success:
            folders = folders_data.get('folders', [])
            for folder in folders:
                if folder.get('name') == folder_name:
                    return True, {
                        'id': str(folder.get('id', '')),
                        'name': folder.get('name', ''),
                    }

        if not push:
            return True, {'id': None, 'name': folder_name, 'note': 'Would create folder'}

        # Create the folder
        success, result = self._api_request(
            '/crm/v3/lists/folders',
            method='POST',
            data={
                "name": folder_name,
                "parentFolderId": parent_folder_id,
            },
        )

        if not success:
            return False, f"Failed to create folder: {result}"

        return True, {
            'id': str(result.get('id', '')),
            'name': result.get('name', folder_name),
        }

    # Standard email banner image
    EMAIL_BANNER_URL = os.getenv('HUBSPOT_EMAIL_BANNER_URL', '')

    # Email folder IDs
    EMAIL_FOLDER_GATED_DOCUMENT = os.getenv('HUBSPOT_EMAIL_FOLDER_ID', '')

    # Contact list folder names
    LIST_FOLDER_GATED_DOCUMENT = os.getenv('HUBSPOT_LIST_FOLDER_DOWNLOAD', 'gated document')
    LIST_FOLDER_WEBINAR = os.getenv('HUBSPOT_LIST_FOLDER_WEBINAR', 'webinar')

    def build_autoresponder_email_content(
        self,
        asset_type: str,
        asset_title: str,
        download_url: str = "",
        replay_url: str = "",
        benefit_bullets: Optional[List[str]] = None,
    ) -> Tuple[str, Dict]:
        """
        Generate subject line and DnD email content structure for an autoresponder.

        Matches the HubSpot DnD email template used in existing autoresponders
        (e.g. email 249298878680). Structure:
        - Banner image (standardized)
        - Rich text with download/watch link + benefit bullets
        - Divider
        - CTA section with "Learn more" link to [your-domain.com]
        - Footer (unsubscribe)

        Args:
            asset_type: 'download' or 'webinar'
            asset_title: Title of the asset/webinar
            download_url: Direct download URL (for gated downloads)
            replay_url: Replay page URL (for recorded webinars)
            benefit_bullets: List of 2-4 bullet points summarizing the content

        Returns:
            Tuple of (subject_line, email_content_dict) where email_content_dict
            has 'flexAreas', 'widgets', 'styleSettings', and 'templatePath'
        """
        # Subject line (asset_title used as-is, no type prefix)
        if asset_type == 'download':
            subject = f"Your copy: {asset_title}"
            cta_url = download_url
            cta_text = "Click here to download"
            intro = f"You are on your way to making the most of <strong>{asset_title}</strong>."
        elif replay_url:
            subject = f"Your webinar replay: {asset_title}"
            cta_url = replay_url
            cta_text = "Click here to watch the replay"
            intro = f"Thank you for your interest in <strong>{asset_title}</strong>."
        else:
            subject = f"You're registered: {asset_title}"
            cta_url = "#"
            cta_text = "We'll send you a reminder before the webinar starts"
            intro = f"You're registered for <strong>{asset_title}</strong>."

        # Build the rich text body
        body_html = (
            f'<p style="margin-bottom: 10px; font-size: 14px; line-height: 150%;">'
            f'{intro}<br><br>'
            f'<a href="{cta_url}" target="_blank" style="font-weight: bold;" rel="noopener">'
            f'{cta_text}</a></p>'
        )

        if benefit_bullets:
            body_html += '<p style="margin-bottom: 10px; font-size: 14px; line-height: 150%;">Here\'s what\'s inside:</p>\n<ul>\n'
            for bullet in benefit_bullets:
                body_html += f'<li style="font-size: 14px; line-height: 150%;">{bullet}</li>\n'
            body_html += '</ul>'

        # DnD widget structure matching existing emails
        widgets = {
            # Banner image
            "module-0-0-0": {
                "body": {
                    "alignment": "center",
                    "corner_radius": 5,
                    "corner_radius_unit": "px",
                    "css_class": "dnd-module",
                    "hs_enable_module_padding": True,
                    "hs_wrapper_css": {
                        "padding-bottom": "24px",
                        "padding-left": "20px",
                        "padding-right": "20px",
                        "padding-top": "16px",
                    },
                    "img": {
                        "alt": f"{os.getenv('COMPANY_NAME', '[COMPANY]') } email banner",
                        "height": 186,
                        "src": self.EMAIL_BANNER_URL,
                        "width": 558,
                    },
                    "link": "",
                    "module_id": 1367093,
                    "path": "@hubspot/image_email",
                    "schema_version": 2,
                },
                "child_css": {},
                "css": {},
                "id": "module-0-0-0",
                "label": None,
                "module_id": 1367093,
                "name": "module-0-0-0",
                "order": 1,
                "smart_type": None,
                "styles": {},
                "type": "module",
            },
            # Main content
            "module-1-0-0": {
                "body": {
                    "css_class": "dnd-module",
                    "hs_enable_module_padding": True,
                    "hs_wrapper_css": {
                        "padding-bottom": "20px",
                        "padding-left": "30px",
                        "padding-right": "30px",
                        "padding-top": "10px",
                    },
                    "html": body_html,
                    "module_id": 1155639,
                    "path": "@hubspot/rich_text",
                    "schema_version": 2,
                },
                "child_css": {},
                "css": {},
                "id": "module-1-0-0",
                "label": None,
                "module_id": 1155639,
                "name": "module-1-0-0",
                "order": 2,
                "smart_type": None,
                "styles": {},
                "type": "module",
            },
            # Divider
            "module_divider": {
                "body": {
                    "color": {"color": "#F6F7FF", "opacity": 100},
                    "height": 2,
                    "hs_enable_module_padding": True,
                    "hs_wrapper_css": {
                        "padding-bottom": "10px",
                        "padding-left": "20px",
                        "padding-right": "20px",
                        "padding-top": "10px",
                    },
                    "line_type": "solid",
                    "module_id": 2191110,
                },
                "child_css": {},
                "css": {},
                "id": "module_divider",
                "label": None,
                "module_id": 2191110,
                "name": "module_divider",
                "order": 3,
                "smart_type": None,
                "styles": {},
                "type": "module",
            },
            # CTA section
            "module_cta": {
                "body": {
                    "hs_enable_module_padding": True,
                    "hs_wrapper_css": {
                        "padding-bottom": "20px",
                        "padding-left": "30px",
                        "padding-right": "30px",
                        "padding-top": "10px",
                    },
                    "html": (
                        '<h2 style="font-size: 22px; line-height: 150%;">The fastest way to understand your application</h2>\n'
                        '<p>[COMPANY] is an Application Understanding Platform for legacy and mainframe applications.&nbsp;</p>\n'
                        '<p>&nbsp;</p>\n'
                        '<p style="text-align: center; font-size: 14px; line-height: 125%;">'
                        '<a href="https://[your-domain.com]/" style="background-color: #4154ff; font-size: 16px; '
                        'font-family: Helvetica, Arial, sans-serif; font-weight: bold; text-decoration: none; '
                        'padding: 12px 16px; color: #ffffff; border-radius: 8px; display: inline-block; '
                        'mso-padding-alt: 0;" rel="noopener">Learn more</a></p>'
                    ),
                    "module_id": 1155639,
                    "path": "@hubspot/rich_text",
                    "schema_version": 2,
                },
                "child_css": {},
                "css": {},
                "id": "module_cta",
                "label": None,
                "module_id": 1155639,
                "name": "module_cta",
                "order": 4,
                "smart_type": None,
                "styles": {},
                "type": "module",
            },
            # Footer
            "module-5-0-0": {
                "body": {
                    "align": "center",
                    "css_class": "dnd-module",
                    "font": {
                        "color": "#696b80",
                        "font": "Helvetica,Arial,sans-serif",
                        "font_set": "DEFAULT",
                        "size": {"units": "px", "value": 12},
                    },
                    "hs_enable_module_padding": True,
                    "hs_wrapper_css": {
                        "padding-bottom": "10px",
                        "padding-left": "30px",
                        "padding-right": "30px",
                        "padding-top": "30px",
                    },
                    "link_font": {
                        "color": "#696b80",
                        "font": "Helvetica,Arial,sans-serif",
                        "size": {"units": "px", "value": 12},
                        "styles": {"bold": False, "italic": False, "underline": True},
                    },
                    "module_id": 2869621,
                    "path": "@hubspot/email_footer",
                    "schema_version": 2,
                    "unsubscribe_link_type": "both",
                },
                "child_css": {},
                "css": {},
                "id": "module-5-0-0",
                "label": None,
                "module_id": 2869621,
                "name": "module-5-0-0",
                "order": 5,
                "smart_type": None,
                "styles": {},
                "type": "module",
            },
            # Preview text
            "preview_text": {
                "body": {"value": ""},
            },
        }

        # FlexAreas layout
        flex_areas = {
            "main": {
                "boxFirstElementIndex": 0,
                "boxLastElementIndex": 3,
                "boxed": True,
                "isSingleColumnFullWidth": False,
                "sections": [
                    {
                        "columns": [{"id": "column-0-0", "widgets": ["module-0-0-0"], "width": 12}],
                        "id": "section-0",
                        "style": {
                            "backgroundColor": "#ffffff",
                            "backgroundType": "CONTENT",
                            "paddingBottom": "10px",
                            "paddingTop": "0px",
                        },
                    },
                    {
                        "columns": [{"id": "column-1-0", "widgets": ["module-1-0-0", "module_divider"], "width": 12}],
                        "id": "section-1",
                        "style": {
                            "backgroundType": "CONTENT",
                            "paddingBottom": "0px",
                            "paddingTop": "0px",
                        },
                    },
                    {
                        "columns": [{"id": "column-2-0", "widgets": ["module_cta"], "width": 12}],
                        "id": "section-2",
                        "style": {
                            "backgroundType": "CONTENT",
                            "paddingBottom": "0px",
                            "paddingTop": "0px",
                        },
                    },
                    {
                        "columns": [{"id": "column-5-0", "widgets": ["module-5-0-0"], "width": 12}],
                        "id": "section-5",
                        "style": {
                            "backgroundColor": "",
                            "backgroundType": "CONTENT",
                            "paddingBottom": "20px",
                            "paddingTop": "10px",
                        },
                    },
                ],
            }
        }

        style_settings = {
            "backgroundColor": "#F6F7FF",
            "backgroundImageType": "REPEAT",
            "bodyBorderColor": "#DBDFFF",
            "bodyBorderColorChoice": "BORDER_MANUAL",
            "bodyBorderWidth": 1.0,
            "bodyColor": "#ffffff",
            "buttonStyleSettings": {
                "backgroundColor": "#00a4bd",
                "cornerRadius": 8,
                "fontStyle": {
                    "bold": False,
                    "color": "#ffffff",
                    "font": "Helvetica,Arial,sans-serif",
                    "italic": False,
                    "size": 16,
                    "underline": False,
                },
            },
            "dividerStyleSettings": {
                "color": {"color": "#F6F7FF", "opacity": 100},
                "height": 2,
                "lineType": "solid",
            },
            "headingOneFont": {"size": 20},
            "headingTwoFont": {"size": 24},
            "linksFont": {
                "bold": False,
                "color": "#1D1E2B",
                "italic": False,
                "underline": True,
            },
            "primaryFont": "Helvetica,Arial,sans-serif",
            "primaryFontColor": "#1D1E2B",
            "primaryFontSize": 14.0,
            "secondaryFont": "Arial, sans-serif",
            "secondaryFontColor": "#23496d",
            "secondaryFontSize": 12.0,
        }

        content = {
            "flexAreas": flex_areas,
            "widgets": widgets,
            "styleSettings": style_settings,
            "templatePath": "@hubspot/email/dnd/Start_from_scratch.html",
        }

        return subject, content


# Module-level convenience functions

def create_landing_page_form(
    name: str,
    form_type: str = "download",
    push: bool = False,
) -> Tuple[bool, any]:
    """
    Create a HubSpot form for a landing page.

    Args:
        name: Form name (e.g., "Download - COBOL Whitepaper")
        form_type: 'download' or 'webinar'
        push: If True, create on HubSpot. If False, show preview.

    Returns:
        Tuple of (success, result)
    """
    client = HubSpotClient()
    submit_text = "Download now" if form_type == "download" else "Register now"
    return client.create_form(name, form_type=form_type, submit_button_text=submit_text, push=push)


def setup_landing_page_pipeline(
    page_type: str,
    title: str,
    excerpt: str,
    slug: str,
    meta_description: str,
    page_content: Dict,
    asset_title: Optional[str] = None,
    pdf_path: Optional[str] = None,
    featured_image: Optional[str] = None,
    asset_slug: Optional[str] = None,
    categories: Optional[List[int]] = None,
    salesforce_campaign_id: Optional[str] = None,
    push: bool = False,
) -> Tuple[bool, any]:
    """
    End-to-end landing page pipeline: upload PDF, create form, create email,
    create contact list, create workflow, publish WordPress page.

    Workflow follows the standard pattern (from GD - COBOL Whitepaper July 2025):
    add-to-list → send email → Salesforce campaign → delay 4h

    Args:
        page_type: 'download' or 'webinar'
        title: Page title (used for WordPress page and HubSpot resource names)
        excerpt: Page excerpt/description
        slug: URL slug
        meta_description: SEO meta description
        page_content: Dict with type-specific content:
            - download: benefit_cards (list of {title, text})
            - webinar: speakers, takeaways, youtube_video_id
        asset_title: The asset's actual name as the user knows it (used in email
            subject line, e.g. "[COMPANY] vs [Competitor]"). Must match the PDF
            title / what appears on the cover. Falls back to title if not provided.
        pdf_path: Local path to PDF file (for gated downloads)
        featured_image: Path to featured image (optional; auto-detected from asset_slug if not provided)
        asset_slug: Asset slug for auto-detecting featured image (e.g., "26Q1-competitive-comparison-claude-cobol")
        categories: WordPress category IDs (optional)
        salesforce_campaign_id: Salesforce campaign ID for workflow (e.g. "701Q500000ipIOAIA2")
        push: If True, create everything. If False, show preview of all steps.

    Returns:
        Tuple of (success, summary_dict or error_message)
    """
    from data_sources.modules.wordpress_client import publish_landing_page
    from data_sources.modules.image_builder import render_image
    from pathlib import Path

    client = HubSpotClient()
    results = {}
    steps_log = []
    run_suffix = client._get_3digit_random()  # Generate unique 3-digit suffix for this run

    # asset_title is used for the email subject — must match what the user is downloading.
    # Falls back to title if not provided.
    if not asset_title:
        asset_title = title

    # Default categories: Guide (125) for downloads, Webinar (137) for webinars
    if not categories:
        categories = [125] if page_type == 'download' else [137]

    # Generate featured image if needed
    if asset_slug:
        lp_image_path = Path(f"content/assets/{asset_slug}/images/lp-image-{asset_slug}.webp")
        if not lp_image_path.exists() and pdf_path:
            steps_log.append("Step 0: Generate landing page image")
            image_result = render_image(
                template_id='gated-document',
                inputs={'pdf_path': pdf_path},
                asset_slug=asset_slug
            )
            if image_result['success']:
                steps_log.append(f"  Image generated: {image_result['path']} ({image_result['size']} bytes)")
            else:
                steps_log.append(f"  Warning: Image generation failed: {image_result.get('error', 'unknown error')}")

        if lp_image_path.exists() and not featured_image:
            featured_image = str(lp_image_path)

    # Determine list folder name based on page type
    list_folder = (
        client.LIST_FOLDER_GATED_DOCUMENT if page_type == 'download'
        else client.LIST_FOLDER_WEBINAR
    )

    # Extract benefit bullets for email from page_content
    benefit_bullets = None
    if page_type == 'download' and page_content.get('benefit_cards'):
        benefit_bullets = [card['text'] for card in page_content['benefit_cards'] if card.get('text')]
    elif page_type == 'webinar' and page_content.get('takeaways'):
        benefit_bullets = [t['text'] for t in page_content['takeaways'] if t.get('text')]

    # Step 1: Upload PDF (if provided)
    download_url = ""
    if pdf_path:
        steps_log.append("Step 1: Upload PDF to HubSpot file manager")
        success, result = client.upload_file(pdf_path, push=push)
        if not success:
            return False, f"Step 1 failed (file upload): {result}"
        results['file'] = result
        if push:
            download_url = result.get('url', '') or result.get('default_hosting_url', '')
        else:
            steps_log.append(f"  {result}")
    else:
        steps_log.append("Step 1: Skip (no PDF path provided)")

    # Step 2: Create HubSpot form
    form_name = f"{'Download' if page_type == 'download' else 'Webinar'} - {title} #{run_suffix}"
    steps_log.append(f"Step 2: Create HubSpot form: {form_name}")
    success, result = client.create_form(
        form_name,
        form_type=page_type,
        submit_button_text="Download now" if page_type == "download" else "Register now",
        push=push,
    )
    if not success:
        return False, f"Step 2 failed (form creation): {result}"
    results['form'] = result
    form_id = result.get('id', 'PREVIEW') if push else 'PREVIEW'
    if not push:
        steps_log.append(f"  {result}")

    # Step 3: Create autoresponder email (in correct folder)
    steps_log.append("Step 3: Create autoresponder email")
    replay_url = page_content.get('youtube_video_id', '')
    if replay_url and page_type == 'webinar':
        replay_url = f"{os.getenv('COMPANY_WEBSITE_URL', '[your-domain.com]')}/webinars/{slug}"

    success, result = client.create_autoresponder_email(
        asset_type=page_type,
        asset_title=asset_title,
        download_url=download_url or "(PDF URL from Step 1)",
        replay_url=replay_url,
        benefit_bullets=benefit_bullets,
        name_suffix=run_suffix,
        push=push,
    )
    if not success:
        return False, f"Step 3 failed (email creation): {result}"
    results['email'] = result
    email_id = result.get('id', 'PREVIEW') if push else 'PREVIEW'
    if not push:
        steps_log.append(f"  {result}")

    # Step 4: Create contact list (in correct folder)
    list_name = f"{'Downloads' if page_type == 'download' else 'Webinar'} - {title} #{run_suffix}"
    steps_log.append(f"Step 4: Create contact list: {list_name} (folder: {list_folder})")
    list_id = None

    # Find or create the folder
    success, folder = client.find_or_create_folder(list_folder, push=push)
    if not success:
        steps_log.append(f"  Warning: Could not create folder '{list_folder}': {folder}")
        folder_id = None
    else:
        folder_id = folder.get('id')

    success, result = client.create_contact_list(
        name=list_name,
        folder_id=folder_id,
        push=push,
    )
    if not success:
        steps_log.append(f"  Warning: Could not create list: {result}")
    else:
        results['list'] = result
        list_id = result.get('id') if push else None
        if not push:
            steps_log.append(f"  {result}")

    # Step 5: Create autoresponder workflow
    workflow_name = f"GD - {title} #{run_suffix}"
    steps_log.append("Step 5: Create autoresponder workflow (disabled)")
    sf_note = f" + Salesforce campaign {salesforce_campaign_id}" if salesforce_campaign_id else ""
    steps_log.append(f"  Actions: add-to-list → send email{sf_note} → delay 4h")
    success, result = client.create_autoresponder_workflow(
        form_id=form_id,
        email_id=email_id,
        name=workflow_name,
        list_id=list_id,
        salesforce_campaign_id=salesforce_campaign_id,
        push=push,
    )
    if not success:
        return False, f"Step 5 failed (workflow creation): {result}"
    results['workflow'] = result
    if not push:
        steps_log.append(f"  {result}")

    # Step 6: Build thank-you content with download URL
    if page_type == 'download':
        dl_link = download_url or "(PDF URL from Step 1)"
        page_content.setdefault('thank_you_title', "Thanks for requesting the white paper!")
        page_content.setdefault(
            'thank_you_text',
            f'<p>You can download it here. We will also send a copy to your email address.</p>'
            f'<p><a href="{dl_link}">Download the white paper</a></p>'
        )

    # Step 6: Publish WordPress landing page
    steps_log.append("Step 6: Publish WordPress landing page (draft)")
    success, result = publish_landing_page(
        post_type=page_type,
        title=title,
        excerpt=excerpt,
        slug=slug,
        meta_description=meta_description,
        hubspot_form_id=form_id,
        page_content=page_content,
        featured_image=featured_image,
        categories=categories,
        push=push,
    )
    if not success:
        return False, f"Step 6 failed (WordPress publish): {result}"
    results['wordpress'] = result
    if not push:
        steps_log.append(f"  {result}")

    # Summary
    if not push:
        preview = "=== LANDING PAGE PIPELINE PREVIEW (not pushed) ===\n"
        preview += "\n".join(steps_log)
        preview += "\n\nTo create everything, run with push=True"
        preview += "\n==================================="
        return True, preview

    # Build summary with HubSpot URLs
    summary = {
        'file': results.get('file'),
        'form': results.get('form'),
        'email': results.get('email'),
        'list': results.get('list'),
        'workflow': results.get('workflow'),
        'wordpress': results.get('wordpress'),
    }

    # Print clickable links
    print("\n=== PIPELINE COMPLETE ===")
    if summary.get('file'):
        print(f"  PDF:      {summary['file'].get('hubspot_url', '')}")
        print(f"            {summary['file'].get('url', '')}")
    if summary.get('form'):
        print(f"  Form:     {summary['form'].get('hubspot_url', '')}")
    if summary.get('email'):
        print(f"  Email:    {summary['email'].get('hubspot_url', '')}")
    if summary.get('list'):
        print(f"  List:     {summary['list'].get('hubspot_url', '')}")
    if summary.get('workflow'):
        print(f"  Workflow: {summary['workflow'].get('hubspot_url', '')}")
    print(f"  WordPress: {results.get('wordpress', '')}")
    print("\n  Manual steps:")
    print("  1. Set email type to 'Automated' in HubSpot (API cannot set this)")
    print("  2. Review and enable the workflow")
    print("========================\n")

    return True, summary
