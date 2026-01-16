# DED ERP Server Launcher
# Keep this window open while using the application

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "   DED ERP System Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "[*] Starting server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Server URL: " -NoNewline
Write-Host "http://localhost:5000" -ForegroundColor Green
Write-Host "Username: " -NoNewline
Write-Host "admin" -ForegroundColor Cyan
Write-Host "Password: " -NoNewline
Write-Host "admin123" -ForegroundColor Cyan
Write-Host ""
Write-Host "========================================" -ForegroundColor Red
Write-Host "  IMPORTANT: DO NOT CLOSE THIS WINDOW!" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Red
Write-Host ""

# Change to script directory
Set-Location $PSScriptRoot

# Run the server
python run.py

Write-Host ""
Write-Host "========================================" -ForegroundColor Yellow
Write-Host "Server stopped!" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to exit"

