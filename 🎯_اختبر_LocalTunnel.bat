@echo off
chcp 65001 >nul
color 0E
title 🎯 اختبار LocalTunnel - Test LocalTunnel

cls
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo                    🎯 اختبار نظام LocalTunnel
echo                    LocalTunnel System Test
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

REM Test 1: Check Python
echo   📋 الاختبار 1: التحقق من Python...
echo.
python --version >nul 2>&1
if errorlevel 1 (
    echo   ❌ Python غير مثبت!
    echo   📥 يرجى تثبيت Python من: https://www.python.org/
    echo.
    goto :end
) else (
    python --version
    echo   ✅ Python مثبت!
    echo.
)

REM Test 2: Check Node.js
echo   📋 الاختبار 2: التحقق من Node.js...
echo.
node --version >nul 2>&1
if errorlevel 1 (
    echo   ❌ Node.js غير مثبت!
    echo   📥 يرجى تثبيت Node.js من: https://nodejs.org/
    echo.
    goto :end
) else (
    node --version
    echo   ✅ Node.js مثبت!
    echo.
)

REM Test 3: Check npm
echo   📋 الاختبار 3: التحقق من npm...
echo.
npm --version >nul 2>&1
if errorlevel 1 (
    echo   ❌ npm غير مثبت!
    echo.
    goto :end
) else (
    npm --version
    echo   ✅ npm مثبت!
    echo.
)

REM Test 4: Check LocalTunnel
echo   📋 الاختبار 4: التحقق من LocalTunnel...
echo.
lt --version >nul 2>&1
if errorlevel 1 (
    echo   ⚠️  LocalTunnel غير مثبت
    echo   💡 سيتم تثبيته تلقائياً عند تشغيل النظام
    echo.
) else (
    lt --version
    echo   ✅ LocalTunnel مثبت!
    echo.
)

REM Test 5: Check files
echo   📋 الاختبار 5: التحقق من الملفات...
echo.

if exist "localtunnel_manager.py" (
    echo   ✅ localtunnel_manager.py موجود
) else (
    echo   ❌ localtunnel_manager.py غير موجود!
)

if exist "🏆_LocalTunnel_مجاني_بدون_حدود.bat" (
    echo   ✅ 🏆_LocalTunnel_مجاني_بدون_حدود.bat موجود
) else (
    echo   ❌ 🏆_LocalTunnel_مجاني_بدون_حدود.bat غير موجود!
)

if exist "run_server.py" (
    echo   ✅ run_server.py موجود
) else (
    echo   ❌ run_server.py غير موجود!
)

echo.

REM Test 6: Check config
echo   📋 الاختبار 6: التحقق من الإعدادات...
echo.

if exist "localtunnel_config.json" (
    echo   ✅ ملف الإعدادات موجود
    echo   📄 محتوى الإعدادات:
    type localtunnel_config.json
    echo.
) else (
    echo   ℹ️  ملف الإعدادات غير موجود (سيتم إنشاؤه عند أول استخدام)
    echo.
)

:end
echo ═══════════════════════════════════════════════════════════════════════════════
echo                    📊 نتيجة الاختبار
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo   إذا كانت جميع الاختبارات ✅، النظام جاهز للاستخدام!
echo.
echo   للبدء:
echo   1. انقر نقرتين على: 🏆_LocalTunnel_مجاني_بدون_حدود.bat
echo   2. اتبع التعليمات
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
pause

