@echo off
echo ========================================
echo  AI Emotion Detection - Deploy Setup
echo ========================================
echo.
echo This script will commit deployment files to GitHub
echo.
pause

echo.
echo [1/3] Adding files to git...
git add .

echo.
echo [2/3] Committing changes...
git commit -m "Add deployment configuration for Render, Railway, and Heroku"

echo.
echo [3/3] Pushing to GitHub...
git push origin main

echo.
echo ========================================
echo  SUCCESS! Files pushed to GitHub
echo ========================================
echo.
echo Next steps:
echo 1. Go to https://render.com or https://railway.app
echo 2. Sign in with GitHub
echo 3. Deploy your repository
echo 4. Check DEPLOY_NOW.md for detailed instructions
echo.
pause
