@echo off
chcp 65001 >nul
color 0A
title DED ERP - Network Access

cls
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo                    🌐 تشغيل النظام للوصول من الشبكة
echo                    Run System for Network Access
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo.
echo  📱 للوصول من الهاتف والأجهزة الأخرى
echo     Access from Phone and Other Devices
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo  🌐 عنوان IP الخاص بك - Your IP Address:
echo.

REM Get IP Address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do (
    set IP=%%a
    goto :found
)
:found
set IP=%IP: =%

echo     %IP%
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo  📱 افتح من الهاتف - Open from Phone:
echo.
echo     http://%IP%:5000
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo  📋 الخطوات - Steps:
echo.
echo  1️⃣  تأكد أن الهاتف والكمبيوتر على نفس الواي فاي
echo     Make sure phone and PC are on same WiFi
echo.
echo  2️⃣  افتح المتصفح على الهاتف
echo     Open browser on your phone
echo.
echo  3️⃣  اكتب الرابط أعلاه
echo     Type the URL above
echo.
echo  4️⃣  سجل الدخول: admin / admin123
echo     Login: admin / admin123
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo  ⚠️  مهم - Important:
echo.
echo  ✅ لا تغلق هذه النافذة!
echo     Don't close this window!
echo.
echo  ✅ النظام يعمل طالما النافذة مفتوحة
echo     System runs while window is open
echo.
echo  ✅ لإيقاف النظام: اضغط CTRL+C
echo     To stop: Press CTRL+C
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo  🚀 جاري تشغيل السيرفر - Starting Server...
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

REM Start Flask with network access
python run.py --host=0.0.0.0 --port=5000

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo  السيرفر توقف - Server Stopped
echo ═══════════════════════════════════════════════════════════════════════════════
pause

