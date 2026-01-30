# PowerShell Script to Create Beautiful Desktop Shortcuts
# UTF-8 Encoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "       Creating Desktop Shortcuts for DED ERP System" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Get paths
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$CurrentDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if ([string]::IsNullOrEmpty($CurrentDir)) {
    $CurrentDir = Get-Location
}

# Create WScript Shell object
$WshShell = New-Object -ComObject WScript.Shell

# ============================================================================
# 1. Create DED ERP Application Shortcut
# ============================================================================

Write-Host "Creating DED ERP Application Shortcut..." -ForegroundColor Yellow

$AppShortcutPath = Join-Path $DesktopPath "DED ERP System.lnk"
$AppTargetPath = Join-Path $CurrentDir "Launch_ERP_Application.bat"

if (Test-Path $AppShortcutPath) {
    Remove-Item $AppShortcutPath -Force
}

if (Test-Path $AppTargetPath) {
    $AppShortcut = $WshShell.CreateShortcut($AppShortcutPath)
    $AppShortcut.TargetPath = $AppTargetPath
    $AppShortcut.WorkingDirectory = $CurrentDir
    $AppShortcut.Description = "DED ERP System - Enterprise Resource Planning"
    $AppShortcut.IconLocation = "C:\Windows\System32\imageres.dll,1"
    $AppShortcut.Save()
    
    Write-Host "  [OK] DED ERP System shortcut created" -ForegroundColor Green
} else {
    Write-Host "  [ERROR] Launch_ERP_Application.bat not found!" -ForegroundColor Red
}

Write-Host ""

# ============================================================================
# 2. Create License Manager Shortcut
# ============================================================================

Write-Host "Creating License Manager Shortcut..." -ForegroundColor Yellow

$LicenseShortcutPath = Join-Path $DesktopPath "License Manager.lnk"
$LicenseTargetPath = Join-Path $CurrentDir "Launch_License_Manager.bat"

if (Test-Path $LicenseShortcutPath) {
    Remove-Item $LicenseShortcutPath -Force
}

if (Test-Path $LicenseTargetPath) {
    $LicenseShortcut = $WshShell.CreateShortcut($LicenseShortcutPath)
    $LicenseShortcut.TargetPath = $LicenseTargetPath
    $LicenseShortcut.WorkingDirectory = $CurrentDir
    $LicenseShortcut.Description = "License Management System"
    $LicenseShortcut.IconLocation = "C:\Windows\System32\imageres.dll,77"
    $LicenseShortcut.Save()
    
    Write-Host "  [OK] License Manager shortcut created" -ForegroundColor Green
} else {
    Write-Host "  [ERROR] Launch_License_Manager.bat not found!" -ForegroundColor Red
}

Write-Host ""

# ============================================================================
# 3. Create Quick Start Guide on Desktop
# ============================================================================

Write-Host "Creating Quick Start Guide..." -ForegroundColor Yellow

$GuideContent = @"
═══════════════════════════════════════════════════════════════════════════════
                    DED ERP SYSTEM - QUICK START GUIDE
                         دليل البدء السريع
═══════════════════════════════════════════════════════════════════════════════

📱 DESKTOP SHORTCUTS / الاختصارات على سطح المكتب
═══════════════════════════════════════════════════════════════════════════════

1. 🏢 DED ERP System
   - Main ERP Application / التطبيق الرئيسي
   - URL: http://localhost:5000
   - Username: admin
   - Password: admin123

2. 🔑 License Manager
   - License Management System / نظام إدارة التراخيص
   - Create and manage client licenses / إنشاء وإدارة تراخيص العملاء

═══════════════════════════════════════════════════════════════════════════════
🚀 HOW TO USE / كيفية الاستخدام
═══════════════════════════════════════════════════════════════════════════════

FOR ERP APPLICATION:
1. Double-click "DED ERP System" on desktop
2. Wait for the application to start
3. Open browser and go to: http://localhost:5000
4. Login with: admin / admin123

FOR LICENSE MANAGER:
1. Double-click "License Manager" on desktop
2. Follow the menu to create/manage licenses

═══════════════════════════════════════════════════════════════════════════════
📋 ERP MODULES / أقسام النظام
═══════════════════════════════════════════════════════════════════════════════

📊 Dashboard          - لوحة التحكم
📦 Inventory          - المخزون
💰 Sales              - المبيعات
🛒 Purchases          - المشتريات
💼 Accounting         - المحاسبة
👥 HR                 - الموارد البشرية
🤝 CRM                - إدارة العملاء
🏪 POS                - نقاط البيع
⚙️  Settings          - الإعدادات

═══════════════════════════════════════════════════════════════════════════════
⚠️  IMPORTANT NOTES / ملاحظات مهمة
═══════════════════════════════════════════════════════════════════════════════

✅ Keep the CMD window open while using the application
   لا تغلق نافذة CMD أثناء استخدام التطبيق

✅ To stop: Press CTRL+C in the CMD window
   للإيقاف: اضغط CTRL+C في نافذة CMD

✅ Default login: admin / admin123
   تسجيل الدخول الافتراضي

═══════════════════════════════════════════════════════════════════════════════
📞 SUPPORT / الدعم
═══════════════════════════════════════════════════════════════════════════════

For help, check the documentation files in:
C:\Users\DELL\DED\

═══════════════════════════════════════════════════════════════════════════════
"@

$GuidePath = Join-Path $DesktopPath "DED_Quick_Start_Guide.txt"
$GuideContent | Out-File -FilePath $GuidePath -Encoding UTF8 -Force

Write-Host "  [OK] Quick Start Guide created" -ForegroundColor Green
Write-Host ""

# ============================================================================
# Summary
# ============================================================================

Write-Host "================================================================" -ForegroundColor Green
Write-Host "                    SHORTCUTS CREATED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Desktop shortcuts created:" -ForegroundColor Cyan
Write-Host "  1. DED ERP System.lnk" -ForegroundColor White
Write-Host "  2. License Manager.lnk" -ForegroundColor White
Write-Host "  3. DED_Quick_Start_Guide.txt" -ForegroundColor White
Write-Host ""
Write-Host "Opening Desktop folder..." -ForegroundColor Yellow
Start-Process "explorer.exe" -ArgumentList $DesktopPath

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')

