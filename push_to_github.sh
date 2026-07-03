#!/bin/bash
# Quick push to GitHub script

set -e

echo "=========================================="
echo "🚀 MemeTide GitHub Push Helper"
echo "=========================================="
echo ""

# Check if repo exists
if [ ! -d ".git" ]; then
    echo "❌ Error: Not a git repository"
    exit 1
fi

# Check remote
REMOTE=$(git remote get-url origin 2>/dev/null || echo "")

if [ -z "$REMOTE" ]; then
    echo "📝 Setting up GitHub remote..."
    echo ""
    echo "Enter GitHub repo URL (e.g., https://github.com/Biliebed/memetide.git):"
    read REPO_URL
    git remote add origin "$REPO_URL"
    echo "✅ Remote added: $REPO_URL"
else
    echo "✅ Remote already configured: $REMOTE"
fi

echo ""
echo "📊 Current status:"
git status --short

echo ""
echo "📦 Commits to push:"
git log --oneline origin/main..HEAD 2>/dev/null || git log --oneline | head -5

echo ""
echo "=========================================="
echo "Ready to push!"
echo "=========================================="
echo ""
echo "Choose authentication method:"
echo "1. SSH (requires SSH key setup)"
echo "2. HTTPS with token (requires Personal Access Token)"
echo "3. Manual (I'll handle it myself)"
echo ""
read -p "Enter choice [1-3]: " CHOICE

case $CHOICE in
    1)
        echo ""
        echo "Using SSH..."
        CURRENT_URL=$(git remote get-url origin)
        if [[ $CURRENT_URL == https* ]]; then
            SSH_URL=$(echo $CURRENT_URL | sed 's|https://github.com/|git@github.com:|')
            git remote set-url origin "$SSH_URL"
            echo "✅ Switched to SSH: $SSH_URL"
        fi
        
        echo ""
        echo "Pushing to GitHub..."
        git branch -M main
        git push -u origin main
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "=========================================="
            echo "✅ SUCCESS! Pushed to GitHub"
            echo "=========================================="
            echo ""
            echo "Next: Deploy to Railway"
            echo "1. Go to https://railway.app"
            echo "2. New Project → Deploy from GitHub"
            echo "3. Select your repo"
            echo "4. Wait ~2 min"
            echo "5. Get URL from Settings → Domains"
        else
            echo ""
            echo "❌ Push failed. Check your SSH key:"
            echo "   cat ~/.ssh/id_ed25519.pub"
            echo "   Add this to GitHub Settings → SSH Keys"
        fi
        ;;
    
    2)
        echo ""
        echo "Using HTTPS with token..."
        echo ""
        echo "Get token: GitHub Settings → Developer settings → Personal access tokens"
        echo "Required scope: repo (all)"
        echo ""
        read -p "Enter your GitHub Personal Access Token: " TOKEN
        
        CURRENT_URL=$(git remote get-url origin)
        if [[ $CURRENT_URL == git@* ]]; then
            HTTPS_URL=$(echo $CURRENT_URL | sed 's|git@github.com:|https://github.com/|')
            git remote set-url origin "$HTTPS_URL"
        fi
        
        REPO_PATH=$(git remote get-url origin | sed 's|https://github.com/||' | sed 's|.git||')
        
        echo ""
        echo "Pushing to GitHub..."
        git branch -M main
        git push https://$TOKEN@github.com/$REPO_PATH.git main
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "=========================================="
            echo "✅ SUCCESS! Pushed to GitHub"
            echo "=========================================="
            echo ""
            echo "Next: Deploy to Railway"
            echo "1. Go to https://railway.app"
            echo "2. New Project → Deploy from GitHub"
            echo "3. Select your repo"
        else
            echo ""
            echo "❌ Push failed. Check your token and try again"
        fi
        ;;
    
    3)
        echo ""
        echo "Manual push commands:"
        echo ""
        echo "# Set main branch"
        echo "git branch -M main"
        echo ""
        echo "# Push (will prompt for credentials)"
        echo "git push -u origin main"
        echo ""
        echo "Or use GitHub CLI:"
        echo "gh auth login"
        echo "git push -u origin main"
        ;;
    
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
