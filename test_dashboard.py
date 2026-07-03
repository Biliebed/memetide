#!/usr/bin/env python3
"""
Test dashboard features end-to-end

Tests all new features:
- Dark mode
- Export
- History
- Sample tweets
"""

import asyncio
import httpx
from datetime import datetime


async def test_dashboard_features():
    """Test all dashboard features"""
    
    print("=" * 60)
    print("🌊 MEMETIDE DASHBOARD FEATURE TESTS")
    print("=" * 60)
    print()
    
    base_url = "http://localhost:8000"
    
    # Test 1: Static file serving
    print("[1/5] Testing static file serving...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{base_url}/static/index.html")
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            html = response.text
            assert "MemeTide" in html, "Missing title"
            assert "toggleTheme" in html, "Missing dark mode"
            assert "exportResults" in html, "Missing export function"
            assert "toggleHistory" in html, "Missing history function"
            assert "Sample Tweets" in html, "Missing sample tweets"
            print("   ✅ All features present in HTML")
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            return False
    
    # Test 2: API scan with sample tweets
    print("\n[2/5] Testing scan with sample tweets...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{base_url}/scan",
                json={
                    "min_mentions": 3,
                    "use_mock_data": True,
                    "fetch_onchain": True,
                    "top_n": 2
                },
                timeout=30.0
            )
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            data = response.json()
            
            predictions = data['data']['predictions']
            assert len(predictions) > 0, "No predictions returned"
            
            # Check sample tweets
            for pred in predictions:
                assert 'sample_tweets' in pred, "Missing sample_tweets field"
                assert isinstance(pred['sample_tweets'], list), "sample_tweets not a list"
                if pred['sample_tweets']:
                    assert len(pred['sample_tweets']) <= 3, "Too many sample tweets"
                    print(f"   ✅ ${pred['token_symbol']}: {len(pred['sample_tweets'])} tweets")
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            return False
    
    # Test 3: Root redirect
    print("\n[3/5] Testing root redirect...")
    async with httpx.AsyncClient(follow_redirects=False) as client:
        try:
            response = await client.get(base_url)
            assert response.status_code in [307, 308], "Should redirect"
            assert "static/index.html" in response.headers.get('location', ''), "Wrong redirect target"
            print("   ✅ Root redirects to dashboard")
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            return False
    
    # Test 4: API info endpoint
    print("\n[4/5] Testing /api endpoint...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{base_url}/api")
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            data = response.json()
            assert 'dashboard' in data, "Missing dashboard field"
            assert data['dashboard'] == "/static/index.html", "Wrong dashboard path"
            print("   ✅ API info includes dashboard link")
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            return False
    
    # Test 5: Multiple scans (for history)
    print("\n[5/5] Testing multiple scans...")
    async with httpx.AsyncClient() as client:
        try:
            scan_ids = []
            for i in range(3):
                response = await client.post(
                    f"{base_url}/scan",
                    json={"min_mentions": 2 + i, "use_mock_data": True, "top_n": 5},
                    timeout=30.0
                )
                assert response.status_code == 200, f"Scan {i+1} failed"
                data = response.json()
                scan_ids.append(data['data']['scan_id'])
            
            print(f"   ✅ Generated {len(scan_ids)} scans for history")
            print(f"      IDs: {', '.join(scan_ids[:3])}...")
        except Exception as e:
            print(f"   ❌ Failed: {e}")
            return False
    
    print()
    print("=" * 60)
    print("✅ ALL DASHBOARD FEATURE TESTS PASSED (5/5)")
    print("=" * 60)
    print()
    print("Dashboard ready at: http://localhost:8000")
    print()
    print("Features tested:")
    print("  ✅ Static file serving")
    print("  ✅ Sample tweets in API response")
    print("  ✅ Root redirect to dashboard")
    print("  ✅ API info endpoint")
    print("  ✅ Multiple scans (history)")
    print()
    print("Manual tests needed:")
    print("  🌙 Dark mode toggle (click moon icon)")
    print("  💾 Export to JSON (click Export button)")
    print("  📜 History view (click History button)")
    print("  📱 Sample tweets display (in results)")
    print()
    
    return True


if __name__ == "__main__":
    try:
        result = asyncio.run(test_dashboard_features())
        exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ Test suite failed: {e}")
        exit(1)
