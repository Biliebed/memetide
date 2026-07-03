#!/usr/bin/env python3
"""
Test script for MemeTide API

Run the API server first:
  python api_server.py

Then run this script:
  python test_api.py
"""

import httpx
import asyncio
import json
from datetime import datetime


BASE_URL = "http://localhost:8000"


async def test_api():
    """Test all API endpoints"""
    
    print("\n" + "="*60)
    print("🌊 MEMETIDE API TEST")
    print("="*60 + "\n")
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        
        # Test 1: Root endpoint
        print("[1/7] Testing root endpoint...")
        try:
            response = await client.get(f"{BASE_URL}/")
            assert response.status_code == 200
            data = response.json()
            print(f"✅ Root: {data['name']} v{data['version']}")
        except Exception as e:
            print(f"❌ Root failed: {e}")
            return
        
        # Test 2: Health check
        print("\n[2/7] Testing health check...")
        try:
            response = await client.get(f"{BASE_URL}/health")
            assert response.status_code == 200
            data = response.json()
            print(f"✅ Health: {data['status']}, uptime {data['uptime_seconds']:.1f}s")
        except Exception as e:
            print(f"❌ Health check failed: {e}")
        
        # Test 3: Scan with mock data
        print("\n[3/7] Testing scan endpoint (mock data)...")
        try:
            payload = {
                "min_mentions": 3,
                "top_n": 5,
                "use_mock_data": True
            }
            response = await client.post(f"{BASE_URL}/scan", json=payload)
            assert response.status_code == 200
            data = response.json()
            
            scan_id = data['scan_id']
            result = data['data']
            
            print(f"✅ Scan complete:")
            print(f"   - Scan ID: {scan_id}")
            print(f"   - Duration: {result['duration_seconds']:.2f}s")
            print(f"   - Tokens found: {result['unique_tokens']}")
            print(f"   - Total mentions: {result['total_mentions']}")
            
            # Print top predictions
            if result['predictions']:
                print(f"\n   Top 3 predictions:")
                for i, pred in enumerate(result['predictions'][:3], 1):
                    print(f"   {i}. ${pred['token_symbol']}: {pred['score']:.1f}/100 ({pred['confidence']})")
        
        except Exception as e:
            print(f"❌ Scan failed: {e}")
        
        # Test 4: History endpoint
        print("\n[4/7] Testing history endpoint...")
        try:
            response = await client.get(f"{BASE_URL}/history?limit=3")
            assert response.status_code == 200
            data = response.json()
            print(f"✅ History: {data['total']} scans, showing {len(data['results'])}")
        except Exception as e:
            print(f"❌ History failed: {e}")
        
        # Test 5: Get scan by ID
        print("\n[5/7] Testing get scan by ID...")
        try:
            response = await client.get(f"{BASE_URL}/history/{scan_id}")
            assert response.status_code == 200
            data = response.json()
            print(f"✅ Get by ID: Found scan {data['data']['scan_id']}")
        except Exception as e:
            print(f"❌ Get by ID failed: {e}")
        
        # Test 6: Stats endpoint
        print("\n[6/7] Testing stats endpoint...")
        try:
            response = await client.get(f"{BASE_URL}/stats")
            assert response.status_code == 200
            data = response.json()
            print(f"✅ Stats:")
            print(f"   - Total scans: {data['total_scans']}")
            print(f"   - Tokens analyzed: {data['total_tokens_analyzed']}")
            print(f"   - Avg duration: {data['average_scan_duration']:.2f}s")
        except Exception as e:
            print(f"❌ Stats failed: {e}")
        
        # Test 7: Background scan
        print("\n[7/7] Testing background scan...")
        try:
            payload = {
                "min_mentions": 2,
                "use_mock_data": True
            }
            response = await client.post(f"{BASE_URL}/scan/background", json=payload)
            assert response.status_code == 200
            data = response.json()
            print(f"✅ Background scan: {data['status']} ({data['scan_id']})")
            
            # Wait a bit then check history
            await asyncio.sleep(2)
            response = await client.get(f"{BASE_URL}/history?limit=1")
            history = response.json()
            print(f"   Background scan completed: {history['results'][0]['scan_id']}")
        
        except Exception as e:
            print(f"❌ Background scan failed: {e}")
    
    print("\n" + "="*60)
    print("✅ API TESTS COMPLETE")
    print("="*60 + "\n")


# --- cURL Examples ---

def print_curl_examples():
    """Print example cURL commands"""
    
    print("\n" + "="*60)
    print("📝 CURL EXAMPLES")
    print("="*60 + "\n")
    
    examples = [
        ("Health Check", "curl http://localhost:8000/health"),
        ("Run Scan (Mock Data)", '''curl -X POST http://localhost:8000/scan \\
  -H "Content-Type: application/json" \\
  -d '{"min_mentions": 3, "use_mock_data": true, "top_n": 5}' '''),
        ("Get History", "curl http://localhost:8000/history?limit=5"),
        ("Get Stats", "curl http://localhost:8000/stats"),
        ("Background Scan", '''curl -X POST http://localhost:8000/scan/background \\
  -H "Content-Type: application/json" \\
  -d '{"min_mentions": 2, "use_mock_data": true}' '''),
    ]
    
    for title, cmd in examples:
        print(f"# {title}")
        print(cmd)
        print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--curl":
        print_curl_examples()
    else:
        asyncio.run(test_api())
