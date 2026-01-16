@echo off
chcp 65001 >nul
color 0B
cls

echo ╔════════════════════════════════════════════════════════════╗
echo ║       🌍 DED Control Panel - Online Access 🌍             ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo 📋 التعليمات - Instructions:
echo.
echo 1️⃣  سيتم فتح نافذتين - Two windows will open:
echo    - النافذة الأولى: Streamlit (التطبيق)
echo    - النافذة الثانية: ngrok (الرابط العام)
echo.
echo 2️⃣  انسخ الرابط من نافذة ngrok
echo    Copy the link from ngrok window
echo.
echo 3️⃣  استخدم الرابط من أي مكان في العالم!
echo    Use the link from anywhere in the world!
echo.
echo ════════════════════════════════════════════════════════════
echo.

REM Check if ngrok exists
if not exist "ngrok.exe" (
    echo ❌ خطأ: ngrok.exe غير موجود!
    echo    Error: ngrok.exe not found!
    echo.
    echo 📥 يرجى تحميل ngrok من:
    echo    Please download ngrok from:
    echo    https://ngrok.com/download
    echo.
    echo 📁 ضع ngrok.exe في نفس المجلد:
    echo    Put ngrok.exe in the same folder:
    echo    C:\Users\DELL\DED
    echo.
    pause
    exit
)

echo ✅ ngrok موجود - ngrok found
echo.
echo 🚀 جاري تشغيل التطبيق - Starting application...
echo.

REM Start Streamlit in a new window
start "Streamlit - DED Control Panel" cmd /k "color 0A && python -m streamlit run DED_Control_Panel_Web.py"

echo ⏳ انتظر 5 ثوانٍ... - Wait 5 seconds...
timeout /t 5 /nobreak >nul

echo.
echo 🌍 جاري تشغيل ngrok - Starting ngrok...
echo.

REM Start ngrok in a new window
start "ngrok - Public URL" cmd /k "color 0E && echo ════════════════════════════════════════════════════════════ && echo    🌍 انسخ الرابط من هنا - Copy the link from here && echo ════════════════════════════════════════════════════════════ && echo. && ngrok http 8501"

echo.
echo ✅ تم! - Done!
echo.
echo 📋 الخطوات التالية - Next steps:
echo.
echo 1️⃣  انظر إلى نافذة ngrok (الصفراء)
echo    Look at the ngrok window (yellow)
echo.
echo 2️⃣  انسخ الرابط الذي يبدأ بـ https://
echo    Copy the link that starts with https://
echo.
echo 3️⃣  افتحه على الهاتف أو أي جهاز!
echo    Open it on your phone or any device!
echo.
echo ⚠️  لا تغلق النافذتين! - Don't close the windows!
echo.
pause

