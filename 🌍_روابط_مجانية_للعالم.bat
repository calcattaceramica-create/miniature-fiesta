@echo off
chcp 65001 >nul
color 0A
title 🌍 روابط مجانية للوصول من أي مكان في العالم

:menu
cls
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo                    🌍 روابط مجانية للوصول من العالم
echo                    Free Links for Global Access
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo.
echo   ┌─────────────────────────────────────────────────────────────────────────┐
echo   │                                                                         │
echo   │  1️⃣  ngrok - سهل وسريع (يحتاج تحميل)                                  │
echo   │     ✅ رابط HTTPS آمن                                                   │
echo   │     ⚠️  محدود: 8 ساعات                                                 │
echo   │                                                                         │
echo   │  2️⃣  LocalTunnel - مجاني تماماً (الأفضل!)                             │
echo   │     ✅ بدون حدود                                                        │
echo   │     ✅ رابط ثابت                                                        │
echo   │     ✅ لا يحتاج تسجيل                                                   │
echo   │                                                                         │
echo   │  3️⃣  Cloudflare Tunnel - احترافي ومجاني                               │
echo   │     ✅ سريع جداً                                                        │
echo   │     ✅ آمن جداً                                                         │
echo   │     ✅ بدون حدود                                                        │
echo   │                                                                         │
echo   │  4️⃣  Serveo - بدون تحميل (SSH)                                         │
echo   │     ✅ لا يحتاج تحميل                                                   │
echo   │     ✅ مجاني تماماً                                                     │
echo   │                                                                         │
echo   │  5️⃣  دليل المقارنة والشرح                                             │
echo   │                                                                         │
echo   │  0️⃣  خروج                                                              │
echo   │                                                                         │
echo   └─────────────────────────────────────────────────────────────────────────┘
echo.
echo.
set /p choice="   اختر رقم الخيار (1-5): "

if "%choice%"=="1" goto ngrok
if "%choice%"=="2" goto localtunnel
if "%choice%"=="3" goto cloudflare
if "%choice%"=="4" goto serveo
if "%choice%"=="5" goto guide
if "%choice%"=="0" exit
goto menu

:ngrok
cls
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo                    🔵 ngrok - سهل وسريع
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo   📋 الخطوات:
echo   ────────────────────────────────────────
echo   1. حمّل ngrok من: https://ngrok.com/download
echo   2. فك الضغط وضع ngrok.exe في هذا المجلد
echo   3. اضغط Enter للمتابعة
echo.
pause
echo.
echo   🚀 جاري تشغيل السيرفر...
echo.
start "DED Server" cmd /k "color 0A && python app.py"
timeout /t 3 /nobreak >nul
echo.
echo   🌍 جاري فتح النفق للعالم...
echo.
start "ngrok Tunnel" cmd /k "color 0E && ngrok http 5000"
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo   ✅ تم!
echo   ────────────────────────────────────────
echo   📱 انسخ الرابط من نافذة ngrok (الصفراء)
echo   🔍 ابحث عن: Forwarding
echo   📋 مثال: https://abc123.ngrok.io
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
pause
goto menu

:localtunnel
cls
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo                    🟢 LocalTunnel - مجاني تماماً (الأفضل!)
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo   📋 التثبيت (مرة واحدة فقط):
echo   ────────────────────────────────────────
echo   جاري التحقق من Node.js...
echo.
where node >nul 2>&1
if errorlevel 1 (
    echo   ❌ Node.js غير مثبت!
    echo.
    echo   📥 يرجى تحميل Node.js من:
    echo   https://nodejs.org/
    echo.
    echo   ثم أعد تشغيل هذا الملف
    pause
    goto menu
)
echo   ✅ Node.js مثبت
echo.
echo   جاري تثبيت LocalTunnel...
call npm install -g localtunnel
echo.
echo   🚀 جاري تشغيل السيرفر...
echo.
start "DED Server" cmd /k "color 0A && python app.py"
timeout /t 3 /nobreak >nul
echo.
echo   🌍 جاري فتح النفق للعالم...
echo.
echo   💡 يمكنك اختيار اسم مخصص للرابط!
echo.
set /p subdomain="   أدخل اسم الرابط (اتركه فارغاً للعشوائي): "
echo.
if "%subdomain%"=="" (
    start "LocalTunnel" cmd /k "color 0B && lt --port 5000"
) else (
    start "LocalTunnel" cmd /k "color 0B && lt --port 5000 --subdomain %subdomain%"
)
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo   ✅ تم!
echo   ────────────────────────────────────────
echo   📱 الرابط سيظهر في النافذة الزرقاء
echo   📋 مثال: https://%subdomain%.loca.lt
echo   🔒 قد يطلب منك كلمة مرور عند أول زيارة (اضغط Click to Continue)
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
pause
goto menu

:cloudflare
cls
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo                    🟠 Cloudflare Tunnel - احترافي ومجاني
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo   📋 الخطوات:
echo   ────────────────────────────────────────
echo   1. حمّل cloudflared من:
echo      https://github.com/cloudflare/cloudflared/releases
echo   2. اختر: cloudflared-windows-amd64.exe
echo   3. أعد تسميته إلى: cloudflared.exe
echo   4. ضعه في هذا المجلد
echo   5. اضغط Enter للمتابعة
echo.
pause
echo.
echo   🚀 جاري تشغيل السيرفر...
echo.
start "DED Server" cmd /k "color 0A && python app.py"
timeout /t 3 /nobreak >nul
echo.
echo   🌍 جاري فتح النفق للعالم...
echo.
start "Cloudflare Tunnel" cmd /k "color 0D && cloudflared tunnel --url http://localhost:5000"
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo   ✅ تم!
echo   ────────────────────────────────────────
echo   📱 انسخ الرابط من النافذة البنفسجية
echo   🔍 ابحث عن: https://
echo   📋 مثال: https://abc-def-ghi.trycloudflare.com
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
pause
goto menu

:serveo
cls
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo                    🔴 Serveo - بدون تحميل (SSH)
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo   ⚠️ هذه الطريقة تحتاج SSH Client
echo   Windows 10/11 يحتوي على SSH مدمج
echo.
echo   🚀 جاري تشغيل السيرفر...
echo.
start "DED Server" cmd /k "color 0A && python app.py"
timeout /t 3 /nobreak >nul
echo.
echo   🌍 جاري فتح النفق للعالم...
echo.
start "Serveo Tunnel" cmd /k "color 0C && ssh -R 80:localhost:5000 serveo.net"
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo   ✅ تم!
echo   ────────────────────────────────────────
echo   📱 الرابط سيظهر في النافذة الحمراء
echo   📋 مثال: https://abc123.serveo.net
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
pause
goto menu

:guide
start "" "🌍_مقارنة_الروابط_المجانية.html"
goto menu

