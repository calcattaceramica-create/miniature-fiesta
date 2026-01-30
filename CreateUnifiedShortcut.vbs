Set WshShell = WScript.CreateObject("WScript.Shell")
DesktopPath = WshShell.SpecialFolders("Desktop")
CurrentPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)

' Remove old shortcuts
Set fso = CreateObject("Scripting.FileSystemObject")
If fso.FileExists(DesktopPath & "\DED ERP System.lnk") Then
    fso.DeleteFile DesktopPath & "\DED ERP System.lnk"
End If
If fso.FileExists(DesktopPath & "\License Manager.lnk") Then
    fso.DeleteFile DesktopPath & "\License Manager.lnk"
End If

' Create new unified shortcut
Set Shortcut = WshShell.CreateShortcut(DesktopPath & "\DED System.lnk")
Shortcut.TargetPath = CurrentPath & "\Launch_DED_System.bat"
Shortcut.WorkingDirectory = CurrentPath
Shortcut.Description = "DED ERP System - Complete Solution"
Shortcut.IconLocation = "C:\Windows\System32\imageres.dll,1"
Shortcut.Save

WScript.Echo "✅ تم إنشاء الاختصار الموحد بنجاح!" & vbCrLf & "✅ Unified shortcut created successfully!" & vbCrLf & vbCrLf & "الاختصار: DED System" & vbCrLf & "Shortcut: DED System"

