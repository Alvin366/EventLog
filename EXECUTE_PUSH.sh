#!/bin/bash

# EventLog - GitHub Push Script
# Execute this to push EventLog to GitHub main branch

set -e  # Exit on error

echo "=========================================="
echo "EventLog - GitHub Push Script"
echo "=========================================="
echo ""

# Step 1: Navigate to EventLog directory
echo "[1/8] Navigating to EventLog directory..."
cd /config/ClaudeProjects/EventLog
echo "✓ Current directory: $(pwd)"
echo ""

# Step 2: Initialize git repository
echo "[2/8] Initializing git repository..."
if [ -d ".git" ]; then
    echo "⚠ Git repository already initialized"
else
    git init
    echo "✓ Git repository initialized"
fi
echo ""

# Step 3: Configure git (global)
echo "[3/8] Configuring git..."
git config --global user.name "Alvin366"
git config --global user.email "alvin366@example.com"
echo "✓ Git configured:"
echo "  - User: $(git config --global user.name)"
echo "  - Email: $(git config --global user.email)"
echo ""

# Step 4: Stage all files
echo "[4/8] Staging all files..."
git add .
echo "✓ Files staged"
git status --short | head -10
echo ""

# Step 5: Create initial commit
echo "[5/8] Creating initial commit..."
git commit -m "feat: Initial EventLog MVP commit

- EventLogCollector custom component for HA Core log monitoring
- Event logger blueprint for processing and deduplication
- Event management scripts (log, acknowledge, close)
- Helper configurations (input_text, input_select, input_boolean, input_number)
- Valiug dashboard card integration
- Complete documentation and deployment guides
- Version 0.1.0-MVP ready for testing

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"

echo "✓ Initial commit created"
echo ""

# Step 6: Rename branch to main
echo "[6/8] Ensuring branch is named 'main'..."
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ]; then
    git branch -M main
    echo "✓ Branch renamed to 'main'"
else
    echo "✓ Branch already named 'main'"
fi
echo ""

# Step 7: Add remote
echo "[7/8] Adding GitHub remote..."
if git remote | grep -q origin; then
    echo "⚠ Remote 'origin' already exists"
    git remote remove origin
fi
git remote add origin https://github.com/Alvin366/EventLog.git
echo "✓ Remote added:"
git remote -v | grep origin
echo ""

# Step 8: Push to GitHub
echo "[8/8] Pushing to GitHub main branch..."
echo "⚠ You will be prompted for GitHub credentials"
echo "  - Use your GitHub username (Alvin366)"
echo "  - Use a Personal Access Token (not your password)"
echo "  - Create token at: https://github.com/settings/tokens"
echo ""

git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ SUCCESS! EventLog pushed to GitHub"
    echo "=========================================="
    echo ""
    echo "Repository: https://github.com/Alvin366/EventLog"
    echo ""
    echo "Next steps:"
    echo "1. Open: https://github.com/Alvin366/EventLog"
    echo "2. Verify all files are present"
    echo "3. Check commit history"
    echo "4. Begin Phase 2 development"
    echo ""
    echo "Useful commands:"
    echo "  git log --oneline                  # See commit history"
    echo "  git status                         # Check status"
    echo "  git pull origin main               # Update from remote"
    echo "  git checkout -b feature/xyz        # Create feature branch"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "❌ PUSH FAILED"
    echo "=========================================="
    echo ""
    echo "Troubleshooting:"
    echo "1. Check your GitHub credentials"
    echo "2. Verify repository exists at: https://github.com/Alvin366/EventLog"
    echo "3. Check internet connection"
    echo "4. For more help, see: GITHUB_PUSH_GUIDE.md"
    echo ""
    exit 1
fi

# Verify push
echo "Verifying push..."
git log -1 --oneline
git branch -r
git status

echo ""
echo "=========================================="
echo "All done! Your EventLog is now on GitHub 🎉"
echo "=========================================="
