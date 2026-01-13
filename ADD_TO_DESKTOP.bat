@echo off
chcp 65001 >nul
title Creating Desktop Shortcuts

echo.
echo ========================================
echo   Creating Desktop Shortcuts
echo ========================================
echo.

:: Create VBS script
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\shortcut.vbs"
echo sDesktop = oWS.SpecialFolders("Desktop") >> "%TEMP%\shortcut.vbs"
echo.>> "%TEMP%\shortcut.vbs"
echo sLinkFile = sDesktop ^& "\DED Control Panel.lnk" >> "%TEMP%\shortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\shortcut.vbs"
echo oLink.TargetPath = "%~dp0DED_Control_Panel_Launcher.bat" >> "%TEMP%\shortcut.vbs"
echo oLink.WorkingDirectory = "%~dp0" >> "%TEMP%\shortcut.vbs"
echo oLink.IconLocation = "C:\Windows\System32\imageres.dll,109" >> "%TEMP%\shortcut.vbs"
echo oLink.Description = "DED Control Panel - Menu" >> "%TEMP%\shortcut.vbs"
echo oLink.Save >> "%TEMP%\shortcut.vbs"
echo.>> "%TEMP%\shortcut.vbs"
echo sLinkFile2 = sDesktop ^& "\DED Panel (Direct).lnk" >> "%TEMP%\shortcut.vbs"
echo Set oLink2 = oWS.CreateShortcut(sLinkFile2) >> "%TEMP%\shortcut.vbs"
echo oLink2.TargetPath = "%~dp0DED_Control_Panel.pyw" >> "%TEMP%\shortcut.vbs"
echo oLink2.WorkingDirectory = "%~dp0" >> "%TEMP%\shortcut.vbs"
echo oLink2.IconLocation = "C:\Windows\System32\imageres.dll,1" >> "%TEMP%\shortcut.vbs"
echo oLink2.Description = "DED Control Panel - Direct" >> "%TEMP%\shortcut.vbs"
echo oLink2.Save >> "%TEMP%\shortcut.vbs"

:: Execute VBS
cscript //nologo "%TEMP%\shortcut.vbs"

:: Clean up
del "%TEMP%\shortcut.vbs"

echo.
echo ========================================
echo   SUCCESS!
echo ========================================
echo.
echo Two shortcuts created on Desktop:
echo   1. DED Control Panel.lnk (Menu)
echo   2. DED Panel (Direct).lnk (Direct)
echo.
pause

