"""
Slack Notifier

Sends LinkedIn post notifications to Slack via incoming webhooks.
Simple, webhook-based integration - no OAuth required.

Setup:
1. Go to https://api.slack.com/apps
2. Create new app or use existing
3. Add "Incoming Webhooks" feature
4. Create webhook for your channel
5. Add SLACK_WEBHOOK_URL to data_sources/config/.env
"""

import os
import json
import base64
from typing import Optional, Dict, Any
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from pathlib import Path

# Load environment from config/.env
_env_path = Path(__file__).parent.parent / "config" / ".env"
if _env_path.exists():
    with open(_env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                if key not in os.environ:  # Don't override existing env vars
                    os.environ[key] = value


class SlackNotifier:
    """
    Sends formatted LinkedIn post notifications to Slack.
    """

    def __init__(self, webhook_url: Optional[str] = None):
        """
        Initialize with webhook URL from parameter or environment.

        Args:
            webhook_url: Slack incoming webhook URL (optional, falls back to env)
        """
        self.webhook_url = webhook_url or os.getenv('SLACK_WEBHOOK_URL')

        if not self.webhook_url:
            raise ValueError(
                "Slack webhook URL not configured. "
                "Set SLACK_WEBHOOK_URL in .env or pass webhook_url parameter."
            )

    def send_post_ready(
        self,
        post_content: str,
        post_type: str = "company",
        title: str = "",
        image_path: Optional[str] = None,
        image_url: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Send notification for a LinkedIn post ready for CEO review.

        Args:
            post_content: The full LinkedIn post text
            post_type: "company" or "ceo"
            title: Brief title/topic for the post
            image_path: Path to generated image (for reference only)
            image_url: Public URL to display image in Slack (must be https)
            metadata: Additional info (source, created date, etc.)

        Returns:
            True if sent successfully, False otherwise
        """
        # Build the message blocks
        blocks = self._build_post_ready_blocks(
            post_content=post_content,
            post_type=post_type,
            title=title,
            image_path=image_path,
            image_url=image_url,
            metadata=metadata
        )

        return self._send_message(blocks)

    def send_ideas_summary(
        self,
        ideas: list,
        total_found: int = 0
    ) -> bool:
        """
        Send summary of newly generated LinkedIn ideas.

        Args:
            ideas: List of dicts with 'filename', 'title', 'source', 'type'
            total_found: Total articles found before filtering

        Returns:
            True if sent successfully, False otherwise
        """
        blocks = self._build_ideas_summary_blocks(ideas, total_found)
        return self._send_message(blocks)

    def _build_post_ready_blocks(
        self,
        post_content: str,
        post_type: str,
        title: str,
        image_path: Optional[str],
        image_url: Optional[str],
        metadata: Optional[Dict[str, Any]]
    ) -> list:
        """Build Slack blocks for post-ready notification."""

        type_emoji = ":office:" if post_type == "company" else ":bust_in_silhouette:"
        type_label = "Company Post" if post_type == "company" else "CEO Post"

        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f":linkedin: New LinkedIn Post Ready",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Type:* {type_emoji} {type_label}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Topic:* {title or 'Untitled'}"
                    }
                ]
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Post Content:*"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": post_content[:2900]  # Slack limit is 3000
                }
            },
            {
                "type": "divider"
            }
        ]

        # Add image if URL provided (displays in Slack)
        if image_url:
            blocks.append({
                "type": "image",
                "image_url": image_url,
                "alt_text": title or "LinkedIn post image"
            })

        # Add image path indicator (for local file reference)
        if image_path:
            blocks.append({
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f":camera: Image file: `{Path(image_path).name}`"
                    }
                ]
            })

        # Add metadata if present
        if metadata:
            meta_text = " | ".join([f"*{k}:* {v}" for k, v in metadata.items()])
            blocks.append({
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": meta_text
                    }
                ]
            })

        # Add posting tips
        blocks.append({
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": ":clock3: Best posting times: Tue-Thu, 8-10am or 12pm"
                }
            ]
        })

        return blocks

    def _build_ideas_summary_blocks(self, ideas: list, total_found: int) -> list:
        """Build Slack blocks for ideas summary notification."""

        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f":bulb: {len(ideas)} New LinkedIn Ideas Generated",
                    "emoji": True
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"Found {total_found} articles, selected {len(ideas)} most relevant"
                    }
                ]
            },
            {
                "type": "divider"
            }
        ]

        # Add each idea
        for i, idea in enumerate(ideas, 1):
            type_emoji = ":office:" if idea.get('type') == 'company' else ":bust_in_silhouette:"
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{i}. {idea.get('title', 'Untitled')}*\n{type_emoji} _{idea.get('type', 'undecided')}_ | Source: {idea.get('source', 'unknown')}"
                }
            })

        blocks.append({
            "type": "divider"
        })

        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Next steps:*\n- Review ideas: `/linkedin`\n- Create post: `/linkedin post [filename]`"
            }
        })

        return blocks

    def _send_message(self, blocks: list) -> bool:
        """
        Send message blocks to Slack webhook.

        Args:
            blocks: List of Slack block kit blocks

        Returns:
            True if successful, False otherwise
        """
        payload = {
            "blocks": blocks
        }

        try:
            data = json.dumps(payload).encode('utf-8')
            request = Request(
                self.webhook_url,
                data=data,
                headers={'Content-Type': 'application/json'}
            )

            with urlopen(request, timeout=10) as response:
                return response.status == 200

        except HTTPError as e:
            print(f"Slack API error: {e.code} - {e.reason}")
            return False
        except URLError as e:
            print(f"Network error sending to Slack: {e.reason}")
            return False
        except Exception as e:
            print(f"Error sending to Slack: {e}")
            return False


def send_linkedin_post(
    post_content: str,
    post_type: str = "company",
    title: str = "",
    image_path: Optional[str] = None,
    image_url: Optional[str] = None,
    webhook_url: Optional[str] = None
) -> bool:
    """
    Convenience function to send a LinkedIn post notification.

    Args:
        post_content: The LinkedIn post text
        post_type: "company" or "ceo"
        title: Post topic/title
        image_path: Path to generated image (local reference)
        image_url: Public URL to display image in Slack
        webhook_url: Slack webhook URL (optional, uses env if not provided)

    Returns:
        True if sent successfully
    """
    try:
        notifier = SlackNotifier(webhook_url)
        return notifier.send_post_ready(
            post_content=post_content,
            post_type=post_type,
            title=title,
            image_path=image_path,
            image_url=image_url
        )
    except ValueError as e:
        print(f"Configuration error: {e}")
        return False


def send_ideas_notification(
    ideas: list,
    total_found: int = 0,
    webhook_url: Optional[str] = None
) -> bool:
    """
    Convenience function to send ideas summary notification.

    Args:
        ideas: List of idea dicts
        total_found: Total articles found
        webhook_url: Slack webhook URL (optional)

    Returns:
        True if sent successfully
    """
    try:
        notifier = SlackNotifier(webhook_url)
        return notifier.send_ideas_summary(ideas, total_found)
    except ValueError as e:
        print(f"Configuration error: {e}")
        return False


if __name__ == '__main__':
    # Test the notifier (requires SLACK_WEBHOOK_URL in environment)
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        test_post = """After 15 years building developer tools, I've learned something counterintuitive:

The hardest problems aren't technical - they're about helping people understand systems they didn't build.

We obsess over code quality, architecture, and performance.

But the real bottleneck? Knowledge transfer.

When engineers leave, their understanding goes with them. When new folks join, they spend months deciphering what exists.

The code is there. The understanding isn't.

What's the biggest knowledge gap you've seen on a team?"""

        print("Sending test post to Slack...")
        success = send_linkedin_post(
            post_content=test_post,
            post_type="ceo",
            title="Knowledge Transfer in Engineering"
        )
        print(f"Result: {'Success' if success else 'Failed'}")
    else:
        print("Usage: python slack_notifier.py --test")
        print("Requires SLACK_WEBHOOK_URL environment variable")
