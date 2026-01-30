Set WshShell = WScript.CreateObject("WScript.Shell")
DesktopPath = WshShell.SpecialFolders("Desktop")
CurrentPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)

' Create DED ERP System Shortcut
Set Shortcut1 = WshShell.CreateShortcut(DesktopPath & "\DED ERP System.lnk")
Shortcut1.TargetPath = CurrentPath & "\Launch_ERP_Application.bat"
Shortcut1.WorkingDirectory = CurrentPath
Shortcut1.Description = "DED ERP System - Enterprise Resource Planning"
Shortcut1.IconLocation = "C:\Windows\System32\imageres.dll,1"
Shortcut1.Save

' Create License Manager Shortcut
Set Shortcut2 = WshShell.CreateShortcut(DesktopPath & "\License Manager.lnk")
Shortcut2.TargetPath = CurrentPath & "\Launch_License_Manager.bat"
Shortcut2.WorkingDirectory = CurrentPath
Shortcut2.Description = "License Management System"
Shortcut2.IconLocation = "C:\Windows\System32\imageres.dll,77"
Shortcut2.Save

WScript.Echo "Shortcuts created successfully on Desktop!"
WScript.Echo ""
WScript.Echo "1. DED ERP System.lnk"
WScript.Echo "2. License Manager.lnk"

