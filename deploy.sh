#!/bin/bash
# deploy.sh - Deploy PPA Attestation Visualizer to GitHub
# Run this script to create the repo and push all code

set -e

REPO_NAME="ppa-attestation-visualizer"
GITHUB_USER="rmartinppa"  # Change this to your GitHub username

echo "🚀 PPA Attestation Visualizer Deployment Script"
echo "================================================"
echo ""

# Check for GitHub token
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Error: GITHUB_TOKEN environment variable not set"
    echo ""
    echo "Please set your GitHub token:"
    echo "  export GITHUB_TOKEN='your_token_here'"
    echo ""
    echo "To create a token:"
    echo "  1. Go to https://github.com/settings/tokens"
    echo "  2. Click 'Generate new token (classic)'"
    echo "  3. Select 'repo' scope"
    echo "  4. Copy and export the token"
    exit 1
fi

echo "✅ GitHub token found"
echo ""

# Create repository via GitHub API
echo "📦 Creating GitHub repository: $REPO_NAME"
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d "{
    \"name\": \"$REPO_NAME\",
    \"description\": \"Visual Hardware Identity Cards for RustChain PPA Fingerprints\",
    \"homepage\": \"https://rmartinppa.github.io/$REPO_NAME\",
    \"private\": false,
    \"has_issues\": true,
    \"has_wiki\": false,
    \"has_pages\": true
  }" | grep -q '"id"' && echo "✅ Repository created successfully" || echo "⚠️  Repository may already exist"

echo ""

# Initialize git if needed
if [ ! -d ".git" ]; then
    echo "🔧 Initializing git repository..."
    git init
    git branch -M main
fi

# Add remote
echo "🔗 Adding GitHub remote..."
git remote remove origin 2>/dev/null || true
git remote add origin "https://$GITHUB_TOKEN@github.com/$GITHUB_USER/$REPO_NAME.git"

# Add all files
echo "📁 Adding files to git..."
git add -A

# Commit
echo "💾 Committing files..."
git commit -m "Initial commit: PPA Attestation Visualizer

- Add ppa_visualizer.py - main visualization module
- Add sample-fingerprint.json - PowerPC G4 example data
- Add hardware_identity.svg - sample output
- Add demo.html - interactive demo page
- Add README.md - comprehensive documentation
- Add deploy.sh - deployment script

Bounty: https://github.com/Scottcjn/Rustchain/issues/2148
Reward: 75 RTC" || echo "⚠️  Nothing to commit"

# Push
echo "⬆️  Pushing to GitHub..."
git push -u origin main --force

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📍 Repository URL: https://github.com/$GITHUB_USER/$REPO_NAME"
echo "🌐 Demo page: https://$GITHUB_USER.github.io/$REPO_NAME/demo.html"
echo ""
echo "Next steps:"
echo "  1. Visit the bounty issue: https://github.com/Scottcjn/Rustchain/issues/2148"
echo "  2. Comment with your submission:"
echo ""
echo "     🎯 Bounty Submission for #2148"
echo ""
echo "     Repository: https://github.com/$GITHUB_USER/$REPO_NAME"
echo "     Demo: https://$GITHUB_USER.github.io/$REPO_NAME/demo.html"
echo ""
echo "     ✅ All requirements met:"
echo "     - Radar/spider chart of 7 channel scores"
echo "     - Oscilloscope waveform for clock drift"
echo "     - Heatmap for cache latency profiles"
echo "     - Jitter constellation star map"
echo "     - Combined visual badge"
echo "     - Pure Python, SVG output"
echo ""
