@echo off
chcp 65001 >nul
title DED System Launcher

echo.
echo ═══════════════════════════════════════════════════════════════
echo                  🚀 DED System Launcher 🚀
echo ═══════════════════════════════════════════════════════════════
echo.
echo جاري تشغيل الواجهة الموحدة...
echo Starting unified launcher...
echo.

cd /d "%~dp0"
start pythonw DED_Simple_Launcher.pyw

echo.
echo ✅ تم التشغيل بنجاح!
echo ✅ Launched successfully!
timeout /t 2 >nul

