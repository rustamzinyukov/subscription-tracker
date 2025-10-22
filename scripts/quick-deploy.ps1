# PowerShell script for Railway deployment
Write-Host "🚂 Railway Deployment Script for Subscription Tracker" -ForegroundColor Green
Write-Host ""

# Check if Railway CLI is installed
try {
    railway --version | Out-Null
    Write-Host "✅ Railway CLI is installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Railway CLI not found. Installing..." -ForegroundColor Red
    npm install -g @railway/cli
}

Write-Host ""
Write-Host "📋 Step 1: Login to Railway" -ForegroundColor Yellow
Write-Host "Please run: railway login" -ForegroundColor Cyan
Write-Host "Press any key when you're logged in..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host ""
Write-Host "📦 Step 2: Initialize Railway project" -ForegroundColor Yellow
railway init

Write-Host ""
Write-Host "🗄️ Step 3: Add PostgreSQL database" -ForegroundColor Yellow
railway add postgresql

Write-Host ""
Write-Host "⚙️ Step 4: Set environment variables" -ForegroundColor Yellow
railway variables set ENVIRONMENT=production
railway variables set DEBUG=false
railway variables set LOG_LEVEL=INFO

Write-Host ""
Write-Host "🔐 Step 5: Generate and set secrets" -ForegroundColor Yellow
$secretKey = -join ((1..32) | ForEach {Get-Random -InputObject @('0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f')})
$jwtSecret = -join ((1..32) | ForEach {Get-Random -InputObject @('0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f')})
$webhookSecret = -join ((1..32) | ForEach {Get-Random -InputObject @('0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f')})

railway variables set SECRET_KEY=$secretKey
railway variables set JWT_SECRET_KEY=$jwtSecret
railway variables set TELEGRAM_WEBHOOK_SECRET=$webhookSecret

Write-Host ""
Write-Host "🤖 Step 6: Set Telegram Bot Token" -ForegroundColor Yellow
Write-Host "Please get your bot token from @BotFather and run:" -ForegroundColor Cyan
Write-Host "railway variables set TELEGRAM_BOT_TOKEN=your-bot-token-here" -ForegroundColor White
Write-Host ""
Write-Host "Press any key when you've set the Telegram token..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host ""
Write-Host "🚀 Step 7: Deploy application" -ForegroundColor Yellow
railway up

Write-Host ""
Write-Host "🌐 Step 8: Get your app URL" -ForegroundColor Yellow
$domain = railway domain
Write-Host "Your app URL: https://$domain" -ForegroundColor Green

Write-Host ""
Write-Host "✅ Deployment completed!" -ForegroundColor Green
Write-Host ""
Write-Host "🔧 Next steps:" -ForegroundColor Yellow
Write-Host "1. Set your Telegram webhook:" -ForegroundColor Cyan
Write-Host "   curl -X POST `"https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook`" -d `"url=https://$domain/api/v1/telegram/webhook`"" -ForegroundColor White
Write-Host ""
Write-Host "2. Test your API:" -ForegroundColor Cyan
Write-Host "   curl https://$domain/health" -ForegroundColor White
Write-Host ""
Write-Host "3. View logs:" -ForegroundColor Cyan
Write-Host "   railway logs" -ForegroundColor White
