Set WshShell = CreateObject("WScript.Shell")

' Delete old shortcuts
On Error Resume Next
Set fso = CreateObject("Scripting.FileSystemObject")
fso.DeleteFile WshShell.SpecialFolders("Desktop") & "\*DED*.lnk"
On Error GoTo 0

' Create new shortcut
Set oShellLink = WshShell.CreateShortcut(WshShell.SpecialFolders("Desktop") & "\DED System.lnk")
oShellLink.TargetPath = WshShell.SpecialFolders("Desktop") & "\Start_DED.vbs"
oShellLink.WindowStyle = 0
oShellLink.Description = "DED Management System"
oShellLink.WorkingDirectory = WshShell.SpecialFolders("Desktop")
oShellLink.Save

WScript.Echo "تم إنشاء الاختصار بنجاح!"

