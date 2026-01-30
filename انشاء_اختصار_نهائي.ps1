$Desktop = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path -Path $Desktop -ChildPath "License Manager.lnk"

# Remove old shortcut if exists
if (Test-Path $ShortcutPath) {
    Remove-Item $ShortcutPath -Force
    Write-Host "Old shortcut removed" -ForegroundColor Yellow
}

# Create new shortcut
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "C:\Users\DELL\DED\Launch_License_Manager.bat"
$Shortcut.WorkingDirectory = "C:\Users\DELL\DED"
$Shortcut.Description = "License Management System"
$Shortcut.IconLocation = "C:\Windows\System32\shell32.dll,48"
$Shortcut.Save()

Write-Host ""
Write-Host "================================================================" -ForegroundColor Green
Write-Host "Shortcut created successfully!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Location: $ShortcutPath" -ForegroundColor Cyan
Write-Host "Target: C:\Users\DELL\DED\Launch_License_Manager.bat" -ForegroundColor Cyan
Write-Host ""
Write-Host "Please test the shortcut on your desktop now!" -ForegroundColor Yellow
Write-Host ""

