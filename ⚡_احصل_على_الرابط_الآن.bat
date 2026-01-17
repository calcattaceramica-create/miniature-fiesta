@echo off
chcp 65001 >nul
color 0A
title 🚀 احصل على الرابط الآن!

echo.
echo ═══════════════════════════════════════════════════════════
echo            🚀 احصل على الرابط الآن!
echo ═══════════════════════════════════════════════════════════
echo.
echo ⚡ جاري تشغيل النظام...
echo.

:: تشغيل السيرفر
start "DED Server" cmd /k "python run.py"

:: انتظار 5 ثواني
timeout /t 5 /nobreak >nul

:: تشغيل LocalTunnel
echo.
echo 🌍 جاري إنشاء الرابط العام...
echo.
start "LocalTunnel" cmd /k "npx localtunnel --port 5000 --subdomain dedapp"

:: انتظار 3 ثواني
timeout /t 3 /nobreak >nul

:: عرض الرابط
cls
echo.
echo ═══════════════════════════════════════════════════════════
echo            ✅ تم! الرابط جاهز!
echo ═══════════════════════════════════════════════════════════
echo.
echo 🌍 الرابط العام:
echo.
echo    👉 https://dedapp.loca.lt
echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo 📋 بيانات الدخول:
echo.
echo    Username: admin
echo    Password: admin123
echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo ⚠️ ملاحظات مهمة:
echo.
echo    1. لا تغلق هذه النافذة!
echo    2. لا تغلق النوافذ الأخرى!
echo    3. الرابط يعمل طالما الكمبيوتر مفتوح
echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo 🎉 استمتع بالنظام!
echo.
pause

