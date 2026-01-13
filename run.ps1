<#
.SYNOPSIS
    MeoBoost - Windows Performance Optimizer
    Official launcher script for downloading and running MeoBoost from source

.DESCRIPTION
    This script:
    1. Checks if Python is installed, installs it automatically if not
    2. Downloads MeoBoost source code from GitHub
    3. Installs required dependencies
    4. Runs MeoBoost directly from Python source
    
    No compiled EXE files - 100% transparent, open-source code.
    
    MeoBoost is an open-source Windows optimization tool.
    Source code: https://github.com/Minhboang11-Meo/meoboost

.NOTES
    - Requires Windows 10/11
    - Administrator privileges required for system tweaks
    - Python is automatically installed if not found
    - All downloads are from official sources only

.LINK
    https://github.com/Minhboang11-Meo/meoboost
#>

# ============================================
#  MeoBoost Launcher Script
#  Version: 2.0.0
#  License: GPL-3.0
#  Method: Source-based (No EXE)
# ============================================

# Strict mode for safety
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Application Configuration
$script:AppName = "MeoBoost"
$script:GitHubOwner = "Minhboang11-Meo"
$script:GitHubRepo = "meoboost"
$script:InstallDirectory = Join-Path $env:USERPROFILE ".meoboost"
$script:SourceDirectory = Join-Path $script:InstallDirectory "source"
$script:VersionFilePath = Join-Path $script:InstallDirectory "version.txt"
$script:PythonMinVersion = [version]"3.8.0"
$script:PythonMaxVersion = [version]"3.12.99"

# Python installer URL (official python.org)
$script:PythonInstallerUrl = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"
$script:PythonInstallerPath = Join-Path $env:TEMP "python-installer.exe"

# Display branded header
function Show-ApplicationHeader {
    Write-Host ""
    Write-Host "  ╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "  ║           MeoBoost - Windows Performance Optimizer       ║" -ForegroundColor Cyan
    Write-Host "  ║                    Source-Based Edition                  ║" -ForegroundColor DarkCyan
    Write-Host "  ║         https://github.com/$script:GitHubOwner/$script:GitHubRepo            ║" -ForegroundColor DarkCyan
    Write-Host "  ╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  100% Open Source • No EXE Files • Fully Transparent" -ForegroundColor Green
    Write-Host ""
}

# Output helper functions
function Write-StatusMessage {
    param([string]$Message)
    Write-Host "  [*] $Message" -ForegroundColor Yellow
}

function Write-SuccessMessage {
    param([string]$Message)
    Write-Host "  [OK] $Message" -ForegroundColor Green
}

function Write-ErrorMessage {
    param([string]$Message)
    Write-Host "  [ERROR] $Message" -ForegroundColor Red
}

function Write-InfoMessage {
    param([string]$Message)
    Write-Host "  [i] $Message" -ForegroundColor Cyan
}

# Check if current session has administrator privileges
function Test-AdministratorPrivileges {
    $currentIdentity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentIdentity)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Request administrator privileges
function Request-AdminPrivileges {
    if (-not (Test-AdministratorPrivileges)) {
        Write-StatusMessage "Requesting administrator privileges..."
        $scriptPath = $MyInvocation.ScriptName
        if ([string]::IsNullOrEmpty($scriptPath)) {
            # Running from irm | iex - need to re-download and run elevated
            Start-Process powershell.exe -Verb RunAs -ArgumentList @(
                "-NoProfile",
                "-ExecutionPolicy", "Bypass",
                "-Command",
                "irm https://raw.githubusercontent.com/$script:GitHubOwner/$script:GitHubRepo/main/run.ps1 | iex"
            )
        }
        else {
            Start-Process powershell.exe -Verb RunAs -ArgumentList @(
                "-NoProfile",
                "-ExecutionPolicy", "Bypass",
                "-File", $scriptPath
            )
        }
        exit
    }
}

# ============================================
#  Python Detection and Installation
# ============================================

function Get-PythonPath {
    <#
    .SYNOPSIS
        Find Python executable in common locations
    #>
    
    # Try standard paths first
    $pythonCommands = @("python", "python3", "py")
    
    foreach ($cmd in $pythonCommands) {
        try {
            $result = & $cmd --version 2>&1
            if ($LASTEXITCODE -eq 0 -and $result -match "Python (\d+\.\d+\.\d+)") {
                $version = [version]$Matches[1]
                if ($version -ge $script:PythonMinVersion -and $version -le $script:PythonMaxVersion) {
                    # Get full path
                    $fullPath = (Get-Command $cmd -ErrorAction SilentlyContinue).Source
                    if ($fullPath) {
                        return @{
                            Path = $fullPath
                            Version = $version
                            Command = $cmd
                        }
                    }
                }
            }
        }
        catch {
            continue
        }
    }
    
    # Check common installation paths
    $commonPaths = @(
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python310\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python39\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python38\python.exe",
        "C:\Python311\python.exe",
        "C:\Python310\python.exe",
        "C:\Python39\python.exe",
        "C:\Python38\python.exe"
    )
    
    foreach ($path in $commonPaths) {
        if (Test-Path $path) {
            try {
                $result = & $path --version 2>&1
                if ($result -match "Python (\d+\.\d+\.\d+)") {
                    $version = [version]$Matches[1]
                    if ($version -ge $script:PythonMinVersion -and $version -le $script:PythonMaxVersion) {
                        return @{
                            Path = $path
                            Version = $version
                            Command = $path
                        }
                    }
                }
            }
            catch {
                continue
            }
        }
    }
    
    return $null
}

function Test-PythonInstalled {
    <#
    .SYNOPSIS
        Check if Python 3.8-3.12 is installed
    #>
    $python = Get-PythonPath
    return $null -ne $python
}

function Install-Python {
    <#
    .SYNOPSIS
        Download and install Python automatically
    #>
    Write-StatusMessage "Python not found. Installing Python 3.11..."
    Write-InfoMessage "Downloading from python.org (official source)..."
    
    try {
        # Download Python installer
        Invoke-WebRequest -Uri $script:PythonInstallerUrl -OutFile $script:PythonInstallerPath -UseBasicParsing
        
        if (-not (Test-Path $script:PythonInstallerPath)) {
            throw "Failed to download Python installer"
        }
        
        $fileSize = (Get-Item $script:PythonInstallerPath).Length / 1MB
        Write-SuccessMessage "Downloaded Python installer ($([math]::Round($fileSize, 1)) MB)"
        
        # Install Python silently
        Write-StatusMessage "Installing Python (this may take a minute)..."
        
        $installArgs = @(
            "/quiet",
            "InstallAllUsers=0",
            "PrependPath=1",
            "Include_test=0",
            "Include_doc=0",
            "Include_launcher=1",
            "Include_pip=1"
        )
        
        $process = Start-Process -FilePath $script:PythonInstallerPath -ArgumentList $installArgs -Wait -PassThru
        
        if ($process.ExitCode -ne 0) {
            throw "Python installation failed with exit code: $($process.ExitCode)"
        }
        
        # Refresh PATH
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
        
        # Verify installation
        Start-Sleep -Seconds 2
        $python = Get-PythonPath
        
        if ($null -eq $python) {
            throw "Python installation completed but Python is not accessible. Please restart PowerShell and try again."
        }
        
        Write-SuccessMessage "Python $($python.Version) installed successfully!"
        
        # Cleanup installer
        Remove-Item $script:PythonInstallerPath -Force -ErrorAction SilentlyContinue
        
        return $python
    }
    catch {
        Write-ErrorMessage "Failed to install Python: $_"
        Write-Host ""
        Write-Host "  Please install Python manually:" -ForegroundColor Gray
        Write-Host "  https://www.python.org/downloads/" -ForegroundColor Cyan
        Write-Host "  (Choose Python 3.11.x, check 'Add to PATH')" -ForegroundColor Gray
        Write-Host ""
        throw
    }
}

# ============================================
#  Source Code Management
# ============================================

function Get-LatestReleaseInfo {
    <#
    .SYNOPSIS
        Fetch latest release information from GitHub API
    #>
    Write-StatusMessage "Checking for latest version..."
    
    $apiEndpoint = "https://api.github.com/repos/$script:GitHubOwner/$script:GitHubRepo/releases/latest"
    
    try {
        $response = Invoke-RestMethod -Uri $apiEndpoint -Method Get -Headers @{
            "Accept"     = "application/vnd.github.v3+json"
            "User-Agent" = "MeoBoost-Launcher/2.0"
        }
        
        return @{
            TagName     = $response.tag_name
            ZipballUrl  = $response.zipball_url
            PublishedAt = $response.published_at
        }
    }
    catch {
        # Fallback to main branch if no releases
        Write-InfoMessage "No releases found, using main branch..."
        return @{
            TagName    = "main"
            ZipballUrl = "https://github.com/$script:GitHubOwner/$script:GitHubRepo/archive/refs/heads/main.zip"
            PublishedAt = (Get-Date).ToString("o")
        }
    }
}

function Test-UpdateAvailable {
    param(
        [Parameter(Mandatory)]
        [string]$LatestVersion
    )
    
    # Check if source directory exists
    if (-not (Test-Path $script:SourceDirectory)) {
        return $true
    }
    
    # Check if main.py exists
    $mainPy = Join-Path $script:SourceDirectory "main.py"
    if (-not (Test-Path $mainPy)) {
        return $true
    }
    
    # Check version file
    if (-not (Test-Path $script:VersionFilePath)) {
        return $true
    }
    
    # Compare versions
    $installedVersion = (Get-Content $script:VersionFilePath -Raw).Trim()
    return $installedVersion -ne $LatestVersion
}

function Install-MeoBoostSource {
    param(
        [Parameter(Mandatory)]
        [string]$DownloadUrl,
        
        [Parameter(Mandatory)]
        [string]$Version
    )
    
    Write-StatusMessage "Downloading MeoBoost $Version source code..."
    
    # Ensure install directory exists
    if (-not (Test-Path $script:InstallDirectory)) {
        New-Item -ItemType Directory -Path $script:InstallDirectory -Force | Out-Null
    }
    
    # Download ZIP
    $zipPath = Join-Path $env:TEMP "meoboost-source.zip"
    Invoke-WebRequest -Uri $DownloadUrl -OutFile $zipPath -UseBasicParsing
    
    if (-not (Test-Path $zipPath)) {
        throw "Failed to download source code"
    }
    
    $zipSize = [math]::Round((Get-Item $zipPath).Length / 1KB, 1)
    Write-SuccessMessage "Downloaded source code ($zipSize KB)"
    
    # Clean existing source
    if (Test-Path $script:SourceDirectory) {
        Remove-Item $script:SourceDirectory -Recurse -Force
    }
    
    # Extract ZIP
    Write-StatusMessage "Extracting source code..."
    $extractPath = Join-Path $env:TEMP "meoboost-extract"
    
    if (Test-Path $extractPath) {
        Remove-Item $extractPath -Recurse -Force
    }
    
    Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force
    
    # Find the extracted folder (GitHub adds prefix like "meoboost-main")
    $extractedFolder = Get-ChildItem $extractPath -Directory | Select-Object -First 1
    
    if ($null -eq $extractedFolder) {
        throw "Failed to extract source code"
    }
    
    # Move to final location
    Move-Item -Path $extractedFolder.FullName -Destination $script:SourceDirectory -Force
    
    # Cleanup
    Remove-Item $zipPath -Force -ErrorAction SilentlyContinue
    Remove-Item $extractPath -Recurse -Force -ErrorAction SilentlyContinue
    
    Write-SuccessMessage "Source code installed to: $script:SourceDirectory"
}

function Save-InstalledVersion {
    param(
        [Parameter(Mandatory)]
        [string]$Version
    )
    Set-Content -Path $script:VersionFilePath -Value $Version -NoNewline
}

# ============================================
#  Dependency Management
# ============================================

function Install-Dependencies {
    param(
        [Parameter(Mandatory)]
        [string]$PythonPath
    )
    
    $requirementsPath = Join-Path $script:SourceDirectory "requirements.txt"
    
    if (-not (Test-Path $requirementsPath)) {
        Write-InfoMessage "No requirements.txt found, skipping dependency installation"
        return
    }
    
    Write-StatusMessage "Installing Python dependencies..."
    
    # Upgrade pip first (quietly)
    & $PythonPath -m pip install --upgrade pip --quiet 2>&1 | Out-Null
    
    # Install requirements
    $result = & $PythonPath -m pip install -r $requirementsPath --quiet 2>&1
    
    if ($LASTEXITCODE -ne 0) {
        Write-ErrorMessage "Some dependencies may have failed to install"
        Write-Host $result
    }
    else {
        Write-SuccessMessage "Dependencies installed successfully"
    }
}

# ============================================
#  Application Launch
# ============================================

function Start-MeoBoostApplication {
    param(
        [Parameter(Mandatory)]
        [string]$PythonPath
    )
    
    $mainPy = Join-Path $script:SourceDirectory "main.py"
    
    if (-not (Test-Path $mainPy)) {
        throw "main.py not found at: $mainPy"
    }
    
    Write-Host ""
    Write-StatusMessage "Starting MeoBoost..."
    Write-Host ""
    Write-Host "  ─────────────────────────────────────────────────────────" -ForegroundColor DarkGray
    Write-Host ""
    
    # Run MeoBoost
    Push-Location $script:SourceDirectory
    try {
        & $PythonPath $mainPy
    }
    finally {
        Pop-Location
    }
}

# ============================================
#  Main Entry Point
# ============================================

function Invoke-MeoBoostLauncher {
    Show-ApplicationHeader
    
    try {
        # Step 1: Check/Request admin privileges
        Request-AdminPrivileges
        
        # Step 2: Check/Install Python
        $python = Get-PythonPath
        
        if ($null -eq $python) {
            $python = Install-Python
        }
        else {
            Write-SuccessMessage "Python $($python.Version) detected"
        }
        
        # Step 3: Check for updates and download source
        $releaseInfo = Get-LatestReleaseInfo
        
        if (Test-UpdateAvailable -LatestVersion $releaseInfo.TagName) {
            Install-MeoBoostSource -DownloadUrl $releaseInfo.ZipballUrl -Version $releaseInfo.TagName
            Save-InstalledVersion -Version $releaseInfo.TagName
            
            # Install dependencies after downloading new source
            Install-Dependencies -PythonPath $python.Path
        }
        else {
            Write-SuccessMessage "Already running latest version ($($releaseInfo.TagName))"
        }
        
        # Step 4: Launch the application
        Start-MeoBoostApplication -PythonPath $python.Path
        
        Write-Host ""
        Write-Host "  ─────────────────────────────────────────────────────────" -ForegroundColor DarkGray
        Write-Host ""
        Write-SuccessMessage "MeoBoost session ended."
        Write-Host ""
    }
    catch {
        Write-ErrorMessage $_.Exception.Message
        Write-Host ""
        Write-Host "  For support, please visit:" -ForegroundColor Gray
        Write-Host "  https://github.com/$script:GitHubOwner/$script:GitHubRepo/issues" -ForegroundColor Cyan
        Write-Host ""
        Read-Host "  Press Enter to exit"
        exit 1
    }
}

# Execute the launcher
Invoke-MeoBoostLauncher
