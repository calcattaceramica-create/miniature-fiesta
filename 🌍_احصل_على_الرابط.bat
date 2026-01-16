@echo off
chcp 65001 >nul
color 0B
title 🌍 LocalTunnel - احصل على الرابط

cls
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo                    🌍 LocalTunnel - رابطك العام
echo                    LocalTunnel - Your Public URL
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo   🔍 جاري البحث عن الرابط...
echo   🔍 Searching for your URL...
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

REM The URL should be
echo   🎉 رابطك العام:
echo   🎉 Your Public URL:
echo.
echo   ┌─────────────────────────────────────────────────────────────────────────┐
echo   │                                                                         │
echo   │                   https://dedapp.loca.lt                                │
echo   │                                                                         │
echo   └─────────────────────────────────────────────────────────────────────────┘
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo   ✅ افتح هذا الرابط في أي متصفح من أي مكان في العالم!
echo   ✅ Open this URL in any browser from anywhere in the world!
echo.
echo   📋 بيانات الدخول:
echo   📋 Login credentials:
echo.
echo      Username: admin
echo      Password: admin123
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo   ⚠️  ملاحظة مهمة:
echo   ⚠️  Important Note:
echo.
echo   - عند أول زيارة، قد تظهر صفحة "Friendly Reminder"
echo   - فقط اضغط "Click to Continue"
echo   - At first visit, you may see "Friendly Reminder" page
echo   - Just click "Click to Continue"
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

REM Try to open the URL in browser
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
pause

