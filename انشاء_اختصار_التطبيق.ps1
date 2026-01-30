# PowerShell Script to Create Desktop Shortcut for DED ERP Application
# سكريبت لإنشاء اختصار سطح المكتب لتطبيق DED ERP

# Set UTF-8 encoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Get desktop path
$DesktopPath = [Environment]::GetFolderPath("Desktop")

# Define shortcut path
$ShortcutPath = Join-Path $DesktopPath "DED ERP System.lnk"

# Remove old shortcut if exists
if (Test-Path $ShortcutPath) {
    Remove-Item $ShortcutPath -Force
    Write-Host "Old shortcut removed" -ForegroundColor Yellow
    Write-Host ""
}

# Get current directory
$CurrentDir = $PSScriptRoot
if ([string]::IsNullOrEmpty($CurrentDir)) {
    $CurrentDir = Get-Location
}

# Define target path
$TargetPath = Join-Path $CurrentDir "Launch_ERP_Application.bat"

# Check if target exists
if (-not (Test-Path $TargetPath)) {
    Write-Host "================================================================" -ForegroundColor Red
    Write-Host "ERROR: Launch_ERP_Application.bat not found!" -ForegroundColor Red
    Write-Host "================================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Expected location: $TargetPath" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

# Create shortcut
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $TargetPath
$Shortcut.WorkingDirectory = $CurrentDir
$Shortcut.Description = "DED ERP System"
$Shortcut.IconLocation = "C:\Windows\System32\shell32.dll,165"
$Shortcut.Save()

# Verify shortcut was created
if (Test-Path $ShortcutPath) {
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Green
    Write-Host "Shortcut created successfully!" -ForegroundColor Green
    Write-Host "================================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Location: $ShortcutPath" -ForegroundColor Cyan
    Write-Host "Target: $TargetPath" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Yellow
    Write-Host "How to use:" -ForegroundColor Yellow
    Write-Host "================================================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. Go to Desktop" -ForegroundColor White
    Write-Host "2. Double-click 'DED ERP System'" -ForegroundColor White
    Write-Host "3. Application will start" -ForegroundColor White
    Write-Host "4. Open browser: http://localhost:5000" -ForegroundColor White
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Green
    Write-Host ""
    
    # Open desktop folder
    Start-Process "explorer.exe" -ArgumentList $DesktopPath
    
} else {
    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Red
    Write-Host "ERROR: Failed to create shortcut!" -ForegroundColor Red
    Write-Host "================================================================" -ForegroundColor Red
    Write-Host ""
}

Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')

