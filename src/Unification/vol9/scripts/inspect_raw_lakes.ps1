# ==============================================================================
# SCRIPT: inspect_raw_lakes.ps1
# PURPOSE: Non-destructive diagnostic - reads first few lines from every
#          raw lake and build script found under the vol5 directory tree.
#          Run this from the vol5 root directory.
#          Output shows exactly what each lake contains and what each
#          build script was designed to do.
#
# USAGE:
#   cd C:\Users\timot\Downloads\Science\src\Unification\vol5
#   powershell -ExecutionPolicy Bypass -File scripts\inspect_raw_lakes.ps1
#
# OUTPUT: Writes inspect_output.txt in the vol5 root for easy review.
# AUTHORS: Timothy John Kish & Mondy
# ==============================================================================

$vol5Root   = Get-Location
$outputFile = Join-Path $vol5Root "inspect_output.txt"
$separator  = "=" * 70

function Write-Section($title) {
    Write-Output ""
    Write-Output $separator
    Write-Output $title
    Write-Output $separator
}

$output = @()

$output += "VOL5 RAW LAKE AND BUILD SCRIPT INSPECTION"
$output += "Run from: $vol5Root"
$output += "Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$output += ""

# -----------------------------------------------------------------------
# 1. Scan all JSONL files under series directories (not lakes/ folder)
#    These are the raw source lakes
# -----------------------------------------------------------------------

$output += $separator
$output += "RAW LAKE FILES (series directories)"
$output += $separator

$seriesDirs = @("B-Series","FRB_Calibration_Network","N-Series","P-Series",
                "Q-Series","S-Series","T-Series")

foreach ($seriesDir in $seriesDirs) {
    $seriesPath = Join-Path $vol5Root $seriesDir
    if (-not (Test-Path $seriesPath)) {
        $output += ""
        $output += "[$seriesDir] - directory not found, skipping"
        continue
    }

    $jsonlFiles = Get-ChildItem -Path $seriesPath -Recurse -Filter "*.jsonl" |
                  Where-Object { $_.FullName -notlike "*\scripts\*" }

    if ($jsonlFiles.Count -eq 0) {
        $output += ""
        $output += "[$seriesDir] - no JSONL files found"
        continue
    }

    foreach ($file in $jsonlFiles) {
        $relPath = $file.FullName.Replace($vol5Root.Path + "\", "")
        $sizeMB  = [math]::Round($file.Length / 1MB, 2)
        $output += ""
        $output += "FILE: $relPath  ($sizeMB MB)"
        $output += "PATH: $($file.FullName)"

        try {
            $lines = Get-Content $file.FullName -TotalCount 5 -ErrorAction Stop
            $lineNum = 0
            foreach ($line in $lines) {
                $lineNum++
                # Truncate long lines for readability
                if ($line.Length -gt 300) {
                    $output += "  Line $lineNum : $($line.Substring(0,300))..."
                } else {
                    $output += "  Line $lineNum : $line"
                }
            }
            # Count total lines
            $totalLines = (Get-Content $file.FullName | Measure-Object -Line).Lines
            $output += "  Total records: $totalLines"
        } catch {
            $output += "  [ERROR reading file: $_]"
        }
    }
}

# -----------------------------------------------------------------------
# 2. Scan all JSON files (non-JSONL) in series lake directories
# -----------------------------------------------------------------------

$output += ""
$output += $separator
$output += "RAW LAKE FILES (JSON format in series directories)"
$output += $separator

foreach ($seriesDir in $seriesDirs) {
    $seriesPath = Join-Path $vol5Root $seriesDir
    if (-not (Test-Path $seriesPath)) { continue }

    $jsonFiles = Get-ChildItem -Path $seriesPath -Recurse -Filter "*.json" |
                 Where-Object { $_.FullName -notlike "*\scripts\*" }

    foreach ($file in $jsonFiles) {
        $relPath = $file.FullName.Replace($vol5Root.Path + "\", "")
        $sizeMB  = [math]::Round($file.Length / 1MB, 2)
        $output += ""
        $output += "FILE: $relPath  ($sizeMB MB)"

        try {
            $content = Get-Content $file.FullName -Raw -ErrorAction Stop
            # Show first 400 chars of structure
            if ($content.Length -gt 400) {
                $output += "  Preview: $($content.Substring(0,400))..."
            } else {
                $output += "  Content: $content"
            }
        } catch {
            $output += "  [ERROR: $_]"
        }
    }
}

# -----------------------------------------------------------------------
# 3. Scan all CSV files in series directories
# -----------------------------------------------------------------------

$output += ""
$output += $separator
$output += "RAW LAKE FILES (CSV format in series directories)"
$output += $separator

foreach ($seriesDir in $seriesDirs) {
    $seriesPath = Join-Path $vol5Root $seriesDir
    if (-not (Test-Path $seriesPath)) { continue }

    $csvFiles = Get-ChildItem -Path $seriesPath -Recurse -Filter "*.csv"

    foreach ($file in $csvFiles) {
        $relPath = $file.FullName.Replace($vol5Root.Path + "\", "")
        $sizeMB  = [math]::Round($file.Length / 1MB, 2)
        $output += ""
        $output += "FILE: $relPath  ($sizeMB MB)"

        try {
            $lines = Get-Content $file.FullName -TotalCount 3 -ErrorAction Stop
            foreach ($line in $lines) {
                if ($line.Length -gt 200) {
                    $output += "  $($line.Substring(0,200))..."
                } else {
                    $output += "  $line"
                }
            }
            $totalLines = (Get-Content $file.FullName | Measure-Object -Line).Lines
            $output += "  Total rows: $totalLines"
        } catch {
            $output += "  [ERROR: $_]"
        }
    }
}

# -----------------------------------------------------------------------
# 4. Scan build scripts - first 20 lines contain the annotation header
# -----------------------------------------------------------------------

$output += ""
$output += $separator
$output += "BUILD SCRIPTS (first 20 lines - annotation headers)"
$output += $separator

foreach ($seriesDir in $seriesDirs) {
    $seriesPath = Join-Path $vol5Root $seriesDir
    if (-not (Test-Path $seriesPath)) { continue }

    $scripts = Get-ChildItem -Path $seriesPath -Recurse -Filter "*.py"

    foreach ($script in $scripts) {
        $relPath = $script.FullName.Replace($vol5Root.Path + "\", "")
        $output += ""
        $output += "SCRIPT: $relPath"

        try {
            $lines = Get-Content $script.FullName -TotalCount 20 -ErrorAction Stop
            foreach ($line in $lines) {
                $output += "  $line"
            }
        } catch {
            $output += "  [ERROR: $_]"
        }
    }
}

# -----------------------------------------------------------------------
# 5. Also check the NS6_7 folder specifically (mentioned as S-Series home)
# -----------------------------------------------------------------------

$output += ""
$output += $separator
$output += "NS6_7 DIRECTORY (S-Series raw data)"
$output += $separator

$ns67Paths = @(
    (Join-Path $vol5Root "S-Series\NS6_7"),
    (Join-Path $vol5Root "NS6_7"),
    (Join-Path $vol5Root "S-Series\NS6_7\lake"),
    (Join-Path $vol5Root "S-Series")
)

$foundNS67 = $false
foreach ($p in $ns67Paths) {
    if (Test-Path $p) {
        $foundNS67 = $true
        $output += "Found at: $p"
        $allFiles = Get-ChildItem -Path $p -Recurse |
                    Where-Object { -not $_.PSIsContainer } |
                    Select-Object Name, Length, LastWriteTime, FullName

        foreach ($f in $allFiles) {
            $relPath = $f.FullName.Replace($vol5Root.Path + "\", "")
            $sizeMB  = [math]::Round($f.Length / 1MB, 2)
            $output += "  $relPath  ($sizeMB MB)  [$($f.LastWriteTime.ToString('yyyy-MM-dd'))]"
        }
        break
    }
}

if (-not $foundNS67) {
    $output += "NS6_7 not found under S-Series or vol5 root"
    $output += "Searched: $($ns67Paths -join ', ')"
}

# -----------------------------------------------------------------------
# 6. Summary of raw_archive
# -----------------------------------------------------------------------

$output += ""
$output += $separator
$output += "RAW ARCHIVE (lakes/raw_archive)"
$output += $separator

$rawArchive = Join-Path $vol5Root "lakes\raw_archive"
if (Test-Path $rawArchive) {
    $archiveFiles = Get-ChildItem -Path $rawArchive
    foreach ($f in $archiveFiles) {
        $sizeMB = [math]::Round($f.Length / 1MB, 2)
        $output += "  $($f.Name)  ($sizeMB MB)"
    }
} else {
    $output += "raw_archive not found"
}

# -----------------------------------------------------------------------
# Write output
# -----------------------------------------------------------------------

$output | Out-File -FilePath $outputFile -Encoding UTF8
Write-Host "Inspection complete. Output written to: $outputFile"
Write-Host "Share inspect_output.txt with Mondy for analysis."
