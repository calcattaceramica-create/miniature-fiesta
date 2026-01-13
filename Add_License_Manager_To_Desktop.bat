@echo off
chcp 65001 >nul
title Add License Manager Shortcut

echo.
echo Creating Desktop Shortcut...
echo.

set DESKTOP=%USERPROFILE%\Desktop

echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%DESKTOP%\License Manager.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%CD%\License_Manager_App.pyw" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%CD%" >> CreateShortcut.vbs
echo oLink.Description = "License Manager" >> CreateShortcut.vbs
echo oLink.IconLocation = "C:\\Windows\\System32\\shell32.dll,48" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs

cscript //nologo CreateShortcut.vbs
del CreateShortcut.vbs

if exist "%DESKTOP%\License Manager.lnk" (
    echo.
    echo Shortcut created successfully!
    echo.
) else (
    echo.
    echo Failed to create shortcut
    echo.
)

echo.
pause
