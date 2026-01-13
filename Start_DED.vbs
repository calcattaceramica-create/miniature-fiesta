Set WshShell = CreateObject("WScript.Shell")

' Kill old processes silently
WshShell.Run "taskkill /F /IM pythonw.exe", 0, True
WshShell.Run "taskkill /F /IM python.exe", 0, True
WScript.Sleep 1000

' Start professional launcher without any window
desktopPath = WshShell.SpecialFolders("Desktop")
WshShell.CurrentDirectory = desktopPath
WshShell.Run "pythonw.exe DED_Professional_Launcher.pyw", 0, False

Set WshShell = Nothing

