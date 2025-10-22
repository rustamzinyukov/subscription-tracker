@echo off
echo 🚀 Deploy via GitHub + Railway
echo.

echo 📋 Quick deployment steps:
echo.

echo 1️⃣ Create GitHub repository:
echo    - Go to https://github.com/new
echo    - Name: subscription-tracker
echo    - Public repository
echo    - Don't initialize with README
echo.

echo 2️⃣ Push code to GitHub:
echo    git remote add origin https://github.com/YOUR_USERNAME/subscription-tracker.git
echo    git branch -M main
echo    git push -u origin main
echo.

echo 3️⃣ Connect Railway to GitHub:
echo    - Go to https://railway.app/dashboard
echo    - Select your project
echo    - Settings → Connect GitHub
echo    - Select subscription-tracker repository
echo.

echo 4️⃣ Railway will auto-deploy from GitHub!
echo.

echo 🎯 Benefits:
echo ✅ No more local file issues
echo ✅ Automatic deployments on git push
echo ✅ Version control
echo ✅ Easy collaboration
echo.

echo Press any key to continue...
pause

echo.
echo 🔧 Let's start with GitHub setup...
echo.

echo Enter your GitHub username:
set /p GITHUB_USERNAME=

echo.
echo Setting up GitHub remote...
git remote remove origin 2>nul
git remote add origin https://github.com/%GITHUB_USERNAME%/subscription-tracker.git

echo.
echo Pushing to GitHub...
git branch -M main
git push -u origin main

echo.
echo ✅ Code pushed to GitHub!
echo.
echo 🌐 Your repository: https://github.com/%GITHUB_USERNAME%/subscription-tracker
echo.

echo 📋 Next steps:
echo 1. Go to https://railway.app/dashboard
echo 2. Select your project
echo 3. Settings → Connect GitHub
echo 4. Select subscription-tracker repository
echo 5. Railway will auto-deploy!
echo.

pause
