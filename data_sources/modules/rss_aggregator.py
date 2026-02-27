"""
RSS Aggregator

Fetches trending topics from RSS feeds and creates LinkedIn idea files.
Used by the /linkedin ideas command.

Setup:
    pip install feedparser python-dateutil

Feeds are hardcoded for simplicity. Extend by editing FEEDS list.
"""

import os
import re
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass, asdict
from urllib.parse import urlparse

try:
    import feedparser
    FEEDPARSER_AVAILABLE = True
except ImportError:
    FEEDPARSER_AVAILABLE = False
    print("Warning: feedparser not installed. Run: pip install feedparser")

try:
    from dateutil import parser as date_parser
    DATEUTIL_AVAILABLE = True
except ImportError:
    DATEUTIL_AVAILABLE = False
    print("Warning: python-dateutil not installed. Run: pip install python-dateutil")


@dataclass
class FeedItem:
    """Represents a single item from an RSS feed."""
    title: str
    link: str
    summary: str
    published: datetime
    source: str
    relevance_score: float = 0.0
    suggested_type: str = "undecided"  # company, ceo, or undecided


class RSSAggregator:
    """
    Fetches and filters RSS feeds for LinkedIn content ideas.
    """

    # Hardcoded feed configuration - focused on enterprise IT, BFSI, and mainframe
    FEEDS = [
        # Mainframe / Legacy specific
        {
            "name": "Planet Mainframe",
            "url": "https://planetmainframe.com/feed/",
            "topics": ["mainframe", "cobol", "z/os", "skills gap"]
        },
        {
            "name": "TechChannel",
            "url": "https://techchannel.com/feed/",
            "topics": ["ibm z", "mainframe", "modernization", "ai"]
        },
        {
            "name": "IT Jungle",
            "url": "https://www.itjungle.com/feed/",
            "topics": ["ibm i", "as400", "enterprise", "modernization"]
        },
        # BFSI / Fintech
        {
            "name": "Finextra",
            "url": "https://www.finextra.com/rss/headlines.aspx",
            "topics": ["banking", "fintech", "payments", "enterprise"]
        },
        # Enterprise IT leadership
        {
            "name": "CIO.com",
            "url": "https://www.cio.com/feed/",
            "topics": ["cio", "enterprise", "digital transformation"]
        },
        {
            "name": "ComputerWeekly",
            "url": "https://www.computerweekly.com/rss/All-Computer-Weekly-content.xml",
            "topics": ["enterprise IT", "banking", "infrastructure"]
        },
        {
            "name": "The Register",
            "url": "https://www.theregister.com/headlines.atom",
            "topics": ["enterprise", "infrastructure", "security"]
        },
        # Developer / Platform
        {
            "name": "The New Stack",
            "url": "https://thenewstack.io/feed/",
            "topics": ["cloud native", "devops", "platform engineering"]
        },
        {
            "name": "InfoQ",
            "url": "https://www.infoq.com/feed/",
            "topics": ["architecture", "devops", "enterprise"]
        },
        {
            "name": "Pragmatic Engineer",
            "url": "https://blog.pragmaticengineer.com/rss/",
            "topics": ["engineering management", "tech leadership", "software engineering"]
        }
    ]

    # Keywords for relevance filtering - enterprise IT, BFSI, and mainframe focus
    RELEVANCE_KEYWORDS = [
        # Legacy modernization (core to Swimm)
        "legacy", "modernization", "cobol", "mainframe", "migration",
        "legacy code", "legacy system", "technical debt",
        "ibm z", "z/os", "ibm i", "as400", "iseries",
        "jcl", "cics", "db2", "replatform",
        # BFSI specific
        "banking", "financial services", "fintech", "insurance",
        "core banking", "payments", "regulatory", "compliance",
        # AI and coding
        "ai coding", "code assistant", "llm", "copilot", "ai agent",
        "generative ai", "genai", "ai developer",
        # Developer productivity
        "developer productivity", "developer experience",
        "onboarding", "documentation", "knowledge management",
        "skills gap", "talent shortage",
        # Enterprise architecture
        "enterprise architecture", "digital transformation",
        "cloud migration", "hybrid cloud", "platform engineering",
        # Tech leadership
        "cto", "cio", "engineering leader", "tech leadership",
        "engineering management", "software engineering"
    ]

    # Keywords that suggest CEO vs company post
    CEO_KEYWORDS = [
        "leadership", "founder", "ceo", "startup", "lessons",
        "learned", "mistake", "failure", "journey", "story",
        "opinion", "controversial", "unpopular", "hot take"
    ]

    # Keywords to EXCLUDE (vendor content, webinars, non-relevant)
    EXCLUDE_KEYWORDS = [
        # Vendor products
        "sap", "salesforce", "oracle", "microsoft dynamics",
        # Promotional content
        "sponsor", "sponsored", "advertisement", "webinar",
        "register now", "sign up", "join us", "free trial",
        # Vendor announcements (usually promotional)
        "announces", "introduces", "launches", "unveils",
        "partnership with", "teams up with"
    ]

    # Non-ASCII threshold for detecting non-English content
    NON_ASCII_THRESHOLD = 0.15  # If >15% non-ASCII chars, skip

    def __init__(self, output_dir: Optional[str] = None):
        """
        Initialize the aggregator.

        Args:
            output_dir: Directory to save idea files (default: topics/linkedin/ideas/)
        """
        if not FEEDPARSER_AVAILABLE:
            raise ImportError("feedparser is required. Install with: pip install feedparser")

        self.output_dir = Path(output_dir) if output_dir else Path("content/topics/linkedin/ideas")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def fetch_all_feeds(self, since_hours: int = 48) -> List[FeedItem]:
        """
        Fetch items from all configured feeds.

        Args:
            since_hours: Only include items from the last N hours

        Returns:
            List of FeedItem objects
        """
        all_items = []
        cutoff = datetime.now() - timedelta(hours=since_hours)

        for feed_config in self.FEEDS:
            try:
                items = self._fetch_feed(feed_config, cutoff)
                all_items.extend(items)
            except Exception as e:
                print(f"Error fetching {feed_config['name']}: {e}")

        return all_items

    def _fetch_feed(self, feed_config: Dict, cutoff: datetime) -> List[FeedItem]:
        """Fetch items from a single feed."""
        feed = feedparser.parse(feed_config["url"])
        items = []

        for entry in feed.entries[:20]:  # Limit to recent 20 entries
            # Parse published date
            published = self._parse_date(entry)
            if published and published < cutoff:
                continue

            item = FeedItem(
                title=entry.get("title", "").strip(),
                link=entry.get("link", ""),
                summary=self._clean_summary(entry.get("summary", entry.get("description", ""))),
                published=published or datetime.now(),
                source=feed_config["name"]
            )

            if item.title and item.link:
                items.append(item)

        return items

    def _parse_date(self, entry) -> Optional[datetime]:
        """Parse date from feed entry."""
        if not DATEUTIL_AVAILABLE:
            return datetime.now()

        for date_field in ["published", "updated", "created"]:
            if date_field in entry:
                try:
                    return date_parser.parse(entry[date_field])
                except:
                    continue

        if hasattr(entry, "published_parsed") and entry.published_parsed:
            try:
                from time import mktime
                return datetime.fromtimestamp(mktime(entry.published_parsed))
            except:
                pass

        return None

    def _clean_summary(self, summary: str) -> str:
        """Clean HTML and truncate summary."""
        # Remove HTML tags
        clean = re.sub(r'<[^>]+>', '', summary)
        # Decode HTML entities
        clean = clean.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        clean = clean.replace('&quot;', '"').replace('&#39;', "'")
        # Normalize whitespace
        clean = re.sub(r'\s+', ' ', clean).strip()
        # Truncate
        return clean[:500] + "..." if len(clean) > 500 else clean

    def filter_relevant(self, items: List[FeedItem]) -> List[FeedItem]:
        """
        Filter and score items by relevance to Swimm's topics.

        Args:
            items: List of FeedItem objects

        Returns:
            Filtered and scored items, sorted by relevance
        """
        scored_items = []

        for item in items:
            # Skip non-English content
            if not self._is_english(item.title):
                continue

            # Skip excluded content (vendor articles, etc.)
            if self._should_exclude(item):
                continue

            score = self._calculate_relevance(item)
            if score > 0:
                item.relevance_score = score
                item.suggested_type = self._suggest_type(item)
                scored_items.append(item)

        # Sort by relevance score, highest first
        scored_items.sort(key=lambda x: x.relevance_score, reverse=True)

        return scored_items

    def _is_english(self, text: str) -> bool:
        """Check if text is likely English (low non-ASCII ratio)."""
        if not text:
            return False
        non_ascii = sum(1 for c in text if ord(c) > 127)
        ratio = non_ascii / len(text)
        return ratio < self.NON_ASCII_THRESHOLD

    def _should_exclude(self, item: FeedItem) -> bool:
        """Check if item matches exclusion keywords."""
        text = f"{item.title} {item.summary}".lower()
        return any(kw in text for kw in self.EXCLUDE_KEYWORDS)

    def _calculate_relevance(self, item: FeedItem) -> float:
        """Calculate relevance score based on keyword matches."""
        text = f"{item.title} {item.summary}".lower()
        score = 0.0

        for keyword in self.RELEVANCE_KEYWORDS:
            if keyword.lower() in text:
                # Weight title matches higher
                if keyword.lower() in item.title.lower():
                    score += 2.0
                else:
                    score += 1.0

        # Normalize to 0-1 range (cap at 10 points)
        return min(score / 10.0, 1.0)

    def _suggest_type(self, item: FeedItem) -> str:
        """Suggest whether item is better for company or CEO post."""
        text = f"{item.title} {item.summary}".lower()

        ceo_matches = sum(1 for kw in self.CEO_KEYWORDS if kw in text)

        if ceo_matches >= 2:
            return "ceo"
        elif ceo_matches == 1:
            return "undecided"
        else:
            return "company"

    def select_top_ideas(
        self,
        items: List[FeedItem],
        max_ideas: int = 5,
        min_relevance: float = 0.1
    ) -> List[FeedItem]:
        """
        Select the top N most interesting ideas.

        Args:
            items: Pre-filtered and scored items
            max_ideas: Maximum number to select
            min_relevance: Minimum relevance score threshold

        Returns:
            Top N items for idea creation
        """
        # Filter by minimum relevance
        qualified = [i for i in items if i.relevance_score >= min_relevance]

        # Take top N
        return qualified[:max_ideas]

    def create_idea_files(self, items: List[FeedItem]) -> List[str]:
        """
        Create idea markdown files for selected items.

        Args:
            items: List of FeedItem objects to create files for

        Returns:
            List of created file paths
        """
        created_files = []
        today = datetime.now().strftime("%Y-%m-%d")

        for item in items:
            slug = self._create_slug(item.title)
            filename = f"{slug}-{today}.md"
            filepath = self.output_dir / filename

            # Skip if file already exists
            if filepath.exists():
                continue

            content = self._format_idea_file(item, today)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            created_files.append(str(filepath))

        return created_files

    def _create_slug(self, title: str) -> str:
        """Create URL-friendly slug from title."""
        # Lowercase and replace spaces with hyphens
        slug = title.lower()
        # Remove special characters
        slug = re.sub(r'[^\w\s-]', '', slug)
        # Replace spaces with hyphens
        slug = re.sub(r'[\s_]+', '-', slug)
        # Truncate to reasonable length
        slug = slug[:50].rstrip('-')
        return slug

    def _format_idea_file(self, item: FeedItem, date: str) -> str:
        """Format idea file content."""
        return f"""---
type: {item.suggested_type}
source: trending
created: {date}
origin: "{item.link}"
relevance: {item.relevance_score:.2f}
---

# {item.title}

## Core Insight
{item.summary}

## Why It Matters
[Why does this matter to developers, engineering leaders, or modernization teams?]

## Angle (optional)
Suggested approach based on source:
- **Company angle**: Position Swimm's expertise on this topic
- **CEO angle**: Personal take, contrarian view, or lessons learned

## Source
- **Feed**: {item.source}
- **Published**: {item.published.strftime("%Y-%m-%d %H:%M") if item.published else "Unknown"}
- **Link**: {item.link}
"""

    def get_trending_ideas(
        self,
        max_ideas: int = 5,
        since_hours: int = 48
    ) -> Tuple[List[str], Dict]:
        """
        Full pipeline: fetch, filter, select, and create idea files.

        Args:
            max_ideas: Maximum number of ideas to create
            since_hours: Only consider items from last N hours

        Returns:
            Tuple of (list of created file paths, statistics dict)
        """
        # Fetch all feeds
        all_items = self.fetch_all_feeds(since_hours)

        # Filter for relevance
        relevant_items = self.filter_relevant(all_items)

        # Select top ideas
        selected = self.select_top_ideas(relevant_items, max_ideas)

        # Create files
        created_files = self.create_idea_files(selected)

        stats = {
            "total_fetched": len(all_items),
            "relevant_found": len(relevant_items),
            "ideas_created": len(created_files),
            "feeds_checked": len(self.FEEDS)
        }

        return created_files, stats

    def get_candidates(
        self,
        max_candidates: int = 5,
        since_hours: int = 48
    ) -> Tuple[List[FeedItem], Dict]:
        """
        Get candidate ideas for approval WITHOUT creating files.

        Args:
            max_candidates: Maximum candidates to return
            since_hours: Only consider items from last N hours

        Returns:
            Tuple of (list of FeedItem candidates, statistics dict)
        """
        # Fetch all feeds
        all_items = self.fetch_all_feeds(since_hours)

        # Filter for relevance (includes English + exclusion checks)
        relevant_items = self.filter_relevant(all_items)

        # Select top candidates
        candidates = self.select_top_ideas(relevant_items, max_candidates)

        stats = {
            "total_fetched": len(all_items),
            "relevant_found": len(relevant_items),
            "candidates_selected": len(candidates),
            "feeds_checked": len(self.FEEDS)
        }

        return candidates, stats

    def format_candidates_table(self, candidates: List[FeedItem]) -> str:
        """Format candidates as a table for user review."""
        lines = ["| # | Title | Angle | URL |", "|---|-------|-------|-----|"]
        for i, item in enumerate(candidates, 1):
            # Truncate title if needed
            title = item.title[:50] + "..." if len(item.title) > 50 else item.title
            # Suggest angle based on type
            if item.suggested_type == "ceo":
                angle = "CEO: Personal take / contrarian view"
            else:
                angle = "Company: Domain expertise / thought leadership"
            lines.append(f"| {i} | {title} | {angle} | {item.link} |")
        return "\n".join(lines)


def generate_linkedin_ideas(
    max_ideas: int = 5,
    output_dir: Optional[str] = None,
    verbose: bool = True
) -> List[Dict]:
    """
    Convenience function to generate LinkedIn ideas from RSS feeds.

    Args:
        max_ideas: Maximum ideas to generate
        output_dir: Where to save idea files
        verbose: Print progress information

    Returns:
        List of dicts with idea info (filename, title, type, source)
    """
    aggregator = RSSAggregator(output_dir)

    if verbose:
        print(f"Fetching from {len(aggregator.FEEDS)} RSS feeds...")

    created_files, stats = aggregator.get_trending_ideas(max_ideas)

    if verbose:
        print(f"Found {stats['total_fetched']} articles")
        print(f"Filtered to {stats['relevant_found']} relevant")
        print(f"Created {stats['ideas_created']} idea files")

    # Return structured info about created ideas
    ideas = []
    for filepath in created_files:
        # Read back the file to get structured info
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract title from first heading
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else Path(filepath).stem

        # Extract type from frontmatter
        type_match = re.search(r'^type: (\w+)', content, re.MULTILINE)
        idea_type = type_match.group(1) if type_match else "undecided"

        # Extract source
        source_match = re.search(r'\*\*Feed\*\*: (.+)$', content, re.MULTILINE)
        source = source_match.group(1) if source_match else "unknown"

        ideas.append({
            "filename": Path(filepath).name,
            "filepath": filepath,
            "title": title,
            "type": idea_type,
            "source": source
        })

    return ideas


if __name__ == '__main__':
    import sys

    if not FEEDPARSER_AVAILABLE:
        print("Error: feedparser not installed. Run: pip install feedparser")
        sys.exit(1)

    # Test the aggregator
    print("Testing RSS Aggregator...")
    print("=" * 60)

    ideas = generate_linkedin_ideas(max_ideas=5, verbose=True)

    print("\n" + "=" * 60)
    print("Generated Ideas:")
    for i, idea in enumerate(ideas, 1):
        print(f"{i}. [{idea['type']}] {idea['title']}")
        print(f"   Source: {idea['source']}")
        print(f"   File: {idea['filename']}")
        print()
