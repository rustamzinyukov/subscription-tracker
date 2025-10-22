@echo off
title Railway Deployment - Subscription Tracker
color 0A

echo.
echo  ███████╗██╗   ██╗██████╗ ███████╗████████╗███████╗███████╗
echo  ██╔════╝██║   ██║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔════╝
echo  ███████╗██║   ██║██████╔╝███████╗   ██║   █████╗  ███████╗
echo  ╚════██║██║   ██║██╔══██╗╚════██║   ██║   ██╔══╝  ╚════██║
echo  ███████║╚██████╔╝██████╔╝███████║   ██║   ███████╗███████║
echo  ╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚══════╝
echo.
echo  🚂 Railway Deployment for Subscription Tracker
echo  ================================================
echo.

echo 📋 Checking prerequisites...

:: Check if Railway CLI is installed
railway --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Railway CLI not found. Installing...
    npm install -g @railway/cli
    if %errorlevel% neq 0 (
        echo ❌ Failed to install Railway CLI. Please install manually.
        pause
        exit /b 1
    )
)

echo ✅ Railway CLI is ready
echo.

echo 🔐 Step 1: Login to Railway
echo Please run: railway login
echo This will open your browser for authentication.
echo.
pause

echo 📦 Step 2: Initialize project
railway init
if %errorlevel% neq 0 (
    echo ❌ Failed to initialize Railway project
    pause
    exit /b 1
)

echo 🗄️ Step 3: Add PostgreSQL database
railway add postgresql
if %errorlevel% neq 0 (
    echo ❌ Failed to add PostgreSQL database
    pause
    exit /b 1
)

echo ⚙️ Step 4: Setting environment variables...
railway variables set ENVIRONMENT=production
railway variables set DEBUG=false
railway variables set LOG_LEVEL=INFO

:: Generate random secrets
for /f %%i in ('powershell -command "Get-Random -Count 32 -InputObject @('0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f') | ForEach-Object {$_} | Join-String"') do set SECRET_KEY=%%i
for /f %%i in ('powershell -command "Get-Random -Count 32 -InputObject @('0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f') | ForEach-Object {$_} | Join-String"') do set JWT_SECRET=%%i
for /f %%i in ('powershell -command "Get-Random -Count 32 -InputObject @('0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f') | ForEach-Object {$_} | Join-String"') do set WEBHOOK_SECRET=%%i

railway variables set SECRET_KEY=%SECRET_KEY%
railway variables set JWT_SECRET_KEY=%JWT_SECRET%
railway variables set TELEGRAM_WEBHOOK_SECRET=%WEBHOOK_SECRET%

echo ✅ Environment variables set
echo.

echo 🤖 Step 5: Telegram Bot Setup
echo.
echo Please create a Telegram bot:
echo 1. Open @BotFather in Telegram
echo 2. Send /newbot
echo 3. Follow instructions to create your bot
echo 4. Copy the bot token
echo.
set /p BOT_TOKEN="Enter your Telegram bot token: "

railway variables set TELEGRAM_BOT_TOKEN=%BOT_TOKEN%

echo ✅ Telegram bot token set
echo.

echo 🚀 Step 6: Deploying application...
railway up
if %errorlevel% neq 0 (
    echo ❌ Deployment failed
    pause
    exit /b 1
)

echo ✅ Application deployed successfully!
echo.

echo 🌐 Getting your app URL...
for /f %%i in ('railway domain') do set APP_URL=%%i

echo.
echo 🎉 Deployment completed!
echo ========================
echo.
echo 🌐 Your app URL: https://%APP_URL%
echo 📚 API Docs: https://%APP_URL%/docs
echo ❤️ Health Check: https://%APP_URL%/health
echo.

echo 🔧 Next steps:
echo 1. Set Telegram webhook:
echo    curl -X POST "https://api.telegram.org/bot%BOT_TOKEN%/setWebhook" -d "url=https://%APP_URL%/api/v1/telegram/webhook"
echo.
echo 2. Test your API:
echo    curl https://%APP_URL%/health
echo.
echo 3. View logs:
echo    railway logs
echo.

echo Press any key to exit...
pause >nul
