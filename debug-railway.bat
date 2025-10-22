@echo off
echo 🔍 Railway Debug Information
echo.

echo 📁 Current directory contents:
dir

echo.
echo 📄 Dockerfile content:
type Dockerfile

echo.
echo 📄 Procfile content:
type Procfile

echo.
echo 🔧 Railway status:
railway status

echo.
echo 🌐 Railway domain:
railway domain

echo.
echo 📋 Railway variables:
railway variables

echo.
echo 🔍 Railway logs:
railway logs

echo.
echo ✅ Debug complete!
pause
