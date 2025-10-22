@echo off
echo 🚂 Railway Deployment Script for Subscription Tracker
echo.

echo 📋 Step 1: Login to Railway
echo Please run: railway login
echo Press any key when you're logged in...
pause

echo.
echo 📦 Step 2: Initialize Railway project
railway init

echo.
echo 🗄️ Step 3: Add PostgreSQL database
railway add postgresql

echo.
echo ⚙️ Step 4: Set environment variables
railway variables set ENVIRONMENT=production
railway variables set DEBUG=false
railway variables set LOG_LEVEL=INFO

echo.
echo 🔐 Step 5: Generate secrets
for /f %%i in ('openssl rand -hex 32') do set SECRET_KEY=%%i
for /f %%i in ('openssl rand -hex 32') do set JWT_SECRET_KEY=%%i
for /f %%i in ('openssl rand -hex 32') do set TELEGRAM_WEBHOOK_SECRET=%%i

railway variables set SECRET_KEY=%SECRET_KEY%
railway variables set JWT_SECRET_KEY=%JWT_SECRET_KEY%
railway variables set TELEGRAM_WEBHOOK_SECRET=%TELEGRAM_WEBHOOK_SECRET%

echo.
echo 🤖 Step 6: Set Telegram Bot Token
echo Please get your bot token from @BotFather and run:
echo railway variables set TELEGRAM_BOT_TOKEN=your-bot-token-here
echo.
echo Press any key when you've set the Telegram token...
pause

echo.
echo 🚀 Step 7: Deploy application
railway up

echo.
echo 🌐 Step 8: Get your app URL
railway domain

echo.
echo ✅ Deployment completed!
echo.
echo 🔧 Next steps:
echo 1. Set your Telegram webhook:
echo    curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" -d "url=https://$(railway domain)/api/v1/telegram/webhook"
echo.
echo 2. Test your API:
echo    curl https://$(railway domain)/health
echo.
echo 3. View logs:
echo    railway logs
