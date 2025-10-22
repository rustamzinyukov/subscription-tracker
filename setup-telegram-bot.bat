@echo off
echo 🤖 Telegram Bot Setup
echo.

echo 📋 Steps to setup Telegram bot:
echo.

echo 1. Create bot in Telegram:
echo    - Open Telegram
echo    - Find @BotFather
echo    - Send /newbot
echo    - Enter bot name: Subscription Tracker Bot
echo    - Enter username: subscription_tracker_bot
echo    - Copy the bot token
echo.

echo 2. Update Railway variables:
echo    - Replace YOUR_BOT_TOKEN_HERE with your actual token
echo    - Update your-secret-key-here with a secure secret
echo.

echo 3. Test the bot:
echo    - Find your bot in Telegram
echo    - Send /start
echo    - Try /list and /add commands
echo.

echo 🔧 Commands to update variables:
echo.
echo railway variables --set "TELEGRAM_BOT_TOKEN=YOUR_ACTUAL_TOKEN"
echo railway variables --set "TELEGRAM_WEBHOOK_SECRET=your-secure-secret"
echo.

echo 📚 Bot Commands:
echo - /start - Start the bot
echo - /list - List your subscriptions
echo - /add - Add new subscription
echo - /help - Show help
echo.

pause
