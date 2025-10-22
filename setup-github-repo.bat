@echo off
echo 🐙 GitHub Repository Setup
echo.

echo 📋 Current Git status:
git status

echo.
echo 🔧 To connect to GitHub:
echo.
echo 1. Create repository on GitHub:
echo    - Go to https://github.com/new
echo    - Repository name: subscription-tracker
echo    - Make it Public
echo    - Don't initialize with README
echo.

echo 2. After creating, run:
echo    git remote add origin https://github.com/YOUR_USERNAME/subscription-tracker.git
echo    git push -u origin main
echo.

echo 3. Connect Railway to GitHub:
echo    - Go to https://railway.app/dashboard
echo    - Select your project
echo    - Settings → Connect GitHub
echo    - Select subscription-tracker repository
echo.

echo 🎯 This will solve the Dockerfile issue!
echo.

pause
