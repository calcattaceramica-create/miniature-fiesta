Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = oWS.SpecialFolders("Desktop") & "\DED License Manager.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = WScript.ScriptFullName
oLink.Arguments = ""
oLink.WorkingDirectory = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
oLink.IconLocation = "shell32.dll,48"
oLink.Description = "DED License Manager - مدير التراخيص"
oLink.WindowStyle = 1
oLink.Save

' Run the application
Set oShell = CreateObject("WScript.Shell")
strPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
oShell.CurrentDirectory = strPath
oShell.Run "pythonw.exe License_Manager_GUI.pyw", 0, False

MsgBox "تم إنشاء اختصار على سطح المكتب!" & vbCrLf & vbCrLf & "يمكنك الآن فتح مدير التراخيص من سطح المكتب", vbInformation, "DED License Manager"

