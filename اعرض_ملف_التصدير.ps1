# سكريبت لعرض وفتح ملف التصدير
# DED ERP System v2.0

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "    📦 عرض ملف التصدير - DED ERP System v2.0" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# المسار الحالي
$currentPath = "C:\Users\DELL\DED"

# البحث عن ملفات ZIP
Write-Host "🔍 البحث عن ملفات التصدير..." -ForegroundColor Green
Write-Host ""

$zipFiles = Get-ChildItem -Path $currentPath -Filter "DED_ERP_System*.zip" | Sort-Object LastWriteTime -Descending

if ($zipFiles.Count -eq 0) {
    Write-Host "❌ لم يتم العثور على ملفات تصدير!" -ForegroundColor Red
    Write-Host ""
    Write-Host "المسار المبحوث: $currentPath" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit
}

Write-Host "✅ تم العثور على $($zipFiles.Count) ملف(ات):" -ForegroundColor Green
Write-Host ""

# عرض الملفات
$counter = 1
foreach ($file in $zipFiles) {
    $sizeKB = [math]::Round($file.Length / 1KB, 2)
    $sizeMB = [math]::Round($file.Length / 1MB, 2)
    
    Write-Host "[$counter] 📦 $($file.Name)" -ForegroundColor Cyan
    Write-Host "    📊 الحجم: $sizeKB KB ($sizeMB MB)" -ForegroundColor Gray
    Write-Host "    📅 التاريخ: $($file.LastWriteTime)" -ForegroundColor Gray
    Write-Host "    📍 المسار: $($file.FullName)" -ForegroundColor Gray
    
    if ($counter -eq 1) {
        Write-Host "    ⭐ الأحدث" -ForegroundColor Yellow
    }
    
    Write-Host ""
    $counter++
}

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# الملف الأحدث
$latestFile = $zipFiles[0]

Write-Host "💡 سيتم فتح الملف الأحدث:" -ForegroundColor Green
Write-Host "   $($latestFile.Name)" -ForegroundColor Yellow
Write-Host ""

# خيارات
Write-Host "اختر ما تريد فعله:" -ForegroundColor Cyan
Write-Host ""
Write-Host "[1] فتح المجلد وتحديد الملف" -ForegroundColor White
Write-Host "[2] فتح المجلد فقط" -ForegroundColor White
Write-Host "[3] نسخ المسار الكامل" -ForegroundColor White
Write-Host "[4] عرض معلومات الملف" -ForegroundColor White
Write-Host "[5] خروج" -ForegroundColor White
Write-Host ""

$choice = Read-Host "اختيارك (1-5)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "✅ فتح المجلد وتحديد الملف..." -ForegroundColor Green
        explorer.exe /select,"$($latestFile.FullName)"
    }
    "2" {
        Write-Host ""
        Write-Host "✅ فتح المجلد..." -ForegroundColor Green
        explorer.exe $currentPath
    }
    "3" {
        Write-Host ""
        Set-Clipboard -Value $latestFile.FullName
        Write-Host "✅ تم نسخ المسار إلى الحافظة!" -ForegroundColor Green
        Write-Host "   $($latestFile.FullName)" -ForegroundColor Yellow
    }
    "4" {
        Write-Host ""
        Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
        Write-Host "    📋 معلومات تفصيلية عن الملف" -ForegroundColor Yellow
        Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "📁 الاسم: $($latestFile.Name)" -ForegroundColor White
        Write-Host "📊 الحجم: $([math]::Round($latestFile.Length / 1KB, 2)) KB" -ForegroundColor White
        Write-Host "📊 الحجم: $([math]::Round($latestFile.Length / 1MB, 2)) MB" -ForegroundColor White
        Write-Host "📅 تاريخ الإنشاء: $($latestFile.CreationTime)" -ForegroundColor White
        Write-Host "📅 تاريخ التعديل: $($latestFile.LastWriteTime)" -ForegroundColor White
        Write-Host "📍 المسار الكامل: $($latestFile.FullName)" -ForegroundColor White
        Write-Host "📂 المجلد: $($latestFile.DirectoryName)" -ForegroundColor White
        Write-Host ""
    }
    "5" {
        Write-Host ""
        Write-Host "👋 إلى اللقاء!" -ForegroundColor Yellow
        exit
    }
    default {
        Write-Host ""
        Write-Host "❌ اختيار غير صحيح!" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
pause

