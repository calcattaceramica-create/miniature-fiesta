@echo off
chcp 65001 >nul
color 0A
title 📌 تثبيت اختصار سطح المكتب - Install Desktop Shortcut

cls
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                                                          ║
echo ║     📌 تثبيت اختصار DED Control Panel                   ║
echo ║     Install DED Control Panel Shortcut                  ║
echo ║                                                          ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo ⏳ جاري إنشاء الاختصار على سطح المكتب...
echo    Creating shortcut on Desktop...
echo.

:: Get Desktop path
for /f "usebackq tokens=3*" %%A in (`reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" /v Desktop`) do set DESKTOP=%%A %%B
call set DESKTOP=%DESKTOP%

:: Get current directory
set CURRENT_DIR=%~dp0

:: Create PowerShell script to create shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\create_shortcut.vbs"
echo sLinkFile = "%DESKTOP%\DED Control Panel.lnk" >> "%TEMP%\create_shortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\create_shortcut.vbs"
echo oLink.TargetPath = "%CURRENT_DIR%DED_Control_Panel_Launcher.bat" >> "%TEMP%\create_shortcut.vbs"
echo oLink.WorkingDirectory = "%CURRENT_DIR%" >> "%TEMP%\create_shortcut.vbs"
echo oLink.IconLocation = "C:\Windows\System32\imageres.dll,109" >> "%TEMP%\create_shortcut.vbs"
echo oLink.Description = "DED Control Panel - لوحة التحكم الشاملة" >> "%TEMP%\create_shortcut.vbs"
echo oLink.WindowStyle = 1 >> "%TEMP%\create_shortcut.vbs"
echo oLink.Save >> "%TEMP%\create_shortcut.vbs"

:: Run the VBS script
cscript //nologo "%TEMP%\create_shortcut.vbs"

:: Clean up
del "%TEMP%\create_shortcut.vbs"

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                                                          ║
echo ║              ✅ تم بنجاح! - Success!                     ║
echo ║                                                          ║
echo ║  تم إنشاء الاختصار على سطح المكتب                       ║
echo ║  Shortcut created on Desktop                            ║
echo ║                                                          ║
echo ║  📍 الموقع: سطح المكتب\DED Control Panel.lnk            ║
echo ║  📍 Location: Desktop\DED Control Panel.lnk             ║
echo ║                                                          ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo 💡 يمكنك الآن:
echo    - النقر المزدوج على الاختصار لفتح القائمة الرئيسية
echo    - اختيار الأمر المطلوب من القائمة
echo.
echo 💡 You can now:
echo    - Double-click the shortcut to open main menu
echo    - Choose the desired command from menu
echo.
pause

