#!/usr/bin/env python3
"""
MemeTide CLI - Quick memecoin trend scan
"""

import asyncio
import sys
import argparse
sys.path.insert(0, '/home/ubuntu/memetide')

from src.engine import MemeTideEngine


async def main():
    parser = argparse.ArgumentParser(
        description="MemeTide - Catch memecoin trends before they explode"
    )
    parser.add_argument(
        '--min-mentions',
        type=int,
        default=3,
        help='Minimum mentions to consider a token (default: 3)'
    )
    parser.add_argument(
        '--top',
        type=int,
        default=10,
        help='Show top N predictions (default: 10)'
    )
    parser.add_argument(
        '--mock',
        action='store_true',
        default=True,
        help='Use mock data for testing (default: True)'
    )
    parser.add_argument(
        '--real',
        action='store_true',
        help='Use real Twitter scraping (requires working Nitter)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )
    
    args = parser.parse_args()
    
    # Determine data source
    use_mock = not args.real if args.real else args.mock
    
    # Initialize engine
    engine = MemeTideEngine(use_mock_data=use_mock)
    
    # Run scan
    result = await engine.scan(min_mentions=args.min_mentions)
    
    # Output results
    if args.json:
        import json
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(engine.format_results(result, top_n=args.top))
        
        # Summary stats
        high_conf = result.get_high_confidence()
        if high_conf:
            print(f"\n🔥 HIGH CONFIDENCE PICKS ({len(high_conf)}):")
            for pred in high_conf:
                print(f"   ${pred.token_symbol} - Score: {pred.score:.1f}, "
                      f"Risk: {pred.risk_level.value}")
        
        print(f"\n💡 Tip: Use --json for structured output")
        print(f"💡 Tip: Use --real for live Twitter data (slower)\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Scan interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
