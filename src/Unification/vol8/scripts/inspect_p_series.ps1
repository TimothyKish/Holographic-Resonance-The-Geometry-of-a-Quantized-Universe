# inspect_p_series.ps1
# Inspect P-Series lake contents to determine what orbital data exists
# Run from vol5 root:
#   powershell -ExecutionPolicy Bypass -File scripts\inspect_p_series.ps1

$vol5 = Get-Location
Write-Host "Inspecting P-Series from: $vol5"
Write-Host "======================================================"

$pSeriesPath = Join-Path $vol5 "P-Series"
if (-not (Test-Path $pSeriesPath)) {
    Write-Host "P-Series not found at: $pSeriesPath"
    exit
}

$jsonlFiles = Get-ChildItem -Path $pSeriesPath -Recurse -Filter "*.jsonl" |
              Where-Object { $_.Name -notlike "*scalarized*" -and $_.Name -notlike "*promoted*" }

foreach ($file in $jsonlFiles) {
    $relPath = $file.FullName.Replace($vol5.Path + "\", "")
    $sizeMB  = [math]::Round($file.Length / 1MB, 3)
    $totalLines = (Get-Content $file.FullName | Measure-Object -Line).Lines

    Write-Host ""
    Write-Host "FILE: $relPath  ($sizeMB MB, $totalLines records)"
    Write-Host "First 3 lines:"

    $lines = Get-Content $file.FullName -TotalCount 3
    foreach ($line in $lines) {
        if ($line.Length -gt 400) {
            Write-Host "  $($line.Substring(0, 400))..."
        } else {
            Write-Host "  $line"
        }
    }
}

Write-Host ""
Write-Host "======================================================"
Write-Host "Also checking for CSV or TSV files in P-Series:"

$csvFiles = Get-ChildItem -Path $pSeriesPath -Recurse -Filter "*.csv"
foreach ($file in $csvFiles) {
    $relPath = $file.FullName.Replace($vol5.Path + "\", "")
    $sizeMB  = [math]::Round($file.Length / 1MB, 3)
    Write-Host ""
    Write-Host "CSV: $relPath  ($sizeMB MB)"
    $lines = Get-Content $file.FullName -TotalCount 3
    foreach ($line in $lines) {
        if ($line.Length -gt 300) {
            Write-Host "  $($line.Substring(0, 300))..."
        } else {
            Write-Host "  $line"
        }
    }
}