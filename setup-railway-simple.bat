@echo off
echo 🚂 Railway Setup - Simple Version
echo.

echo ✅ Project created: subscription-tracker
echo.

echo 📋 Next steps:
echo 1. Go to https://railway.app/dashboard
echo 2. Find your project 'subscription-tracker'
echo 3. Click on it
echo 4. Click 'Add Service' or 'New Service'
echo 5. Choose 'Database' and select PostgreSQL
echo 6. Wait for database to be created
echo 7. Copy the DATABASE_URL from the database service
echo.

echo 🔧 After adding database, run these commands:
echo railway variables set DATABASE_URL=your-database-url
echo railway variables set SECRET_KEY=your-secret-key
echo railway variables set JWT_SECRET_KEY=your-jwt-secret
echo railway up
echo.

echo 🌐 Your project dashboard:
echo https://railway.app/dashboard
echo.

pause
