@echo off
echo 🚂 Simple Railway Deployment
echo.

echo Step 1: Login to Railway
echo Please run: railway login
echo Press any key when logged in...
pause

echo.
echo Step 2: Initialize project
railway init

echo.
echo Step 3: Add database
railway add postgresql

echo.
echo Step 4: Set environment variables
railway variables set ENVIRONMENT=production
railway variables set DEBUG=false

echo.
echo Step 5: Deploy
railway up

echo.
echo Step 6: Get URL
railway domain

echo.
echo ✅ Done! Your app is deployed.
pause
