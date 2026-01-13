@echo off
chcp 65001 >nul
echo ========================================
echo    نظام إدارة الموارد البشرية
echo    HR Management System
echo ========================================
echo.

echo [1/4] التحقق من المتطلبات...
python --version
if errorlevel 1 (
    echo ❌ Python غير مثبت!
    pause
    exit /b 1
)

echo.
echo [2/4] تثبيت المتطلبات...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ فشل تثبيت المتطلبات!
    pause
    exit /b 1
)

echo.
echo [3/4] إنشاء قاعدة البيانات...
python init_db.py
if errorlevel 1 (
    echo ⚠️  تحذير: قد تكون قاعدة البيانات موجودة مسبقاً
)

echo.
echo [4/4] إضافة بيانات تجريبية...
python seed_hr_data.py
if errorlevel 1 (
    echo ⚠️  تحذير: قد تكون البيانات موجودة مسبقاً
)

echo.
echo ========================================
echo ✅ النظام جاهز للتشغيل!
echo ========================================
echo.
echo سيتم فتح المتصفح تلقائياً على:
echo http://localhost:5000/hr/dashboard
echo.
echo للإيقاف: اضغط Ctrl+C
echo ========================================
echo.

echo تشغيل التطبيق...
start http://localhost:5000/hr/dashboard
python run.py

pause

