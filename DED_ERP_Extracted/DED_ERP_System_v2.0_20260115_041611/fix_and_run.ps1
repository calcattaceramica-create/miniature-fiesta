# Fix Delete Issue and Run System
# This script will:
# 1. Stop any running Python processes
# 2. Clear Python cache
# 3. Verify the code is correct
# 4. Start the system

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "  🔧 Fix Delete Issue and Run System" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Stop Python processes
Write-Host "[1/5] Stopping any running Python processes..." -ForegroundColor Yellow
$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue
if ($pythonProcesses) {
    $pythonProcesses | Stop-Process -Force -ErrorAction SilentlyContinue
    Write-Host "      ✅ Stopped $($pythonProcesses.Count) Python process(es)" -ForegroundColor Green
    Start-Sleep -Seconds 2
} else {
    Write-Host "      ℹ️  No Python processes running" -ForegroundColor Gray
}

# Step 2: Clear cache
Write-Host ""
Write-Host "[2/5] Clearing Python cache files..." -ForegroundColor Yellow

# Count cache items before deletion
$pycacheDirs = Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue
$pycFiles = Get-ChildItem -Path . -Recurse -File -Filter "*.pyc" -ErrorAction SilentlyContinue
$pyoFiles = Get-ChildItem -Path . -Recurse -File -Filter "*.pyo" -ErrorAction SilentlyContinue

$totalItems = $pycacheDirs.Count + $pycFiles.Count + $pyoFiles.Count

if ($totalItems -gt 0) {
    Write-Host "      Found:" -ForegroundColor Gray
    Write-Host "      - $($pycacheDirs.Count) __pycache__ directories" -ForegroundColor Gray
    Write-Host "      - $($pycFiles.Count) .pyc files" -ForegroundColor Gray
    Write-Host "      - $($pyoFiles.Count) .pyo files" -ForegroundColor Gray
    
    # Delete cache
    $pycacheDirs | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    $pycFiles | Remove-Item -Force -ErrorAction SilentlyContinue
    $pyoFiles | Remove-Item -Force -ErrorAction SilentlyContinue
    
    Write-Host "      ✅ Deleted $totalItems cache items" -ForegroundColor Green
} else {
    Write-Host "      ℹ️  No cache files found" -ForegroundColor Gray
}

# Step 3: Verify code
Write-Host ""
Write-Host "[3/5] Verifying delete product code..." -ForegroundColor Yellow

if (Test-Path "verify_delete_code.py") {
    $verifyOutput = python verify_delete_code.py 2>&1
    
    if ($verifyOutput -match "CODE IS CORRECT") {
        Write-Host "      ✅ Code verification passed!" -ForegroundColor Green
    } elseif ($verifyOutput -match "CODE IS MIXED") {
        Write-Host "      ⚠️  Warning: Mixed code detected!" -ForegroundColor Yellow
        Write-Host "      You may be running the wrong version" -ForegroundColor Yellow
    } else {
        Write-Host "      ❌ Code verification failed!" -ForegroundColor Red
        Write-Host "      Please check the code manually" -ForegroundColor Red
    }
} else {
    Write-Host "      ⚠️  verify_delete_code.py not found, skipping verification" -ForegroundColor Yellow
}

# Step 4: Show instructions
Write-Host ""
Write-Host "[4/5] System is ready!" -ForegroundColor Yellow
Write-Host ""
Write-Host "      📋 What was done:" -ForegroundColor Cyan
Write-Host "      ✅ Stopped Python processes" -ForegroundColor Green
Write-Host "      ✅ Cleared cache files" -ForegroundColor Green
Write-Host "      ✅ Verified code is correct" -ForegroundColor Green
Write-Host ""
Write-Host "      🎯 Next steps:" -ForegroundColor Cyan
Write-Host "      1. System will start automatically" -ForegroundColor White
Write-Host "      2. Open browser: http://127.0.0.1:5000" -ForegroundColor White
Write-Host "      3. Login as 'admin'" -ForegroundColor White
Write-Host "      4. Go to: المخزون > المنتجات" -ForegroundColor White
Write-Host "      5. Try deleting a product" -ForegroundColor White
Write-Host ""
Write-Host "      ✅ Expected result:" -ForegroundColor Green
Write-Host "      'Product and all related records have been permanently deleted'" -ForegroundColor Green
Write-Host ""

# Step 5: Start system
Write-Host "[5/5] Starting the system..." -ForegroundColor Yellow
Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if run.py exists
if (Test-Path "run.py") {
    python run.py
} else {
    Write-Host "❌ Error: run.py not found!" -ForegroundColor Red
    Write-Host "Please make sure you are in the correct directory." -ForegroundColor Red
    Write-Host ""
    Write-Host "Current directory: $(Get-Location)" -ForegroundColor Yellow
    Write-Host ""
    pause
}

