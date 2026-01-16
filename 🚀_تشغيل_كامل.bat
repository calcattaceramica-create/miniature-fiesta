@echo off
chcp 65001 >nul
color 0A
title 🚀 تشغيل السيرفر و LocalTunnel

cls
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo                    🚀 تشغيل النظام الكامل
echo                    Starting Complete System
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo   📋 سيتم تشغيل:
echo   📋 Will start:
echo.
echo   1️⃣ السيرفر المحلي (Flask Server)
echo   2️⃣ LocalTunnel (Public URL)
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

REM Start Flask Server in a new window
echo   🔄 جاري تشغيل السيرفر المحلي...
echo   🔄 Starting Flask Server...
start "🟢 Flask Server - لا تغلق هذه النافذة" /min cmd /c "color 0A && title 🟢 Flask Server && python start_server_simple.py"

REM Wait for server to start
echo.
echo   ⏳ انتظار 5 ثواني حتى يبدأ السيرفر...
echo   ⏳ Waiting 5 seconds for server to start...
timeout /t 5 /nobreak >nul

REM Start LocalTunnel in a new window
echo.
echo   🔄 جاري تشغيل LocalTunnel...
echo   🔄 Starting LocalTunnel...
start "🔵 LocalTunnel - لا تغلق هذه النافذة" cmd /c "color 0B && title 🔵 LocalTunnel && lt --port 5000 --subdomain dedapp && pause"

REM Wait for LocalTunnel to start
echo.
echo   ⏳ انتظار 8 ثواني حتى يبدأ LocalTunnel...
echo   ⏳ Waiting 8 seconds for LocalTunnel to start...
timeout /t 8 /nobreak >nul

cls
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo                    ✅ النظام يعمل الآن!
echo                    System is Running!
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo   ✅ السيرفر المحلي يعمل
echo   ✅ Flask Server is running
echo.
echo   ✅ LocalTunnel يعمل
echo   ✅ LocalTunnel is running
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo   🌍 رابطك العام:
echo   🌍 Your Public URL:
echo.
echo   ┌─────────────────────────────────────────────────────────────────────────┐
echo   │                                                                         │
echo   │                   https://dedapp.loca.lt                                │
echo   │                                                                         │
echo   └─────────────────────────────────────────────────────────────────────────┘
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo   🔑 كلمة مرور LocalTunnel:
echo   🔑 LocalTunnel Password:
echo.
echo   ┌─────────────────────────────────────────────────────────────────────────┐
echo   │                                                                         │
echo   │                         185.5.48.115                                    │
echo   │                                                                         │
echo   └─────────────────────────────────────────────────────────────────────────┘
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo   📋 بيانات تسجيل الدخول:
echo   📋 Login Credentials:
echo.
echo      Username: admin
echo      Password: admin123
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo   💡 هل تريد فتح الرابط في المتصفح؟ (y/n)
echo   💡 Do you want to open the URL in browser? (y/n)
echo.
set /p OPEN_BROWSER="   اختيارك / Your choice: "

if /i "%OPEN_BROWSER%"=="y" (
    echo.
    echo   🌐 جاري فتح المتصفح...
    echo   🌐 Opening browser...
    start https://dedapp.loca.lt
    echo.
    echo   ✅ تم فتح المتصفح!
    echo   ✅ Browser opened!
)

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo   ⚠️  ملاحظة مهمة جداً:
echo   ⚠️  Very Important Note:
echo.
echo   - لا تغلق النافذة الخضراء (Flask Server)
echo   - لا تغلق النافذة الزرقاء (LocalTunnel)
echo   - إذا أغلقت أي منهما، الرابط لن يعمل!
echo.
echo   - Don't close the green window (Flask Server)
echo   - Don't close the blue window (LocalTunnel)
echo   - If you close any of them, the URL won't work!
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
pause

