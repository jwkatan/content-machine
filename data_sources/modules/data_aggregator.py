"""
Data Aggregator

Combines data from multiple sources (GA4, GSC, DataForSEO) for comprehensive analysis.
"""

import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from dotenv import load_dotenv


# Focus topics for performance review filtering
# Only content matching these keywords gets full detailed analysis
# Other content appears in a condensed summary for quality control
FOCUS_TOPIC_KEYWORDS = [
    # Core topics
    'mainframe', 'cobol', 'application-understanding',
    'forward-engineer', 'reverse-engineer',
    # Additional topics
    'legacy', 'modernization', 'migration',
    'code-comprehension', 'codebase', 'code-analysis',
]


def _matches_focus_topic(text: str) -> bool:
    """
    Check if URL or keyword matches any focus topic.

    Args:
        text: URL path or keyword to check

    Returns:
        True if text contains any focus topic keyword
    """
    if not text:
        return False
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in FOCUS_TOPIC_KEYWORDS)

try:
    from .google_analytics import GoogleAnalytics
    from .google_search_console import GoogleSearchConsole
    from .dataforseo import DataForSEO
except ImportError:
    # Fallback for direct execution
    from google_analytics import GoogleAnalytics
    from google_search_console import GoogleSearchConsole
    from dataforseo import DataForSEO


class DataAggregator:
    """
    Aggregates data from multiple sources for comprehensive content analysis
    """

    def __init__(self):
        """Initialize all data source clients"""
        load_dotenv('data_sources/config/.env')

        try:
            self.ga = GoogleAnalytics()
        except Exception as e:
            print(f"Warning: Google Analytics not configured: {e}")
            self.ga = None

        try:
            self.gsc = GoogleSearchConsole()
        except Exception as e:
            print(f"Warning: Google Search Console not configured: {e}")
            self.gsc = None

        try:
            self.dfs = DataForSEO()
        except Exception as e:
            print(f"Warning: DataForSEO not configured: {e}")
            self.dfs = None

    def get_comprehensive_page_performance(
        self,
        url: str,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Get all available data for a specific page

        Args:
            url: Page path or full URL
            days: Days to analyze

        Returns:
            Dict with data from all sources
        """
        result = {
            'url': url,
            'analyzed_at': datetime.now().isoformat(),
            'period_days': days,
            'ga4': None,
            'gsc': None,
            'dataforseo': None
        }

        # Google Analytics data
        if self.ga:
            try:
                trends = self.ga.get_page_trends(url, days=days)
                result['ga4'] = {
                    'total_pageviews': trends['total_pageviews'],
                    'trend_direction': trends['trend_direction'],
                    'trend_percent': trends['trend_percent'],
                    'timeline': trends['timeline']
                }
            except Exception as e:
                result['ga4'] = {'error': str(e)}

        # Google Search Console data
        if self.gsc:
            try:
                page_perf = self.gsc.get_page_performance(url, days=days)
                result['gsc'] = page_perf
            except Exception as e:
                result['gsc'] = {'error': str(e)}

        # DataForSEO - Get rankings for top keywords from GSC
        if self.dfs and result.get('gsc') and result['gsc'].get('top_keywords'):
            try:
                top_keywords = [kw['keyword'] for kw in result['gsc']['top_keywords'][:5]]
                domain = os.getenv('GSC_SITE_URL', '').replace('https://', '').replace('http://', '')

                rankings = self.dfs.get_rankings(domain=domain, keywords=top_keywords)
                result['dataforseo'] = {
                    'rankings': rankings
                }
            except Exception as e:
                result['dataforseo'] = {'error': str(e)}

        return result

    def identify_content_opportunities(
        self,
        days: int = 30,
        min_monthly_pageviews: int = 100
    ) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
        """
        Identify content opportunities across all data sources.

        Results are categorized into 'focus' and 'other' based on topic keywords.
        Focus topics (mainframe, COBOL, legacy, etc.) get full analysis.
        Other topics appear in condensed format for quality control.

        Returns:
            Dict with categorized opportunities, each containing 'focus' and 'other' lists
        """
        def categorize(items: List[Dict], key_field: str) -> Dict[str, List[Dict]]:
            """Split items into focus and other categories."""
            focus = [i for i in items if _matches_focus_topic(i.get(key_field, ''))]
            other = [i for i in items if not _matches_focus_topic(i.get(key_field, ''))]
            return {'focus': focus, 'other': other}

        opportunities = {
            'quick_wins': {'focus': [], 'other': []},
            'declining_content': {'focus': [], 'other': []},
            'low_ctr': {'focus': [], 'other': []},
            'trending_topics': {'focus': [], 'other': []},
            'competitor_gaps': {'focus': [], 'other': []}
        }

        # Quick wins from GSC
        if self.gsc:
            try:
                quick_wins = self.gsc.get_quick_wins(days=days)
                opportunities['quick_wins'] = categorize(quick_wins[:20], 'keyword')
            except Exception as e:
                print(f"Error getting quick wins: {e}")

        # Declining content from GA4
        if self.ga:
            try:
                declining = self.ga.get_declining_pages(
                    comparison_days=days,
                    threshold_percent=-20.0
                )
                opportunities['declining_content'] = categorize(declining[:15], 'path')
            except Exception as e:
                print(f"Error getting declining pages: {e}")

        # Low CTR pages from GSC
        if self.gsc:
            try:
                low_ctr = self.gsc.get_low_ctr_pages(days=days)
                opportunities['low_ctr'] = categorize(low_ctr[:15], 'url')
            except Exception as e:
                print(f"Error getting low CTR pages: {e}")

        # Trending topics from GSC
        if self.gsc:
            try:
                trending = self.gsc.get_trending_queries()
                opportunities['trending_topics'] = categorize(trending[:15], 'query')
            except Exception as e:
                print(f"Error getting trending queries: {e}")

        return opportunities

    def generate_performance_report(
        self,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Generate comprehensive performance report

        Args:
            days: Days to analyze

        Returns:
            Complete performance report
        """
        report = {
            'generated_at': datetime.now().isoformat(),
            'period_days': days,
            'summary': {},
            'top_performers': [],
            'opportunities': {},
            'recommendations': []
        }

        # Summary metrics
        if self.ga:
            try:
                top_pages = self.ga.get_top_pages(days=days, limit=100)
                report['summary']['total_pageviews'] = sum(p['pageviews'] for p in top_pages)
                report['summary']['total_sessions'] = sum(p['sessions'] for p in top_pages)
                report['summary']['avg_engagement_rate'] = sum(p['engagement_rate'] for p in top_pages) / len(top_pages)
                report['top_performers'] = top_pages[:10]
            except Exception as e:
                print(f"Error getting GA4 summary: {e}")

        if self.gsc:
            try:
                keywords = self.gsc.get_keyword_positions(days=days)
                report['summary']['total_keywords'] = len(keywords)
                report['summary']['total_clicks'] = sum(kw['clicks'] for kw in keywords)
                report['summary']['total_impressions'] = sum(kw['impressions'] for kw in keywords)
                report['summary']['avg_ctr'] = sum(kw['ctr'] for kw in keywords) / len(keywords) if keywords else 0
            except Exception as e:
                print(f"Error getting GSC summary: {e}")

        # Opportunities
        report['opportunities'] = self.identify_content_opportunities(days=days)

        # Generate recommendations
        report['recommendations'] = self._generate_recommendations(report['opportunities'])

        return report

    def _generate_recommendations(
        self,
        opportunities: Dict[str, Dict[str, List[Dict[str, Any]]]]
    ) -> List[Dict[str, str]]:
        """
        Generate actionable recommendations from opportunities.

        Prioritizes focus topics over other topics.

        Args:
            opportunities: Categorized opportunities from identify_content_opportunities

        Returns:
            List of recommendations
        """
        recommendations = []

        # Helper to get first item from focus, falling back to other
        def get_top_item(category: Dict[str, List]) -> Optional[Dict]:
            if category.get('focus'):
                return category['focus'][0]
            elif category.get('other'):
                return category['other'][0]
            return None

        # Quick wins (prioritize focus topics)
        quick_wins = opportunities.get('quick_wins', {})
        top_quick_win = get_top_item(quick_wins)
        if top_quick_win:
            is_focus = bool(quick_wins.get('focus'))
            recommendations.append({
                'priority': 'high' if is_focus else 'low',
                'type': 'optimize',
                'is_focus_topic': is_focus,
                'action': f"Optimize for '{top_quick_win['keyword']}'",
                'reason': f"Currently ranking #{top_quick_win['position']:.0f} with {top_quick_win['impressions']:,} impressions. Small improvements could push to page 1.",
                'keyword': top_quick_win['keyword'],
                'current_position': top_quick_win['position']
            })

        # Declining content
        declining = opportunities.get('declining_content', {})
        worst_decline = get_top_item(declining)
        if worst_decline:
            is_focus = bool(declining.get('focus'))
            recommendations.append({
                'priority': 'high' if is_focus else 'low',
                'type': 'update',
                'is_focus_topic': is_focus,
                'action': f"Update declining article: {worst_decline['title']}",
                'reason': f"Traffic down {abs(worst_decline['change_percent']):.1f}% ({worst_decline['previous_pageviews']:,} → {worst_decline['pageviews']:,} pageviews). Needs refresh.",
                'url': worst_decline['path'],
                'change_percent': worst_decline['change_percent']
            })

        # Low CTR
        low_ctr = opportunities.get('low_ctr', {})
        worst_ctr = get_top_item(low_ctr)
        if worst_ctr:
            is_focus = bool(low_ctr.get('focus'))
            recommendations.append({
                'priority': 'medium' if is_focus else 'low',
                'type': 'optimize_meta',
                'is_focus_topic': is_focus,
                'action': f"Improve meta elements for: {worst_ctr['url']}",
                'reason': f"Getting {worst_ctr['impressions']:,} impressions but only {worst_ctr['ctr']}% CTR. Better title/description could add {worst_ctr['missed_clicks']:,} clicks/month.",
                'url': worst_ctr['url'],
                'potential_clicks': worst_ctr['missed_clicks']
            })

        # Trending topics
        trending = opportunities.get('trending_topics', {})
        top_trend = get_top_item(trending)
        if top_trend:
            is_focus = bool(trending.get('focus'))
            recommendations.append({
                'priority': 'medium' if is_focus else 'low',
                'type': 'create_new',
                'is_focus_topic': is_focus,
                'action': f"Create content for trending topic: '{top_trend['query']}'",
                'reason': f"Search interest up {top_trend['change_percent']:.1f}% with {top_trend['recent_impressions']:,} recent impressions. Strike while hot!",
                'query': top_trend['query'],
                'growth': top_trend['change_percent']
            })

        return recommendations

    def get_priority_queue(
        self,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get prioritized list of content tasks

        Args:
            limit: Number of tasks to return

        Returns:
            Prioritized task list for Performance Agent
        """
        opportunities = self.identify_content_opportunities()
        recommendations = self._generate_recommendations(opportunities)

        # Sort by priority
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        recommendations.sort(key=lambda x: priority_order.get(x['priority'], 3))

        return recommendations[:limit]


# Example usage
if __name__ == "__main__":
    aggregator = DataAggregator()

    print("=" * 80)
    print("CONTENT PERFORMANCE REPORT")
    print("=" * 80)

    # Generate full report
    report = aggregator.generate_performance_report(days=30)

    print(f"\nReport Period: Last {report['period_days']} days")
    print(f"Generated: {report['generated_at']}")

    # Summary
    if report['summary']:
        print("\n📊 SUMMARY")
        print("-" * 80)
        if 'total_pageviews' in report['summary']:
            print(f"Total Pageviews: {report['summary']['total_pageviews']:,}")
            print(f"Total Sessions: {report['summary']['total_sessions']:,}")
            print(f"Avg Engagement Rate: {report['summary']['avg_engagement_rate']:.1%}")
        if 'total_clicks' in report['summary']:
            print(f"Total Clicks (GSC): {report['summary']['total_clicks']:,}")
            print(f"Total Impressions: {report['summary']['total_impressions']:,}")
            print(f"Avg CTR: {report['summary']['avg_ctr']:.2%}")

    # Top performers
    if report.get('top_performers'):
        print("\n🏆 TOP 10 PERFORMERS")
        print("-" * 80)
        for i, page in enumerate(report['top_performers'][:10], 1):
            print(f"{i}. {page['title']}")
            print(f"   {page['pageviews']:,} views | {page['engagement_rate']:.1%} engagement")

    # Recommendations
    if report.get('recommendations'):
        print("\n✅ TOP RECOMMENDATIONS")
        print("-" * 80)
        for i, rec in enumerate(report['recommendations'][:5], 1):
            print(f"\n{i}. [{rec['priority'].upper()}] {rec['action']}")
            print(f"   {rec['reason']}")

    print("\n" + "=" * 80)
