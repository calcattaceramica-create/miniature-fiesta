Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = oWS.SpecialFolders("Desktop") & "\DED System Launcher.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)

' Get current directory
currentDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)

oLink.TargetPath = currentDir & "\DED_Modern_Launcher.pyw"
oLink.WorkingDirectory = currentDir
oLink.Description = "DED Management System - Unified Launcher"
oLink.IconLocation = "C:\Windows\System32\shell32.dll,13"
oLink.Save

MsgBox "تم إنشاء الاختصار على سطح المكتب بنجاح!" & vbCrLf & vbCrLf & "Shortcut created successfully on Desktop!" & vbCrLf & vbCrLf & "اسم الاختصار: DED System Launcher", vbInformation, "تم بنجاح - Success"

