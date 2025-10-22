#!/bin/bash

# Railway setup script for Subscription Tracker

echo "🚂 Setting up Railway project..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

# Login to Railway
echo "🔐 Logging in to Railway..."
railway login

# Create new project
echo "📦 Creating new Railway project..."
railway init

# Add PostgreSQL database
echo "🗄️ Adding PostgreSQL database..."
railway add postgresql

# Set up environment variables
echo "⚙️ Setting up environment variables..."

# Get database URL
DB_URL=$(railway variables get DATABASE_URL)
echo "Database URL: $DB_URL"

# Set other required variables
railway variables set SECRET_KEY=$(openssl rand -hex 32)
railway variables set JWT_SECRET_KEY=$(openssl rand -hex 32)
railway variables set TELEGRAM_WEBHOOK_SECRET=$(openssl rand -hex 32)
railway variables set ENVIRONMENT=production
railway variables set DEBUG=false
railway variables set LOG_LEVEL=INFO
railway variables set CORS_ORIGINS=https://$(railway domain)

echo "✅ Railway setup completed!"
echo "🔧 Next steps:"
echo "1. Set your TELEGRAM_BOT_TOKEN: railway variables set TELEGRAM_BOT_TOKEN=your-bot-token"
echo "2. Deploy: railway up"
echo "3. Set webhook: curl -X POST https://api.telegram.org/bot<TOKEN>/setWebhook -d url=https://$(railway domain)/api/v1/telegram/webhook"
