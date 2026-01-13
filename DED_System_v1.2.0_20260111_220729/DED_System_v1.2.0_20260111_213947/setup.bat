@echo off
chcp 65001 >nul
echo ========================================
echo    نظام إدارة الموارد البشرية و CRM
echo    DED HR ^& CRM System Setup
echo ========================================
echo.

echo [1/6] التحقق من Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ خطأ: Python غير مثبت!
    echo يرجى تثبيت Python 3.8 أو أحدث من: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python مثبت

echo.
echo [2/6] إنشاء البيئة الافتراضية...
if exist venv (
    echo ⚠️  البيئة الافتراضية موجودة بالفعل
) else (
    python -m venv venv
    echo ✅ تم إنشاء البيئة الافتراضية
)

echo.
echo [3/6] تفعيل البيئة الافتراضية...
call venv\Scripts\activate
echo ✅ تم تفعيل البيئة الافتراضية

echo.
echo [4/6] تثبيت المتطلبات...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ خطأ في تثبيت المتطلبات!
    pause
    exit /b 1
)
echo ✅ تم تثبيت المتطلبات

echo.
echo [5/6] إنشاء قاعدة البيانات...
if exist instance\erp_system.db (
    echo ⚠️  قاعدة البيانات موجودة بالفعل
    set /p recreate="هل تريد إعادة إنشاء قاعدة البيانات؟ (y/n): "
    if /i "%recreate%"=="y" (
        del instance\erp_system.db
        python init_db.py
        echo ✅ تم إعادة إنشاء قاعدة البيانات
    )
) else (
    python init_db.py
    echo ✅ تم إنشاء قاعدة البيانات
)

echo.
echo [6/6] إنشاء البيانات التجريبية...
set /p seed="هل تريد إنشاء بيانات تجريبية؟ (y/n): "
if /i "%seed%"=="y" (
    python seed_data.py
    python seed_crm_data.py
    echo ✅ تم إنشاء البيانات التجريبية
)

echo.
echo ========================================
echo ✅ تم الإعداد بنجاح!
echo ========================================
echo.
echo لتشغيل التطبيق:
echo   1. افتح Terminal جديد
echo   2. نفذ: venv\Scripts\activate
echo   3. نفذ: python run.py
echo   4. افتح المتصفح على: http://127.0.0.1:5000
echo.
echo بيانات الدخول الافتراضية:
echo   اسم المستخدم: admin
echo   كلمة المرور: admin123
echo.
echo ========================================
pause

