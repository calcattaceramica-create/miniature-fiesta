@echo off
chcp 65001 >nul
color 0A
title 🎯 تشغيل سريع - DED ERP

cls
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo                    🎯 تشغيل سريع - DED ERP System
echo                    Quick Start - DED ERP System
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo   📡 تشغيل السيرفر المحلي...
echo   📡 Starting Flask Server...
echo.

REM Start Flask Server in new window
start "🟢 Flask Server - DO NOT CLOSE" python run.py

echo   ✅ السيرفر بدأ في نافذة جديدة
echo   ✅ Server started in new window
echo.
echo   ⏳ انتظار 10 ثواني حتى يبدأ السيرفر...
echo   ⏳ Waiting 10 seconds for server to start...
timeout /t 10 >nul

echo.
echo   🌍 تشغيل LocalTunnel...
echo   🌍 Starting LocalTunnel...
echo.

REM Start LocalTunnel in new window
start "🔵 LocalTunnel - DO NOT CLOSE" lt --port 5000 --subdomain dedapp

echo   ✅ LocalTunnel بدأ في نافذة جديدة
echo   ✅ LocalTunnel started in new window
echo.
echo   ⏳ انتظار 10 ثواني حتى يتصل LocalTunnel...
echo   ⏳ Waiting 10 seconds for LocalTunnel to connect...
timeout /t 10 >nul

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo                    ✅ النظام جاهز!
echo                    ✅ System Ready!
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo   🔗 رابطك العام:
echo   🔗 Your Public URL:
echo.
echo      https://dedapp.loca.lt
echo.
echo   🔑 كلمة مرور LocalTunnel (أول زيارة فقط):
echo   🔑 LocalTunnel Password (first visit only):
echo.
echo      185.5.48.115
echo.
echo   📋 تسجيل الدخول:
echo   📋 Login Credentials:
echo.
echo      Username: admin
echo      Password: admin123
echo.
echo   ⚠️  ملاحظات مهمة:
echo   ⚠️  Important Notes:
echo.
echo      - نافذتان مفتوحتان (Flask Server + LocalTunnel)
echo      - Two windows are open (Flask Server + LocalTunnel)
echo.
echo      - لا تغلق أي منهما!
echo      - DO NOT close either of them!
echo.
echo      - انتظر 5 ثواني إضافية قبل فتح الرابط
echo      - Wait 5 more seconds before opening the URL
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

REM Open success page
start "" "✅_النظام_جاهز.html"

echo   🎉 تم فتح صفحة النجاح في المتصفح!
echo   🎉 Success page opened in browser!
echo.
echo   يمكنك إغلاق هذه النافذة الآن
echo   You can close this window now
echo.
pause

