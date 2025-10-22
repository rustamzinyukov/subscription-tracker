# Telegram Bot Setup Script
Write-Host "🤖 Telegram Bot Setup for Subscription Tracker" -ForegroundColor Green
Write-Host ""

Write-Host "📋 Step 1: Create Telegram Bot" -ForegroundColor Yellow
Write-Host "1. Open @BotFather in Telegram" -ForegroundColor Cyan
Write-Host "2. Send /newbot" -ForegroundColor White
Write-Host "3. Follow the instructions to create your bot" -ForegroundColor White
Write-Host "4. Save the bot token you receive" -ForegroundColor White
Write-Host ""
Write-Host "Press any key when you have your bot token..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host ""
Write-Host "🔧 Step 2: Configure Bot Commands" -ForegroundColor Yellow
Write-Host "Send these commands to @BotFather:" -ForegroundColor Cyan
Write-Host ""
Write-Host "/setcommands" -ForegroundColor White
Write-Host "start - Начать работу с ботом" -ForegroundColor White
Write-Host "help - Показать справку" -ForegroundColor White
Write-Host "list - Показать все подписки" -ForegroundColor White
Write-Host "add - Добавить новую подписку" -ForegroundColor White
Write-Host "stats - Показать статистику трат" -ForegroundColor White
Write-Host "settings - Настройки" -ForegroundColor White
Write-Host ""
Write-Host "Press any key when you've set the commands..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host ""
Write-Host "🌐 Step 3: Set Webhook" -ForegroundColor Yellow
Write-Host "Enter your Railway app domain (e.g., your-app.railway.app):" -ForegroundColor Cyan
$domain = Read-Host

Write-Host ""
Write-Host "Enter your bot token:" -ForegroundColor Cyan
$botToken = Read-Host

Write-Host ""
Write-Host "Setting webhook..." -ForegroundColor Yellow
$webhookUrl = "https://$domain/api/v1/telegram/webhook"

try {
    $response = Invoke-RestMethod -Uri "https://api.telegram.org/bot$botToken/setWebhook" -Method Post -Body @{url=$webhookUrl}
    if ($response.ok) {
        Write-Host "✅ Webhook set successfully!" -ForegroundColor Green
        Write-Host "Webhook URL: $webhookUrl" -ForegroundColor Cyan
    } else {
        Write-Host "❌ Failed to set webhook: $($response.description)" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Error setting webhook: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "🔍 Step 4: Test Bot" -ForegroundColor Yellow
Write-Host "1. Find your bot in Telegram" -ForegroundColor Cyan
Write-Host "2. Send /start" -ForegroundColor White
Write-Host "3. Try /help to see available commands" -ForegroundColor White
Write-Host ""
Write-Host "✅ Telegram bot setup completed!" -ForegroundColor Green
