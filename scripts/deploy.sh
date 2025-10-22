#!/bin/bash

# Railway deployment script for Subscription Tracker

echo "🚂 Deploying to Railway..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Please install it first:"
    echo "npm install -g @railway/cli"
    exit 1
fi

# Login to Railway (if not already logged in)
echo "🔐 Checking Railway authentication..."
railway whoami || railway login

# Link to existing project or create new one
echo "🔗 Linking to Railway project..."
railway link

# Set environment variables
echo "⚙️ Setting environment variables..."
railway variables set ENVIRONMENT=production
railway variables set DEBUG=false
railway variables set LOG_LEVEL=INFO

# Deploy
echo "🚀 Deploying application..."
railway up

echo "✅ Deployment completed!"
echo "🌐 Your app should be available at: https://$(railway domain)"
