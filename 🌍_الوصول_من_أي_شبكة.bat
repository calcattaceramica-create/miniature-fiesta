@echo off
chcp 65001 >nul
color 0B
title DED ERP - الوصول من أي شبكة

cls
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo                    🌍 الوصول من أي شبكة وأي جهاز
echo                    Access from Any Network and Device
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo.
echo  اختر طريقة الوصول - Choose Access Method:
echo.
echo  ┌─────────────────────────────────────────────────────────────────────────┐
echo  │                                                                         │
echo  │  1️⃣  الوصول من نفس الشبكة (WiFi)                                       │
echo  │     Access from Same Network (WiFi)                                    │
echo  │     📱 للهاتف والأجهزة على نفس الواي فاي                               │
echo  │                                                                         │
echo  │  2️⃣  الوصول من الإنترنت (ngrok)                                        │
echo  │     Access from Internet (ngrok)                                       │
echo  │     🌍 من أي مكان في العالم                                            │
echo  │                                                                         │
echo  │  3️⃣  عرض عنوان IP الخاص بك                                            │
echo  │     Show Your IP Address                                               │
echo  │                                                                         │
echo  │  4️⃣  دليل الاستخدام التفصيلي                                           │
echo  │     Detailed User Guide                                                │
echo  │                                                                         │
echo  │  0️⃣  خروج - Exit                                                       │
echo  │                                                                         │
echo  └─────────────────────────────────────────────────────────────────────────┘
echo.
echo.

set /p choice="  اختر رقم (1-4): "

if "%choice%"=="1" goto network
if "%choice%"=="2" goto ngrok
if "%choice%"=="3" goto showip
if "%choice%"=="4" goto guide
if "%choice%"=="0" exit
goto menu

:network
cls
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo                    📱 الوصول من نفس الشبكة
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo  🌐 عنوان IP الخاص بك:
echo.
ipconfig | findstr /i "IPv4"
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo  📋 الخطوات:
echo.
echo  1️⃣  تأكد أن الهاتف والكمبيوتر على نفس الواي فاي
echo  2️⃣  شغّل السيرفر الآن
echo  3️⃣  افتح من الهاتف: http://عنوان_IP:5000
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo  🚀 جاري تشغيل السيرفر...
echo.

python -c "import socket; print('  ✅ عنوان IP:', socket.gethostbyname(socket.gethostname()))"
echo.
echo  📱 افتح من الهاتف:
python -c "import socket; print('     http://' + socket.gethostbyname(socket.gethostname()) + ':5000')"
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

python run.py --host=0.0.0.0 --port=5000

pause
exit

:ngrok
cls
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo                    🌍 الوصول من الإنترنت (ngrok)
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

REM Check if ngrok exists
if not exist "ngrok.exe" (
    echo  ❌ ngrok غير موجود!
    echo.
    echo  📥 يرجى تحميل ngrok من:
    echo     https://ngrok.com/download
    echo.
    echo  📁 ضع ngrok.exe في المجلد:
    echo     %CD%
    echo.
    pause
    goto menu
)

echo  ✅ ngrok موجود
echo.
echo  🚀 جاري تشغيل السيرفر...
echo.

REM Start Flask in background
start /B python run.py --host=0.0.0.0 --port=5000

echo  ⏳ انتظر 5 ثوانٍ...
timeout /t 5 /nobreak >nul

echo.
echo  🌍 جاري تشغيل ngrok...
echo.

REM Start ngrok
start "ngrok - Public URL" cmd /k "color 0E && echo ════════════════════════════════════════════════════════════ && echo    🌍 انسخ الرابط من هنا - Copy the link from here && echo ════════════════════════════════════════════════════════════ && echo. && ngrok http 5000"

echo.
echo  ✅ تم!
echo.
echo  📋 انظر إلى نافذة ngrok وانسخ الرابط
echo.
pause
exit

:showip
cls
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo                    🌐 عنوان IP الخاص بك
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
ipconfig
echo.
pause
goto menu

:guide
start "" "🌍_دليل_الوصول_من_أي_شبكة.html"
goto menu

