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
echo [4/6] ترقية pip...
python -m pip install --upgrade pip
echo ✅ تم ترقية pip

echo.
echo [5/6] تثبيت المتطلبات...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ خطأ في تثبيت المتطلبات!
    pause
    exit /b 1
)
echo ✅ تم تثبيت المتطلبات

echo.
echo [6/6] إنشاء قاعدة البيانات...
if exist erp_system.db (
    echo ⚠️  قاعدة البيانات موجودة بالفعل
    set /p recreate="هل تريد إعادة إنشاء قاعدة البيانات؟ (y/n): "
    if /i "%recreate%"=="y" (
        del erp_system.db
        flask --app run init-db
        echo ✅ تم إعادة إنشاء قاعدة البيانات
    )
) else (
    echo إنشاء قاعدة البيانات...
    flask --app run init-db
    if errorlevel 1 (
        echo ⚠️ حدث خطأ، محاولة بطريقة بديلة...
        python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Database created!')"
    )
    echo ✅ تم إنشاء قاعدة البيانات
)

echo.
echo ========================================
echo ✅ تم الإعداد بنجاح!
echo ========================================
echo.
echo لتشغيل التطبيق:
echo   1. شغّل ملف DED_Modern_Launcher.pyw
echo   2. أو شغّل: python run.py
echo   3. افتح المتصفح على: http://127.0.0.1:5000
echo.
echo بيانات الدخول الافتراضية:
echo   اسم المستخدم: admin
echo   كلمة المرور: admin123
echo.
echo ========================================
pause

