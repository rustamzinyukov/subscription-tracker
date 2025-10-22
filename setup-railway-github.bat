@echo off
echo 🚂 Railway + GitHub Setup
echo.

echo 📋 Steps to connect Railway with GitHub:
echo.
echo 1. Go to https://railway.app/dashboard
echo 2. Find your project 'subscription-tracker'
echo 3. Click on the project
echo 4. Go to Settings tab
echo 5. Under 'Source', click 'Connect GitHub'
echo 6. Select your 'subscription-tracker' repository
echo 7. Choose the 'main' branch
echo 8. Save the settings
echo.

echo 🔧 Alternative: Use Railway CLI:
echo.
echo railway connect github
echo.
echo Then select your repository and branch.
echo.

echo ✅ After connecting GitHub:
echo - Railway will automatically deploy from GitHub
echo - Every push to main branch will trigger deployment
echo - No more local file issues!
echo.

pause
