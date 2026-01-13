@echo off
chcp 65001 >nul
color 0B
title 🚀 DED Control Panel - لوحة التحكم الشاملة

:: ═══════════════════════════════════════════════════════════
::  🚀 DED Control Panel Launcher
::  لوحة التحكم الشاملة - مشغل متقدم
:: ═══════════════════════════════════════════════════════════

cls
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                                                          ║
echo ║        🚀 DED Control Panel - لوحة التحكم الشاملة        ║
echo ║                                                          ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo ═══════════════════════════════════════════════════════════
echo  📋 القائمة الرئيسية - Main Menu
echo ═══════════════════════════════════════════════════════════
echo.
echo  [1] 🚀 تشغيل لوحة التحكم
echo      Launch Control Panel
echo.
echo  [2] 🧪 إنشاء تراخيص تجريبية
echo      Create Test Licenses
echo.
echo  [3] 📊 عرض الإحصائيات
echo      Show Statistics
echo.
echo  [4] 📁 فتح مجلد المشروع
echo      Open Project Folder
echo.
echo  [5] 📝 عرض التوثيق
echo      View Documentation
echo.
echo  [6] 🌐 فتح معاينة HTML
echo      Open HTML Preview
echo.
echo  [7] 🔄 تحديث قاعدة البيانات
echo      Update Database
echo.
echo  [8] 🧹 تنظيف الملفات المؤقتة
echo      Clean Temp Files
echo.
echo  [9] ℹ️  معلومات النظام
echo      System Information
echo.
echo  [0] ❌ خروج
echo      Exit
echo.
echo ═══════════════════════════════════════════════════════════
echo.
set /p choice="اختر رقم الأمر - Choose option: "

if "%choice%"=="1" goto launch_panel
if "%choice%"=="2" goto create_test
if "%choice%"=="3" goto show_stats
if "%choice%"=="4" goto open_folder
if "%choice%"=="5" goto view_docs
if "%choice%"=="6" goto open_preview
if "%choice%"=="7" goto update_db
if "%choice%"=="8" goto clean_temp
if "%choice%"=="9" goto system_info
if "%choice%"=="0" goto exit
goto menu

:launch_panel
cls
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║  🚀 تشغيل لوحة التحكم - Launching Control Panel         ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo ⏳ جاري التشغيل...
echo.
cd /d "%~dp0"
start pythonw DED_Control_Panel.pyw
timeout /t 2 >nul
echo ✅ تم تشغيل لوحة التحكم بنجاح!
echo.
echo 💡 نصيحة: افتح تبويب "تشغيل التطبيق" لرؤية الميزات الجديدة
echo.
pause
goto menu

:create_test
cls
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║  🧪 إنشاء تراخيص تجريبية - Creating Test Licenses      ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
cd /d "%~dp0"
python test_license_ui.py
echo.
echo ✅ تم إنشاء التراخيص التجريبية!
echo.
echo 📋 التراخيص المنشأة:
echo    - ✅ ترخيص نشط (100 يوم)
echo    - ⏸️  ترخيص معلق (50 يوم)
echo    - ❌ ترخيص منتهي (-10 يوم)
echo    - ⚠️  ترخيص قريب الانتهاء (5 أيام)
echo.
set /p copy_choice="هل تريد نسخها لملف التراخيص الفعلي؟ (Y/N): "
if /i "%copy_choice%"=="Y" (
    copy /y licenses_test.json licenses.json >nul
    echo ✅ تم النسخ بنجاح!
)
echo.
pause
goto menu

:show_stats
cls
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║  📊 إحصائيات التراخيص - License Statistics             ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
cd /d "%~dp0"
python -c "import json; data=json.load(open('licenses.json')); total=len(data); active=sum(1 for l in data.values() if l.get('status')=='active'); suspended=sum(1 for l in data.values() if l.get('status')=='suspended'); print(f'\n📊 إجمالي التراخيص: {total}\n✅ نشطة: {active}\n⏸️  معلقة: {suspended}\n')"
echo.
pause
goto menu

:open_folder
cls
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║  📁 فتح مجلد المشروع - Opening Project Folder           ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
cd /d "%~dp0"
start explorer .
echo ✅ تم فتح المجلد!
timeout /t 2 >nul
goto menu

:view_docs
cls
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║  📝 التوثيق المتاح - Available Documentation            ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo  [1] 📘 دليل البدء السريع - QUICK_START_GUIDE.md
echo  [2] 📗 توثيق الميزات - LICENSE_UI_FEATURES.md
echo  [3] 📙 سجل التغييرات - VERSION_2.0_CHANGELOG.md
echo  [4] 📕 ملخص التسليم - DELIVERY_SUMMARY.md
echo  [5] 📄 تصميم الواجهة - UI_LAYOUT.txt
echo  [0] 🔙 رجوع
echo.
set /p doc_choice="اختر الملف: "
cd /d "%~dp0"
if "%doc_choice%"=="1" start notepad QUICK_START_GUIDE.md
if "%doc_choice%"=="2" start notepad LICENSE_UI_FEATURES.md
if "%doc_choice%"=="3" start notepad VERSION_2.0_CHANGELOG.md
if "%doc_choice%"=="4" start notepad DELIVERY_SUMMARY.md
if "%doc_choice%"=="5" start notepad UI_LAYOUT.txt
if "%doc_choice%"=="0" goto menu
timeout /t 1 >nul
goto view_docs

:open_preview
cls
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║  🌐 فتح معاينة HTML - Opening HTML Preview              ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
cd /d "%~dp0"
start demo_preview.html
echo ✅ تم فتح المعاينة في المتصفح!
timeout /t 2 >nul
goto menu

:update_db
cls
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║  🔄 تحديث قاعدة البيانات - Updating Database            ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo ⏳ جاري التحديث...
cd /d "%~dp0"
if exist licenses_test.json (
    copy /y licenses_test.json licenses.json >nul
    echo ✅ تم تحديث قاعدة البيانات من ملف الاختبار!
) else (
    echo ⚠️  ملف الاختبار غير موجود!
)
echo.
pause
goto menu

:clean_temp
cls
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║  🧹 تنظيف الملفات المؤقتة - Cleaning Temp Files         ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
cd /d "%~dp0"
echo ⏳ جاري التنظيف...
if exist __pycache__ (
    rd /s /q __pycache__
    echo ✅ تم حذف __pycache__
)
if exist *.pyc (
    del /q *.pyc
    echo ✅ تم حذف ملفات .pyc
)
echo.
echo ✅ اكتمل التنظيف!
pause
goto menu

:system_info
cls
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║  ℹ️  معلومات النظام - System Information                ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo 📦 اسم المشروع: DED Control Panel
echo 📌 الإصدار: 2.0.0
echo 📅 التاريخ: 2026-01-12
echo 👨‍💻 المطور: DED Team + Augment AI
echo.
echo 📊 الملفات الرئيسية:
cd /d "%~dp0"
if exist DED_Control_Panel.pyw echo    ✅ DED_Control_Panel.pyw
if exist licenses.json echo    ✅ licenses.json
if exist test_license_ui.py echo    ✅ test_license_ui.py
if exist demo_preview.html echo    ✅ demo_preview.html
echo.
echo 🐍 إصدار Python:
python --version
echo.
pause
goto menu

:exit
cls
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                                                          ║
echo ║              👋 شكراً لاستخدامك DED Panel               ║
echo ║              Thank you for using DED Panel              ║
echo ║                                                          ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
timeout /t 2 >nul
exit

