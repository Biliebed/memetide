#!/bin/bash
# Test live Railway deployment

API_URL="https://memetide-production.up.railway.app"

echo "🌊 Testing MemeTide Live Deployment"
echo "================================"
echo ""

echo "1️⃣  Health Check..."
curl -s $API_URL/health | python3 -m json.tool
echo ""
echo ""

echo "2️⃣  Stats Endpoint..."
curl -s $API_URL/stats | python3 -m json.tool
echo ""
echo ""

echo "3️⃣  Mock Data Scan (Quick)..."
curl -s -X POST $API_URL/scan \
  -H "Content-Type: application/json" \
  -d '{"min_mentions": 3, "use_mock_data": true, "top_n": 3}' | python3 -m json.tool
echo ""
echo ""

echo "4️⃣  API Documentation..."
echo "📚 Swagger UI: $API_URL/docs"
echo "📚 ReDoc: $API_URL/redoc"
echo ""

echo "✅ Test Complete!"
