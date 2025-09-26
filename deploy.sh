#!/bin/bash
set -e

# Render the site
quarto render

# Deploy to deployment branch
git checkout deployment
git add -f _site/  # Force-add ignored files
git commit -m "Deploy: $(date +'%Y-%m-%d %H:%M:%S')"
git push origin deployment

# Return to main
git checkout main
