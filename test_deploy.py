#!/usr/bin/env python3
"""
Test deployment readiness

Simulates production environment checks.
"""

import os
import sys
import subprocess
import asyncio
import httpx


def test_requirements():
    """Check if requirements.txt is valid"""
    print("[1/5] Testing requirements.txt...")
    
    try:
        with open("requirements.txt") as f:
            lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
        
        print(f"   ✅ Found {len(lines)} dependencies")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def test_dockerfile():
    """Check if Dockerfile exists and is valid"""
    print("\n[2/5] Testing Dockerfile...")
    
    if not os.path.exists("Dockerfile"):
        print("   ❌ Dockerfile not found")
        return False
    
    with open("Dockerfile") as f:
        content = f.read()
    
    checks = [
        ("FROM python:", "Base image"),
        ("COPY requirements.txt", "Requirements copy"),
        ("pip install", "Dependency install"),
        ("CMD", "Start command"),
    ]
    
    for check, name in checks:
        if check in content:
            print(f"   ✅ {name}")
        else:
            print(f"   ❌ Missing: {name}")
            return False
    
    return True


def test_procfile():
    """Check if Procfile exists"""
    print("\n[3/5] Testing Procfile...")
    
    if not os.path.exists("Procfile"):
        print("   ❌ Procfile not found")
        return False
    
    with open("Procfile") as f:
        content = f.read()
    
    if "uvicorn" in content and "api_server:app" in content:
        print("   ✅ Procfile valid")
        return True
    else:
        print("   ❌ Invalid Procfile format")
        return False


def test_port_env():
    """Test if PORT environment variable is handled"""
    print("\n[4/5] Testing PORT environment variable...")
    
    with open("api_server.py") as f:
        content = f.read()
    
    if 'os.getenv("PORT"' in content or "os.environ.get('PORT'" in content:
        print("   ✅ PORT env variable handled")
        return True
    else:
        print("   ❌ PORT env variable not handled")
        return False


async def test_api_startup():
    """Test if API can start and respond"""
    print("\n[5/5] Testing API startup...")
    
    # Start server in background
    env = os.environ.copy()
    env["PORT"] = "9876"
    
    proc = subprocess.Popen(
        ["python", "api_server.py"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    try:
        # Wait for startup
        await asyncio.sleep(3)
        
        # Test health endpoint
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:9876/health")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ API started successfully")
                print(f"   Status: {data['status']}")
                print(f"   Version: {data['version']}")
                return True
            else:
                print(f"   ❌ API returned {response.status_code}")
                return False
    
    except Exception as e:
        print(f"   ❌ API startup failed: {e}")
        return False
    
    finally:
        proc.terminate()
        proc.wait(timeout=2)


async def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🚀 MEMETIDE DEPLOYMENT READINESS TEST")
    print("="*60 + "\n")
    
    results = []
    
    # Run tests
    results.append(test_requirements())
    results.append(test_dockerfile())
    results.append(test_procfile())
    results.append(test_port_env())
    results.append(await test_api_startup())
    
    # Summary
    print("\n" + "="*60)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ ALL CHECKS PASSED ({passed}/{total})")
        print("\n🚀 Ready to deploy!")
        print("\nNext steps:")
        print("1. Push to GitHub: git push origin main")
        print("2. Deploy to Railway: See DEPLOY_QUICK.md")
        print("3. Test live API: curl YOUR_URL/health")
        print("="*60 + "\n")
        sys.exit(0)
    else:
        print(f"❌ CHECKS FAILED ({passed}/{total})")
        print("\n⚠️ Fix issues before deploying")
        print("="*60 + "\n")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
