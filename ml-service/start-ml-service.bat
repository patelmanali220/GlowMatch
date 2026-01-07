@echo off
echo ========================================
echo  GlowMatch ML Service Launcher
echo ========================================
echo.
echo Starting ML Service on port 8001...
echo Keep this window open to keep the service running!
echo.
echo Press Ctrl+C to stop the service
echo ========================================
echo.

cd /d "%~dp0"
python app/main.py

echo.
echo ========================================
echo ML Service has stopped
echo ========================================
pause
