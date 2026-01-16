@echo off
chcp 65001 >nul
echo ═══════════════════════════════════════════════════════════════════════════════
echo                     🚀 نشر نظام التراخيص على Render
echo                     Deploy License System to Render
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo.
echo ✅ النظام جاهز للنشر!
echo.
echo.
echo الخطوة 1️⃣: رفع الكود إلى GitHub
echo ────────────────────────────────────────
echo.
git add .
git commit -m "Enable license system with auto-protection and management"
git push origin main
echo.
echo ✅ تم رفع الكود بنجاح!
echo.
echo.
echo الخطوة 2️⃣: انتظر إعادة النشر على Render
echo ────────────────────────────────────────
echo.
echo 1. افتح Render Dashboard: https://dashboard.render.com
echo 2. انتظر حتى يكتمل النشر (2-3 دقائق)
echo 3. عندما ترى "Deploy live" ✅
echo.
echo.
echo الخطوة 3️⃣: تفعيل جداول التراخيص
echo ────────────────────────────────────────
echo.
echo في Render Shell، قم بتشغيل:
echo.
echo    python add_license_to_render.py
echo.
echo.
echo الخطوة 4️⃣: اختبار النظام
echo ────────────────────────────────────────
echo.
echo افتح التطبيق وسجل الدخول:
echo    Username: admin
echo    Password: admin123
echo.
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo                     ✅ النظام جاهز للاستخدام!
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo 📚 للمزيد من التفاصيل، راجع:
echo    - DEPLOY_TO_RENDER_NOW.txt
echo    - HOW_TO_GIVE_LICENSE.txt
echo    - LICENSE_SYSTEM_GUIDE_AR.md
echo.
pause

