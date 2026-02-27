"""
Export detailed opportunities data for performance review
"""

import json
import os
from modules.data_aggregator import DataAggregator

if __name__ == "__main__":
    aggregator = DataAggregator()

    print("Collecting detailed opportunities data...")

    # Get full report
    report = aggregator.generate_performance_report(days=30)

    # Get opportunities
    opportunities = report['opportunities']

    print("\n" + "="*80)
    print("QUICK WINS (Position 11-20)")
    print("="*80)
    for i, qw in enumerate(opportunities.get('quick_wins', [])[:15], 1):
        print(f"\n{i}. {qw['keyword']}")
        print(f"   Position: {qw['position']:.1f}")
        print(f"   Impressions: {qw['impressions']:,}")
        print(f"   Clicks: {qw['clicks']:,}")
        print(f"   CTR: {qw['ctr']:.2%}")

    print("\n" + "="*80)
    print("DECLINING CONTENT")
    print("="*80)
    for i, dc in enumerate(opportunities.get('declining_content', [])[:15], 1):
        print(f"\n{i}. {dc['title']}")
        print(f"   URL: {dc['path']}")
        print(f"   Previous: {dc['previous_pageviews']:,} → Current: {dc['pageviews']:,}")
        print(f"   Change: {dc['change_percent']:.1f}%")

    print("\n" + "="*80)
    print("LOW CTR PAGES")
    print("="*80)
    for i, lc in enumerate(opportunities.get('low_ctr', [])[:15], 1):
        print(f"\n{i}. {lc['url']}")
        print(f"   Impressions: {lc['impressions']:,}")
        print(f"   Clicks: {lc['clicks']:,}")
        print(f"   CTR: {lc['ctr']:.2%}")
        if 'expected_ctr' in lc:
            print(f"   Expected CTR: {lc['expected_ctr']:.2%}")
        if 'missed_clicks' in lc:
            print(f"   Missed clicks/month: {lc['missed_clicks']:,}")
        print(f"   Avg Position: {lc['avg_position']:.1f}")

    print("\n" + "="*80)
    print("TRENDING TOPICS")
    print("="*80)
    for i, tt in enumerate(opportunities.get('trending_topics', [])[:15], 1):
        print(f"\n{i}. {tt['query']}")
        print(f"   Recent impressions: {tt['recent_impressions']:,}")
        print(f"   Previous impressions: {tt['previous_impressions']:,}")
        print(f"   Change: +{tt['change_percent']:.1f}%")

    print("\n" + "="*80)
    print("\nSUMMARY METRICS")
    print("="*80)
    print(json.dumps(report['summary'], indent=2))

    # Save to JSON for reference
    _export_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'opportunities_export.json')
    with open(_export_path, 'w') as f:
        json.dump({
            'summary': report['summary'],
            'opportunities': opportunities,
            'top_performers': report['top_performers']
        }, f, indent=2, default=str)

    print("\n✅ Data exported to opportunities_export.json")
