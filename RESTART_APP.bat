@echo off
chcp 65001 >nul
echo ═══════════════════════════════════════════════════════════════
echo    🔄 إعادة تشغيل التطبيق - Restarting Application
echo ═══════════════════════════════════════════════════════════════
echo.

echo 🛑 إيقاف جميع عمليات Python...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM pythonw.exe /T >nul 2>&1
timeout /t 2 >nul

echo.
echo ✅ تم إيقاف جميع العمليات
echo.
echo 🚀 تشغيل التطبيق...
echo.

start "DED ERP System" python run.py

echo.
echo ⏳ انتظار تشغيل الخادم...
timeout /t 5 >nul

echo.
echo 🌐 فتح المتصفح...
start http://localhost:5000/auth/login

echo.
echo ═══════════════════════════════════════════════════════════════
echo    ✅ تم تشغيل التطبيق بنجاح!
echo ═══════════════════════════════════════════════════════════════
echo.
echo 📝 بيانات تسجيل الدخول:
echo    اسم المستخدم: admin
echo    كلمة المرور: admin123
echo    مفتاح الترخيص: CEC9-79EE-C42F-2DAD
echo.
echo ⚠️  لا تغلق هذه النافذة!
echo.
pause

