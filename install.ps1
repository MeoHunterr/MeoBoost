<#
.SYNOPSIS
    MeoBoost - Windows Performance Optimizer
#>

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

$Repo = "meohunterr/MeoBoost"
$Dir = Join-Path $env:LOCALAPPDATA "MeoBoost"
$Src = Join-Path $Dir "source"

function Write-S { param([string]$M) Write-Host "  [*] $M" -ForegroundColor Yellow }
function Write-O { param([string]$M) Write-Host "  [OK] $M" -ForegroundColor Green }
function Write-E { param([string]$M) Write-Host "  [!] $M" -ForegroundColor Red }

Write-Host ""
Write-Host "  MeoBoost - Windows Performance Optimizer" -ForegroundColor Cyan
Write-Host "  100% Open Source | No EXE Files" -ForegroundColor DarkCyan
Write-Host ""

# Admin check
$id = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object Security.Principal.WindowsPrincipal($id)
if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-S "Requesting admin privileges..."
    Start-Process powershell -Verb RunAs -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`""
    exit
}

$PyDir = Join-Path $Dir "python_embed"
$PyExe = Join-Path $PyDir "python.exe"

# 1. Check if Python Embed is missing, then download
if (-not (Test-Path $PyExe)) {
    Write-S "Preparing portable Python environment..."
    
    # Create directory
    if (-not (Test-Path $PyDir)) { New-Item -ItemType Directory -Path $PyDir -Force | Out-Null }
    
    # Download Python 3.11.9 Embeddable (Pure ZIP, safe)
    $pyUrl = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip"
    $zipPath = Join-Path $env:TEMP "python_embed.zip"
    
    # Check cache
    if (-not (Test-Path $zipPath)) {
        Write-S "Downloading Python core..."
        Invoke-WebRequest -Uri $pyUrl -OutFile $zipPath -UseBasicParsing
    } else {
        Write-S "Using cached Python core..."
    }
    
    # Extract
    Write-S "Extracting..."
    Expand-Archive -Path $zipPath -DestinationPath $PyDir -Force
    # Keep zip for cache
    
    # --- IMPORTANT: CONFIGURE TO RUN PIP ---
    # Default ._pth file blocks site import, need to fix it to install pip
    $pthFile = Get-ChildItem -Path $PyDir -Filter "*._pth" | Select-Object -ExpandProperty FullName
    if ($pthFile) {
        $content = Get-Content $pthFile
        # Uncomment "import site"
        $content = $content -replace "#import site", "import site" 
        Set-Content -Path $pthFile -Value $content
    }

    # Download and install PIP
    Write-S "Installing pip package manager..."
    $getPip = Join-Path $env:TEMP "get-pip.py"
    if (-not (Test-Path $getPip)) {
        Invoke-WebRequest -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile $getPip -UseBasicParsing
    }
    
    # Run get-pip.py using the downloaded python
    & $PyExe $getPip --no-warn-script-location --disable-pip-version-check | Out-Null
    
    Write-O "Portable Python ready!"
} else {
    Write-O "Using existing portable Python."
}

# 2. Download Source Code
# (Must be done before installing dependencies so requirements.txt exists)
if (-not (Test-Path $Src)) {
    Write-S "Downloading source code..."
    if (-not (Test-Path $Dir)) { New-Item -ItemType Directory -Path $Dir -Force | Out-Null }
    $zipPath = Join-Path $env:TEMP "MeoBoost.zip"
    Invoke-WebRequest -Uri "https://github.com/$Repo/archive/refs/heads/main.zip" -OutFile $zipPath -UseBasicParsing
    
    # Handle directory locking if re-running
    if ($PWD.Path.StartsWith($Src)) { Set-Location $env:USERPROFILE }
    if (Test-Path $Src) { Remove-Item $Src -Recurse -Force }
    
    $extractDir = Join-Path $env:TEMP "MeoBoost_ext"
    if (Test-Path $extractDir) { Remove-Item $extractDir -Recurse -Force }
    Expand-Archive -Path $zipPath -DestinationPath $extractDir -Force
    $extracted = Get-ChildItem $extractDir -Directory | Select-Object -First 1
    Move-Item -Path $extracted.FullName -Destination $Src -Force
    Remove-Item $zipPath, $extractDir -Recurse -Force -ErrorAction SilentlyContinue
    Write-O "Source code ready"
}

# 3. Install Dependencies
# Note: When using embed python, pip module is in the script, so call differently
$reqFile = Join-Path $Src "requirements.txt"
if (Test-Path $reqFile) {
    # Smart check: Try importing modules first
    $needsInstall = $true
    try {
        & $PyExe -c "import rich, requests" 2>$null
        if ($LASTEXITCODE -eq 0) { $needsInstall = $false }
    } catch {}

    if ($needsInstall) {
        Write-S "Installing dependencies..."
        # Call pip via module
        & $PyExe -m pip install -r $reqFile -q --no-warn-script-location --disable-pip-version-check
        Write-O "Dependencies installed."
    } else {
        Write-O "Dependencies already installed."
    }
}

# 4. Run Tool
Write-Host ""
Write-S "Starting MeoBoost..."
Write-Host ""

Set-Location $Src
& $PyExe main.py

Write-Host ""
Write-O "Session ended."
