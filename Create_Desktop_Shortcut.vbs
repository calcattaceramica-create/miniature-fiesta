Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = oWS.SpecialFolders("Desktop") & "\DED Control Panel.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = WScript.ScriptFullName
oLink.Arguments = ""
oLink.WorkingDirectory = Left(WScript.ScriptFullName, InStrRev(WScript.ScriptFullName, "\") - 1)
oLink.IconLocation = "C:\Windows\System32\shell32.dll,137"
oLink.Description = "DED Control Panel - لوحة التحكم الشاملة"
oLink.WindowStyle = 1
oLink.Save

' Create shortcut for the BAT file
sLinkFile2 = oWS.SpecialFolders("Desktop") & "\DED Control Panel.lnk"
Set oLink2 = oWS.CreateShortcut(sLinkFile2)
oLink2.TargetPath = Left(WScript.ScriptFullName, InStrRev(WScript.ScriptFullName, "\") - 1) & "\DED_Control_Panel_Launcher.bat"
oLink2.WorkingDirectory = Left(WScript.ScriptFullName, InStrRev(WScript.ScriptFullName, "\") - 1)
oLink2.IconLocation = "C:\Windows\System32\imageres.dll,109"
oLink2.Description = "DED Control Panel - لوحة التحكم الشاملة"
oLink2.WindowStyle = 1
oLink2.Save

MsgBox "✅ تم إنشاء الاختصار على سطح المكتب بنجاح!" & vbCrLf & vbCrLf & "Shortcut created successfully on Desktop!", 64, "DED Control Panel"

