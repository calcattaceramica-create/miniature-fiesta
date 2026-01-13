@echo off
chcp 65001 >nul
title 🚀 DED Control Panel Launcher

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║        🚀 DED Control Panel - لوحة التحكم الشاملة           ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 📋 جاري التحقق من المتطلبات...
echo    Checking requirements...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ خطأ: Python غير مثبت!
    echo    Error: Python is not installed!
    echo.
    echo 💡 الرجاء تثبيت Python من: https://www.python.org/downloads/
    echo    Please install Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python مثبت
echo    Python is installed
echo.

REM Check if DED_Control_Panel.pyw exists
if not exist "DED_Control_Panel.pyw" (
    echo ❌ خطأ: ملف DED_Control_Panel.pyw غير موجود!
    echo    Error: DED_Control_Panel.pyw file not found!
    pause
    exit /b 1
)

echo ✅ ملف لوحة التحكم موجود
echo    Control panel file found
echo.

echo 🚀 جاري تشغيل لوحة التحكم...
echo    Launching control panel...
echo.

REM Run the control panel
pythonw DED_Control_Panel.pyw

if errorlevel 1 (
    echo.
    echo ❌ حدث خطأ أثناء التشغيل!
    echo    An error occurred during execution!
    echo.
    echo 💡 جرب التشغيل بهذا الأمر لرؤية الأخطاء:
    echo    Try running with this command to see errors:
    echo    python DED_Control_Panel.pyw
    pause
    exit /b 1
)

echo.
echo ✅ تم تشغيل لوحة التحكم بنجاح!
echo    Control panel launched successfully!
echo.
echo 📝 ملاحظة: يمكنك إغلاق هذه النافذة الآن
echo    Note: You can close this window now
echo.

timeout /t 3 >nul
exit /b 0

