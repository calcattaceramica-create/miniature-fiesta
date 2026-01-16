@echo off
chcp 65001 >nul
color 0B
title DED ERP - Internet Access (ngrok)

cls
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo                    🌍 تشغيل النظام للوصول من الإنترنت
echo                    Run System for Internet Access
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo.
echo  🌐 الوصول من أي مكان في العالم
echo     Access from Anywhere in the World
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

REM Check if ngrok exists
if not exist "ngrok.exe" (
    echo  ❌ خطأ: ngrok.exe غير موجود!
    echo     Error: ngrok.exe not found!
    echo.
    echo ═══════════════════════════════════════════════════════════════════════════════
    echo.
    echo  📥 يرجى تحميل ngrok من:
    echo     Please download ngrok from:
    echo.
    echo     https://ngrok.com/download
    echo.
    echo ═══════════════════════════════════════════════════════════════════════════════
    echo.
    echo  📁 ضع ngrok.exe في المجلد:
    echo     Put ngrok.exe in the folder:
    echo.
    echo     %CD%
    echo.
    echo ═══════════════════════════════════════════════════════════════════════════════
    echo.
    echo  📋 الخطوات:
    echo.
    echo  1️⃣  اذهب إلى: https://ngrok.com/download
    echo  2️⃣  حمّل النسخة لـ Windows
    echo  3️⃣  فك الضغط عن الملف
    echo  4️⃣  ضع ngrok.exe في المجلد أعلاه
    echo  5️⃣  شغّل هذا الملف مرة أخرى
    echo.
    echo ═══════════════════════════════════════════════════════════════════════════════
    echo.
    pause
    exit
)

echo  ✅ ngrok موجود - ngrok found
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo  🚀 جاري تشغيل السيرفر - Starting Server...
echo.

REM Start Flask in background
start /B python run.py

echo  ⏳ انتظر 10 ثوانٍ حتى يبدأ السيرفر...
echo     Wait 10 seconds for server to start...
echo.
timeout /t 10 /nobreak >nul

echo  ✅ السيرفر يعمل - Server is running
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo  🌍 جاري تشغيل ngrok - Starting ngrok...
echo.
echo  📋 ستفتح نافذة جديدة مع الرابط العام
echo     A new window will open with the public URL
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

REM Start ngrok in a new window
start "ngrok - Public URL" cmd /k "color 0E && echo ════════════════════════════════════════════════════════════ && echo. && echo    🌍 انسخ الرابط من هنا - Copy the link from here && echo. && echo ════════════════════════════════════════════════════════════ && echo. && ngrok http 5000 && echo. && echo ════════════════════════════════════════════════════════════ && echo    الرابط أعلاه - Link above && echo ════════════════════════════════════════════════════════════"

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo  ✅ تم! - Done!
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo  📋 الخطوات التالية - Next Steps:
echo.
echo  1️⃣  انظر إلى نافذة ngrok (الصفراء)
echo     Look at the ngrok window (yellow)
echo.
echo  2️⃣  ابحث عن السطر الذي يبدأ بـ "Forwarding"
echo     Find the line starting with "Forwarding"
echo.
echo  3️⃣  انسخ الرابط الذي يبدأ بـ https://
echo     Copy the link starting with https://
echo.
echo  4️⃣  افتحه على الهاتف أو أي جهاز!
echo     Open it on your phone or any device!
echo.
echo  مثال - Example:
echo     https://abc123.ngrok.io
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo  ⚠️  مهم - Important:
echo.
echo  ✅ لا تغلق هذه النافذة!
echo     Don't close this window!
echo.
echo  ✅ لا تغلق نافذة ngrok!
echo     Don't close ngrok window!
echo.
echo  ✅ الرابط يعمل طالما النافذتان مفتوحتان
echo     Link works while both windows are open
echo.
echo  ✅ لإيقاف النظام: اضغط CTRL+C في كلا النافذتين
echo     To stop: Press CTRL+C in both windows
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo  📱 استخدم الرابط من:
echo     Use the link from:
echo.
echo  ✅ الهاتف - Phone
echo  ✅ التابلت - Tablet
echo  ✅ أي كمبيوتر - Any Computer
echo  ✅ من أي مكان في العالم! - From Anywhere in the World!
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
pause

