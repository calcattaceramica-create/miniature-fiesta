@echo off
chcp 65001 >nul
color 0A
cls

echo ╔════════════════════════════════════════════════════════════╗
echo ║          🚀 DED Control Panel - Web Version 🚀            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 📱 للوصول من الهاتف - Access from Phone:
echo.
echo 1️⃣  تأكد أن الهاتف والكمبيوتر على نفس الواي فاي
echo    Make sure phone and PC are on same WiFi
echo.
echo 2️⃣  انتظر حتى يظهر Network URL
echo    Wait for Network URL to appear
echo.
echo 3️⃣  افتح Network URL على الهاتف
echo    Open Network URL on your phone
echo.
echo ════════════════════════════════════════════════════════════
echo.
echo 🌐 عنوان IP الخاص بك - Your IP Address:
echo.
ipconfig | findstr /i "IPv4"
echo.
echo ════════════════════════════════════════════════════════════
echo.
echo 🚀 جاري تشغيل التطبيق - Starting Application...
echo.
echo ⚠️  لا تغلق هذه النافذة! - Don't close this window!
echo.
echo ════════════════════════════════════════════════════════════
echo.

python -m streamlit run DED_Control_Panel_Web.py

pause

