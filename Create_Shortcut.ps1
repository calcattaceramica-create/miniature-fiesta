# Create Desktop Shortcut for DED Control Panel

Write-Host ""
Write-Host "Creating Desktop Shortcut..." -ForegroundColor Cyan
Write-Host ""

# Get Desktop path
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "DED Control Panel.lnk"

# Get current directory
$CurrentDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Create WScript Shell object
$WshShell = New-Object -ComObject WScript.Shell

# Create shortcut
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = Join-Path $CurrentDir "DED_Control_Panel_Launcher.bat"
$Shortcut.WorkingDirectory = $CurrentDir
$Shortcut.IconLocation = "C:\Windows\System32\imageres.dll,109"
$Shortcut.Description = "DED Control Panel"
$Shortcut.Save()

Write-Host "Shortcut created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Location: $ShortcutPath" -ForegroundColor Yellow
Write-Host ""

# Also create a direct launcher shortcut
$DirectShortcutPath = Join-Path $DesktopPath "DED Panel (Direct).lnk"
$DirectShortcut = $WshShell.CreateShortcut($DirectShortcutPath)
$DirectShortcut.TargetPath = "pythonw.exe"
$DirectShortcut.Arguments = Join-Path $CurrentDir "DED_Control_Panel.pyw"
$DirectShortcut.WorkingDirectory = $CurrentDir
$DirectShortcut.IconLocation = "C:\Windows\System32\imageres.dll,1"
$DirectShortcut.Description = "DED Control Panel - Direct Launch"
$DirectShortcut.Save()

Write-Host "Direct launcher also created!" -ForegroundColor Green
Write-Host ""
Write-Host "Location: $DirectShortcutPath" -ForegroundColor Yellow
Write-Host ""

Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Two shortcuts created on Desktop:" -ForegroundColor Cyan
Write-Host "  1. DED Control Panel.lnk - Menu launcher" -ForegroundColor White
Write-Host "  2. DED Panel (Direct).lnk - Direct launcher" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to exit"

