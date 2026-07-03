#!/bin/bash
# Quick GitHub push with token

echo "=========================================="
echo "🚀 Quick GitHub Push"
echo "=========================================="
echo ""
echo "Get token: https://github.com/settings/tokens"
echo "Click: Generate new token (classic)"
echo "Scopes: ✓ repo (all)"
echo ""
read -p "Paste your GitHub token: " TOKEN

if [ -z "$TOKEN" ]; then
    echo "❌ No token provided"
    exit 1
fi

echo ""
echo "Pushing to GitHub..."

cd ~/memetide
git branch -M main
git push https://$TOKEN@github.com/Biliebed/memetide.git main

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ SUCCESS! Pushed to GitHub"
    echo "=========================================="
    echo ""
    echo "Now deploy on Railway:"
    echo "1. Go to: https://railway.app"
    echo "2. Login with GitHub"
    echo "3. New Project → Deploy from GitHub repo"
    echo "4. Select: Biliebed/memetide"
    echo "5. Wait ~2 minutes"
    echo "6. Get URL from Settings → Domains"
    echo ""
else
    echo ""
    echo "❌ Push failed. Check your token."
fi
