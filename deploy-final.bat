@echo off
echo 🚂 Final Railway Deployment
echo.

echo ✅ Project: subscription-tracker
echo ✅ Database: PostgreSQL configured
echo ✅ Variables: Set
echo.

echo 🔧 Current status:
railway status

echo.
echo 🌐 Your app URL:
railway domain

echo.
echo 📋 Next steps:
echo 1. Wait for deployment to complete (check logs with: railway logs)
echo 2. Test your API: curl https://your-app.railway.app/health
echo 3. View API docs: https://your-app.railway.app/docs
echo.

echo 🔍 To check deployment status:
echo railway logs
echo.

echo 🎉 Your Subscription Tracker is being deployed!
echo.

pause
