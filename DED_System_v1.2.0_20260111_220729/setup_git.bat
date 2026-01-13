@echo off
chcp 65001 >nul
echo ============================================================
echo 🎯 تهيئة Git للمشروع
echo ============================================================
echo.

REM التحقق من وجود Git
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Git غير مثبت!
    echo.
    echo 📥 الرجاء تثبيت Git من:
    echo    https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo ✅ Git مثبت
echo.

REM التحقق من وجود .git
if exist .git (
    echo ⚠️ المشروع مهيأ بالفعل لـ Git
    echo.
    choice /C YN /M "هل تريد إعادة التهيئة؟ (سيتم حذف السجل الحالي)"
    if errorlevel 2 goto :skip_init
    if errorlevel 1 (
        echo.
        echo 🗑️ حذف .git القديم...
        rmdir /s /q .git
    )
)

echo.
echo 📝 تهيئة Git...
git init
if %ERRORLEVEL% NEQ 0 (
    echo ❌ فشل في تهيئة Git
    pause
    exit /b 1
)

:skip_init

echo.
echo ✅ تم تهيئة Git بنجاح
echo.

REM إضافة جميع الملفات
echo 📦 إضافة الملفات...
git add .
if %ERRORLEVEL% NEQ 0 (
    echo ❌ فشل في إضافة الملفات
    pause
    exit /b 1
)

echo.
echo ✅ تمت إضافة الملفات
echo.

REM عمل Commit
echo 💾 إنشاء Commit...
git commit -m "DED HR & CRM System v1.2.0 - Complete Export"
if %ERRORLEVEL% NEQ 0 (
    echo ⚠️ تحذير: قد يكون هناك مشكلة في الـ Commit
    echo    (ربما لا توجد تغييرات جديدة)
)

echo.
echo ============================================================
echo ✅ تم تهيئة Git بنجاح!
echo ============================================================
echo.
echo 📋 الخطوات التالية:
echo.
echo 1️⃣ أنشئ مستودع جديد على GitHub:
echo    https://github.com/new
echo.
echo 2️⃣ انسخ رابط المستودع (مثال):
echo    https://github.com/username/ded-system.git
echo.
echo 3️⃣ نفذ الأوامر التالية (استبدل الرابط برابطك):
echo.
echo    git remote add origin https://github.com/username/ded-system.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo ============================================================
echo.
echo 💡 نصيحة: يمكنك استخدام GitHub Desktop لسهولة أكبر:
echo    https://desktop.github.com/
echo.
echo ============================================================
echo.

pause

