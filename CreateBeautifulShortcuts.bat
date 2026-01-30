@echo off
chcp 65001 >nul
title Creating Desktop Shortcuts

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo                   Creating Beautiful Desktop Shortcuts
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

cd /d "%~dp0"

REM Create VBScript to make shortcuts
echo Set WshShell = WScript.CreateObject("WScript.Shell") > CreateShortcuts.vbs
echo DesktopPath = WshShell.SpecialFolders("Desktop") >> CreateShortcuts.vbs
echo. >> CreateShortcuts.vbs

REM Create DED ERP System Shortcut
echo ' Create DED ERP System Shortcut >> CreateShortcuts.vbs
echo Set Shortcut1 = WshShell.CreateShortcut(DesktopPath ^& "\DED ERP System.lnk") >> CreateShortcuts.vbs
echo Shortcut1.TargetPath = "%~dp0Launch_ERP_Application.bat" >> CreateShortcuts.vbs
echo Shortcut1.WorkingDirectory = "%~dp0" >> CreateShortcuts.vbs
echo Shortcut1.Description = "DED ERP System - Enterprise Resource Planning" >> CreateShortcuts.vbs
echo Shortcut1.IconLocation = "C:\Windows\System32\imageres.dll,1" >> CreateShortcuts.vbs
echo Shortcut1.Save >> CreateShortcuts.vbs
echo. >> CreateShortcuts.vbs

REM Create License Manager Shortcut
echo ' Create License Manager Shortcut >> CreateShortcuts.vbs
echo Set Shortcut2 = WshShell.CreateShortcut(DesktopPath ^& "\License Manager.lnk") >> CreateShortcuts.vbs
echo Shortcut2.TargetPath = "%~dp0Launch_License_Manager.bat" >> CreateShortcuts.vbs
echo Shortcut2.WorkingDirectory = "%~dp0" >> CreateShortcuts.vbs
echo Shortcut2.Description = "License Management System" >> CreateShortcuts.vbs
echo Shortcut2.IconLocation = "C:\Windows\System32\imageres.dll,77" >> CreateShortcuts.vbs
echo Shortcut2.Save >> CreateShortcuts.vbs

REM Run the VBScript
cscript //NoLogo CreateShortcuts.vbs

REM Delete the temporary VBScript
del CreateShortcuts.vbs

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo                   Shortcuts Created Successfully!
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo Desktop shortcuts created:
echo   1. DED ERP System.lnk
echo   2. License Manager.lnk
echo.
echo Opening Desktop folder...
explorer "%USERPROFILE%\Desktop"

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
pause

