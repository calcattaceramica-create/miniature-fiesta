@echo off
chcp 65001 >nul
color 0A

echo.
echo ════════════════════════════════════════════════════════════
echo    🚀 DED ERP System - Web Version
echo    نظام تخطيط موارد المؤسسات - نسخة الويب
echo ════════════════════════════════════════════════════════════
echo.
echo 📦 جاري التحقق من المكتبات المطلوبة...
echo.

REM Check if streamlit is installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo ⚠️  Streamlit غير مثبت!
    echo.
    echo 📥 جاري تثبيت المكتبات المطلوبة...
    echo.
    pip install -r requirements_erp_web.txt
    echo.
    echo ✅ تم تثبيت المكتبات بنجاح!
    echo.
) else (
    echo ✅ جميع المكتبات مثبتة!
    echo.
)

echo ════════════════════════════════════════════════════════════
echo    🌐 جاري تشغيل نظام ERP...
echo ════════════════════════════════════════════════════════════
echo.
echo 📌 سيفتح المتصفح تلقائياً على:
echo    http://localhost:8501
echo.
echo 🔐 بيانات الدخول:
echo    المستخدم: admin
echo    كلمة المرور: admin123
echo.
echo ⚠️  لا تغلق هذه النافذة!
echo.
echo ════════════════════════════════════════════════════════════
echo.

REM Start Streamlit
streamlit run DED_ERP_Web.py

echo.
echo ════════════════════════════════════════════════════════════
echo    ⛔ تم إيقاف النظام!
echo ════════════════════════════════════════════════════════════
echo.
pause

